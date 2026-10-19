# -*- coding: utf-8 -*-
"""김포↔제주 주말 마일리지 글 초안 — 숫자·날짜는 build_jeju.py 가 만든 _summary.json 에서 뽑는다.
사용: python gen_jeju_draft.py "<글 폴더>"
"""
import sys, os, json, datetime as dt
sys.stdout.reconfigure(encoding='utf-8')
OUT = sys.argv[1]
S = json.load(open(os.path.join(OUT, '_summary.json'), encoding='utf-8'))
DET = S.pop('DET')
COMBO = S.pop('COMBO')
def combo(air, name):
    return [dt.date.fromisoformat(x) for x in COMBO['%s|%s' % (air, name)]]
def wk(ds):
    return ', '.join('%d/%d 주말' % (d.month, d.day) for d in ds) if ds else '없음'
AIR = {'KE': '대한항공', 'OZ': '아시아나'}
WD = '월화수목금토일'


def days(air, name, which=0):
    return [dt.date.fromisoformat(x) for x in S['%s|%s' % (air, name)][which]]


def md(d):
    return '%d월 %d일' % (d.month, d.day)


def mdl(ds):
    """[date] → '10월 10일, 12월 5·12·26일'"""
    if not ds:
        return '없음'
    bym = {}
    for d in ds:
        bym.setdefault(d.month, []).append(str(d.day))
    return ', '.join('%d월 %s일' % (m, '·'.join(v)) for m, v in sorted(bym.items()))


SAT_N = len(days('KE', '토 아침 김포→제주', 0)) + len(days('KE', '토 아침 김포→제주', 1))
SUN_N = len(days('KE', '일 저녁 제주→김포', 0)) + len(days('KE', '일 저녁 제주→김포', 1))
ke_sat_am, oz_sat_am = days('KE', '토 아침 김포→제주'), days('OZ', '토 아침 김포→제주')
ke_sun_pm, oz_sun_pm = days('KE', '일 저녁 제주→김포'), days('OZ', '일 저녁 제주→김포')
oz_sun_miss = days('OZ', '일 저녁 제주→김포', 2)
oz_sun_seen = SUN_N - len(oz_sun_miss)
assert len(ke_sun_pm) == 0 and len(oz_sun_pm) == 0
ke_fri, oz_fri = days('KE', '금 저녁 김포→제주'), days('OZ', '금 저녁 김포→제주')
ke_sun_am, oz_sun_am = days('KE', '일 아침 제주→김포'), days('OZ', '일 아침 제주→김포')
ke_sat_pm_back, oz_sat_pm_back = days('KE', '토 저녁 제주→김포'), days('OZ', '토 저녁 제주→김포')


def pairs(fri, sun):
    return [f for f in fri if f + dt.timedelta(days=2) in set(sun)]


ke_pair, oz_pair = combo('KE', '금 저녁 → 일 아침'), combo('OZ', '금 저녁 → 일 아침')
ke_mon, oz_mon = days('KE', '월 전체 제주→김포'), days('OZ', '월 전체 제주→김포')
ke_mon_pm, oz_mon_pm = days('KE', '월 저녁 제주→김포'), days('OZ', '월 저녁 제주→김포')
ke_mon_am, oz_mon_am = days('KE', '월 아침 제주→김포'), days('OZ', '월 아침 제주→김포')
MON_N = len(days('KE', '월 전체 제주→김포', 0)) + len(days('KE', '월 전체 제주→김포', 1))
ke_last = DET['KE']['sun_last']
oz_last = DET['OZ']['sun_last']
hm = lambda t: '%d시 %s분' % (int(t[:2]), t[3:]) if t[3:] != '00' else '%d시' % int(t[:2])
ke_last_latest = hm(max(v[0] for v in ke_last.values()))
oz_last_latest = hm(max(v[0] for v in oz_last.values()))
oz_sun_noon = days('OZ', '일 낮 제주→김포')
hm2 = lambda t: '%d시 %s분' % (int(t[:2]), t[3:]) if t[3:] != '00' else '%d시' % int(t[:2])
def sat_am_sentence(air):
    out = []
    for d in days(air, '토 아침 김포→제주'):
        fl = DET[air]['sat_am'][d.isoformat()]
        if len(fl) == 1:
            out.append('%s %s %s 한 편' % (md(d), hm2(fl[0][0]), fl[0][1]))
        else:
            out.append('%s %s부터 %s까지 %d편' % (md(d), hm2(fl[0][0]), hm2(fl[-1][0]), len(fl)))
    return ', '.join(out) if out else '없음'
ke_sat_noon, ke_sat_pm = days('KE', '토 낮 김포→제주'), days('KE', '토 저녁 김포→제주')
oz_sat_noon, oz_sat_pm = days('OZ', '토 낮 김포→제주'), days('OZ', '토 저녁 김포→제주')
assert len(days('KE', '일 전체 제주→김포')) == len(ke_sun_am), '대한항공 일요일 좌석이 아침 편만이 아님'
assert len(days('OZ', '일 전체 제주→김포')) == len(oz_sun_am), '아시아나 일요일 좌석이 아침 편만이 아님'
# 공개 달력과 실시간의 차이
diff_total = diff_n = 0
try:
    for ln in open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', '_jeju_live_vs_public.txt'), encoding='utf-8').read().splitlines()[1:]:
        c = [x.strip() for x in ln.split('|')]
        if len(c) < 5 or not c[2].isdigit():
            continue
        if c[3] == '달력 없음':
            continue
        diff_total += 1
        if c[3] != c[4]:
            diff_n += 1
except Exception:
    pass
day_trip_both = [d for d in ke_sat_am if d in set(ke_sat_pm_back)]


def sat_table():
    out = ['| 토요일 | 대한항공 | 아시아나 |', '|---|---|---|']
    ke_d, oz_d = DET['KE']['sat_am'], DET['OZ']['sat_am']
    sats = sorted(set(days('KE', '토 아침 김포→제주', 0) + days('KE', '토 아침 김포→제주', 1)))
    for d in sats:
        k = ke_d.get(d.isoformat()); o = oz_d.get(d.isoformat())
        out.append('| %s | %s | %s |' % (md(d), ('%d편' % len(k)) if k else '0', ('%d편' % len(o)) if o else '0'))
    return '\n'.join(out)


BODY = f"""[[TITLE: 제주 마일리지 항공권 주말 | 일요일 저녁 제주→김포 좌석이 대한항공 {SUN_N}번 중 0번이었어]]
[[CATEGORY: Travel > 정보]]

===== ✂️ 여기부터 복사 =====

날이 좋아서 한라산이나 다녀올까 했어. 마일리지도 있겠다, 토요일 아침에 내려가서 일요일 저녁에 올라오면 딱이잖아.
그래서 10월부터 12월까지 주말마다 김포↔제주 마일리지 좌석이 있는지 대한항공, 아시아나 둘 다 열어봤어.

결론부터 말하면 **일요일 저녁에 제주에서 돌아오는 마일리지 좌석은 대한항공 일요일 {SUN_N}번 중 0번, 아시아나도 {oz_sun_seen}번 중 0번이었어.** 토요일 아침에 내려가는 좌석은 대한항공 12번 중 {len(ke_sat_am)}번, 아시아나 12번 중 {len(oz_sat_am)}번이었고.
한라산 1박 2일을 마일리지로 짜는 건, 이 화면으로는 안 되는 거였어.

[[IMG:jeju_thumb_20261004.png | 토요일 아침에 가서 일요일 저녁에 오는 조합. 칸 하나가 주말 하루고 색칠한 칸이 좌석이 있던 날이야. 직접 만든 그림이야]]

---

🗓️ 숫자는 「10월부터 12월까지 주말 며칠 중 며칠」이야

본 화면은 두 항공사 홈페이지의 마일리지 항공권 예매 화면이야. 로그인해서 성인 1명, 편도로 날짜를 하나씩 눌러 봤고, 10월 4일 밤 11시부터 자정 사이에 직접 만든 조회 프로그램으로 받았어. 처음엔 로그인 없이 보는 공개 좌석 달력으로 봤는데, 예매 화면과 하루에 몇 편씩 어긋나서 전부 다시 열었어.
10월 5일부터 12월 28일까지 금요일 12번, 토요일 12번, 일요일 {SUN_N}번, 월요일 {MON_N}번을 봤어. 편마다 출발 시각이 있으니 10시 전 출발을 「아침」, 17시 이후 출발을 「저녁」으로 나눴어.
공개 달력과 예매 화면을 같은 날짜로 견줘 보니, 좌석 있는 편 수가 다른 날이 {diff_total}일 가운데 {diff_n}일이었어. 그래서 이 글의 숫자는 전부 예매 화면 값이야.

{('아시아나는 조회한 날인 10월 4일 당일 편이 예매 화면에 뜨지 않아서, 일요일은 12번으로 셌어.' if [d.isoformat() for d in oz_sun_miss] == ['2026-10-04'] else '한 가지 알고 봐야 해. 아시아나 예매 화면은 일요일 %d번(%s)에 제주→김포 달력이 뜨지 않았어. 그 날은 세지 않았어.' % (len(oz_sun_miss), mdl(oz_sun_miss))) if oz_sun_miss else '두 항공사 모두 본 날짜의 달력이 전부 떴어.'}

---

🌅 토요일 아침 김포→제주는 대한항공 {len(ke_sat_am)}번, 아시아나 {len(oz_sat_am)}번이었어

10시 전에 출발하는 김포→제주 편에 일반석 마일리지 좌석이 있던 토요일이야. 칸 안 숫자는 좌석이 있던 편 수야.

{sat_table()}

있던 날을 편까지 적으면 대한항공은 {sat_am_sentence('KE')}, 아시아나는 {sat_am_sentence('OZ')}이야.
**10월 10일 말고는 아침 편이 사실상 없는 거야.** 11월 토요일 아침은 두 항공사 모두 0이었어.

낮이나 저녁에 내려가는 건 사정이 달라. 토요일 12번 가운데 대한항공은 낮 {len(ke_sat_noon)}번, 저녁 {len(ke_sat_pm)}번에 좌석이 있었고, 아시아나는 낮 {len(oz_sat_noon)}번, 저녁 {len(oz_sat_pm)}번이야. 문제는 아침이야.

[[IMG:jeju_sat_out_20261004.png | 토요일 김포→제주. 진한 칸이 10시 전 출발이야. 직접 만든 표 이미지야]]

[[IMG:jeju_sat_times_20261004.png | 토요일 김포→제주, 편마다 출발 시각을 점으로 찍은 그림. 색칠한 점이 좌석 있는 편, 10시 왼쪽이 아침이야. 직접 만든 그림]]

---

🌇 일요일 저녁 제주→김포는 두 항공사 모두 0번이었어

여기가 막히는 데야. 17시 이후에 제주에서 올라오는 편에 좌석이 있던 일요일이 대한항공 {SUN_N}번 중 0번, 아시아나 {oz_sun_seen}번 중 0번이었어.

일요일에 좌석이 있던 편은 전부 아침이야. 대한항공은 좌석이 있던 일요일 {len(ke_sun_am)}번 모두 아침 편이었고, 가장 늦은 게 {ke_last_latest} 출발이었어. 아시아나도 좌석이 있던 일요일 {len(oz_sun_am)}번이 모두 아침 편에 있었고, {('낮 편은 ' + mdl(oz_sun_noon) + ' ' + str(len(oz_sun_noon)) + '번뿐이었고') if oz_sun_noon else '낮과 저녁 편은 한 번도 없었고'}, 가장 늦은 출발이 {oz_last_latest}이었어. 대한항공은 낮 편도 0번이야.

**일요일에 한라산을 내려와서 저녁 비행기로 올라오는 그림은, 마일리지로는 이 석 달 안에 없었어.**

[[IMG:jeju_sun_back_20261004.png | 일요일 제주→김포. 저녁 칸은 전부 비어 있어. 직접 만든 표 이미지야]]

[[IMG:jeju_sun_times_20261004.png | 일요일 제주→김포, 편마다 출발 시각. 17시 점선 오른쪽에 색칠한 점이 하나도 없어. 직접 만든 그림]]

---

🧭 금·토에 내려가서 일·월에 올라오는 조합은 이렇게 열려 있었어

그래서 조합을 넓혀 봤어. 금요일 저녁에 내려가거나, 월요일에 올라오는 경우까지.

월요일 제주→김포는 대한항공이 {MON_N}번 중 {len(ke_mon)}번, 아시아나가 {len(oz_mon) + len(days('OZ', '월 전체 제주→김포', 1))}번 중 {len(oz_mon)}번 좌석이 있었어. 월요일 저녁(17시 이후)만 보면 대한항공 {len(ke_mon_pm)}번, 아시아나 {len(oz_mon_pm)}번이야.
금요일 17시 이후 김포→제주는 대한항공 {mdl(ke_fri)}, 아시아나 {mdl(oz_fri)}이었어.

주말마다 가는 편과 오는 편이 같이 열린 조합을 세면 이래. 10월 10일부터 12월 26일까지 12주말 기준이야.

| 조합 | 대한항공 | 아시아나 |
|---|---|---|
| 토 아침 → 일 저녁 | {len(combo('KE', '토 아침 → 일 저녁'))}번 | {len(combo('OZ', '토 아침 → 일 저녁'))}번 |
| 토 아침 → 월 아침 | {len(combo('KE', '토 아침 → 월 아침'))}번 | {len(combo('OZ', '토 아침 → 월 아침'))}번 |
| 금 저녁 → 일 아침 | {len(combo('KE', '금 저녁 → 일 아침'))}번 | {len(combo('OZ', '금 저녁 → 일 아침'))}번 |
| 금 저녁 → 일 저녁 | {len(combo('KE', '금 저녁 → 일 저녁'))}번 | {len(combo('OZ', '금 저녁 → 일 저녁'))}번 |
| 금 저녁 → 월 아침 | {len(combo('KE', '금 저녁 → 월 아침'))}번 | {len(combo('OZ', '금 저녁 → 월 아침'))}번 |
| 토 저녁 → 월 저녁 | {len(combo('KE', '토 저녁 → 월 저녁'))}번 | {len(combo('OZ', '토 저녁 → 월 저녁'))}번 |
| 토 아무 때 → 월 아무 때 | {len(combo('KE', '토 아무 때 → 월 아무 때'))}번 | {len(combo('OZ', '토 아무 때 → 월 아무 때'))}번 |

**가장 많이 열린 건 대한항공 「금 저녁 → 일 아침」 {len(ke_pair)}번({wk(ke_pair)})이었어.** 금요일 밤에 내려가서 토요일에 산에 가고 일요일 아침 비행기로 올라오는 그림이야.
월요일까지 쓸 수 있으면 「금 저녁 → 월 아침」이 대한항공 {wk(combo('KE', '금 저녁 → 월 아침'))}, 「토 아무 때 → 월 아무 때」가 대한항공 {wk(combo('KE', '토 아무 때 → 월 아무 때'))}이야. 아시아나는 「금 저녁 → 일 아침」 {wk(oz_pair)}, 「토 아무 때 → 월 아무 때」 {wk(combo('OZ', '토 아무 때 → 월 아무 때'))}이었어.

[[IMG:jeju_matrix_ke_20261004.png | 대한항공, 주말마다 금·토 출발과 일·월 복귀 시간대별 좌석 있는 편 수. 직접 만든 표 이미지야]]

[[IMG:jeju_matrix_oz_20261004.png | 아시아나, 같은 표. 직접 만든 표 이미지야]]

[[IMG:jeju_combos_20261004.png | 가는 편과 오는 편이 같은 주말에 둘 다 있던 조합별 횟수. 직접 만든 그림]]

토요일 저녁에 바로 올라오는 당일치기도 봤어. 토요일 17시 이후 제주→김포에 좌석이 있던 날은 대한항공 {mdl(ke_sat_pm_back)}, 아시아나 {mdl(oz_sat_pm_back)}이야. 아침에 내려가는 편까지 같은 날 있던 건 대한항공 {mdl(day_trip_both)}인데, 한라산 입산 시간은 따로 확인해야 해.

---

🕘 이 숫자는 10월 4일 밤 기준이고, 오전 9시 지나서 다시 봐야 해

마일리지 좌석은 하루 안에도 바뀌어. 지난주에 아시아나 런던→인천 비즈니스를 세 번 봤는데 새벽 4시엔 2일, 오전 11시엔 19일, 다음 날 밤엔 13일이었어.
대한항공은 보너스 좌석이 오전 9시 정각에 열리는 걸 직접 확인한 적도 있어. 이 글에서 0이라고 적힌 날짜도, 가고 싶은 주말이 정해졌으면 오전 9시 지나서 예매 화면에서 한 번 더 봐.

그리고 이번에 본 건 마일리지 좌석뿐이야. 돈 내고 사는 항공권은 따로야. 아시아나 마일리지는 12월 16일 출발까지가 지금 규정이고, 그 뒤는 대한항공으로 합쳐지니까 그것도 같이 봐 둬.

[[LINK:https://blog.naver.com/baiyan_novembre/224430913269 | ▶ 아시아나 마일리지 비즈니스, 합병 전 74일 국제선 전부 열어봤어]]

[[LINK:https://blog.naver.com/baiyan_novembre/224423671841 | ▶ 대한항공 마일리지 좌석은 오전 9시에 열려]]

#제주마일리지 #제주마일리지항공권 #김포제주마일리지 #대한항공마일리지제주 #아시아나마일리지제주 #주말제주항공권 #한라산등반 #마일리지좌석 #보너스항공권 #걷고읽고떠나고

===== ✂️ 여기까지 =====

# 🚧 작업 메모 — 발행 전 이 아래는 전부 삭제

## 이 글의 원칙

「한라산 가자 → 마일리지로 되나」 한 가지 질문. 숫자는 「주말 N번 중 M번」만. 퍼센트·원인 금지(0-9).
본문·표·날짜는 `gen_jeju_draft.py` 가 `_summary.json` 에서 뽑는다. 숫자를 손으로 고치지 말고 `build_jeju.py` → 이 스크립트 순서로 다시 돌린다.
제목 숫자는 대한항공 기준({SUN_N}번 중 0번). 아시아나 달력이 안 뜬 일요일이 있으면 본문에서 「{oz_sun_seen}번 중 0번」으로 적는다(없으면 문장이 바뀐다).

## 근거 자료

로그인한 예매 화면 실시간 조회, 2026-10-04 23:11~ (대한항공 `jeju_ke_live.json`, 아시아나 `jeju_oz_live.json`). 공개 달력(10/3 기준)과의 날짜별 차이는 _원본 폴더의 `_jeju_live_vs_public.txt`.
이 폴더 `제주_주말_마일리지_편별_20261004.csv`(편마다 시각·좌석), `_일별_20261004.csv`, `_원본\\jeju_ke_weekend.json`·`jeju_oz_weekend.json`.
대한항공 편에는 진에어 공동운항(KE5xxx)이 섞여 있다 — 편별 CSV 비고 열. 아시아나는 좌석 수까지 나오고(10 상한), 대한항공은 유/무만.
아침 = 10:00 전 출발, 낮 = 10:00~16:59, 저녁 = 17:00 이후. 10/25 부터 대한항공 겨울 시간표로 편명이 바뀐다.

## 발행 전 확인할 것

🚧 오전 9시 지난 뒤 가까운 주말(10/10, 10/11) 하나만 예매 화면에서 대조. 공개 달력과 실시간은 다를 수 있다.
🚧 「한라산 입산 시간은 따로 확인해야 해」 — 성판악·관음사 입산 통제 시각을 글에 넣지 않았다. 넣으려면 국립공원 공지 확인 뒤.
🚧 11/7 제주 일정은 개인 일이라 본문에 넣지 않았다.

## 사진 배치

| 파일 | 위치 |
|---|---|
| jeju_thumb_20261004.png | 도입 = 썸네일 |
| jeju_sat_out_20261004.png | 🌅 |
| jeju_sat_times_20261004.png | 🌅 (시각 점 그림) |
| jeju_sun_back_20261004.png | 🌇 |
| jeju_sun_times_20261004.png | 🌇 (시각 점 그림) |
| jeju_matrix_ke_20261004.png | 🧭 |
| jeju_matrix_oz_20261004.png | 🧭 |
| jeju_combos_20261004.png | 🧭 (조합 카드) |

## 🚫 하지 말 것

🚫 「주말엔 마일리지 못 쓴다」로 일반화하지 않는다. 본 건 10~12월 금·토·일·월, 10/4 밤 한 시점.
🚫 「오전 9시에 풀린다」를 아시아나 사실처럼 쓰지 않는다. 확인 권유까지만.
🚫 아시아나 달력에 안 뜬 날을 「없음」으로 세지 않는다.
🚫 조회 프로그램·로그인 얘기 금지. 보유 마일리지·회원 정보 금지.

## 제목 후보

1. 제주 마일리지 항공권 주말 | 일요일 저녁 제주→김포 좌석이 대한항공 {SUN_N}번 중 0번이었어 (현재)
2. 김포 제주 마일리지 주말 | 한라산 1박 2일 조합은 10~12월에 없었고, 금 저녁 출발은 6번 있었어
3. 제주 마일리지 좌석 | 토요일 아침에 내려가는 편은 12번 중 4번, 일요일 저녁 귀경은 0번

## 발행 전 체크

본문에서 `[[` 와 `🚧` 검색. 사진 다 넣었으면 `[[IMG` 0개. 첫 사진이 jeju_thumb_20261004.png 인지. 카테고리는 발행 화면에서 직접.
"""
path = os.path.join(OUT, 'jeju_weekend_post_draft.md')
open(path, 'w', encoding='utf-8').write(BODY)
body = BODY.split('===== ✂️ 여기부터 복사 =====')[1].split('===== ✂️ 여기까지 =====')[0]
print('written', path, '| 본문', len(body), '자 | IMG', body.count('[[IMG'), '| 표', body.count('|---|'))
print('KE 금→일 조합', [d.isoformat() for d in ke_pair], '| OZ', [d.isoformat() for d in oz_pair], '| 당일치기', [d.isoformat() for d in day_trip_both])
