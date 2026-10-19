# -*- coding: utf-8 -*-
"""비즈니스 좌석 중심 초안(v2) — '같은 날 새벽과 오전이 달랐다'가 축. 숫자·날짜는 전부 데이터에서 뽑는다.

사용: python gen_biz_draft.py "<글 폴더>"
"""
import sys, os, json, datetime as dt, collections

OUTDIR = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
sys.argv = ['build_europe.py', os.path.join(HERE, 'data', '_buildtest')]
import build_europe as B          # 새벽 전체(10곳, 76일)
sys.argv = ['compare_runs.py', OUTDIR]
import compare_runs as C          # 새벽 vs 오전 (75일, 런던·파리·프랑크푸르트)
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

sys.stdout.reconfigure(encoding='utf-8')


def fmt(dates):
    dates = sorted(dates)
    if not dates:
        return '없음'
    runs, s, p = [], dates[0], dates[0]
    for d in dates[1:]:
        if d == p + dt.timedelta(days=1):
            p = d
            continue
        runs.append((s, p))
        s = p = d
    runs.append((s, p))
    bym = collections.OrderedDict()
    for a, b in runs:
        if a.month == b.month:
            bym.setdefault(a.month, []).append(str(a.day) if a == b else '%d~%d' % (a.day, b.day))
        else:
            last = (dt.date(a.year, a.month + 1, 1) - dt.timedelta(days=1)).day
            bym.setdefault(a.month, []).append(str(a.day) if a.day == last else '%d~%d' % (a.day, last))
            bym.setdefault(b.month, []).append('1' if b.day == 1 else '1~%d' % b.day)
    return ', '.join('%d월 %s일' % (m, '·'.join(v)) for m, v in bym.items())


def R(air, o, d, cab):
    return C.RES[(air, o, d, cab)]


def cnt(air, o, d, cab):
    a, b = R(air, o, d, cab)
    return len(a), len(b)


# ── 핵심 사실 (틀리면 여기서 멈춘다) ──
L0, L1 = R('OZ', 'LHR', 'ICN', 'b')
assert len(L0) == 2 and len(L1) == 19, (len(L0), len(L1))
new_b, gone_b = L1 - L0, L0 - L1
re_oz = json.load(open(os.path.join(HERE, 'data', 're_oz.json'), encoding='utf-8'))['res']
oz_dawn = json.load(open(os.path.join(HERE, 'data', 'oz_daily.json'), encoding='utf-8'))['res']
a11 = re_oz['LHR-ICN']['A']['days']['2026-11-01']
b11 = re_oz['LHR-ICN']['B']['days']['2026-11-01']
assert a11['E'] and not a11['B'] and b11['B']          # 전체 조회는 일반석 표시만, 비즈니스 조회는 비즈니스 표시
assert oz_dawn['LHR-ICN']['B']['flights']['2026-11-29'][0]['biz'] == '매진' and dt.date(2026, 11, 29) in L1
MILE = re_oz['LHR-ICN']['B']['flights']['2026-11-01'][0]['biz']   # '62,500마일'
T0a, T0b = C.T0.split('~')
T1a, T1b = C.T1.split('~')
hm = lambda t: '%d시 %s분' % (int(t[:2]), t[3:])


def biz_rows():
    rows = ['| 노선 | 새벽 | 오전 |', '|---|---|---|']
    for air, o, d, name in (('OZ', 'LHR', 'ICN', '아시아나 런던→인천'), ('OZ', 'ICN', 'LHR', '아시아나 인천→런던'), ('OZ', 'ICN', 'CDG', '아시아나 인천→파리'),
                            ('OZ', 'CDG', 'ICN', '아시아나 파리→인천'), ('KE', 'ICN', 'LHR', '대한항공 인천→런던'), ('KE', 'LHR', 'ICN', '대한항공 런던→인천'),
                            ('KE', 'ICN', 'CDG', '대한항공 인천→파리'), ('KE', 'CDG', 'ICN', '대한항공 파리→인천')):
        a, b = cnt(air, o, d, 'b')
        rows.append('| %s | %d일 | %d일 |' % (name, a, b))
    return '\n'.join(rows)


def eco_rows():
    rows, same = ['| 노선 | 새벽 | 오전 |', '|---|---|---|'], []
    lines = []
    for air, o, d, name in (('OZ', 'ICN', 'CDG', '아시아나 인천→파리'), ('OZ', 'CDG', 'ICN', '아시아나 파리→인천'), ('OZ', 'LHR', 'ICN', '아시아나 런던→인천'),
                            ('KE', 'LHR', 'ICN', '대한항공 런던→인천'), ('OZ', 'ICN', 'FRA', '아시아나 인천→프랑크푸르트'), ('OZ', 'ICN', 'LHR', '아시아나 인천→런던'),
                            ('KE', 'ICN', 'LHR', '대한항공 인천→런던'), ('KE', 'ICN', 'CDG', '대한항공 인천→파리'), ('KE', 'CDG', 'ICN', '대한항공 파리→인천'),
                            ('KE', 'ICN', 'FRA', '대한항공 인천→프랑크푸르트')):
        a, b = R(air, o, d, 'e')
        if a == b:
            same.append(name)
            continue
        rows.append('| %s | %d일 | %d일 |' % (name, len(a), len(b)))
        part = []
        if b - a:
            part.append('새로 열린 날 ' + fmt(b - a))
        if a - b:
            part.append('사라진 날 ' + fmt(a - b))
        lines.append(name + ', ' + ' / '.join(part))
    return '\n'.join(rows), '\n'.join(lines), same


def dawn_biz():
    out = []
    for c, nm in B.CITIES:
        for air in ('OZ', 'KE'):
            for o, d in (('ICN', c), (c, 'ICN')):
                if B.has(air, o, d):
                    b = B.days_of(air, o, d, 'b')
                    if b:
                        out.append('%s %s %s' % ('아시아나' if air == 'OZ' else '대한항공', '인천→' + nm if o == 'ICN' else nm + '→인천', fmt(b)))
    zero = [nm for c, nm in B.CITIES if sum(len(B.days_of(air, o, d, 'b')) for air in ('OZ', 'KE') for o, d in (('ICN', c), (c, 'ICN')) if B.has(air, o, d)) == 0]
    return '\n'.join(out), '·'.join(zero)


def thumb(fn):
    S = C
    W, H = 1080, 1080
    fig = plt.figure(figsize=(W / 100, H / 100), dpi=100, facecolor=S.SURF)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)
    ax.axis('off')
    ax.text(60, 92, '마일리지 비즈니스 좌석', fontsize=56, fontweight='bold', color=S.INK, va='center')
    ax.text(60, 168, '아시아나 런던 → 인천 · 같은 날 두 번 조회', fontsize=31, color=S.INK2, va='center')
    y = 250
    for label, cur, prev in (('새벽 4시', L0, None), ('오전 11시', L1, L0)):
        ax.text(60, y + 40, label, fontsize=44, fontweight='bold', color=S.INK, va='center')
        ax.text(W - 60, y + 40, '%d일' % len(cur), fontsize=84, fontweight='bold', color=S.INK, va='center', ha='right')
        gx, gy, cs = 60, y + 110, 48.5
        for i, day in enumerate(S.DAYS):
            cx, cy = gx + (i % 20) * cs, gy + (i // 20) * cs
            if day in cur:
                fc = S.INK if (prev is not None and day not in prev) else S.COL['OZ']
                ax.add_patch(Rectangle((cx, cy), cs - 8, cs - 8, facecolor=fc, edgecolor='none'))
            elif prev is not None and day in prev:
                ax.add_patch(Rectangle((cx, cy), cs - 8, cs - 8, facecolor=S.SURF, edgecolor=S.INK, lw=1.6))
            else:
                ax.add_patch(Rectangle((cx, cy), cs - 8, cs - 8, facecolor=S.NONE, edgecolor='none'))
        y += 110 + 4 * cs + 56
    ax.text(60, 1000, '칸 하나가 하루 (2026.10.3~12.16 출발) · 검은 칸이 오전에 새로 열린 날', fontsize=22, color=S.MUTED, va='center')
    ax.text(60, 1036, '2026년 10월 2일 조회, 직접 만든 그림', fontsize=22, color=S.MUTED, va='center')
    fig.savefig(os.path.join(OUTDIR, fn), dpi=100, facecolor=S.SURF)
    plt.close(fig)
    print(fn, W, 'x', H)


eco_table, eco_lines, eco_same = eco_rows()
dawn_list, dawn_zero = dawn_biz()

BODY = f"""[[TITLE: 아시아나 마일리지 비즈니스 | 새벽엔 2일이던 런던 좌석이 오전엔 19일이었어]]
[[CATEGORY: Travel > 정보]]

===== ✂️ 여기부터 복사 =====

아시아나 마일리지를 지금 규정 그대로 쓸 수 있는 건 12월 16일 출발까지야. 12월 17일이면 아시아나가 대한항공으로 합쳐지거든.
그 전에 유럽을 비즈니스로 다녀올 수 있나 싶어서 마일리지 좌석을 열어봤어. 새벽에 봤을 땐 거의 없었어. 그런데 같은 날 오전에 다시 열어보니 달라져 있었어.

결론부터 말하면 **런던에서 돌아오는 아시아나 비즈니스가 새벽 4시엔 {len(L0)}일, 오전 11시엔 {len(L1)}일이었어.** 한 번 보고 없다고 접으면 안 되는 거야.

[[IMG:biz_thumb.png | 아시아나 런던→인천 비즈니스. 위가 새벽, 아래가 같은 날 오전이야. 검은 칸이 그사이 새로 열린 날이야. 직접 만든 그림이야]]

---

⏳ 아시아나 마일리지를 지금 규정대로 쓰는 건 12월 16일 출발까지야

합병한다고 마일리지가 사라지는 건 아니야. 아시아나 마일리지는 합병 뒤에도 10년 동안 따로 남아. 달라지는 건 쓰는 조건이야.
9월에 통합 안내 사이트에서 확인한 내용을 줄이면 이래.

| | 합병 전 | 합병 뒤 |
|---|---|---|
| 탈 수 있는 편 | 아시아나, 스타얼라이언스 | 대한항공 운항 노선 |
| 적용 규정 | 아시아나 규정 | 공제표만 아시아나, 나머지는 스카이패스 |
| 스카이패스로 전환 | 해당 없음 | 제휴 적립분은 1 : 0.82 |

**지금 아는 규정 그대로 쓸 수 있는 기간이 합병 전까지인 거야.** 그래서 12월 16일 출발까지만 봤어.

---

🌙 새벽 4시, 유럽 비즈니스는 열 곳을 다 봐도 이게 전부였어

10월 2일 새벽 {hm('03:40')}부터 {hm('05:17')} 사이에 아시아나와 대한항공 마일리지 예매 화면을 열었어. 로그인해서 성인 1명, 편도, 직항으로 조회했고, 직접 만든 조회 프로그램으로 받았어.
아시아나는 런던·파리·프랑크푸르트·로마·밀라노·바르셀로나·프라하·이스탄불 여덟 곳, 대한항공은 바르셀로나 대신 암스테르담·마드리드를 넣은 아홉 곳이야. 10월 2일부터 12월 16일까지 76일 가운데 비즈니스 좌석이 있던 날을 전부 적으면 이래. 대한항공은 프레스티지석이야.

{dawn_list}

**{dawn_zero}는 두 항공사 가는 편, 오는 편 어디에도 없었어.** 여기까지만 보면 합병 전에 유럽을 비즈니스로 가는 건 거의 안 되는 것처럼 보여.

[[IMG:eu_business.png | 새벽에 본 유럽 열 곳의 비즈니스 좌석. 날짜까지 전부 적었어. 직접 만든 표 이미지야]]

---

☀️ 오전 11시, 런던→인천 비즈니스가 {len(L1)}일로 늘어 있었어

같은 날 {hm(T1a)}부터 {hm(T1b)} 사이에 런던과 파리를 다시 조회했어. 다른 도시는 다시 보지 못했어.
오전에는 10월 2일 출발편이 조회에서 빠져서, 두 번을 견줄 때는 10월 3일부터 12월 16일까지 75일로 맞췄어.

{biz_rows()}

달라진 건 아시아나 런던→인천 한 줄이야.
새로 열린 날 {fmt(new_b)}
사라진 날 {fmt(gone_b)}

새벽에는 11월 29일 OZ522편 비즈니스가 「매진」으로 찍혀 있었어. 오전에는 같은 편이 {MILE}로 열려 있었어.
왜 한꺼번에 열렸는지는 화면에 나오지 않아서 몰라. 본 건 새벽에 없던 날이 일곱 시간 뒤에 있었다는 것까지야.

다만 인천→런던 가는 편은 오전에도 0일이었어. **런던을 비즈니스로 왕복하는 조합은 여전히 없었고, 돌아오는 편만 비즈니스로 잡을 수 있었어.**

[[IMG:eu_change_business.png | 새벽과 오전 비즈니스 비교. 검은 칸이 오전에 새로 열린 날, 테두리만 있는 칸이 사라진 날이야. 직접 만든 표 이미지야]]

---

🪑 파리·런던 일반석도 일곱 시간 사이에 움직였어

비즈니스만 그런 게 아니었어. 일반석도 같은 75일 기준으로 달라진 노선이 있었어.

{eco_table}

{eco_lines}

나머지 {len(eco_same)}개 방향({', '.join(eco_same)})은 새벽과 오전이 같았어.
인천→파리는 새벽에 좌석없음이던 10월 4·11·18일이 오전에 열려 있었어. 그사이에 직접 화면을 눌러 본 것과도 맞았어.

[[IMG:eu_change_economy.png | 새벽과 오전 일반석 비교. 런던·파리와 인천→프랑크푸르트야. 직접 만든 표 이미지야]]

---

🔎 아시아나 달력은 좌석등급을 「비즈니스」로 골라야 비즈니스가 보여

조회하다가 걸린 게 하나 있어. 아시아나 마일리지 예매 화면에서 좌석등급을 「전체」로 두면 달력에 하루 표시가 하나만 떠.
런던→인천 11월 1일이 그랬어. 「전체」로 보면 일반석 표시만 있었고, 좌석등급을 「비즈니스」로만 골라 다시 조회하니 그날에 비즈니스 표시가 떴어.
**일반석이 있는 날은 비즈니스 표시가 가려지는 거야.** 비즈니스를 찾는 거라면 좌석등급에서 비즈니스만 골라서 조회해야 해.

---

🕐 마일리지 좌석은 시간을 달리해서 한 번 더 봐야 해

이번에 해 보고 정리한 건 세 가지야.

하나, 한 번 보고 접지 않는다. 새벽에 2일이던 노선이 오전에 19일이었어.
둘, 가는 편과 오는 편을 따로 본다. 좌석이 따로 열려서 한쪽만 있는 경우가 많아.
셋, 아시아나는 좌석등급을 비즈니스로 골라서 본다.

몇 시에 보는 게 좋은지는 말 못 해. 내가 견준 건 하루, 두 번뿐이야. 오전에 늘어난 노선도 있었고 줄어든 날짜도 있었어.
그리고 이 숫자는 10월 2일에 찍힌 값이야. 이 글을 읽는 시점엔 또 달라져 있을 테니, 날짜는 예매 화면에서 직접 확인해.

[[LINK:https://blog.naver.com/baiyan_novembre/224412501059 | ▶ 아시아나 마일리지 대한항공 통합, 계정 연결은 이렇게 했어]]

[[LINK:https://blog.naver.com/baiyan_novembre/224423671841 | ▶ 대한항공 마일리지 좌석은 오전 9시에 열려]]

#아시아나마일리지 #아시아나마일리지비즈니스 #마일리지비즈니스 #아시아나마일리지사용 #보너스항공권 #마일리지항공권 #아시아나합병 #대한항공마일리지 #런던마일리지 #걷고읽고떠나고

===== ✂️ 여기까지 =====

# 🚧 작업 메모 — 발행 전 이 아래는 전부 삭제

## 이 판(v2)의 원칙 — 2026-10-02 사용자 지시

비즈니스 좌석을 찾아오는 사람에게 맞춘다. 나라를 많이 늘어놓지 않는다. 「같은 날에도 좌석이 바뀌니 시간을 달리해 다시 보라」가 축.
숫자는 센 값만. 퍼센트·합계·차이값 없음. 원인 단정 없음(0-9).
본문·표·날짜는 `gen_biz_draft.py` 가 데이터에서 뽑는다. 숫자를 손으로 고치지 말고 스크립트를 다시 돌린다.
v1(일반석 도시별 비교)은 `eu_mileage_post_draft.md` 로 남아 있다. 발행하지 않는다.

## 근거 자료

새벽: 2026-10-02 03:40~05:17, 유럽 10곳, 76일(10/2~12/16). `_원본\\oz_daily.json` · `ke_live.json`.
오전: 2026-10-02 {C.T1}, 아시아나 런던·파리 왕복 + 인천→프랑크푸르트 일반석, 대한항공 런던·파리 왕복 + 인천→프랑크푸르트. `_원본\\re_oz.json` · `re_ke.json`.
비교는 75일(10/3~12/16). `유럽_같은날_두번조회_비교.csv`.
아시아나 런던→인천 비즈니스: 새벽 조회에서 11/1~13 구간은 04:02 기준 달력(10/29 선택)으로 덮였고 비즈니스 표시가 없었다. 11/29 는 새벽 편 내역이 「매진」.
아시아나 오전 수집은 11:11 차단(Access Denied)으로 로마·바르셀로나를 받지 못했다. 본문에는 「다른 도시는 다시 보지 못했어」로만 적었다.

## 발행 전 확인할 것

🚧 **런던→인천 비즈니스 날짜를 수동으로 두세 개 대조**(11/1, 11/18, 12/4). 제목에 걸린 숫자다. 회사 회선에서는 아시아나 접속이 된다.
🚧 ⏳ 섹션 표는 9/15 발행 글에서 가져왔다. 통합 안내 사이트를 한 번 더 연다.
🚧 `{MILE}` 은 화면 문구 그대로다. 공제표와 대조하지 않았다.

## 사진 배치 — 파일은 전부 이 폴더에 있다

| 파일 | 위치 | 비고 |
|---|---|---|
| biz_thumb.png | 도입 = 썸네일 | 런던→인천 비즈니스 새벽 {len(L0)}일 / 오전 {len(L1)}일 |
| eu_business.png | 🌙 섹션 | 새벽 기준, 세로로 김 |
| eu_change_business.png | ☀️ 섹션 | 새벽·오전 비교 |
| eu_change_economy.png | 🪑 섹션 | 새벽·오전 비교 |

## 🚫 하지 말 것

🚫 「오전에 풀린다」「몇 시에 보면 된다」처럼 규칙으로 쓰지 않는다. 하루, 두 시각뿐이다.
🚫 왜 열렸는지(취소·추가 공급 등) 쓰지 않는다.
🚫 「합병 전에 안 쓰면 사라진다」 류 금지(10-3). 「나는 합병 전에 다 쓸 거야」도 쓰지 않는다.
🚫 조회 프로그램·로그인 유지·차단 얘기를 본문에 쓰지 않는다.
🚫 보유 마일리지·회원 정보는 넣지 않는다.

## 제목 후보

1. 아시아나 마일리지 비즈니스 | 새벽엔 2일이던 런던 좌석이 오전엔 19일이었어 (현재)
2. 아시아나 마일리지 비즈니스 좌석 | 한 번 보고 접지 마, 같은 날 오전에 19일로 늘어 있었어
3. 아시아나 마일리지 사용 | 합병 전 유럽 비즈니스, 새벽과 오전이 달랐어

## 발행 전 체크

본문에서 `[[` 와 `🚧` 검색. 사진 다 넣었으면 `[[IMG` 0개.
첫 사진이 biz_thumb.png 인지. 카테고리는 발행 화면에서 직접 고른다.
경계선 두 줄 원문 그대로.
발행 후 9/15 통합 글 하단에 이 글 링크 추가.
"""

thumb('biz_thumb.png')
path = os.path.join(OUTDIR, 'eu_biz_post_draft.md')
open(path, 'w', encoding='utf-8').write(BODY)
body = BODY.split('===== ✂️ 여기부터 복사 =====')[1].split('===== ✂️ 여기까지 =====')[0]
print('written', path, '| 본문', len(body), '자 | IMG', body.count('[[IMG'), '| 표', body.count('|---|'))
