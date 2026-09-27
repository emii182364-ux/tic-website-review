"""Builds preview/ (desktop) and preview/m/ (mobile) from the downloaded Wix pages.

Applies the fixes from Fix Reports #1 and #2 to a copy of each page, then adds a
"preview" banner, turns off search indexing and keeps navigation inside the preview.

Usage: python3 tools/make_preview.py <desktop-originals-dir> <mobile-originals-dir>
"""
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = json.load(open(os.path.join(ROOT, 'tools', 'fixes.json'), encoding='utf-8'))
OLD_ZOOM = 'https://taipeichurch.us19.list-manage.com/track/click?u=1b22dd056ddf40dff17202407&amp;id=951648d59f&amp;e=47691d8f60'
NEW_ZOOM = 'https://us02web.zoom.us/j/6807975448?pwd=WTFXYXRqZUJpTVNQTUJSUmFiamRBZz09'
HERO = '7dfb7a_9da4631d291543b9a7fb6bf9aeab0087'


def apply_fixes(name, s, log):
    def fix(old, new, label):
        n = s.count(old)
        if n:
            log.append(f'{name} | {label} | {n}x')
        return s.replace(old, new)

    for old, new, label, pages in DATA['text']:
        if name in pages:
            s = fix(old, new, label)
    if name == 'groups':
        s = fix(OLD_ZOOM, NEW_ZOOM, 'Mailchimp tracking link -> direct Zoom link')
    if name == 'home':
        new_map = re.search(r'https://www\.google\.com/maps/place/Taipei\+International\+Church/@25\.0781275[^"]*', s)
        for old in set(re.findall(r'https://www\.google\.com/maps/place/[^"]*?569%E8%99%9FB2[^"]*', s)):
            if new_map:
                s = fix(old, new_map.group(0), 'Old map link -> new venue')
        lb = re.search(r'<script type="application/ld\+json">(\{"@context":"https://schema.org/","@type":"LocalBusiness".*?)</script>', s, re.S)
        if lb:
            s = s.replace(lb.group(1), json.dumps(DATA['schema'], ensure_ascii=False), 1)
            log.append(f'{name} | Structured data LocalBusiness (old address) -> Church | 1x')
    s = fix('"@type":"WebSite","name":"taipeichurch"', '"@type":"WebSite","name":"Taipei International Church"', 'WebSite structured data name')
    s = fix('| taipeichurch', '| Taipei International Church', 'Page title')
    if 'name="description"' not in s and name in DATA['descriptions']:
        s = re.sub(r'(<title>.*?</title>)', lambda m: m.group(1) + '\n<meta name="description" content="' + html.escape(DATA['descriptions'][name]) + '">', s, 1)
        log.append(f'{name} | Added SEO description | 1x')

    alts = DATA['alts']
    count = 0

    def add_alt(m):
        nonlocal count
        tag = m.group(0)
        alt = re.search(r'\balt="([^"]*)"', tag)
        if alt and alt.group(1).strip():
            return tag
        src = re.search(r'\bsrc="([^"]+)"', tag)
        mid = re.search(r'media/([0-9a-f]{6}_[0-9a-f]{32})', src.group(1)) if src else None
        if not mid or mid.group(1) not in alts:
            return tag
        count += 1
        a = html.escape(alts[mid.group(1)], quote=True)
        return re.sub(r'\balt=""', f'alt="{a}"', tag) if alt else tag.replace('<img ', f'<img alt="{a}" ', 1)

    s = re.sub(r'<img\b[^>]*>', add_alt, s)
    if count:
        log.append(f'{name} | Added image descriptions (alt text) | {count}x')
    return s


def preview_wrap(name, s, pages, mobile):
    live = 'https://www.taipeichurch.org/' + ('' if name == 'home' else name)
    up = '../../' if mobile else '../'
    here = 'index.html' if name == 'home' else f'{name}.html'
    other = (f'../{here}' if mobile else f'm/{here}')
    banner = (
        '<div id="tic-preview-banner" style="position:sticky;top:0;z-index:2147483647;background:#FFDA00;color:#1D1800;'
        'font:600 14px/1.4 system-ui,sans-serif;padding:10px 16px;text-align:center;border-bottom:2px solid #046EB8">'
        'PREVIEW for review only: a corrected copy of taipeichurch.org (Fix Reports #1 and #2). This is not the official website. '
        f'<a href="{live}" style="color:#046EB8">Official site</a> · <a href="{up}index.html" style="color:#046EB8">Back to the reports</a> · '
        f'<a href="{up}preview/CHANGES.txt" style="color:#046EB8">What changed</a> · '
        f'<a href="{other}" style="color:#046EB8">{"Desktop" if mobile else "Mobile"} version</a></div>'
    )
    head_extra = (
        '<meta name="robots" content="noindex, nofollow">\n'
        # Wix reveal animations need Wix's own scripts, which do not run on this host; show the elements instead.
        '<style>[id^="comp-"]{opacity:1!important}</style>\n'
    )
    if not mobile:
        head_extra += ('<script>if (Math.min(screen.width, screen.height) <= 760 && !sessionStorage.getItem("tic-desktop")) '
                       f'location.replace("m/{here}");</script>\n')
    else:
        banner = banner.replace('>Desktop version</a>', ' onclick="sessionStorage.setItem(\'tic-desktop\',1)">Desktop version</a>')
    s = re.sub(r'<meta name="robots"[^>]*>', '', s)
    s = re.sub(r'(<head[^>]*>)', lambda m: m.group(1) + '\n' + head_extra, s, 1)
    s = re.sub(r'<link rel="canonical" href="[^"]*"', f'<link rel="canonical" href="{live}"', s)
    for q in pages:
        target = 'index.html' if q == 'home' else f'{q}.html'
        if q == 'home':
            s = re.sub(r'href="https://www\.taipeichurch\.org/?"', f'href="{target}"', s)
        else:
            s = re.sub(rf'href="https://www\.taipeichurch\.org/{re.escape(q)}(#[^"]*)?"', lambda m: f'href="{target}{m.group(1) or ""}"', s)
    if name == 'home':
        # Homepage photo: show the whole photo, cropped towards the city instead of the sky.
        full = f'https://static.wixstatic.com/media/{HERO}~mv2.jpg/v1/fit/w_2400,h_2400,q_85/{HERO}~mv2.jpg'
        s = s.replace('</head>', '<style>[data-motion-part^="BG_IMG pageBackground"] img{visibility:hidden!important}' +
                      (f'[data-motion-part^="BG_IMG pageBackground"]{{background:#dfe7ee url("{full}") 42% 0/auto 470px no-repeat!important}}' if mobile else
                       f'[data-motion-part^="BG_IMG pageBackground"]{{background:url("{full}") 50% 88%/cover no-repeat!important}}') + '</style>\n</head>', 1)
    if name == 'home':
        # The five "Worship" photo strips have uneven heights and gaps on the live site; even them out.
        s = s.replace('</body>', """<script>addEventListener('load',function(){setTimeout(function(){
var els=['comp-l4jicfmq','comp-ktjbnzsz','comp-l4jiiz0g','comp-l4jiafbk','comp-l4jigf6b'].map(function(i){return document.getElementById(i)}).filter(Boolean);
if(els.length<2)return;var top=function(e){return e.getBoundingClientRect().top+scrollY};
var t0=top(els[0]),last=els[els.length-1],span=top(last)+last.offsetHeight-t0,sum=0;els.forEach(function(e){sum+=e.offsetHeight});
var n=els.length,gap=Math.round((span-sum)/(n-1)),h=Math.round((span-gap*(n-1))/n);
els.forEach(function(e){e.style.setProperty('height',h+'px','important');e.querySelectorAll('*').forEach(function(c){c.style.setProperty('height','100%','important')});
var im=e.querySelector('img');if(im)im.style.setProperty('object-fit','cover','important')});
els.forEach(function(e,i){e.style.transform='translateY('+Math.round(t0+i*(h+gap)-top(e))+'px)'});},600)});</script>
</body>""", 1)
    if name == 'home':
        # "WATCH NOW" under Sermons is white on a light photo; give it a solid blue background.
        s = s.replace('</head>', '<style>a.wixui-button[href*="zbgDi1MM3fw"]{background:#046EB8!important;border-color:#046EB8!important;'
                      'box-shadow:0 2px 8px rgba(0,0,0,.35)!important}a.wixui-button[href*="zbgDi1MM3fw"] *{color:#fff!important}</style>\n</head>', 1)
    if name == 'home':
        # YouTube testimony video under the Sunday Walk Guide (Wix adds it with its own scripts).
        s = re.sub(r'(<div id="comp-mkxfegu5"[^>]*>)(</div>)',
                   r'\1<iframe src="https://www.youtube.com/embed/C3PYD58G69w" title="I didn&#x27;t believe God healed today, but God healed someone I prayed for" '
                   r'style="width:100%;height:100%;border:0;display:block" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture; fullscreen" '
                   r'allowfullscreen loading="lazy"></iframe>\2', s, 1)
        # Map: draw the walking route, then pop in the B1 marker, when the map scrolls into view (like the live site).
        s = s.replace('</head>', """<style>
#comp-m95o4vnc.tic-wait{clip-path:inset(0 100% 0 0)}
#comp-m95o4vnc.tic-go{animation:ticReveal 1.8s ease-out both}
#comp-l32dikmg.tic-wait{clip-path:circle(0% at 50% 50%)}
#comp-l32dikmg.tic-go{animation:ticPop .7s 1.6s cubic-bezier(.3,1.6,.6,1) both}
@keyframes ticReveal{from{clip-path:inset(0 100% 0 0)}to{clip-path:inset(0 0 0 0)}}
@keyframes ticPop{from{clip-path:circle(0% at 50% 50%);transform:scale(.6)}to{clip-path:circle(75% at 50% 50%);transform:scale(1)}}
@media (prefers-reduced-motion:reduce){#comp-m95o4vnc.tic-wait,#comp-l32dikmg.tic-wait{clip-path:none}#comp-m95o4vnc.tic-go,#comp-l32dikmg.tic-go{animation:none}}
</style>
</head>""", 1)
        s = s.replace('</body>', """<script>(function(){var r=document.getElementById('comp-m95o4vnc'),m=document.getElementById('comp-l32dikmg');
if(!r||!m||!('IntersectionObserver' in window))return;[r,m].forEach(function(e){e.classList.add('tic-wait')});
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){[r,m].forEach(function(x){x.classList.remove('tic-wait');x.classList.add('tic-go')});io.disconnect()}})},{threshold:.4});
io.observe(r)})();</script>
</body>""", 1)
    s = re.sub(r'(<body[^>]*>)', lambda m: m.group(1) + banner, s, 1)
    return s


def build(src, dst, mobile, log):
    os.makedirs(dst, exist_ok=True)
    pages = sorted(f[:-5] for f in os.listdir(src) if f.endswith('.html'))
    for p in pages:
        s = open(os.path.join(src, f'{p}.html'), encoding='utf-8').read()
        s = apply_fixes(p, s, log if not mobile else [])
        s = preview_wrap(p, s, pages, mobile)
        out = 'index.html' if p == 'home' else f'{p}.html'
        open(os.path.join(dst, out), 'w', encoding='utf-8').write(s)
    return pages


if __name__ == '__main__':
    desktop_src, mobile_src = sys.argv[1], sys.argv[2]
    out = os.path.join(ROOT, 'preview')
    log = []
    build(desktop_src, out, False, log)
    build(mobile_src, os.path.join(out, 'm'), True, log)
    with open(os.path.join(out, 'CHANGES.txt'), 'w', encoding='utf-8') as f:
        f.write('Corrected preview of taipeichurch.org. The live website was NOT modified; page layout is unchanged.\n'
                'Fixes applied (desktop and mobile versions):\n\nPage | Change | Count\n' + '\n'.join(log) +
                '\n\nPreview-only adjustments: yellow banner, no search indexing, Wix reveal animations switched off so all\n'
                'content is visible, homepage photo cropped towards the city.\n')
    print('\n'.join(log))
