"""Generates the proposal website in new/ (English by default, Traditional Chinese option).

Edit the text below, then run:  python3 tools/build_newsite.py
Every piece of text is written as T("English", "中文").
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'new')

MAPS = ('https://www.google.com/maps/place/Taipei+International+Church/@25.0781275,121.5471857,17z/data=!3m2!4b1!5s0x3442ac0e560c0d19:0x6abfbf84bf544af3'
        '!4m6!3m5!1s0x3442ae9007bd5ea5:0xecdffa70b2f7908!8m2!3d25.0781275!4d121.5497606!16s%2Fg%2F119vqfkkb')
LIVE = 'https://youtube.com/live/92o5PuY5Jyo'
YOUTUBE = 'https://www.youtube.com/channel/UCb_DF4LVCX5aLkdkOqmkyjA'
SPOTIFY = 'https://open.spotify.com/show/6KYo14ZcT2LvSujbNx273A'
NEWSLETTER = 'https://taipeichurch.us19.list-manage.com/subscribe?u=1b22dd056ddf40dff17202407&amp;id=8b123f88da'
GIVE_ONLINE = 'https://taipeichurch.eoffering.org.tw/'
GIVE_PAGE = 'https://www.taipeichurch.org/giving'
ZOOM = 'https://us02web.zoom.us/j/6807975448?pwd=WTFXYXRqZUJpTVNQTUJSUmFiamRBZz09'
ADDR_EN = 'B1, No. 41, Aly. 7, Ln. 397, Mingshui Rd., Zhongshan Dist., Taipei City 10466'
ADDR_ZH = '台北市中山區明水路397巷7弄41號B1'


def T(en, zh, tag='span', cls=''):
    c = f' class="{cls}"' if cls else ''
    return f'<{tag}{c} lang="en">{en}</{tag}><{tag}{c} lang="zh-Hant">{zh}</{tag}>'


def P(en, zh, cls=''):
    return T(en, zh, 'p', cls)


NAV = [
    ('index.html', 'Home', '首頁'),
    ('visit.html', 'Visit', '參觀教會'),
    ('about.html', 'About', '關於我們'),
    ('team.html', 'Team', '同工團隊'),
    ('connect.html', 'Groups & Serve', '小組與服事'),
    ('news.html', "What's On", '最新消息'),
]


def page(fname, title_en, body, desc):
    cur = ' aria-current="page"'
    nav = ''.join('<a href="%s"%s>%s</a>' % (h, cur if h == fname else '', T(en, zh)) for h, en, zh in NAV)
    return f'''<!doctype html>
<html lang="en" data-lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<title>{title_en} | Taipei International Church</title>
<meta name="description" content="{desc}">
<link rel="icon" href="img/tic-pin.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;700&display=swap">
<link rel="stylesheet" href="style.css">
<script>document.documentElement.classList.add("js")</script>
<script src="site.js" defer></script>
</head>
<body>
<div class="proposal">PROPOSAL for review · not the official website · <a href="https://www.taipeichurch.org/">taipeichurch.org</a> · <a href="../index.html">Reports</a></div>
<header class="top">
  <div class="wrap">
    <a class="brand" href="index.html"><img src="img/tic-logo.png" alt="TIC" width="40" height="36"><span><b>Taipei International Church</b><small>台北國際教會</small></span></a>
    <button class="lang" type="button">中文</button>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav">{T("Menu", "選單")}</button>
    <nav class="nav" id="nav" aria-label="Main">{nav}<a class="give" href="give.html">{T("Give", "奉獻")}</a></nav>
  </div>
</header>
<main>
{body}
</main>
<footer>
  <div class="wrap">
    <div class="cols">
      <div>
        <span class="logo"><img src="img/tic-logo.png" alt="Taipei International Church" width="54" height="48"></span>
        <p>Taipei International Church<br>{ADDR_EN}</p>
        <p lang="zh-TW" style="margin-top:6px">{ADDR_ZH}</p>
        <p style="margin-top:10px"><span class="email">info@taipeichurch.org</span></p>
      </div>
      <div><h4>{T("Sundays", "主日")}</h4><ul><li>{T("10:30 AM worship in Dazhi", "上午10:30 大直實體崇拜")}</li><li>{T("11:00 AM online", "上午11:00 線上崇拜")}</li><li><a href="visit.html">{T("Plan your visit", "計劃您的來訪")}</a></li></ul></div>
      <div><h4>{T("Connect", "連結")}</h4><ul><li><a href="connect.html">{T("Groups", "小組")}</a></li><li><a href="connect.html#serve">{T("Serve", "服事")}</a></li><li><a href="give.html">{T("Give", "奉獻")}</a></li><li><a href="give.html#pray">{T("Prayer", "代禱")}</a></li><li><a href="{NEWSLETTER}">{T("Newsletter", "電子報")}</a></li></ul></div>
      <div><h4>{T("Follow", "追蹤我們")}</h4><ul><li><a href="{YOUTUBE}">YouTube</a></li><li><a href="https://www.facebook.com/Taipei.Intl.Church/">Facebook</a></li><li><a href="https://www.instagram.com/tic_taipeichurch/">Instagram</a></li><li><a href="https://twitter.com/TIConlinechurch">X</a></li><li><a href="{SPOTIFY}">Spotify</a></li></ul></div>
    </div>
    <p class="legal">© Taipei International Church · 台北國際教會 · {T("Since 1957", "創立於1957年")}</p>
  </div>
</footer>
</body>
</html>
'''


def times():
    return f'''<div class="times" aria-label="Sunday times">
  <div class="time"><b>10:30</b><span>{T("Worship in person", "實體崇拜")}</span><small>{T("B1, TIC Worship Center, Dazhi", "大直 台北國際教會敬拜中心 B1")}</small></div>
  <div class="time"><b>11:00</b><span>{T("Online service", "線上崇拜")}</span><small><a href="{LIVE}">{T("Watch live on YouTube", "YouTube 直播")}</a></small></div>
  <div class="time"><b>11:20</b><span>TIC Kids</span><small>{T("Pre-K to grade 5", "學前班至五年級")}</small></div>
</div>'''


def path_card(href, img, alt, k_en, k_zh, h_en, h_zh, p_en, p_zh, go_en, go_zh):
    return f'''<a class="path" href="{href}"><img src="img/{img}" alt="{alt}" loading="lazy" width="1200" height="750">
<div><span class="lbl">{T(k_en, k_zh)}</span><h3>{T(h_en, h_zh)}</h3>{P(p_en, p_zh)}<span>{T(go_en, go_zh)} →</span></div></a>'''


HOME = f'''
<section class="hero" style="padding:0">
  <img src="img/taipei-skyline.jpg" alt="Taipei skyline with Taipei 101 at sunset" width="1200" height="800" fetchpriority="high">
  <div class="wrap">
    <div>
      <p class="eyebrow">台北國際教會 · SINCE 1957</p>
      <h1>{T('<small class="welcome">Welcome to</small>Taipei<br>International<br>Church', '<small class="welcome">歡迎來到</small>台北國際教會')}</h1>
      {P("A multicultural, multigenerational, English-speaking church filled with the power of the Holy Spirit. You belong here.", "一間多元文化、跨世代、以英語聚會、充滿聖靈能力的教會。這裡就是你的家。", "lede")}
      <div class="row"><a class="btn btn-y" href="visit.html">{T("Plan your visit", "計劃您的來訪")}</a><a class="btn btn-o" href="{LIVE}">{T("Watch online", "線上觀看")}</a></div>
    </div>
    {times()}
  </div>
</section>
<div class="strips" aria-label="Worship with us at 10:30 AM"><img src="img/strip-1.jpg" alt="" width="1600" height="100" loading="lazy"><img src="img/strip-2.jpg" alt="" width="1600" height="100" loading="lazy"><img src="img/strip-3.jpg" alt="" width="1600" height="100" loading="lazy"><img src="img/strip-4.jpg" alt="" width="1600" height="100" loading="lazy"><img src="img/strip-5.jpg" alt="" width="1600" height="100" loading="lazy"></div>

<section class="warm">
  <div class="wrap grid split">
    <div>
      <p class="kicker">{T("We've moved", "我們搬家了")}</p>
      <div class="head" style="margin-bottom:16px"><h2>{T("Our new home in Dazhi", "我們在大直的新家")}</h2></div>
      {P("We have officially moved into our new venue: a warm and beautiful space where we can worship and keep growing together in faith and fellowship. We meet in B1 at the TIC Worship Center, a 6-minute walk from Dazhi MRT Station.", "教會已正式遷入新的聚會場所，一個溫暖又美麗的空間，讓我們一同敬拜，並在信仰與團契中持續成長。我們在台北國際教會敬拜中心B1聚會，距離捷運大直站步行約6分鐘。", "muted")}
      <div class="row" style="margin-top:18px"><a class="btn btn-b" href="visit.html">{T("Directions & map", "交通與地圖")}</a><a class="btn btn-o" href="{MAPS}">Google Maps</a></div>
    </div>
    <div class="photo"><img src="img/entrance.jpg" alt="Entrance to the TIC Worship Center with the Taipei International Church sign" loading="lazy" width="1200" height="791"></div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="head"><p class="kicker">{T("Find your place", "找到你的位置")}</p><h2>{T("Get involved", "參與我們")}</h2></div>
    <div class="grid g4">
      {path_card("about.html", "church-family.jpg", "The TIC church family gathered in the sanctuary", "About", "關於", "The church", "認識教會", "Our beliefs, vision, values and history since 1957.", "我們的信仰、異象、價值與自1957年以來的歷史。", "Learn more", "了解更多")}
      {path_card("news.html#stories", "praise.jpg", "A worshipper lifting a hand during praise", "Stories", "見證", "My life changed at TIC", "我在台北國際教會的改變", "Real stories of what God is doing in our church family.", "聽聽教會家人分享神在他們生命中的作為。", "Listen now", "立即收聽")}
      {path_card("connect.html", "fellowship-meal.jpg", "Friends sharing a meal together", "Connect", "連結", "Meet new friends", "認識新朋友", "Join a small group and grow in faith during the week.", "加入小組，在平日一起在信仰中成長。", "Find a group", "尋找小組")}
      {path_card("connect.html#serve", "hospitality.jpg", "Hospitality volunteers in aprons", "Serve", "服事", "Opportunities", "服事機會", "Use your gifts on a Sunday team or in the community.", "在主日團隊或社區中發揮你的恩賜。", "Start serving", "開始服事")}
    </div>
  </div>
</section>

<section class="dark">
  <div class="wrap grid split">
    <div>
      <div class="head"><p class="kicker">{T("Messages", "講道信息")}</p><h2>{T("Every Sunday, wherever you are", "每個主日，無論你在哪裡")}</h2>
      {P("Join the live stream, catch up on recent sermons, or listen to the podcast on your commute.", "參加線上直播、收看近期講道，或在通勤時收聽 Podcast。")}</div>
      <div class="grid media">
        <a href="{LIVE}"><i>▶</i><span>{T("Live service", "線上直播")}<small>{T("Sundays 11:00 AM on YouTube", "每主日上午11:00 YouTube")}</small></span></a>
        <a href="https://youtu.be/zbgDi1MM3fw?t=288"><i>▶</i><span>{T("Latest sermon", "最新講道")}<small>{T("Watch now", "立即觀看")}</small></span></a>
        <a href="{SPOTIFY}"><i>♪</i><span>Podcast<small>Spotify</small></span></a>
      </div>
    </div>
    <div class="video"><iframe src="https://www.youtube-nocookie.com/embed/C3PYD58G69w" title="Testimony: I didn't believe God healed today, but God healed someone I prayed for" loading="lazy" allow="encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe></div>
  </div>
</section>

<section class="alt">
  <div class="wrap grid g2">
    <div class="card" style="background:var(--warm);border:0">
      <p class="kicker">{T("Our leaders", "教會同工")}</p>
      <h2 style="font-size:clamp(28px,6vw,40px)">{T("A warm group of people who love God, love people and love life", "一群愛神、愛人、熱愛生命的溫暖團隊")}</h2>
      <a class="btn btn-b" style="margin-top:18px" href="team.html">{T("Meet the team", "認識團隊")}</a>
    </div>
    <div class="card" id="pray">
      <p class="kicker">{T("Pray with us", "與我們一同禱告")}</p>
      <h2 style="font-size:clamp(28px,6vw,40px)">{T("Share a prayer request or a praise", "分享代禱事項或感恩")}</h2>
      {P("Our church family would love to pray with you and celebrate what God is doing.", "教會家人很樂意與你一同禱告，並為神的作為感恩。", "muted")}
      <div class="row" style="margin-top:16px"><a class="btn btn-y" href="give.html#pray">{T("Prayer request", "代禱事項")}</a><a class="btn btn-o" href="give.html#pray">{T("Share a praise", "分享感恩")}</a></div>
    </div>
  </div>
</section>
'''

VISIT = f'''
<section class="pagehead" style="padding:0"><img src="img/welcome-sign.jpg" alt="" width="1200" height="800"><div class="wrap">
<h1>{T("Plan your visit", "計劃您的來訪")}</h1>{P("Everything you need for your first Sunday at TIC.", "第一次來台北國際教會所需要的資訊。")}</div></section>

<section>
  <div class="wrap grid split">
    <div class="card">
      <p class="lbl">{T("Address", "地址")}</p>
      <p style="font-weight:700;font-size:18px;margin:6px 0 16px">{ADDR_EN}</p>
      <p class="lbl">{T("In Chinese · show your taxi driver", "中文地址 · 可出示給計程車司機")}</p>
      <p class="zhaddr" id="zh-addr">{ADDR_ZH}</p>
      <div class="row" style="margin-top:16px"><a class="btn btn-b" href="{MAPS}">Google Maps</a><button class="btn btn-o" type="button" data-copy="zh-addr">{T("Copy Chinese address", "複製中文地址")}</button></div>
    </div>
    <div>
      <div class="head" style="margin-bottom:14px"><p class="kicker">{T("Sunday walk guide", "主日步行指南")}</p><h2>{T("6 minutes from Dazhi MRT", "捷運大直站步行6分鐘")}</h2></div>
      <div class="map"><img src="img/walk-map.jpg" alt="Walking route from Dazhi MRT Station along Mingshui Road to the B1 entrance" width="1600" height="678" loading="lazy"></div>
    </div>
  </div>
</section>

<section class="alt">
  <div class="wrap grid split">
    <div>
      <div class="head"><p class="kicker">{T("Your first Sunday", "你的第一個主日")}</p><h2>{T("What to expect", "聚會流程")}</h2></div>
      <ol class="steps">
        <li data-n="1"><div>{T("<b>Arrive a little before 10:30</b><span>Look for the blue TIC sign and head down to B1.</span>", "<b>請在10:30前抵達</b><span>找到藍色的台北國際教會招牌，往下到B1。</span>")}</div></li>
        <li data-n="2"><div>{T("<b>Worship together</b><span>Families stay together for the singing, then children from Pre-K to grade 12 go to their programs.</span>", "<b>一同敬拜</b><span>全家一起參加詩歌敬拜，之後學前班至12年級的孩子前往各自的聚會。</span>")}</div></li>
        <li data-n="3"><div>{T("<b>Check in your kids</b><span>A parent or authorized adult checks each child in and out. Nursery care is available during the service.</span>", "<b>兒童報到</b><span>每位孩子都需由家長或授權的成人辦理報到及接回。崇拜期間提供育嬰室照顧。</span>")}</div></li>
        <li data-n="4"><div>{T("<b>Say hello at the welcome table</b><span>Ask questions, sign up for the newsletter or find a way to serve.</span>", "<b>到接待桌打個招呼</b><span>有問題可以詢問、訂閱電子報，或找到服事的機會。</span>")}</div></li>
      </ol>
    </div>
    <div class="photo"><img src="img/welcome-sign.jpg" alt="Church members welcoming people outside under the Taipei International Church sign" loading="lazy" width="1200" height="800"></div>
  </div>
</section>

<section class="warm" id="families">
  <div class="wrap">
    <div class="head"><p class="kicker">{T("Families", "家庭事工")}</p><h2>{T("Room for every generation", "每個世代都有位置")}</h2></div>
    <div class="grid g3">
      <div class="card"><p class="lbl">{T("Infants & toddlers", "嬰幼兒")}</p><h3 style="font-size:21px;margin:6px 0">{T("Nursery", "育嬰室")}</h3>{P("Loving care during the 10:30 service.", "上午10:30崇拜期間，由同工悉心照顧。", "muted")}</div>
      <div class="card"><p class="lbl">{T("Pre-K – grade 5", "學前班至五年級")}</p><h3 style="font-size:21px;margin:6px 0">TIC Kids · 11:20–12:00</h3>{P("Worship, Bible teaching and small groups by grade.", "敬拜、聖經教導，並依年級分組活動。", "muted")}</div>
      <div class="card"><p class="lbl">{T("Grades 7 – 12", "7至12年級")}</p><h3 style="font-size:21px;margin:6px 0">{T("Youth service", "青少年聚會")}</h3>{P("Every Sunday during the service.", "每主日崇拜時段。", "muted")}</div>
    </div>
    <div class="grid g3" style="margin-top:14px">
      <div class="photo"><img src="img/kids-stage.jpg" alt="Children singing on stage during Sunday worship" loading="lazy" width="1200" height="800"></div>
      <div class="photo"><img src="img/preschool.jpg" alt="Preschool class at TIC Kids" loading="lazy" width="1200" height="800"></div>
      <div class="photo"><img src="img/kids-worship.jpg" alt="Kids worshipping with their teacher" loading="lazy" width="1200" height="800"></div>
    </div>
  </div>
</section>
'''

VALUES = [
    ("Bible based", "以聖經為本", "Scripture shapes what we believe and how we live.", "聖經塑造我們的信仰與生活。"),
    ("Valuing diversity", "重視多元", "Many nations, cultures and ages, united in Christ.", "來自不同國家、文化與年齡，在基督裡合一。"),
    ("Expecting transformation", "期待生命改變", "Come as you are, but don't stay as you came.", "帶著原本的你來，但不要一成不變。"),
    ("Building community", "建立群體", "Life happens in small groups and serving teams.", "生命在小組與服事團隊中成長。"),
    ("Practicing servanthood", "實踐僕人精神", "Following Jesus by serving others.", "藉著服事他人跟隨耶穌。"),
]
TIMELINE = [
    ("1957", "First services for expats at Wesley Methodist Church, downtown Taipei.", "在台北市區衛理堂開始為外籍人士舉行聚會。"),
    ("1967", "Renamed Taipei International Methodist Church.", "更名為台北國際衛理教會。"),
    ("1972", "Becomes Taipei International Church.", "更名為台北國際教會。"),
    ("1989", "Moves with Taipei American School to Tianmu.", "隨台北美國學校遷至天母。"),
    ("1990s", "A Tagalog Fellowship begins for Filipino workers in Taiwan.", "為在台菲律賓勞工成立他加祿語團契。"),
    ("2021", "The church moves to Dazhi.", "教會遷至大直。"),
    ("2023", "Pastor Brad Warne begins as senior pastor.", "Brad Warne 牧師就任主任牧師。"),
    ("Today", "A new home in B1 at the TIC Worship Center on Mingshui Road.", "在明水路台北國際教會敬拜中心B1的新家。"),
]
PASTORS = [("Edward Knettler", "1957–60"), ("Franklin Smith", "1960–63"), ("William Ury", "1966–67"), ("Frank Manton", "1967–72"),
           ("William Ury", "1972–77"), ("Mike VanderPol", "1977–85"), ("Gene VanderWell", "1985–90"), ("Nate Showalter", "1990–98"),
           ("Paul Ko", "1993–2013 · Tagalog Fellowship"), ("Mike Osment", "2000–03"), ("Kim Crutchfield", "2003–10"), ("Michael Payne", "2011–15"),
           ("Roberto Awa-Ao", "2014–present · Filipino Ministry"), ("Mike VanderPol", "2015–16 · interim"), ("Peter Palma", "2016–22"),
           ("Nate Showalter", "2022 · interim"), ("Brad Warne", "2023–present")]

VALUES_HTML = ''.join('<div class="card"><h3 style="font-size:19px;color:var(--blue)">%s</h3>%s</div>' % (T(a, b), P(c, d, 'muted')) for a, b, c, d in VALUES)
TIMELINE_HTML = ''.join('<li><b>%s</b>%s</li>' % (y, P(e, z)) for y, e, z in TIMELINE)
PASTORS_HTML = ''.join('<tr><td>%s</td><td>%s</td></tr>' % (n, y) for n, y in PASTORS)

ABOUT = f'''
<section class="pagehead" style="padding:0"><img src="img/church-family.jpg" alt="" width="1200" height="800"><div class="wrap">
<h1>{T("About TIC", "關於我們")}</h1>{P("A non-denominational, English-speaking church in Taipei, welcoming people from every nation and background since 1957.", "自1957年以來，一間不分宗派、以英語聚會的教會，歡迎來自各國、各種背景的人。")}</div></section>

<section>
  <div class="wrap grid split">
    <div><p class="kicker">{T("Our vision", "我們的異象")}</p>
    <blockquote class="big">{T("Disciples who shine the light of God's love on <em>Taipei, Taiwan</em> and the world.", "成為將神的愛之光照耀<em>台北、台灣</em>與全世界的門徒。")}</blockquote></div>
    <div>
      {P("<strong>Our mission:</strong> we are a multicultural, multigenerational, English-speaking church filled with the power of the Holy Spirit. We proclaim the good news in word and action, and bring glory to God in all we do.", "<strong>我們的使命：</strong>我們是一間多元文化、跨世代、以英語聚會、充滿聖靈能力的教會。我們以言語和行動傳揚福音，凡事榮耀神。", "muted")}
      <div class="facts" style="margin-top:18px"><div><b>1957</b>{T("First service", "首次聚會")}</div><div><b>5</b>{T("Mission areas", "使命範疇")}</div><div><b>B1</b>{T("Home in Dazhi", "大直的家")}</div></div>
      <div class="tags" style="margin-top:14px"><span>Worship</span><span>Connect</span><span>Grow</span><span>Serve</span><span>Go</span></div>
    </div>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <div class="head"><p class="kicker">{T("Our values", "我們的價值")}</p><h2>{T("What shapes us", "塑造我們的價值")}</h2></div>
    <div class="grid g3">{VALUES_HTML}</div>
  </div>
</section>

<section>
  <div class="wrap grid g2">
    <div class="card creed">
      <p class="lbl">{T("Statement of faith", "信仰告白")}</p>
      <h3>{T("The Apostles' Creed", "使徒信經")}</h3>
      {P("I believe in God, the Father almighty, creator of heaven and earth. I believe in Jesus Christ, his only Son, our Lord, who was conceived by the Holy Spirit, born of the Virgin Mary, suffered under Pontius Pilate, was crucified, died, and was buried; he descended to the dead. On the third day he rose again; he ascended into heaven, he is seated at the right hand of the Father, and he will come to judge the living and the dead. I believe in the Holy Spirit, the holy catholic Church, the communion of saints, the forgiveness of sins, the resurrection of the body, and the life everlasting. Amen.",
         "我信上帝，全能的父，創造天地的主。我信我主耶穌基督，上帝的獨生子；因聖靈感孕，由童貞女馬利亞所生；在本丟彼拉多手下受難，被釘於十字架，受死，埋葬；降在陰間；第三天從死人中復活；升天，坐在全能父上帝的右邊；將來必從那裡降臨，審判活人死人。我信聖靈；我信聖而公之教會；我信聖徒相通；我信罪得赦免；我信身體復活；我信永生。阿們。")}
    </div>
    <div class="card">
      <p class="lbl">{T("What we believe", "我們的信仰")}</p>
      <h3 style="font-size:30px;margin:6px 0 12px">{T("Jesus is Lord", "耶穌是主")}</h3>
      {P("We confess Jesus Christ as Lord and Savior and seek to glorify God the Father, Son and Holy Spirit.", "我們承認耶穌基督是主和救主，並尋求榮耀聖父、聖子、聖靈三一真神。", "muted")}
      {P("The Bible is God's unique revelation: inspired, infallible, and the supreme and final authority in all it teaches.", "聖經是神獨特的啟示，是受感、無誤的，並在其所教導的一切事上具有至高與最終的權威。", "muted")}
      <p class="muted" style="font-size:14px;margin-top:10px">Deut 6:4–9 · 2 Tim 3:15–16 · Heb 4:12 · 1 Thess 2:13 · 1 Pet 2:21</p>
    </div>
  </div>
</section>

<section class="dark" id="history">
  <div class="wrap">
    <div class="head"><p class="kicker">{T("Our story", "我們的故事")}</p><h2>{T("A light in Taipei since 1957", "自1957年在台北發光")}</h2>
    {P("In October 1957, Methodist missionary Pastor Edward Knettler began English services for expats in downtown Taipei.", "1957年10月，衛理公會傳教士 Edward Knettler 牧師開始在台北市區為外籍人士舉行英語聚會。")}</div>
    <ul class="timeline">{TIMELINE_HTML}</ul>
    <details class="more-box"><summary>{T("All our pastors", "歷任牧師")}</summary><div class="tbl"><table>{PASTORS_HTML}</table></div></details>
  </div>
</section>
'''

STAFF = [("brad", "Brad Warne", "Pastor", "牧師"), ("jennifer", "Jennifer Cheng", "Executive Assistant", "行政助理"),
         ("joe", "Joe C. Phanoella", "Director of Media & Technology", "媒體與科技總監"), ("dior", "Diorella Yu de Leon", "Account Manager", "帳務經理"),
         ("vivian", "Vivian Hu", "Finance", "財務")]
ELDERS = [("eric", "Eric Lin", "Chair of Elders", "長老會主席"), ("annmarie", "Ann-Marie Padgett", "Elder", "長老"), ("alita", "Alita Wang", "Elder", "長老"),
          ("daniel", "Daniel Teng", "Elder", "長老"), ("jun", "Jun Baldoz", "Elder", "長老"), ("henry", "Henry Liu", "Treasurer", "司庫")]


def people(lst):
    items = ['<div class="person"><img src="img/team-%s.jpg" alt="%s" loading="lazy" width="360" height="360"><b>%s</b>%s</div>' % (k, n, n, T(r, z)) for k, n, r, z in lst]
    return '<div class="people">' + ''.join(items) + '</div>'


TEAM = f'''
<section class="pagehead" style="padding:0"><div class="wrap">
<h1>{T("Meet the team", "認識我們的團隊")}</h1>{P("Our pastoral staff, administrative staff and elders are a warm group of people who love God, love people and love life.", "我們的牧養同工、行政同工與長老，是一群愛神、愛人、熱愛生命的溫暖團隊。")}</div></section>
<section><div class="wrap"><div class="head"><p class="kicker">{T("Staff", "同工")}</p></div>{people(STAFF)}</div></section>
<section class="alt"><div class="wrap"><div class="head"><p class="kicker">{T("Elders & treasurer", "長老與司庫")}</p></div>{people(ELDERS)}</div></section>
'''

GROUPS = [
    ("person women", "Tuesdays · 10:00–11:30 AM", "每週二 上午10:00–11:30", "Women's Bible Study", "姊妹查經", "At the TIC Ministry Center in Dazhi.", "在大直台北國際教會事工中心。"),
    ("online ya men", "2nd & 4th Tuesdays", "每月第二、四個週二", "Young Adult Men", "青年弟兄查經", "Online Bible study for men ages 18–35.", "18–35歲弟兄的線上查經。"),
    ("person ya", "Wednesdays · 7:30–9:30 PM", "每週三 晚上7:30–9:30", "Young Adults Bible Study", "青年查經", "College age to mid-30s, in Dazhi.", "大學生至30多歲，在大直聚會。"),
    ("online", "Wednesdays · 8:00–9:00 PM", "每週三 晚上8:00–9:00", "Community Bible Study", "社區查經", "On Zoom, studying Matthew.", "Zoom 線上，研讀馬太福音。"),
    ("online men", "Wednesdays · 8:30–9:30 PM", "每週三 晚上8:30–9:30", "Men's Bible Study", "弟兄查經", f'On Zoom, studying Luke. <a href="{ZOOM}">Join on Zoom</a>', f'Zoom 線上，研讀路加福音。<a href="{ZOOM}">加入 Zoom</a>'),
    ("online prayer", "Fridays · 12:00–12:30 PM", "每週五 中午12:00–12:30", "Friday Zoom Prayer", "週五 Zoom 禱告會", f'Lunchtime prayer online. <a href="{ZOOM}">Join on Zoom</a>', f'午間線上禱告。<a href="{ZOOM}">加入 Zoom</a>'),
    ("person", "Fridays · 7:00–9:00 PM", "每週五 晚上7:00–9:00", "Life Group", "生命小組", "At a host's home in Taipei.", "在台北的接待家庭聚會。"),
    ("person", "Every other Saturday · 10:00–11:30 AM", "隔週六 上午10:00–11:30", "Shilin Saturday Group", "士林週六小組", "Near Taipei American School.", "靠近台北美國學校。"),
    ("person men", "One Saturday a month", "每月一個週六", "Men's Group", "弟兄聚會", "Fellowship and food.", "團契與美食。"),
    ("person ya women", "One Saturday afternoon a month", "每月一個週六下午", "Kingdom Young Women", "國度青年姊妹", "For women ages 18–35.", "18–35歲姊妹。"),
    ("person prayer", "Last Sunday of the month", "每月最後一個主日", "Worship Circle", "敬拜圈", "Extended worship and prayer for revival.", "延長的敬拜與為復興禱告。"),
    ("person", "Sundays · 5:00–7:00 PM", "每主日 下午5:00–7:00", "Neihu Bible Study", "內湖查經", "A Sunday evening group in Neihu.", "在內湖的主日晚間小組。"),
    ("online prayer", "Mondays · 7:30–8:00 PM", "每週一 晚上7:30–8:00", "Monday LINE Prayer", "週一 LINE 禱告會", "Pray together on LINE.", "在 LINE 上一同禱告。"),
    ("online prayer", "Every day", "每天", "Daily Prayer Group", "每日禱告群組", "A LINE group for prayer requests.", "分享代禱事項的 LINE 群組。"),
]
TEAMS = [("Worship", "敬拜團", "Lead the church in song.", "帶領會眾敬拜。"), ("Welcome", "招待", "Greet guests and newcomers.", "迎接訪客與新朋友。"),
         ("Tech", "音控", "Run sound and video.", "負責音響與影像。"), ("Media", "媒體", "Capture services and run the livestream.", "拍攝崇拜並負責直播。"),
         ("Kids", "兒童", "Teach and care for preschool to grade 5.", "教導並照顧學前至五年級的孩子。"), ("Youth", "青少年", "Walk alongside our teenagers.", "陪伴青少年成長。"),
         ("Hospitality", "愛宴", "Coffee, refreshments and care for people in need.", "咖啡、茶點，並關懷有需要的人。")]

GROUPS_HTML = ''.join('<div class="card group" data-t="%s"><span class="when">%s</span><h3>%s</h3>%s</div>' % (t, T(we, wz), T(ne, nz), P(de, dz)) for t, we, wz, ne, nz, de, dz in GROUPS)
TEAMS_HTML = ''.join('<div class="card"><h3 style="font-size:19px">%s</h3>%s</div>' % (T(a, b), P(c, d, 'muted')) for a, b, c, d in TEAMS)

CONNECT = f'''
<section class="pagehead" style="padding:0"><img src="img/fellowship-meal.jpg" alt="" width="1200" height="800"><div class="wrap">
<h1>{T("Groups & serve", "小組與服事")}</h1>{P("Church gets personal in smaller groups. Meet new friends, study the Bible and pray together through the week.", "在小組中，教會生活更貼近彼此。平日一起認識新朋友、查經與禱告。")}</div></section>

<section>
  <div class="wrap">
    <div class="head"><p class="kicker">{T("Find a group", "尋找小組")}</p><h2>{T("Groups for every week", "每週的小組")}</h2></div>
    <div class="chips" role="group" aria-label="Filter groups" style="margin-bottom:18px">
      <button class="chip" type="button" data-f="all" aria-pressed="true">{T("All", "全部")}</button>
      <button class="chip" type="button" data-f="person" aria-pressed="false">{T("In person", "實體")}</button>
      <button class="chip" type="button" data-f="online" aria-pressed="false">{T("Online", "線上")}</button>
      <button class="chip" type="button" data-f="ya" aria-pressed="false">{T("Young adults", "青年")}</button>
      <button class="chip" type="button" data-f="men" aria-pressed="false">{T("Men", "弟兄")}</button>
      <button class="chip" type="button" data-f="women" aria-pressed="false">{T("Women", "姊妹")}</button>
      <button class="chip" type="button" data-f="prayer" aria-pressed="false">{T("Prayer", "禱告")}</button>
    </div>
    <div class="grid g3">{GROUPS_HTML}</div>
    {P('Contact any group: <span class="email">info@taipeichurch.org</span>', '聯絡任何小組：<span class="email">info@taipeichurch.org</span>', "muted")}
  </div>
</section>

<section class="warm">
  <div class="wrap grid split">
    <div class="photo"><img src="img/filipino-ministry.jpg" alt="Filipino Ministry members in matching yellow shirts" loading="lazy" width="1200" height="800"></div>
    <div>
      <div class="head" style="margin-bottom:14px"><p class="kicker">{T("Tagalog · Pastor Obet", "他加祿語 · Obet 牧師")}</p><h2>{T("Filipino Ministry", "菲律賓事工")}</h2></div>
      <div class="grid">
        <div class="card"><b>Taipei</b> · {T("Sundays 2:00 PM", "主日 下午2:00")}<br><span class="muted">2F-1, No. 26, Zhongshan N. Rd. Sec. 3 · 台北市中山區中山北路3段26號2F-1</span></div>
        <div class="card"><b>Taoyuan</b> · {T("Sundays 10:30 AM", "主日 上午10:30")}<br><span class="muted">Mamsky Pinoy Restaurant, 208 ShanYing Rd, Guishan · 桃園市龜山區山鶯路208號</span></div>
        <div class="card"><b>Hualien</b> · {T("Sundays 10:30 AM", "主日 上午10:30")}<br><span class="muted">{T("Looking for a new venue", "正在尋找新場地")}</span></div>
      </div>
    </div>
  </div>
</section>

<section id="serve">
  <div class="wrap">
    <div class="head"><p class="kicker">{T("Serve", "服事")}</p><h2>{T("Use your gifts", "發揮你的恩賜")}</h2>
    {P("Every member is rooted in Christ and empowered to serve. Stop by the welcome table on Sunday to get started.", "每位肢體都在基督裡扎根，並被賦予服事的能力。主日請到接待桌開始參與。")}</div>
    <div class="grid g4">{TEAMS_HTML}
      <div class="photo"><img src="img/media-team.jpg" alt="Media team members filming the service" loading="lazy" width="1200" height="800"></div></div>
  </div>
</section>
'''

NEWS = f'''
<section class="pagehead" style="padding:0"><img src="img/worship-band.jpg" alt="" width="1200" height="800"><div class="wrap">
<h1>{T("What's on", "最新消息")}</h1>{P("This week at TIC, stories from our church family and messages to watch.", "本週活動、教會家人的見證，以及可以收看的講道。")}</div></section>

<section>
  <div class="wrap grid split">
    <div class="card" style="background:var(--yellow);color:var(--yellow-ink);border:0">
      <p class="lbl" style="color:var(--yellow-ink)">{T("This Sunday", "本主日")}</p>
      <p style="font:700 52px/1 var(--display)">SEP 27</p>
      <h3 style="font-size:30px;margin:8px 0">{T("Sunday service · 10:30 AM", "主日崇拜 · 上午10:30")}</h3>
      {P("A message on generosity from 2 Corinthians 9:6–15. In person in Dazhi and live online at 11:00 AM.", "講道主題：慷慨（哥林多後書9:6–15）。大直實體聚會，上午11:00線上直播。")}
    </div>
    <div class="grid">
      <div class="card"><span class="lbl">{T("Tuesdays", "每週二")}</span><br><b>{T("Women's Bible Study", "姊妹查經")}</b> · 10:00–11:30 AM</div>
      <div class="card"><span class="lbl">{T("Wednesdays", "每週三")}</span><br><b>{T("Young Adults Bible Study", "青年查經")}</b> · 7:30–9:30 PM</div>
      <div class="card"><span class="lbl">{T("Monthly", "每月")}</span><br><b>{T("Men's Group", "弟兄聚會")}</b> · {T("one Saturday", "一個週六")}</div>
      <div class="card"><span class="lbl">{T("Last Sunday", "每月最後主日")}</span><br><b>{T("Worship Circle", "敬拜圈")}</b></div>
    </div>
  </div>
</section>

<section class="alt" id="stories">
  <div class="wrap">
    <div class="head"><p class="kicker">{T("Stories", "見證")}</p><h2>{T("My life changed at TIC", "我在台北國際教會的改變")}</h2></div>
    <div class="grid g3">
      <div class="card"><h3 style="font-size:21px">Surrendered</h3>{P("Iquo Phillip shares about the loss of her son and how TIC became her family's home in Taiwan.", "Iquo Phillip 分享失去兒子的經歷，以及台北國際教會如何成為她家人在台灣的家。", "muted")}</div>
      <div class="card"><h3 style="font-size:21px">Make Room</h3>{P("Our 2025 InterGen & Young Adults retreat at Ting Tao Camp in Yilan.", "2025年跨世代與青年退修會，在宜蘭聽濤營舉行。", "muted")}</div>
      <div class="card"><h3 style="font-size:21px">{T("Sent to the nations", "差派到萬國")}</h3>{P("Mission trips to Madagascar and the Philippines, and helping a young woman come home from Cambodia.", "前往馬達加斯加與菲律賓的宣教之旅，並幫助一位年輕女子從柬埔寨返家。", "muted")}</div>
    </div>
    <div class="grid g4" style="margin-top:14px">
      <div class="card"><b>Dion</b>{P("Healed after eight years of pain from a sports injury.", "運動傷害疼痛八年後得醫治。", "muted")}</div>
      <div class="card"><b>Mae</b>{P("Learned to depend completely on God through paralysis.", "在癱瘓中學會完全依靠神。", "muted")}</div>
      <div class="card"><b>Vivian</b>{P("Baptized in 2019 during cancer treatment.", "2019年在癌症治療期間受洗。", "muted")}</div>
      <div class="card"><b>Dior</b>{P("Saw God heal someone she prayed for.", "親眼看見神醫治她所代禱的人。", "muted")}</div>
    </div>
  </div>
</section>

<section class="dark">
  <div class="wrap grid split">
    <div class="video"><iframe src="https://www.youtube-nocookie.com/embed/C3PYD58G69w" title="Testimony video" loading="lazy" allow="encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe></div>
    <div class="grid media">
      <a href="{LIVE}"><i>▶</i><span>{T("Live service", "線上直播")}<small>{T("Sundays 11:00 AM", "每主日上午11:00")}</small></span></a>
      <a href="{YOUTUBE}"><i>▶</i><span>{T("All sermons", "所有講道")}<small>YouTube</small></span></a>
      <a href="{SPOTIFY}"><i>♪</i><span>Podcast<small>Spotify</small></span></a>
    </div>
  </div>
</section>
'''

GIVE = f'''
<section class="pagehead" style="padding:0"><div class="wrap">
<h1>{T("Give & pray", "奉獻與代禱")}</h1>{P("Your giving supports ministry in Taipei, care for people in need, and missionaries around the world.", "您的奉獻支持台北的事工、關懷有需要的人，以及世界各地的宣教士。")}</div></section>

<section>
  <div class="wrap grid split">
    <div class="card">
      <p class="kicker">{T("Ways to give", "奉獻方式")}</p>
      <div class="ways">
        <div class="way"><i>1</i><div>{T("<b>Credit card</b><br><span class='muted'>Give online through our secure giving page.</span>", "<b>信用卡</b><br><span class='muted'>透過安全的線上奉獻頁面奉獻。</span>")}</div></div>
        <div class="way"><i>2</i><div>{T("<b>Bank transfer (TWD)</b><br><span class='muted'>Domestic transfer. Account details are on the giving page.</span>", "<b>國內台幣轉帳</b><br><span class='muted'>帳戶資料請見奉獻頁面。</span>")}</div></div>
        <div class="way"><i>3</i><div>{T("<b>Overseas wire</b><br><span class='muted'>Email the last four digits of your account and the amount to giving@taipeichurch.org.</span>", "<b>海外匯款</b><br><span class='muted'>請將帳號末四碼與金額寄至 giving@taipeichurch.org。</span>")}</div></div>
      </div>
      <div class="row"><a class="btn btn-y" href="{GIVE_ONLINE}">{T("Give online", "線上奉獻")}</a><a class="btn btn-o" href="{GIVE_PAGE}">{T("Bank details", "帳戶資料")}</a></div>
      {P("Need an annual tax receipt? Ask giving@taipeichurch.org for a TIC Intentional Giving ID.", "需要年度奉獻收據嗎？請向 giving@taipeichurch.org 申請奉獻編號。", "muted")}
    </div>
    <div class="card" id="pray" style="background:var(--blue);color:#fff;border:0">
      <p class="kicker" style="color:var(--yellow)">{T("Pray with us", "與我們一同禱告")}</p>
      <h2 style="font-size:clamp(30px,7vw,44px)">{T("Share a prayer request or a praise", "分享代禱事項或感恩")}</h2>
      {P("Write to us and our prayer team will pray with you. You can also join the Friday Zoom prayer or the daily LINE prayer group.", "寫信給我們，禱告團隊會與你一同禱告。你也可以參加週五 Zoom 禱告會或每日 LINE 禱告群組。")}
      <p style="margin-top:14px"><span class="email">info@taipeichurch.org</span></p>
      <div class="row" style="margin-top:14px"><a class="btn btn-y" href="https://www.taipeichurch.org/contact">{T("Send a request", "送出代禱")}</a><a class="btn btn-o" href="connect.html">{T("Prayer groups", "禱告小組")}</a></div>
    </div>
  </div>
</section>
'''

PAGES = [
    ('index.html', 'Home', HOME, 'Taipei International Church (TIC) is a multicultural, multigenerational, English-speaking church in Dazhi, Taipei. Sunday worship 10:30 AM, online 11:00 AM.'),
    ('visit.html', 'Plan your visit', VISIT, 'Plan your first Sunday at Taipei International Church in Dazhi: address in English and Chinese, walking map from Dazhi MRT, kids and families.'),
    ('about.html', 'About', ABOUT, "Vision, mission, values, beliefs and history of Taipei International Church since 1957."),
    ('team.html', 'Team', TEAM, 'Meet the pastor, staff and elders of Taipei International Church.'),
    ('connect.html', 'Groups & serve', CONNECT, 'Small groups, prayer meetings, Filipino Ministry and serving teams at Taipei International Church.'),
    ('news.html', "What's on", NEWS, "What's on at Taipei International Church: this Sunday, weekly groups, stories and sermons."),
    ('give.html', 'Give & pray', GIVE, 'Give to Taipei International Church or share a prayer request.'),
]

if __name__ == '__main__':
    for fname, title, body, desc in PAGES:
        with open(os.path.join(OUT, fname), 'w', encoding='utf-8') as f:
            f.write(page(fname, title, body, desc))
    print('Built', len(PAGES), 'pages into new/')
