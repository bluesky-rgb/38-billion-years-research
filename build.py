"""Build the research site from data/*.json."""
import json, os, html
HERE = os.path.dirname(os.path.abspath(__file__))
def J(n): return json.load(open(os.path.join(HERE, 'data', n), encoding='utf-8'))
CH, TL, NOTES, EPS, METHOD, VIS = J('chapters.json'), J('timeline.json'), J('notes.json'), J('episodes.json'), J('method.json'), J('vision.json')
VID = 'https://bluesky-rgb.github.io/38-billion-years-video/site/'
REPO_V = 'https://github.com/bluesky-rgb/38-billion-years-video'
REPO_R = 'https://github.com/bluesky-rgb/38-billion-years-research'
e_ = html.escape
NOTE = {n['id']: n for n in NOTES}
EP = {e['id']: e for e in EPS}
EP_CH = {1: 'earth', 2: 'earth', 3: 'life', 4: 'life', 5: 'life', 6: 'cell', 7: 'cell', 8: 'planet', 9: 'body', 10: 'body', 11: 'body', 12: 'body', 13: 'land', 14: 'land', 15: 'land', 16: 'mammal', 17: 'mammal', 18: 'mammal', 19: 'human', 20: 'human', 21: 'human', 22: 'human', 23: 'human', 24: 'human', 25: 'society', 26: 'society'}
CHD = {c['id']: c for c in CH}
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@600;900&family=Noto+Sans+SC:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap">'
NAV = [('index.html', '首页'), ('ch-earth.html', '章节'), ('timeline.html', '大时间轴'), ('questions.html', '问答'), ('glossary.html', '概念词典'), ('method.html', '方法'), (VID, '视频系列'), (REPO_R, 'GitHub')]
def nav(cur):
    s = '<nav class="nav" aria-label="网站导航"><a class="brand" href="index.html">38 亿年 · 研究笔记</a>'
    for h, l in NAV:
        on = ' aria-current="page"' if cur == h or (cur.startswith('ch-') and h == 'ch-earth.html') else ''
        s += f'<a href="{h}"{on}>{l}</a>'
    return s + '</nav>'
def page(name, title, desc, body):
    open(os.path.join(HERE, name), 'w', encoding='utf-8').write(f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e_(title)}</title><meta name="description" content="{e_(desc)}">{FONTS}<link rel="stylesheet" href="style.css"></head>
<body><div class="wrap">{nav(name)}{body}<p class="foot">内容采用 CC BY-NC 4.0。配套视频：<a href="{VID}">《38 亿年家谱》</a>。</p></div></body></html>
''')
def sec(t, inner, lead=''): return f'<section class="block"><h2>{t}</h2>{f"<p class=col>{lead}</p>" if lead else ""}{inner}</section>'
def note_html(n):
    return f'<article class="note" id="{n["id"]}"><h3>{e_(n["title"])}</h3><p class="q">{e_(n["q"])}</p><ul>{"".join(f"<li>{e_(x)}</li>" for x in n["a"])}</ul></article>'
def vids(ids):
    out = ''
    for i in ids:
        e = EP.get(i)
        if not e: continue
        s = ['第 0 季', '第 1 季', '第 2 季', '第 3 季', '第二部'][e['season']]
        out += f'<a href="{VID}ep{i:02d}.html"><img src="{VID}posters/ep{i}.jpg" alt="" loading="lazy"><span><b>{e_(e["title"])}</b><span>{s} · 第 {e["episode"]} 集 · 看视频</span></span></a>'
    return f'<div class="vids">{out}</div>' if out else '<p class="col">这一章对应的视频还在规划中。</p>'
def fmt_age(a):
    if a >= 1: return f'{a:g} 亿年前'
    w = a * 10000
    return f'{w:g} 万年前' if w >= 1 else f'{w * 10000:g} 年前'

# ---------- chapters ----------
for k, c in enumerate(CH):
    cards = [cd for i in c['eps'] for cd in EP[i]['concept_cards']] if c['eps'] else []
    chips = '<div class="chips">' + ''.join(f'<span class="chip"><b>{e_(x["term"])}</b>{e_(x["definition"])}</span>' for x in cards) + '</div>' if cards else '<p class="col">待视频制作时补充。</p>'
    ev = [t for t in TL if t['ch'] == c['id']]
    evh = '<ol class="dt">' + ''.join(f'<li><time>{fmt_age(t["age"])}</time><span>{e_(t["text"])}</span></li>' for t in sorted(ev, key=lambda x: -x['age'])) + '</ol>'
    prev = f'<a href="ch-{CH[k - 1]["id"]}.html">← {CH[k - 1]["n"]}. {e_(CH[k - 1]["title"])}</a>' if k else '<a href="index.html">← 首页</a>'
    nxt = f'<a href="ch-{CH[k + 1]["id"]}.html">{CH[k + 1]["n"]}. {e_(CH[k + 1]["title"])} →</a>' if k + 1 < len(CH) else '<a href="timeline.html">大时间轴 →</a>'
    body = f'''<header class="page-head"><p class="kicker">第 {c["n"]} 章 · {c["span"]}</p><h1>{e_(c["title"])}</h1><p class="lede">{e_(c["sub"])}</p></header>
<p class="thesis">{e_(c["thesis"])}</p>
{sec("因果链", '<ol class="chain">' + "".join(f"<li>{e_(x)}</li>" for x in c["chain"]) + '</ol>', "按正向流程排列：每一步都是下一步的前提。")}
{sec("关键事件", evh)}
{sec("问与答", '<div class="notes">' + "".join(note_html(NOTE[i]) for i in c["notes"] if i in NOTE) + '</div>', "制作中真实提出过的问题。")}
{sec("关键概念", chips)}
{sec("还没有定论的地方", '<ul class="open">' + "".join(f"<li>{e_(x)}</li>" for x in c["open"]) + '</ul>', "科学还在推进，这些地方写进视频时都用了“可能”“科学家认为”。")}
{sec("对应的视频", vids(c["eps"]))}
<nav class="pager" aria-label="翻页">{prev}{nxt}</nav>'''
    page(f'ch-{c["id"]}.html', f'{c["title"]} · 38 亿年研究笔记', c['thesis'], body)

# ---------- index ----------
lines = '<div class="tbl"><table class="lines"><thead><tr><th>时间</th><th>合作：谁和谁组成整体</th><th>信息：靠什么记住和传递</th></tr></thead><tbody>' + ''.join(
    f'<tr{" class=gene" if i == 4 else ""}><td class="k">{e_(l["era"])}</td><td>{e_(l["coop"])}</td><td>{e_(l["info"])}</td></tr>' for i, l in enumerate(VIS['lines'])) + '</tbody></table></div>'
chaps = '<div class="chapters">' + ''.join(f'<a class="chap" href="ch-{c["id"]}.html"><span class="no">第 {c["n"]} 章 · {c["span"]}</span><h3>{e_(c["title"])}</h3><span class="sub">{e_(c["sub"])}</span><p>{e_(c["thesis"])}</p></a>' for c in CH) + '</div>'
nterms = sum(len(e['concept_cards']) for e in EPS)
body = f'''<header class="top"><p class="kicker">研究笔记 · 我们对"你从哪里来"的理解</p><h1>38 亿年<em>研究笔记</em></h1>
<p class="lede">从星云收缩成太阳，到细胞、脊梁、登陆，再到人和社会。这里把制作视频过程中弄懂的东西，按主题整理成一条完整的因果链。</p>
<div class="facts"><span><b>{len(CH)}</b>个章节</span><span><b>{len(NOTES)}</b>个问答</span><span><b>{nterms}</b>个概念</span><span><b>{len(TL)}</b>个关键事件</span></div></header>
<p class="thesis">{e_(VIS["thesis"])}</p>
{sec("两条主线", lines, "每一次大跃迁都同时发生两件事：原本独立的单位合作成更大的整体，信息有了新的储存和传递方式。从 7 万年前那一行起，变化从靠基因改为靠文化。")}
{sec("七个章节", chaps)}
{sec("终点：社会的本质", '<ul class="plain">' + "".join(f"<li>{e_(x)}</li>" for x in VIS["society"]) + '</ul>', "这是整个研究最初的问题。往回追到生命起源，是为了让答案有根。")}
{sec("怎么读", '<ul class="plain"><li>想看全景：先读“两条主线”，再看<a href="timeline.html">大时间轴</a>。</li><li>想弄懂某件事：进对应章节，按因果链从上往下读。</li><li>遇到生词：查<a href="glossary.html">概念词典</a>。</li><li>想看画面：每章末尾都链接了对应的视频。</li></ul>')}'''
page('index.html', '38 亿年研究笔记', '我们对“你从哪里来”的理解：两条主线、七个章节、大时间轴、问答与概念词典。', body)

# ---------- timeline ----------
items = ''.join(f'<li><time>{fmt_age(t["age"])}</time><span>{e_(t["text"])}{f" · <a href={chr(34)}{VID}ep{t[chr(101)+chr(112)]:02d}.html{chr(34)}>视频</a>" if t["ep"] else ""}</span><a class="c" href="ch-{t["ch"]}.html">{e_(CHD[t["ch"]]["title"])}</a></li>' for t in sorted(TL, key=lambda x: -x['age']))
import math
X = lambda a: 40 + (math.log10(46) - math.log10(max(a, 0.0005))) / (math.log10(46) - math.log10(0.0005)) * 900
svg = ['<svg viewBox="0 0 980 150" role="img" aria-label="对数时间轴：越接近今天，刻度越密"><rect x="40" y="70" width="900" height="5" rx="2" class="tl-bar"/>']
for a, lab in ((46, '46 亿'), (10, '10 亿'), (1, '1 亿'), (0.1, '1000 万'), (0.01, '100 万'), (0.001, '10 万'), (0.0005, '5 万年前')):
    svg.append(f'<line x1="{X(a):.0f}" x2="{X(a):.0f}" y1="78" y2="88" class="tl-tick"/><text x="{X(a):.0f}" y="106" text-anchor="middle" class="tl-lab">{lab}</text>')
cols = {c['id']: c['n'] for c in CH}
for t in TL:
    svg.append(f'<circle cx="{X(t["age"]):.1f}" cy="{58 - (cols[t["ch"]] % 3) * 12}" r="5" class="tl-done"/>')
svg.append('</svg>')
body = f'''<header class="page-head"><p class="kicker">大时间轴 · {len(TL)} 个事件</p><h1>46 亿年，一条线</h1>
<p class="lede">时间轴用的是对数刻度：每往右一格，时间缩短十倍。否则人类的全部历史会挤成最右边一个看不见的点。</p></header>
<div class="timeline">{"".join(svg)}</div>
<ol class="dt" style="margin-top:24px">{items}</ol>'''
page('timeline.html', '大时间轴 · 38 亿年研究笔记', '46 亿年里的关键事件，按时间排列。', body)

# ---------- questions ----------
by_ch = []
for c in CH:
    ns = [NOTE[i] for i in c['notes'] if i in NOTE]
    if ns: by_ch.append(f'<section class="block"><h2><a href="ch-{c["id"]}.html" style="color:inherit;text-decoration:none">{c["n"]}. {e_(c["title"])}</a></h2><div class="notes">{"".join(note_html(n) for n in ns)}</div></section>')
body = f'''<header class="page-head"><p class="kicker">问答 · {len(NOTES)} 个</p><h1>我们问过的问题</h1>
<p class="lede">每个问题都来自真实的“没看懂”。先把它弄懂，再写进视频。</p></header>{"".join(by_ch)}'''
page('questions.html', '问答 · 38 亿年研究笔记', '制作中提出的全部问题与答案，按章节归类。', body)

# ---------- glossary ----------
groups = ''
for c in CH:
    cards = [(cd, e) for e in EPS if EP_CH.get(e['id']) == c['id'] for cd in e['concept_cards']]
    if not cards: continue
    groups += f'<section class="gloss" data-g><h2><a href="ch-{c["id"]}.html">{c["n"]}. {e_(c["title"])}</a></h2><dl>' + ''.join(f'<div data-t="{e_(cd["term"] + cd["definition"])}"><dt>{e_(cd["term"])}</dt><dd>{e_(cd["definition"])}</dd></div>' for cd, e in cards) + '</dl></section>'
body = f'''<header class="page-head"><p class="kicker">概念词典 · {nterms} 个词</p><h1>每个词，一句白话</h1>
<p class="lede">按章节归类。输入关键词可以筛选。</p>
<label for="q" class="cap">搜索概念</label><input id="q" class="search" type="search" placeholder="例如：氧气、细胞、板块"></header>{groups}
<p id="none" class="cap" hidden>没有找到，换个词试试。</p>
<script>(function(){{var q=document.getElementById('q'),none=document.getElementById('none');q.addEventListener('input',function(){{var v=q.value.trim(),any=false;document.querySelectorAll('[data-g]').forEach(function(g){{var n=0;g.querySelectorAll('[data-t]').forEach(function(d){{var ok=!v||d.dataset.t.indexOf(v)>-1;d.hidden=!ok;if(ok)n++;}});g.hidden=n===0;if(n)any=true;}});none.hidden=any;}});}})();</script>'''
page('glossary.html', '概念词典 · 38 亿年研究笔记', '全部概念按章节归类，可搜索。', body)

# ---------- method ----------
M = METHOD
steps = '<ol class="steps">' + ''.join(f'<li><b>{i + 1}</b><strong>{a}</strong><span>{e_(b)}</span></li>' for i, (a, b) in enumerate(M['steps'])) + '</ol>'
tbl = lambda h, rows: '<div class="tbl"><table><thead><tr>' + ''.join(f'<th>{x}</th>' for x in h) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join(f'<td>{e_(x)}</td>' for x in r) + '</tr>' for r in rows) + '</tbody></table></div>'
body = f'''<header class="page-head"><p class="kicker">方法</p><h1>怎样才算弄懂</h1>
<p class="lede">我们用同一套“正向流程”理解每一件事：不允许凭空出现，不允许跳步。</p></header>{steps}
{sec("从“没看懂”里学到的", tbl(["当时的问题", "学到的规则"], M["lessons"]))}
{sec("自查清单", '<ol class="plain">' + "".join(f"<li>{e_(x)}</li>" for x in M["selfcheck"]) + '</ol>')}'''
page('method.html', '方法 · 38 亿年研究笔记', '正向流程：前提、形成、变化、概念、影响、引出。', body)
print('built', len(CH) + 5, 'pages')
