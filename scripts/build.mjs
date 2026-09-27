// Builds the review site (site/) and the Word documents (site/downloads/)
// from the Markdown files in content/. Edit content/*.md, then run `npm run build`.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { marked } from 'marked';
import sizeOf from 'image-size';
import {
  Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell,
  WidthType, ShadingType, LevelFormat, AlignmentType, BorderStyle, Footer, PageNumber,
  ImageRun, VerticalAlign,
} from 'docx';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const CONTENT = path.join(ROOT, 'content');
const OUT = path.join(ROOT, 'site');
const BLUE = '046EB8', INK = '0E1B2C', SOFT = '4A5A6E', PAGE_W = 9638;

const docs = fs.readdirSync(CONTENT).filter(f => f.endsWith('.md')).sort().map(file => {
  const md = fs.readFileSync(path.join(CONTENT, file), 'utf8');
  const title = (md.match(/^# (.+)$/m) || [, file])[1].trim();
  const slug = file.replace(/\.md$/, '');
  return { file, slug, title, md };
});

fs.rmSync(OUT, { recursive: true, force: true });
fs.mkdirSync(path.join(OUT, 'downloads'), { recursive: true });
fs.cpSync(path.join(CONTENT, 'images'), path.join(OUT, 'images'), { recursive: true });

// ---------- Word ----------
const border = { style: BorderStyle.SINGLE, size: 4, color: 'D5DFE8' };
const borders = { top: border, bottom: border, left: border, right: border };

function inlineRuns(tokens, opts = {}) {
  const runs = [];
  for (const t of tokens || []) {
    if (t.type === 'strong') runs.push(...inlineRuns(t.tokens, { ...opts, bold: true }));
    else if (t.type === 'em') runs.push(...inlineRuns(t.tokens, { ...opts, italics: true }));
    else if (t.type === 'codespan') runs.push(new TextRun({ text: unescape(t.text), font: 'Consolas', ...opts }));
    else if (t.type === 'link') runs.push(...inlineRuns(t.tokens, { ...opts, color: BLUE }));
    else if (t.type === 'image') {
      const file = path.join(CONTENT, t.href);
      if (fs.existsSync(file)) {
        const { width, height } = sizeOf(fs.readFileSync(file));
        const scale = Math.min(1, 120 / width);
        runs.push(new ImageRun({ type: 'jpg', data: fs.readFileSync(file), transformation: { width: Math.round(width * scale), height: Math.round(height * scale) } }));
      }
    } else if (t.type === 'br') runs.push(new TextRun({ break: 1 }));
    else if (t.tokens) runs.push(...inlineRuns(t.tokens, opts));
    else runs.push(new TextRun({ text: unescape(t.text ?? t.raw ?? ''), ...opts }));
  }
  return runs;
}
const unescape = s => s.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'");

function tableFor(tok) {
  const n = tok.header.length;
  const weights = tok.header.map((h, i) => Math.max(h.text.length, ...tok.rows.map(r => Math.min(r[i].text.length, 90))) + 6);
  const sum = weights.reduce((a, b) => a + b, 0);
  const cols = weights.map(w => Math.round(PAGE_W * w / sum));
  cols[n - 1] += PAGE_W - cols.reduce((a, b) => a + b, 0);
  const row = (cells, head) => new TableRow({
    tableHeader: head, cantSplit: true,
    children: cells.map((c, i) => new TableCell({
      width: { size: cols[i], type: WidthType.DXA }, borders, verticalAlign: VerticalAlign.CENTER,
      margins: { top: 70, bottom: 70, left: 100, right: 100 },
      shading: head ? { type: ShadingType.CLEAR, fill: BLUE, color: 'auto' } : undefined,
      children: [new Paragraph({ children: inlineRuns(c.tokens, head ? { bold: true, color: 'FFFFFF', size: 19 } : { size: 19 }) })],
    })),
  });
  return new Table({ width: { size: PAGE_W, type: WidthType.DXA }, columnWidths: cols, rows: [row(tok.header, true), ...tok.rows.map(r => row(r, false))] });
}

function toDocx(doc) {
  const children = [];
  let listId = 0;
  const numbering = [{ reference: 'bul', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 280 } } } }] }];
  for (const tok of marked.lexer(doc.md)) {
    if (tok.type === 'heading') {
      const heading = [HeadingLevel.TITLE, HeadingLevel.HEADING_1, HeadingLevel.HEADING_2, HeadingLevel.HEADING_3][tok.depth - 1];
      if (tok.depth === 1) children.push(new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: 'TAIPEI INTERNATIONAL CHURCH', bold: true, color: BLUE, size: 22, characterSpacing: 40 })] }));
      children.push(new Paragraph({ heading, keepNext: true, children: inlineRuns(tok.tokens) }));
    } else if (tok.type === 'paragraph') {
      children.push(new Paragraph({ spacing: { after: 120 }, children: inlineRuns(tok.tokens) }));
    } else if (tok.type === 'list') {
      const ref = tok.ordered ? `num${listId++}` : 'bul';
      if (tok.ordered) numbering.push({ reference: ref, levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 360 } } } }] });
      for (const item of tok.items) {
        const inner = item.tokens.flatMap(t => t.type === 'text' || t.type === 'paragraph' ? (t.tokens || [t]) : []);
        children.push(new Paragraph({ numbering: { reference: ref, level: 0 }, spacing: { after: 80 }, children: inlineRuns(inner) }));
        for (const t of item.tokens) if (t.type === 'code') children.push(...codeBlock(t.text));
      }
    } else if (tok.type === 'table') {
      children.push(tableFor(tok), new Paragraph({ children: [] }));
    } else if (tok.type === 'code') {
      children.push(...codeBlock(tok.text));
    }
  }
  return new Document({
    title: doc.title,
    styles: {
      default: { document: { run: { font: { ascii: 'Arial', hAnsi: 'Arial', eastAsia: 'PingFang TC' }, size: 21, color: INK } } },
      paragraphStyles: [
        { id: 'Title', name: 'Title', basedOn: 'Normal', run: { size: 38, bold: true, color: INK }, paragraph: { spacing: { after: 120 }, border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: 'FFDA00', space: 8 } } } },
        { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 28, bold: true, color: BLUE }, paragraph: { spacing: { before: 300, after: 120 }, outlineLevel: 0 } },
        { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 23, bold: true, color: INK }, paragraph: { spacing: { before: 200, after: 100 }, outlineLevel: 1 } },
        { id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 21, bold: true, color: INK }, paragraph: { spacing: { before: 160, after: 80 }, outlineLevel: 2 } },
      ],
    },
    numbering: { config: numbering },
    sections: [{
      properties: { page: { margin: { top: 1134, bottom: 1134, left: 1134, right: 1134 } } },
      footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: `${doc.title}  ·  page `, color: SOFT, size: 16 }), new TextRun({ children: [PageNumber.CURRENT], color: SOFT, size: 16 })] })] }) },
      children,
    }],
  });
}
function codeBlock(text) {
  return text.split('\n').map(line => new Paragraph({ spacing: { after: 0 }, children: [new TextRun({ text: line, font: 'Consolas', size: 16 })] }));
}

// ---------- HTML ----------
const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
function page({ title, body, current }) {
  const nav = docs.map(d => `<a href="${d.slug}.html"${d.slug === current ? ' aria-current="page"' : ''}>${esc(d.title)}</a>`).join('');
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>${esc(title)} · TIC Website Review</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<header class="top"><a class="brand" href="index.html"><span class="mark">TIC</span><span>Website Review</span></a><nav>${nav}</nav></header>
<main>${body}</main>
<footer>Prepared for Taipei International Church. Not affiliated with or published by the church. Edit the files in <code>content/</code> to update this site and the Word documents.</footer>
</body>
</html>
`;
}

const renderer = new marked.Renderer();
renderer.table = function (tok) {
  return `<div class="table">${marked.Renderer.prototype.table.call(this, tok)}</div>`;
};
marked.use({ renderer });

for (const doc of docs) {
  const buf = await Packer.toBuffer(toDocx(doc));
  const docxName = `TIC-${doc.slug}.docx`;
  fs.writeFileSync(path.join(OUT, 'downloads', docxName), buf);
  const html = marked.parse(doc.md).replace(/<h1>(.*?)<\/h1>/, `<p class="eyebrow">Taipei International Church</p><h1>$1</h1><p class="dl"><a class="btn" href="downloads/${docxName}" download>Download Word document</a></p>`);
  fs.writeFileSync(path.join(OUT, `${doc.slug}.html`), page({ title: doc.title, body: `<article>${html}</article>`, current: doc.slug }));
  doc.docxName = docxName;
}

const cards = docs.map(d => `<li><a class="card" href="${d.slug}.html"><b>${esc(d.title)}</b><span>Read online</span></a><a class="small" href="downloads/${d.docxName}" download>Word document</a></li>`).join('');
fs.writeFileSync(path.join(OUT, 'index.html'), page({
  title: 'Overview', current: '',
  body: `<article><p class="eyebrow">Taipei International Church</p><h1>taipeichurch.org website review</h1>
<p>A review of taipeichurch.org with step-by-step fixes. Nothing here changes the live website: every fix is made by hand in the Wix Editor.</p>
<ol class="cards">${cards}</ol>
<h2>How to update</h2>
<ol><li>Edit the Markdown file in <code>content/</code> on GitHub (pencil icon).</li><li>Commit the change. The site and the Word documents rebuild automatically in about a minute.</li></ol></article>`,
}));
fs.copyFileSync(path.join(ROOT, 'scripts', 'style.css'), path.join(OUT, 'style.css'));
fs.writeFileSync(path.join(OUT, 'robots.txt'), 'User-agent: *\nDisallow: /\n');
console.log(`Built ${docs.length} documents into site/`);
