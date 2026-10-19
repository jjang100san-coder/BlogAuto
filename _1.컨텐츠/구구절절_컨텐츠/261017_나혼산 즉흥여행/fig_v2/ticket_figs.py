# -*- coding: utf-8 -*-
"""나혼산 즉흥 여행 — 탑승권 양식 13장(2026-10-18). 숫자는 base data 세 파일·데이터랩 원자료 확인분만.
사용: python ticket_figs.py [이름 ...]"""
import sys, json, datetime as dt, pathlib
from ticket_cards_base import ticket, render, icon, badge, ic, cubes, HERE

F = {}
def band_icon(name, w=128, left=1160, top=16):
    return f'<img class="i3" src="icons/{name}_t.png" style="position:absolute;left:{left}px;top:{top - 158}px;width:{w}px;height:{w}px;z-index:3">'

# 01 큰 예약 96%
CAT = """.two{display:grid;grid-template-columns:1fr 1fr;gap:20px}.cat .hd{display:flex;align-items:center;gap:10px}
.cat .nm{font-size:23px;font-weight:900}.cat .cnt{font-size:15px;font-weight:700;color:var(--muted);margin-top:2px}.cat .blk{margin-top:6px}"""
def cat(ic3, name, cnt, a, b):
    return f'<div class="cat"><div class="hd">{icon(ic3, 86)}<div><div class="nm">{name}</div><div class="cnt">{cnt}</div></div></div><div class="blk">{cubes(a, b)}</div></div>'
F["N1_big_bookings_first"] = ticket(1, "내 여행 글 68편", "큰 예약은 <em>96%</em>가 미리였다",
    '<div class="two">' + cat("suitcase", "항공·숙소·렌터카·투어", "미리 48 · 현장 2", 48, 2) + cat("map", "동선·식당·현지 교통", "미리 29 · 현장 44", 29, 44) + '</div>',
    ["미리 정한 비율", ("96<small>%</small>", "var(--pre)", "항공·숙소·렌터카·투어"), ("40<small>%</small>", "var(--ons)", "동선·식당·현지 교통")],
    "비행기·숙소는 미리, 즉흥은 그날", (520, 575),
    "내 블로그 여행 후기 68편 직접 셈(2026.10.17) · 블록 하나 = 결정 하나 · 알 수 없음 36 제외", CAT, kind="ticket")

# 02 즉흥이라 쓴 글 다섯 편
ROWS2 = (("2024.3 맨체스터", "「아무 계획 없이」", "기차는 앱으로 미리 예약", True),
         ("2025.11 화담숲", "「번개로 가자고 해서」", "대기번호 76,043번, 두 달 전 예약", True),
         ("2023.6 교토", "「즉흥적으로 들어간 집」", "왕복 항공권 2인, 미리 결제", True),
         ("2023.11 후쿠오카", "「일정표도 안 짰어」", "숙소 두 곳, 미리 예약", True),
         ("2019.5 미국 주말", "「계획이랄 게 없었어」", "큰 예약 없음 — 사는 곳에서 차로", None))
CSS2 = """.r2{display:grid;grid-template-columns:150px 270px 40px 1fr 34px;align-items:center;gap:8px;padding:15px 4px;border-bottom:2px dashed var(--line)}
.r2 .w{font-size:15.5px;font-weight:700;color:var(--muted)}.r2 .q{font-size:20px;font-weight:900;color:var(--ons)}.r2 .p{font-size:20px;font-weight:800;color:var(--navy)}
.r2.dim .p{color:#9A917F;font-weight:700}.r2 .gray{display:inline-grid;place-items:center;width:30px;height:30px;border-radius:50%;background:#D9CFBC;color:#fff;font-weight:900}"""
rows = ""
for w, q, pre, ok in ROWS2:
    b = badge(True) if ok else '<span class="gray">–</span>'
    rows += f'<div class="r2{"" if ok else " dim"}"><div class="w">{w}</div><div class="q">{q}</div><div>{ic("arrow", 26, "#B9AE98")}</div><div class="p">{pre}</div>{b}</div>'
F["N2_five_impromptu_posts"] = ticket(2, "「즉흥」이라 쓴 글", "즉흥이라 쓴 글 다섯 편, <em>넷</em>은 예약이 먼저",
    rows, ["「즉흥」이라 쓴 글", ("4<small>/5</small>", "var(--pre)", "같은 여행의 큰 예약이 먼저"), ("1", "#9A917F", "사는 곳에서 차로 나선 주말")],
    "즉흥이라 쓰고, 예약은 미리", (520, 598), "각 글 본문 문장(2026.10.17 확인) · 화담숲 대기번호·예약 시점은 화담숲 예약 글", CSS2)

# 03 후쿠오카 메모 두 줄
CSS3 = """.notes{display:flex;gap:34px;justify-content:center;margin-top:6px}
.note{width:250px;height:330px;background:#fff;box-shadow:0 2px 0 rgba(60,45,20,.05),0 10px 22px rgba(60,45,20,.12);padding:46px 22px 20px;position:relative}
.note:before{content:"";position:absolute;left:80px;top:-10px;width:90px;height:24px;background:rgba(208,122,34,.25)}
.note .who{position:absolute;top:14px;left:22px;font-size:15px;font-weight:800;color:var(--muted);letter-spacing:.08em}
.note .ln{height:16px;border-radius:4px;background:var(--navy);opacity:.85;margin:18px 0}
.note .bl{height:2px;background:#E7E0D0;margin:30px 0 30px}
.note .tx{font-size:21px;font-weight:900;color:var(--ons);margin:14px 0 4px;border-bottom:2px solid var(--ons);padding-bottom:6px}"""
def full_note(rot):
    return f'<div class="note" style="transform:rotate({rot}deg)"><div class="who">동행의 일정표</div>' + '<div class="ln" style="width:88%"></div><div class="ln" style="width:70%"></div><div class="ln" style="width:92%"></div><div class="ln" style="width:64%"></div><div class="ln" style="width:84%"></div><div class="ln" style="width:58%"></div></div>'
mine = '<div class="note" style="transform:rotate(-1deg)"><div class="who" style="color:var(--ons)">내 메모</div><div class="tx">비행기 왕복</div><div class="tx">숙소 두 곳</div><div class="bl"></div><div class="bl"></div><div class="bl"></div></div>'
F["N3_fukuoka_two_lines"] = ticket(3, "2023.11 후쿠오카", "셋이 간 후쿠오카, 내 메모엔 <em>두 줄</em>",
    '<div class="notes">' + full_note(-2) + full_note(1.5) + mine + '</div>',
    ["내 메모", ("2<small>줄</small>", "var(--ons)", "비행기 · 숙소"), ("0<small>줄</small>", "#9A917F", "그날 어디 갈지")],
    "「완전 무계획으로 갈 배짱은 없었다」", (250, 598), "블로그 후쿠오카 11월 글 두 편 + 본인 확인(2026.10.17) · 일정표 그림은 모식", CSS3)

# 04 즉흥의 뜻 세 가지
CSS4 = """.qs{display:grid;grid-template-columns:repeat(3,1fr);gap:26px;margin-top:4px}
.qq{border-left:7px solid;padding:6px 0 6px 18px;min-height:250px}
.qq .w{font-size:15px;font-weight:800;letter-spacing:.06em;margin-bottom:14px}
.qq .t{font-size:23px;font-weight:800;line-height:1.5;color:var(--ink)}
.qq .f{font-size:15px;color:var(--muted);font-weight:700;margin-top:12px}
.stub .big2{font-size:46px;font-weight:900;line-height:1.1;color:var(--navy);margin-top:10px}"""
Q4 = (("표준국어대사전 「즉흥」", "그 자리에서 바로 일어나는 감흥. 또는 그런 기분.", "", "var(--navy)"),
      ("MBC가 말한 「즉흥 여행」", "목적지와 항공권을 미리 정하지 않은 채 당일 여행지를 결정해 떠나는 방식", "9.4 입장문", "var(--ons)"),
      ("MBC가 덧붙인 문장", "모든 과정이 아무런 사전 준비 없이 진행된 것으로 받아들여질 수 있다는 점", "→ 「충분히 고려하지 못했습니다」", "var(--red)"))
qs = "".join(f'<div class="qq" style="border-color:{c}"><div class="w" style="color:{c}">{w}</div><div class="t">「{t}」</div><div class="f">{f}</div></div>' for w, t, f, c in Q4)
stub4 = '<div class="lab">기준</div><div class="t" style="margin-top:14px">한 번에 많은 사람이 듣는 방송에서 말의 뜻은</div><div class="big2">듣는 쪽</div><div class="t" style="margin-top:14px">심의규정 제14조<br>「시청자를 혼동케 하여서는 아니 된다」</div>'
F["N4_three_meanings"] = ticket(4, "「즉흥」의 뜻", "「즉흥」, 세 곳에서 <em>다르게</em> 쓰였다",
    band_icon("dict") + '<div class="qs">' + qs + '</div>', stub4,
    "기준은 시청자", (420, 598), "표준국어대사전 「즉흥」, MBC 9.4 입장문(한겨레·더팩트 대조), 방송심의에 관한 규정 제14조(객관성)", CSS4, "navy")

# 05 날짜순
EV5 = (("7.22", "공항에 촬영 허가 공문", "8월 6일 카운터 발권 장면 · 오전 11시10분 편", "var(--muted)"),
       ("8.6", "출국", "공문에 적힌 그 편으로", "var(--muted)"),
       ("8.14·21", "방송 두 편", "공항에서 목적지를 고르는 장면", "var(--navy)"),
       ("8.25", "MBC 1차 입장", "「촬영 지원이나 협찬 등을 받은 사실은 없습니다」", "var(--ons)"),
       ("8.31", "MBC 2차 입장", "금전 협찬은 없고, 행정 절차·촬영 협조는 받았다", "var(--ons)"),
       ("9.4", "MBC 3차 입장", "앞의 「지원 없음」은 금전 지원만 · 스태프 항공권은 미리", "var(--ons)"),
       ("10.16", "공문 보도", "MBC 「촬영 허가를 받으려고 정리한 예시 상황」", "var(--red)"))
CSS5 = """.it5{display:grid;grid-template-columns:96px 22px 200px 1fr;align-items:center;gap:10px;height:54px;border-bottom:1px dashed var(--line)}
.it5 .d{font-size:20px;font-weight:900;font-variant-numeric:tabular-nums}.it5 .dot{width:14px;height:14px;border-radius:50%}
.it5 .e{font-size:19px;font-weight:900}.it5 .x{font-size:16.5px;font-weight:600;color:var(--ink2);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}"""
it5 = "".join(f'<div class="it5"><div class="d" style="color:{c}">{d}</div><div class="dot" style="background:{c}"></div><div class="e">{e}</div><div class="x">{x}</div></div>' for d, e, x, c in EV5)
F["N5_dates_in_order"] = ticket(5, "날짜순", "방송 석 주 전 공문부터 <em>10월</em> 보도까지",
    band_icon("calendar") + it5, ["입장문", ("3<small>번</small>", "var(--ons)", "8.25 → 8.31 → 9.4"), ("86<small>일</small>", "var(--pre)", "7.22 공문 → 10.16 보도")],
    "처음 발표는 일주일 뒤 고쳐졌다", (540, 598), "한겨레·텐아시아·스포티비뉴스 10.16(인천국제공항공사가 국회에 낸 자료), MBC 입장문 8.25·8.31·9.4", CSS5)

# 06 미리 한 것 셋, 안 한 것 하나
CSS6 = """.g6{display:grid;grid-template-columns:3fr 1.1fr;gap:0;margin-top:2px}
.g6 .side{padding:0 10px}.g6 .side+.side{border-left:2px dashed var(--line)}
.g6 .hd{display:flex;align-items:center;gap:10px;font-size:19px;font-weight:900;margin-bottom:6px}
.objs{display:flex;justify-content:space-around}.ob{width:200px;text-align:center;position:relative}
.ob img{margin:0 auto}.ob .l{font-size:19px;font-weight:900;margin-top:-4px}.ob .d{font-size:15px;color:var(--muted);font-weight:700;margin-top:4px}
.ob .chk{position:absolute;top:10px;right:22px}"""
def ob(ic3, l, d, ok=True):
    bd = badge(ok, 34) if ok else ""
    return f'<div class="ob">{icon(ic3, 170)}{bd}<div class="l">{l}</div><div class="d">{d}</div></div>'
g6 = ('<div class="g6"><div class="side"><div class="hd" style="color:var(--pre)">' + badge(True, 26) + '미리 한 것</div><div class="objs">'
      + ob("permit", "촬영 허가 공문", "7월 22일") + ob("tickets", "스태프 항공권", "미리 발권") + ob("camera", "현지 촬영 협조", "미리 요청") + '</div></div>'
      + '<div class="side"><div class="hd" style="color:var(--red)">' + badge(False, 26) + '안 한 것</div><div class="objs">'
      + ob("license", "운전 서류", "「뒤늦게 확인」", False) + '</div></div></div>')
F["N5b_prepared_or_not"] = ticket(6, "MBC 입장문이 말한 것", "미리 한 것 <em>셋</em>, 안 한 것 <em>하나</em>",
    g6, ["미리 한 것 : 안 한 것", ("3<small> : 1</small>", "var(--pre)", "공문 · 스태프 항공권 · 촬영 협조<br>vs 운전 서류(면허 공증)")],
    "준비했으면 즉흥이 아니고, 안 했으면 위험했다", (250, 598),
    "MBC 입장문 8.25·9.4, 인천국제공항공사가 국회에 낸 자료(10.16 보도), 주카자흐스탄 대사관 공지(8.20·8.25)", CSS6)

# 07 검색이 다시 뜬 날
raw = json.load(open(HERE.parent / "base data" / "_raw_데이터랩_카자흐스탄_2026-10-17.json", encoding="utf-8"))
dd = {r["period"]: r["ratio"] for r in raw["results"][0]["data"]}
D0, D1 = dt.date(2026, 8, 10), dt.date(2026, 10, 16)
days = [D0 + dt.timedelta(i) for i in range((D1 - D0).days + 1)]
WC, HC, PADL, PADB = 920, 360, 40, 40
def gx(x): return PADL + (x - D0).days / (D1 - D0).days * (WC - PADL - 14)
def gy(v): return 18 + (1 - v / 100) * (HC - PADB - 18)
pts = " ".join("%.1f,%.1f" % (gx(x), gy(dd.get(x.isoformat(), 0))) for x in days)
area = f"{gx(D0):.1f},{gy(0):.1f} " + pts + f" {gx(D1):.1f},{gy(0):.1f}"
EVc = ((dt.date(2026, 8, 14), "1편 방송", 0), (dt.date(2026, 8, 21), "2편·알마티 보도", 1), (dt.date(2026, 8, 25), "1차 입장", 2),
       (dt.date(2026, 8, 31), "2차 입장", 0), (dt.date(2026, 9, 4), "3차 입장", 1), (dt.date(2026, 10, 16), "공문 보도", 0))
svg = [f'<svg width="{WC}" height="{HC + 60}" viewBox="0 0 {WC} {HC + 60}" style="font-family:NK">']
for v in (0, 50, 100):
    svg.append(f'<line x1="{PADL}" x2="{WC - 10}" y1="{gy(v):.1f}" y2="{gy(v):.1f}" stroke="#E7E0D0" stroke-width="1.5"/><text x="{PADL - 8}" y="{gy(v) + 5:.1f}" text-anchor="end" font-size="13" fill="#9A917F" font-weight="700">{v}</text>')
svg.append(f'<polygon points="{area}" fill="rgba(61,98,174,.12)"/><polyline points="{pts}" fill="none" stroke="#22335A" stroke-width="3.2" stroke-linejoin="round"/>')
for day, lab, lv in EVc:
    x = gx(day); y = gy(dd.get(day.isoformat(), 0)); ly = HC - PADB + 22 + lv * 22
    anc = "end" if day == D1 else "middle"
    svg.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{y:.1f}" y2="{ly - 15}" stroke="#D07A22" stroke-width="1.6" stroke-dasharray="3 3"/><circle cx="{x:.1f}" cy="{y:.1f}" r="6.5" fill="#D07A22" stroke="#FFFCF5" stroke-width="2.5"/><text x="{x:.1f}" y="{ly}" text-anchor="{anc}" font-size="15" font-weight="800" fill="#D07A22">{lab}</text>')
svg.append(f'<text x="{gx(dt.date(2026, 8, 26)) + 12:.1f}" y="{gy(100) + 6:.1f}" font-size="15" font-weight="900" fill="#22335A">8.26 최고</text></svg>')
F["N5c_search_peaks"] = ticket(7, "왜 계속 화제였나", "검색이 다시 뜬 날 = <em>새 사실</em>이 나온 날",
    band_icon("search") + "".join(svg), ["검색이 가장 높은 날", ("8.26", "var(--pre)", "1차 입장문 다음 날 (=100)"), ("10.16", "var(--ons)", "공문 보도 날 다시 상승")],
    "해명이 바뀔 때마다 다시 떴다", (560, 598), "네이버 데이터랩 검색어트렌드(검색어 8개 묶음, 2026.10.17 조회) · 검색량이 아니라 상대 추이")

# 08 알리는 규칙
CSS8 = """.t8{display:grid;grid-template-columns:170px 1fr 1fr;margin-top:2px}
.t8>div{padding:16px 14px;border-bottom:2px dashed var(--line);font-size:19px;font-weight:800}
.t8 .h{font-size:20px;font-weight:900;color:#fff;border-bottom:0}.t8 .k{font-size:15px;color:var(--muted);font-weight:800}
.stub .n.s{font-size:44px;line-height:1.1}"""
cells = ['<div></div>', '<div class="h" style="background:var(--navy)">방송 · 방송법</div>', '<div class="h" style="background:var(--ons)">유튜브 · 공정위 지침</div>']
for k, a, b in (("받은 것에 드는 것", "돈 · 물품 · 용역 · 인력 · 장소", "현금 · 제품 · 상품권 · 포인트 · 할인"),
                ("알리는 규칙", "「할 수 있다」 — 정해진 방식만", "「공개하여야 한다」 — 매 건마다"),
                ("알리는 자리", "프로그램 끝 자막 1회", "제목이나 영상 안 · 시작과 끝")):
    cells += [f'<div class="k">{k}</div>', f'<div>{a}</div>', f'<div>{b}</div>']
stub8 = '<div class="lab">알리는 규칙</div><div class="row"><div class="n s" style="color:var(--navy)">할 수<br>있다</div><div class="t">방송</div></div><div class="row"><div class="n s" style="color:var(--ons)">하여야<br>한다</div><div class="t">유튜브</div></div>'
F["N6_tell_rules"] = ticket(8, "알리는 규칙", "방송은 「알릴 수 <em>있다</em>」, 유튜브는 「<em>알려야</em> 한다」",
    band_icon("tvphone", 120, 1166, 20) + '<div class="t8">' + "".join(cells) + '</div>', stub8,
    "촬영 협조가 협찬인지는 아직 결론 없음", (300, 598), "방송법 제2조제22호·제74조, 협찬고지 규칙 제8조, 공정위 추천·보증 심사지침(2026.6.1 시행)", CSS8, "navy")

# 09 할 일 하나
CSS9 = """.w9{display:grid;grid-template-columns:330px 1fr;gap:36px;align-items:start}
.memo{background:#fff;box-shadow:0 2px 0 rgba(60,45,20,.05),0 10px 22px rgba(60,45,20,.12);padding:22px 24px;transform:rotate(-1.5deg);position:relative}
.memo:before{content:"";position:absolute;left:110px;top:-10px;width:100px;height:24px;background:rgba(61,98,174,.22)}
.memo .h{font-size:15px;font-weight:800;color:var(--muted);letter-spacing:.08em;margin-bottom:10px}
.memo .l{font-size:21px;font-weight:900;color:var(--navy);border-bottom:2px solid #E7E0D0;padding:10px 0}
.memo .o{color:var(--ons);border:2.5px dashed var(--ons);border-radius:8px;padding:8px 10px;margin:12px 0}
.memo .b{height:2px;background:#E7E0D0;margin:26px 0}
.qt{border-left:6px solid var(--ons);padding:6px 0 6px 16px;margin-bottom:18px}
.qt .w{font-size:15px;font-weight:800;color:var(--muted)}.qt .t{font-size:21px;font-weight:800;margin-top:3px}"""
memo = '<div class="memo"><div class="h">다음 여행 메모</div><div class="l">비행기</div><div class="l">숙소</div><div class="l">렌터카</div><div class="l o">그날 정하기</div><div class="b"></div></div>'
qts = "".join(f'<div class="qt"><div class="w">{w}</div><div class="t">「{t}」</div></div>' for w, t in (
    ("구마모토", "계획에 없던 30분이 제일 선명해"), ("규슈 일주", "전부 계획에 없던 거야"),
    ("후쿠오카 11월", "일정표에 아무것도 안 적혀 있던 시간"), ("미서부", "제일 좋았던 곳들은 일정표에 없더라고")))
F["N7_one_blank_line"] = ticket(9, "할 일 하나", "다음 여행 메모엔 「그날 정하기」 <em>한 줄</em>",
    '<div class="w9">' + memo + '<div>' + qts + '</div></div>', ["남겨 둘 것", ("1<small>줄</small>", "var(--ons)", "그날 정하기"), ("4<small>편</small>", "var(--pre)", "내 글에 남은 비슷한 문장")],
    "다 채우지 않기로 했다", (620, 598), "블로그 구마모토성·규슈 렌터카·후쿠오카 11월 코스·미서부 2년 뒤 글 본문(2026.10.17 확인) · 메모는 모식", CSS9, kind="ticket")

# 10 종류별
CSS10 = """.k10{display:grid;grid-template-columns:150px 1fr 70px 76px;align-items:center;gap:12px;height:50px;border-bottom:1px dashed var(--line)}
.k10 .l{font-size:19px;font-weight:900}.k10 .bar10{display:flex;gap:3px;height:26px}.k10 .bar10 div{border-radius:4px}
.k10 .ab{font-size:15px;font-weight:700;color:var(--muted)}.k10 .p{font-size:22px;font-weight:900;text-align:right}"""
K10 = (("항공", 6, 0), ("숙소", 17, 0), ("렌터카", 10, 1), ("투어·입장권", 15, 1), ("동선", 17, 18), ("현지 교통", 3, 6), ("식당", 6, 13))
rows10 = ""
for l, a, b in K10:
    pc = round(a / (a + b) * 100); col = "var(--pre)" if pc >= 50 else "var(--ons)"
    seg = f'<div style="width:{a*16}px;background:var(--pre)"></div>' + (f'<div style="width:{b*16}px;background:var(--ons)"></div>' if b else "")
    rows10 += f'<div class="k10"><div class="l">{l}</div><div class="bar10">{seg}</div><div class="ab">{a} : {b}</div><div class="p" style="color:{col}">{pc}%</div></div>'
F["H1_by_kind"] = ticket(10, "한 걸음 더 · 종류별", "항공·숙소는 <em>전부</em> 미리, 식당은 셋 중 하나",
    band_icon("bars") + rows10, ["미리 정한 비율", ("100<small>%</small>", "var(--pre)", "항공 · 숙소"), ("32<small>%</small>", "var(--ons)", "식당")],
    "", (0, 0), "여행 후기 결정 항목 중 시점이 적힌 123가지(직접 셈) · 기타 10가지 제외 · 미리는 일정표 1개, 현장은 들른 곳마다 셈", CSS10)

# 11 옛 신문
DEC = ("1920s", "1930s", "1940s", "1950s", "1960s", "1970s", "1980s", "1990s")
MU = (79, 38, 2, 26, 254, 63, 61, 109); BP = (0, 0, 0, 0, 0, 0, 4, 2162); JH = (0, 0, 0, 0, 0, 0, 1, 2)
s11 = ['<svg width="920" height="440" viewBox="0 0 920 440" style="font-family:NK">']
BY = 340
for k, d in enumerate(DEC):
    cx = 70 + k * 112
    h = MU[k]; s11.append(f'<rect x="{cx - 34}" y="{BY - h}" width="30" height="{h}" rx="3" fill="#B9AE98"/>')
    if BP[k]:
        hb = min(BP[k], 290); s11.append(f'<rect x="{cx + 2}" y="{BY - hb}" width="30" height="{hb}" rx="3" fill="#22335A"/>')
        if BP[k] > 290: s11.append(f'<path d="M{cx - 2} {BY - 200} l40 -8 M{cx - 2} {BY - 190} l40 -8" stroke="#FFFCF5" stroke-width="5"/><text x="{cx + 17}" y="{BY - hb - 10}" text-anchor="middle" font-size="16" font-weight="900" fill="#22335A">2,162</text>')
    s11.append(f'<text x="{cx}" y="{BY + 26}" text-anchor="middle" font-size="15" font-weight="700" fill="#4A5163">{d}</text>')
    col = "#C8463C" if JH[k] else "#D9CFBC"
    s11.append(f'<text x="{cx}" y="{BY + 62}" text-anchor="middle" font-size="22" font-weight="900" fill="{col}">{JH[k]}</text>')
s11.append(f'<line x1="20" x2="900" y1="{BY}" y2="{BY}" stroke="#4A5163" stroke-width="2"/>')
s11.append('<rect x="20" y="10" width="16" height="16" rx="3" fill="#B9AE98"/><text x="44" y="24" font-size="15" font-weight="800" fill="#4A5163">무전여행 632</text>'
           '<rect x="180" y="10" width="16" height="16" rx="3" fill="#22335A"/><text x="204" y="24" font-size="15" font-weight="800" fill="#4A5163">배낭여행 2,166</text>'
           '<text x="350" y="24" font-size="15" font-weight="900" fill="#C8463C">즉흥여행 = 아래 빨간 숫자</text></svg>')
F["H2_old_papers"] = ticket(11, "한 걸음 더 · 옛 신문", "1920~1999 신문에 「즉흥여행」은 <em>세 번</em>",
    band_icon("paper") + "".join(s11), ["「즉흥여행」 기사", ("3<small>번</small>", "var(--red)", "첫 기사 1989.1.31<br>설 연휴 즉흥 나들이 후회"), ("2,166", "var(--pre)", "「배낭여행」 · 거의 1990년대")],
    "", (0, 0), "네이버 뉴스 라이브러리 5개 신문, 따옴표 구절 검색(2026.10.17) · 그 말이 나온 횟수 · 1963 무전여행은 영화 광고 많음")

# 12 카자흐스탄 운전 서류
CSS12 = """.s12{display:grid;grid-template-columns:1fr 50px 1fr 50px 1fr;align-items:center;margin-top:10px}
.st{text-align:center}.st img{margin:0 auto}.st .h{font-size:20px;font-weight:900;margin-top:4px}.st .d{font-size:16px;font-weight:700;color:var(--ink2);margin-top:6px;line-height:1.45}
.st .flag{width:150px;height:150px;margin:10px auto;border-radius:50%;background:var(--pre-l);display:grid;place-items:center;font-size:20px;font-weight:900;color:var(--navy);line-height:1.3}
.st .rel{position:relative;display:inline-block}.st .rel .chk{position:absolute;right:6px;top:8px}"""
s12 = ('<div class="s12"><div class="st"><div class="rel">' + icon("license", 160) + badge(False, 36) + '</div><div class="h">한국 국제운전면허증</div><div class="d">제네바 협약 방식<br>카자흐스탄에선 인정 안 됨</div></div>'
       + '<div>' + ic("arrow", 34, "#B9AE98") + '</div>'
       + '<div class="st"><div class="flag">카자흐스탄<br>비엔나 협약</div><div class="h">따르는 협약이 다름</div><div class="d">1994년 가입</div></div>'
       + '<div>' + ic("arrow", 34, "#B9AE98") + '</div>'
       + '<div class="st"><div class="rel">' + icon("permit", 160) + badge(True, 36) + '</div><div class="h">필요한 서류</div><div class="d">한국 면허 원본<br>+ 러시아어 공증 번역본</div></div></div>')
F["H3_driving_papers"] = ticket(12, "한 걸음 더 · 운전 서류", "카자흐스탄 운전, 국제면허증만으론 <em>안 된다</em>",
    s12, ["필요한 서류", ("2<small>가지</small>", "var(--ok)", "면허 원본 + 공증 번역본"), ('<span style="font-size:54px">반나절</span>', "var(--pre)", "한국 공관에서 공증 받을 때")],
    "국제운전면허증만으로는 운전 불가", (330, 598), "주카자흐스탄 대한민국 대사관 공지(8.20·8.25), 외교부 해외안전여행 운전면허 상호인정, 유엔 조약 현황", CSS12, "red")

# 13 시청률
RT = (("8.14", 5.8), ("8.21", 6.5), ("8.28", 5.1), ("9.4", 5.2), ("9.11", 4.8), ("9.18", 4.2), ("9.25", 3.5), ("10.2", 6.0), ("10.9", 5.0))
s13 = ['<svg width="920" height="420" viewBox="0 0 920 420" style="font-family:NK">']
def rx(i): return 70 + i * 100
def ry(v): return 340 - (v - 3) / 4 * 290
for v in (3, 4, 5, 6, 7):
    s13.append(f'<line x1="50" x2="900" y1="{ry(v):.1f}" y2="{ry(v):.1f}" stroke="#E7E0D0" stroke-width="1.5"/><text x="40" y="{ry(v) + 5:.1f}" text-anchor="end" font-size="13" fill="#9A917F" font-weight="700">{v}%</text>')
s13.append('<polyline points="%s" fill="none" stroke="#22335A" stroke-width="3.5" stroke-linejoin="round"/>' % " ".join("%.1f,%.1f" % (rx(i), ry(v)) for i, (_, v) in enumerate(RT)))
for i, (d, v) in enumerate(RT):
    c = "#D07A22" if d == "9.25" else "#22335A"
    s13.append(f'<circle cx="{rx(i)}" cy="{ry(v):.1f}" r="7" fill="{c}" stroke="#FFFCF5" stroke-width="2.5"/><text x="{rx(i)}" y="{ry(v) - 16:.1f}" text-anchor="middle" font-size="16" font-weight="900" fill="{c}">{v}</text><text x="{rx(i)}" y="372" text-anchor="middle" font-size="14" font-weight="700" fill="#4A5163">{d}</text>')
s13.append(f'<text x="{rx(6) + 14}" y="{ry(3.5) + 5:.1f}" font-size="14" font-weight="800" fill="#D07A22">추석 기간</text></svg>')
F["H4_ratings"] = ticket(13, "한 걸음 더 · 시청률", "그동안의 시청률 — <em>숫자만</em>",
    band_icon("tvphone", 120, 1166, 20) + "".join(s13), ["닐슨 전국 가구", ("6.5", "var(--pre)", "8.21 알마티 2편"), ("3.5", "var(--ons)", "9.25 추석 기간")],
    "이 숫자만으로 원인은 말할 수 없다", (430, 598), "닐슨코리아(각 회차 보도) · 10.16 방송분은 10.17 기준 확인 못 함", "", "navy")

if __name__ == "__main__":
    render(F, sys.argv[1:] or None)
