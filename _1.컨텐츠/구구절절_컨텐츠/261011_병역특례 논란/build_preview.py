# -*- coding: utf-8 -*-
"""초안(구역 B)을 도해+설명 순서 그대로 보여주는 검토용 HTML 로 변환한다. 출력: 병역특례_그림으로.html"""
import re, html, os
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "초안_아시안게임 병역특례.md"), encoding="utf-8").read()
title_line = re.search(r"\[\[TITLE:\s*(.+?)\]\]", src).group(1)
body = src.split("===== ✂️ 여기부터 복사 =====")[1].split("===== ✂️ 여기까지 =====")[0].strip()

def inline(s):
    s = html.escape(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return s

sections = [s.strip() for s in body.split("\n---\n")]
out = []
fig_no = 0
toc = []
for si, sec in enumerate(sections):
    lines = [l for l in sec.split("\n")]
    parts = []
    head = None
    for ln in lines:
        if not ln.strip():
            continue
        m = re.match(r"\[\[IMG:\s*([^|\]]+?)\s*\|\s*(.*?)\s*\]\]", ln)
        if m:
            fname, cap = m.group(1), m.group(2)
            fig_no += 1
            parts.append(f'<figure><img src="img/{html.escape(fname)}" alt="{html.escape(cap)}" loading="lazy"><figcaption><span class="fn">그림 {fig_no}</span> {inline(cap)}</figcaption></figure>')
            continue
        if ln.startswith("#"):
            tags = " ".join(f'<span class="tag">{html.escape(t)}</span>' for t in ln.split())
            parts.append(f'<p class="tags">{tags}</p>')
            continue
        if head is None and si > 0 and re.match(r"^\S+\s", ln) and len(ln) < 60:
            head = ln
            sid = f"s{si}"
            toc.append((sid, ln))
            parts.append(f'<h2 id="{sid}">{inline(ln)}</h2>')
            continue
        parts.append(f"<p>{inline(ln)}</p>")
    cls = "lead" if si == 0 else "sec"
    out.append(f'<section class="{cls}">' + "\n".join(parts) + "</section>")

toc_html = "".join(f'<li><a href="#{sid}">{html.escape(t)}</a></li>' for sid, t in toc)
page = f"""<title>병역특례, 그림으로</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@600;700&family=Noto+Sans+KR:wght@400;500;700&display=swap">
<style>
/* 레이아웃: 한 줄 문서. 그림이 본문과 같은 폭으로 번갈아 선다. 왼쪽에 얇은 차례. */
:root{{
  --bg:#f6f4ee; --paper:#fffdf8; --fg:#1f2320; --muted:#6b7068; --line:#d9d5c9;
  --ink:#2b3a4a; --olive:#5b6b3f; --gold:#b8891e; --gold-soft:#f3e7c7;
  --display:"Noto Serif KR",serif; --body:"Noto Sans KR","Apple SD Gothic Neo","Malgun Gothic",sans-serif;
}}
@media (prefers-color-scheme: dark){{ :root:not([data-theme="light"]){{
  --bg:#171a18; --paper:#1f2320; --fg:#e8e6dd; --muted:#a3a79c; --line:#363b36;
  --ink:#c6d3e0; --olive:#a9b98a; --gold:#d9ab45; --gold-soft:#3a3120; color-scheme:dark }} }}
:root[data-theme="dark"]{{
  --bg:#171a18; --paper:#1f2320; --fg:#e8e6dd; --muted:#a3a79c; --line:#363b36;
  --ink:#c6d3e0; --olive:#a9b98a; --gold:#d9ab45; --gold-soft:#3a3120; color-scheme:dark }}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--fg);font-family:var(--body);font-size:17px;line-height:1.75;padding-inline:16px;padding-block:0 80px}}
.wrap{{max-width:1180px;margin:0 auto;display:grid;grid-template-columns:220px minmax(0,1fr);gap:40px}}
@media (max-width:860px){{.wrap{{grid-template-columns:minmax(0,1fr)}} nav.toc{{display:none}}}}
header{{grid-column:1/-1;padding-block:48px 24px;border-bottom:1px solid var(--line)}}
header .eyebrow{{font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:var(--olive);font-weight:700}}
header h1{{font-family:var(--display);font-size:clamp(26px,3.4vw,38px);line-height:1.3;margin:10px 0 6px;text-wrap:balance}}
header p{{margin:0;color:var(--muted);font-size:15px}}
nav.toc{{position:sticky;top:env(safe-area-inset-top,0px);align-self:start;padding-top:28px;font-size:13.5px}}
nav.toc ol{{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:8px}}
nav.toc a{{color:var(--muted);text-decoration:none;display:block;border-left:2px solid var(--line);padding-left:10px;line-height:1.4}}
nav.toc a:hover,nav.toc a:focus{{color:var(--fg);border-left-color:var(--gold)}}
main{{min-width:0;max-width:720px}}
section{{padding-block:28px;border-bottom:1px solid var(--line)}}
section.lead p{{font-size:18px}}
section.lead p:first-child{{font-family:var(--display);font-size:26px;color:var(--ink)}}
h2{{font-family:var(--display);font-size:22px;line-height:1.35;margin:0 0 14px;text-wrap:balance;color:var(--ink)}}
p{{margin:0 0 14px;max-width:66ch}}
strong{{background:var(--gold-soft);padding:0 3px;font-weight:700}}
figure{{margin:18px 0 22px;background:var(--paper);border:1px solid var(--line);border-radius:6px;overflow:hidden}}
figure img{{display:block;width:100%;max-width:100%;height:auto}}
figcaption{{font-size:14px;color:var(--muted);padding:10px 14px;border-top:1px solid var(--line);line-height:1.5}}
figcaption .fn{{color:var(--gold);font-weight:700;margin-right:6px;font-variant-numeric:tabular-nums}}
p.tags{{display:flex;flex-wrap:wrap;gap:6px}}
.tag{{font-size:13px;color:var(--olive);border:1px solid var(--line);border-radius:999px;padding:2px 10px}}
footer{{grid-column:1/-1;color:var(--muted);font-size:13px;padding-top:24px}}
a:focus-visible{{outline:2px solid var(--gold);outline-offset:2px}}
</style>
<div class="wrap">
<header>
  <div class="eyebrow">구구절절 · 발행 전 검토용</div>
  <h1>{html.escape(title_line)}</h1>
  <p>초안 본문과 도해 17장을 글 순서 그대로 붙였다. 본문 수정은 초안 md 파일에서.</p>
</header>
<nav class="toc"><ol>{toc_html}</ol></nav>
<main>
{chr(10).join(out)}
</main>
<footer>근거 일람: 병역특례_공부노트_2026-10-11.md · 도해 제작: make_diagrams.py · 썸네일: Higgsfield gpt_image_2_5 (AI 생성 이미지 · 특정 인물 아님)</footer>
</div>
"""
open(os.path.join(HERE, "병역특례_그림으로.html"), "w", encoding="utf-8").write(page)
print("figures", fig_no, "sections", len(sections), "toc", len(toc))
