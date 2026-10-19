# -*- coding: utf-8 -*-
"""유럽 마일리지 좌석 비교 글 초안 생성 — 숫자·날짜는 전부 수집 데이터에서 뽑는다(손으로 고치지 않는다)

사용: python gen_europe_draft.py "<글 폴더>"
"""
import sys, os, datetime as dt, collections

OUTDIR = sys.argv[1]
sys.argv = ['build_europe.py', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', '_buildtest')]
import build_europe as B

sys.stdout.reconfigure(encoding='utf-8')
NM = B.CNAME


def fmt(dates):
    """[date] → '10월 2~6·8~11일, 12월 4일'"""
    if not dates:
        return ''
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


def n(air, o, d, cab='e'):
    return len(B.days_of(air, o, d, cab)) if B.has(air, o, d) else None


def cell(air, o, d):
    v = n(air, o, d)
    return '%d일' % v if v is not None else '—'


def table(codes):
    rows = ['| 노선 | 아시아나 | 대한항공 |', '|---|---|---|']
    for c in codes:
        rows.append('| 인천→%s | %s | %s |' % (NM[c], cell('OZ', 'ICN', c), cell('KE', 'ICN', c)))
        rows.append('| %s→인천 | %s | %s |' % (NM[c], cell('OZ', c, 'ICN'), cell('KE', c, 'ICN')))
    return '\n'.join(rows)


def dates_line(air, o, d):
    """있는 날이 많으면 없던 날을, 적으면 있던 날을 적는다"""
    have = B.days_of(air, o, d, 'e')
    miss = [x for x in B.DAYS if x not in have]
    name = ('아시아나 ' if air == 'OZ' else '대한항공 ') + ('인천→' + NM[d] if o == 'ICN' else NM[o] + '→인천')
    if len(have) >= 45:
        return '%s, 없던 날 %s' % (name, fmt(miss))
    return '%s %s' % (name, fmt(have))


def dates_block(codes, airs=('OZ', 'KE')):
    out = []
    for c in codes:
        for o, d in (('ICN', c), (c, 'ICN')):
            for air in airs:
                if B.has(air, o, d):
                    out.append(dates_line(air, o, d))
    return '\n'.join(out)


def union(o, d):
    return len([x for x in B.DAYS if B.info('OZ', o, d)[x]['e'] == 'Y' or B.info('KE', o, d)[x]['e'] == 'Y'])


def overlap(c):
    """아시아나 좌석이 있던 날 중 대한항공 편이 뜬 날 수 (가는 편+오는 편 각각)"""
    res = []
    for o, d in (('ICN', c), (c, 'ICN')):
        oz = set(B.days_of('OZ', o, d, 'e'))
        ke = {x for x in B.DAYS if B.info('KE', o, d)[x]['e'] in 'YN'}
        res.append(len(oz & ke))
    return res


def ke_listed(o, d):
    return len([x for x in B.DAYS if B.info('KE', o, d)[x]['e'] in 'YN'])


def dep_times(air, o, d):
    c = collections.Counter()
    for x in B.info(air, o, d).values():
        for f in x['flights']:
            c[f['dep']] += 1
    return [t for t, _ in c.most_common(2)]


def biz_lines():
    out = []
    for c, nm in B.CITIES:
        for air in ('OZ', 'KE'):
            for o, d in (('ICN', c), (c, 'ICN')):
                if B.has(air, o, d):
                    b = B.days_of(air, o, d, 'b')
                    if b:
                        out.append('%s %s %s' % ('아시아나' if air == 'OZ' else '대한항공', '인천→' + nm if o == 'ICN' else nm + '→인천', fmt(b)))
    return out


def biz_zero_cities():
    z = []
    for c, nm in B.CITIES:
        tot = sum(n(air, o, d, 'b') or 0 for air in ('OZ', 'KE') for o, d in (('ICN', c), (c, 'ICN')))
        if tot == 0:
            z.append(nm)
    return z


def oct_days(air, o, d, have=True):
    inf = B.info(air, o, d)
    return [x for x in B.DAYS if x.month == 10 and (inf[x]['e'] == 'Y') == have]


ALT = ['FRA', 'FCO', 'MXP', 'PRG']
for c in ALT:
    assert overlap(c) == [0, 0], (c, overlap(c))
assert all(dep_times('OZ', 'ICN', c)[0] == dep_times('KE', 'ICN', c)[0] for c in ALT)
SPAN = B.span_txt().replace('2026.10.2 ', '')
t_a, t_b = [x.replace(':', '시 ') + '분' for x in SPAN.split('~')]
more_back = [nm for c, nm in B.CITIES for air in ('OZ', 'KE') if B.has(air, 'ICN', c) and n(air, c, 'ICN') > n(air, 'ICN', c)]

union_rows = ['| 노선 | 둘 중 한 곳이라도 있던 날 |', '|---|---|']
for c in ALT:
    union_rows.append('| 인천→%s | %d일 |' % (NM[c], union('ICN', c)))
    union_rows.append('| %s→인천 | %d일 |' % (NM[c], union(c, 'ICN')))

BODY = f"""[[TITLE: 아시아나 마일리지 유럽 | 합병 전 76일, 파리 일반석은 아시아나 {n('OZ','ICN','CDG')}일 대한항공 {n('KE','ICN','CDG')}일이었어]]
[[CATEGORY: Travel > 정보]]

===== ✂️ 여기부터 복사 =====

아시아나 마일리지를 지금 규정 그대로 쓸 수 있는 건 12월 16일 출발까지야. 12월 17일이면 아시아나가 대한항공으로 합쳐지거든. 내가 조회한 10월 2일부터 세면 76일이야.
그 76일 동안 유럽 가는 일반석 마일리지 좌석이 며칠 열려 있는지, 아시아나와 대한항공 예매 화면을 같은 날 새벽에 나란히 열어봤어. 날짜를 하루씩 눌러서 편명과 출발 시각까지 받았어.

결론부터 말하면 **런던은 아시아나 {n('OZ','ICN','LHR')}일, 대한항공 {n('KE','ICN','LHR')}일로 둘 다 넉넉했고, 파리는 아시아나 {n('OZ','ICN','CDG')}일, 대한항공 {n('KE','ICN','CDG')}일이었어.** 비즈니스는 두 항공사를 합쳐도 있던 날을 전부 적을 수 있을 만큼 적었어.

[[IMG:eu_thumb.png | 합병 전 76일, 인천→파리 일반석. 칸 하나가 하루고 색칠한 칸이 마일리지 좌석이 있던 날이야. 직접 만든 그림이야]]

---

⏳ 아시아나 마일리지를 지금 규정대로 쓰는 건 12월 16일 출발까지야

합병한다고 마일리지가 사라지는 건 아니야. 아시아나 마일리지는 합병 뒤에도 10년 동안 따로 남아. 달라지는 건 쓰는 조건이야.
9월에 통합 안내 사이트에서 확인한 내용을 줄이면 이래.

| | 합병 전 | 합병 뒤 |
|---|---|---|
| 탈 수 있는 편 | 아시아나, 스타얼라이언스 | 대한항공 운항 노선 |
| 적용 규정 | 아시아나 규정 | 공제표만 아시아나, 나머지는 스카이패스 |
| 스카이패스로 전환 | 해당 없음 | 제휴 적립분은 1 : 0.82 |

**지금 아는 규정 그대로 쓸 수 있는 기간이 합병 전까지인 거야.** 그래서 같은 76일을 두 항공사 화면에서 따로 세어봤어. 아시아나 마일리지로 잡을 수 있는 날과 대한항공 마일리지로 잡을 수 있는 날이 각각 며칠인지 보려는 거야.

---

🗓️ 숫자는 전부 「합병 전 76일 중 며칠」이야

본 화면은 두 항공사 홈페이지의 마일리지 항공권 예매 화면이야. 로그인해서 성인 1명, 편도, 직항으로 조회했어. 10월 2일 {t_a}부터 {t_b} 사이에 직접 만든 조회 프로그램으로 받았어.

세는 법은 하나야. 10월 2일부터 12월 16일까지가 76일이고, 그날 출발하는 편에 일반석 마일리지 좌석이 열려 있으면 「있는 날」로 셌어.

두 화면이 다르게 생겨서 하나는 알고 봐야 해. **대한항공은 편은 뜨는데 좌석이 없는 날과 편이 아예 없는 날이 구분돼. 아시아나 화면은 둘 다 「좌석없음」으로만 나와.** 그래서 아시아나 숫자가 작은 도시에는 자리가 다 찬 날과 비행기가 안 뜨는 날이 섞여 있어.

도시는 열 곳이야. 아시아나가 가는 여덟 곳에 대한항공만 가는 암스테르담과 마드리드를 더했어. 바르셀로나는 이 기간 대한항공 화면에 편이 없었어. 대한항공은 빈·취리히·부다페스트·리스본도 가는데 이번 조회에는 넣지 않았어.

[[IMG:eu_overview_out.png | 인천에서 가는 편 열 곳. 주황이 아시아나, 파랑이 대한항공 일반석이 있던 날 수야. 직접 만든 표 이미지야]]

---

🎡 런던은 아시아나 {n('OZ','ICN','LHR')}일, 대한항공 {n('KE','ICN','LHR')}일이었어

런던 히스로는 두 항공사 모두 매일 편이 떠. 76일 중 일반석이 있던 날이야.

{table(['LHR'])}

가는 편은 어느 쪽 마일리지든 날짜를 고를 수 있었어. 없던 날만 적으면 이래.
{dates_block(['LHR'])}

**돌아오는 편은 10월에 빈 날이 많았어.** 조회한 10월 2일부터 31일까지 30일 가운데 아시아나는 {len(oct_days('OZ','LHR','ICN',False))}일, 대한항공은 {len(oct_days('KE','LHR','ICN',False))}일에 좌석이 없었어. 10월에 런던에서 돌아올 거면 오는 편 날짜부터 잡아야 해.

---

🗼 파리는 아시아나 {n('OZ','ICN','CDG')}일, 대한항공 {n('KE','ICN','CDG')}일이었어

파리 샤를 드 골은 차이가 났어.

{table(['CDG'])}

있던 날을 적으면 이래. 대한항공 가는 편은 없던 날을 적었어.
{dates_block(['CDG'])}

대한항공 화면에는 인천→파리에 KE901과 KE5901 두 편이 떴어. 대한항공은 76일 중 {ke_listed('ICN','CDG')}일에 편이 있었고 그중 {n('KE','ICN','CDG')}일에 일반석이 있었어.
파리에서 돌아오는 편은 10월에 좌석이 있던 날이 아시아나 {fmt(oct_days('OZ','CDG','ICN'))}, 대한항공 {fmt(oct_days('KE','CDG','ICN'))}뿐이었어.

---

🍺 프랑크푸르트·로마·밀라노는 두 항공사가 같은 날 뜨지 않았어

이 세 도시와 프라하는 화면을 나란히 놓고 보니 눈에 띄는 게 있었어. **아시아나에 좌석이 있던 날과 대한항공 편이 뜬 날이 하루도 겹치지 않았어.** 출발 시각은 같았어. 인천→프랑크푸르트는 아시아나 OZ541도 대한항공 KE945도 {dep_times('OZ','ICN','FRA')[0].replace(':','시 ')}분 출발로 찍혀 있었어.
왜 이렇게 짜여 있는지는 화면에 나오지 않아서 몰라. 본 건 날짜가 번갈아 있었다는 것까지야.

{table(['FRA', 'FCO', 'MXP'])}

대한항공은 76일 중 편이 뜬 날이 프랑크푸르트 {ke_listed('ICN','FRA')}일, 로마 {ke_listed('ICN','FCO')}일, 밀라노 {ke_listed('ICN','MXP')}일이었어. 세 곳 모두 매일 뜨는 노선이 아니었어.

날짜가 안 겹치니까, 두 항공사 마일리지를 다 가진 사람은 고를 수 있는 날이 늘어나. 둘 중 한 곳이라도 일반석이 있던 날을 세면 이래.

{chr(10).join(union_rows)}

있던 날은 이래.
{dates_block(['FRA', 'FCO', 'MXP'])}

[[IMG:eu_strip_1.png | 런던·파리·프랑크푸르트·로마·밀라노. 줄 하나가 76일이고 색칠한 칸이 일반석이 있던 날이야. 직접 만든 표 이미지야]]

---

🏰 프라하·이스탄불은 대한항공 쪽이 더 많이 열려 있었어

{table(['PRG', 'IST'])}

인천→프라하는 대한항공이 편이 뜬 {ke_listed('ICN','PRG')}일 전부에 일반석이 있었어. 프라하도 위 세 도시처럼 아시아나 좌석이 있던 날과 대한항공 편이 뜬 날이 겹치지 않았어.
이스탄불은 대한항공이 76일 중 {ke_listed('ICN','IST')}일에 편이 떴어.

{dates_block(['PRG', 'IST'])}

---

⛪ 바르셀로나는 아시아나만, 암스테르담·마드리드는 대한항공만 떴어

{table(['BCN', 'AMS', 'MAD'])}

바르셀로나는 아시아나 마일리지로만 갈 수 있었어. 가는 편은 {n('OZ','ICN','BCN')}일로, 아시아나 가는 편 가운데 런던 다음으로 많았어.
열 곳 가운데 {'·'.join(more_back)}만 오는 편이 가는 편보다 많았어.

{dates_block(['BCN', 'AMS', 'MAD'])}

[[IMG:eu_strip_2.png | 바르셀로나·프라하·이스탄불·암스테르담·마드리드. 흰 칸은 대한항공 편이 없는 날이야. 직접 만든 표 이미지야]]

---

🛬 유럽에서 돌아오는 편은 따로 세어야 해

마일리지 항공권은 가는 편과 오는 편 좌석이 따로 열려. 가는 날이 있어도 돌아오는 날이 없으면 왕복이 안 돼.

[[IMG:eu_overview_in.png | 유럽에서 인천으로 돌아오는 편. 가는 편 그림과 같은 순서야. 직접 만든 표 이미지야]]

로마에서 돌아오는 대한항공은 {n('KE','FCO','ICN')}일, 프라하에서 돌아오는 아시아나는 {n('OZ','PRG','ICN')}일이었어. 가는 편만 보고 일정을 짜면 돌아오는 날에서 막혀.

---

💺 유럽 비즈니스는 있던 날을 다 적어도 이게 전부야

비즈니스는 아시아나는 좌석등급을 비즈니스로만 골라 따로 조회했고, 대한항공은 프레스티지석을 봤어. 76일 중 좌석이 있던 날을 전부 적으면 이래.

{chr(10).join(biz_lines())}

**{'·'.join(biz_zero_cities())}는 두 항공사 가는 편, 오는 편 어디에도 비즈니스가 없었어.**
왕복으로 맞출 수 있는 조합은 프라하 하나였어. 대한항공으로 {fmt(B.days_of('KE','ICN','PRG','b'))}에 가고 아시아나로 {fmt(B.days_of('OZ','PRG','ICN','b'))}에 돌아오는 건데, 항공사가 달라서 마일리지를 양쪽에 다 갖고 있어야 해.

[[IMG:eu_business.png | 도시별 비즈니스 좌석이 있던 날과 날짜. 직접 만든 표 이미지야]]

---

🕐 유럽 노선 편명과 출발 시각은 이렇게 찍혀 있었어

날짜를 하루씩 눌러서 받은 편명과 출발 시각이야. 10월 말에 시각이 바뀌는 노선이 많아서 자주 나온 시각 두 개를 적었어.

[[IMG:eu_flights.png | 도시별 편명과 출발 시각. 직접 만든 표 이미지야]]

일반석 편도는 두 항공사 모두 대부분 35,000마일로 찍혔어. 52,500마일로 찍힌 날도 있었어.
아시아나 런던과 이스탄불은 일부 날짜가 화면에 「할인 30,000마일」로 떠 있었어. 대한항공 이스탄불도 30,000마일인 날이 있었어.

---

정리하면 이래. 합병 전 76일 안에 유럽을 일반석으로 갈 거라면 런던은 어느 쪽 마일리지든 날짜가 넉넉해. 파리·밀라노·프라하·이스탄불은 대한항공 쪽에 날짜가 더 많았고, 바르셀로나는 아시아나만 떴어.
프랑크푸르트·로마·밀라노·프라하는 두 항공사가 뜨는 날이 달라서, 한쪽 마일리지만 있으면 고를 수 있는 날이 그만큼 줄어.
비즈니스는 날짜를 고르는 게 아니라 위에 적은 날짜에 일정을 맞춰야 해.

다만 이건 10월 2일 새벽에 찍힌 값이야. 마일리지 좌석은 계속 바뀌니까 날짜를 정했으면 예매 화면에서 한 번 더 확인해.
그리고 이번에 본 건 두 항공사가 자기 편명으로 띄우는 직항뿐이야. 스타얼라이언스나 스카이팀 제휴 항공사 좌석, 경유편은 넣지 않았어.

[[LINK:https://blog.naver.com/baiyan_novembre/224412501059 | ▶ 아시아나 마일리지 대한항공 통합, 계정 연결은 이렇게 했어]]

[[LINK:https://blog.naver.com/baiyan_novembre/224423671841 | ▶ 대한항공 마일리지 좌석은 오전 9시에 열려]]

#아시아나마일리지 #대한항공마일리지 #아시아나마일리지사용 #마일리지항공권 #보너스항공권 #유럽마일리지 #아시아나합병 #런던마일리지 #파리마일리지 #걷고읽고떠나고

===== ✂️ 여기까지 =====

# 🚧 작업 메모 — 발행 전 이 아래는 전부 삭제

## 이 글의 원칙

아시아나·대한항공을 같은 76일(2026-10-02~12-16 출발), 같은 조건(성인 1명·편도·직항·일반석)으로 나란히 본다.
모든 숫자는 「76일 중 N일」. 도시끼리·항공사끼리 더한 합계, 퍼센트, 차이값은 쓰지 않는다(0-9).
「둘 중 한 곳이라도 있던 날」은 더한 값이 아니라 날짜를 하나씩 센 값이다.
본문·표·날짜는 `gen_europe_draft.py` 가 데이터에서 뽑는다. 숫자를 손으로 고치지 말고 스크립트를 다시 돌린다.

## 근거 자료

조회 2026-10-02 {SPAN}, 로그인한 마일리지 예매 화면. 대한항공 18개 방향×76일 미수집 0건, 아시아나 16개 방향 완료.
이 폴더: `유럽_마일리지좌석_편별_raw.csv`(2,312행) · `_일별.csv` · `_노선요약.csv` · `_원본\\`(json, 스크립트).
아시아나 일반석 = 좌석등급 「전체」 조회의 이코노미 표시 + 날짜별 클릭 내역. 아시아나 비즈니스 = 좌석등급 「비즈니스」만 고른 달력.
대한항공 = 하루 1회 조회의 일반석(KEBONUSEY)·프레스티지석(KEBONUSPR). 편이 뜬 날 구분은 대한항공 공개 좌석 달력의 편 목록.
⏳ 섹션 표는 9/15 발행 글에서 가져왔다. 발행 전 통합 안내 사이트를 한 번 더 연다.

## 발행 전 확인할 것

🚧 **「같은 날 뜨지 않았어」 문단**: 화면 데이터로 확인한 건 「아시아나 좌석이 있던 날 ∩ 대한항공 편이 뜬 날 = 0」(프랑크푸르트·로마·밀라노·프라하, 가는 편·오는 편 모두)과 「출발 시각 동일」까지다. 공동운항·요일 나눠 운항이라고 쓰려면 두 항공사 스케줄표나 공지로 확인한 뒤에 쓴다.
🚧 마일 숫자(35,000 / 52,500 / 할인 30,000)는 화면 문구 그대로다. 공제표와 대조하지 않았다.

## 사진 배치 — 파일은 전부 이 폴더에 있다

| 파일 | 위치 | 비고 |
|---|---|---|
| eu_thumb.png | 도입 = 썸네일 | 인천→파리, 아시아나 {n('OZ','ICN','CDG')}일 / 대한항공 {n('KE','ICN','CDG')}일 |
| eu_overview_out.png | 🗓️ 섹션 | 가는 편 열 곳 |
| eu_strip_1.png | 🍺 섹션 끝 | 런던·파리·프랑크푸르트·로마·밀라노 |
| eu_strip_2.png | ⛪ 섹션 끝 | 바르셀로나·프라하·이스탄불·암스테르담·마드리드 |
| eu_overview_in.png | 🛬 섹션 | 오는 편 열 곳 |
| eu_business.png | 💺 섹션 | 세로로 김 |
| eu_flights.png | 🕐 섹션 | 편명·출발 시각 |

## 🚫 하지 말 것

🚫 「합병 전에 안 쓰면 사라진다」 류 금지. 마일리지는 10년 따로 남는다(10-3).
🚫 「나는 합병 전에 다 쓸 거야」라고 쓰지 않는다. 9/15 글에서 「그냥 통합하기로 했어」라고 썼다.
🚫 아시아나의 좌석 없는 날을 「매진」이라 부르지 않는다. 화면이 편 없는 날과 구분해 주지 않는다.
🚫 어느 항공사가 「더 잘 열어 준다」 같은 평가·원인 금지. 본 건 그 새벽의 숫자까지.
🚫 합병 뒤 좌석이 어떻게 될지 쓰지 않는다. 12월 17일 이후 날짜는 세지 않았다.
🚫 조회 프로그램 만드는 법·로그인 유지 방법·브라우저 얘기를 본문에 쓰지 않는다.
🚫 보유 마일리지·회원 정보는 넣지 않는다.

## 제목 후보

1. 아시아나 마일리지 유럽 | 합병 전 76일, 파리 일반석은 아시아나 {n('OZ','ICN','CDG')}일 대한항공 {n('KE','ICN','CDG')}일이었어 (현재)
2. 아시아나 대한항공 마일리지 유럽 | 합병 전 76일, 일반석 좌석 있는 날을 도시별로 세어봤어
3. 마일리지 유럽 항공권 | 프랑크푸르트·로마는 아시아나와 대한항공이 같은 날 뜨지 않았어

## 발행 타이밍 — 빨리

10월 초 날짜는 지나가는 중이다. 며칠 밀리면 `launch.py` 로 다시 조회하고 `build_europe.py` → `gen_europe_draft.py` 순서로 통째로 간다.
발행 후 9/15 통합 글 하단에 이 글 링크 추가.

## 발행 전 체크

본문에서 `[[` 와 `🚧` 검색. 사진 다 넣었으면 `[[IMG` 0개.
첫 사진이 eu_thumb.png 인지. 카테고리는 발행 화면에서 직접 고른다.
경계선 두 줄 원문 그대로.
"""

path = os.path.join(OUTDIR, 'eu_mileage_post_draft.md')
open(path, 'w', encoding='utf-8').write(BODY)
body = BODY.split('===== ✂️ 여기부터 복사 =====')[1].split('===== ✂️ 여기까지 =====')[0]
print('written', path, '| 본문', len(body), '자 | IMG', body.count('[[IMG'), '| 표', body.count('|---|'))
print('오는 편이 더 많은 곳:', more_back)
print('겹침 0 확인:', {c: overlap(c) for c in ALT}, '| IST', overlap('IST'))
