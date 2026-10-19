# -*- coding: utf-8 -*-
"""2027년 10월 연휴 — 복귀편(10/3·10/4) + 출발편 하루 뒤 변화 → 후속 글 초안. 숫자는 _summary_return.json 과 CSV 에서.
사용: python gen_holiday_return_draft.py "<글 폴더>" [<앞 글 URL>]
"""
import sys, os, csv, json, collections
sys.stdout.reconfigure(encoding='utf-8')
OUT = sys.argv[1]
PREV_URL = sys.argv[2] if len(sys.argv) > 2 else ''
J = json.load(open(os.path.join(OUT, '_summary_return.json'), encoding='utf-8'))
S, CH = J['ret'], J['change']
D3, D4 = '20271003', '20271004'
AS, EU, AM = S['아시아'], S['유럽'], S['미주·대양주']
rows = list(csv.DictReader(open(os.path.join(OUT, '2027년10월연휴_대한항공_마일리지_복귀편별_20261009.csv'), encoding='utf-8-sig')))


def josa(w, a, b):
    ch = w[-1]
    return w + (a if (ord(ch) - 0xAC00) % 28 else b) if '가' <= ch <= '힣' else w + a


def n(reg, d, k):
    return S[reg][d][k]


def cnt(reg, k):
    return sum(S[reg][d][k] if not isinstance(S[reg][d][k], list) else len(S[reg][d][k]) for d in (D3, D4))


def tot(reg):
    return S[reg][D3]['n'] + S[reg][D4]['n']


def fmt_list(items, with_seats=False):
    out = []
    for it in items:
        city, flt, dep = it[0], it[1], it[2]
        out.append('%s %s' % (city, flt) + (' %d석' % it[3] if with_seats and len(it) > 3 else ''))
    return ', '.join(out)


def day_of(ymd):
    return '10월 %d일' % int(ymd[6:8])


# 유럽 표: 도시 | 10/3 | 10/4 (칸 = 편별 일반석)
def eu_table():
    by = collections.OrderedDict()
    for r in rows:
        if r['권역'] != '유럽':
            continue
        b = by.setdefault(r['도시'], {D3: [], D4: []})
        v = r['일반석 잔여(표시 상한 9)']
        v = '9석 이상' if v == '9' else ('0석' if v == '0' else v + '석')
        b[r['복귀일']].append('%s %s' % (r['현지 출발시각'], v))
    out = ['| 도시 | 10/3 일 | 10/4 월 |', '|---|---|---|']
    for c in ['런던', '파리', '프랑크푸르트', '암스테르담', '로마', '밀라노', '마드리드', '리스본', '프라하', '빈', '취리히', '부다페스트', '이스탄불']:
        if c not in by:
            continue
        b = by[c]
        out.append('| %s | %s | %s |' % (c, '·'.join(b[D3]) or '편 없음', '·'.join(b[D4]) or '편 없음'))
    return '\n'.join(out)


eu_zero = [fmt_list(S['유럽'][d]['zero']) for d in (D3, D4)]
eu_prok4 = fmt_list(S['유럽'][D4]['prok'])
am_prok = ', '.join(['3일 ' + fmt_list([x]) for x in S['미주·대양주'][D3]['prok']] + ['4일 ' + fmt_list([x]) for x in S['미주·대양주'][D4]['prok']])
as_low3 = fmt_list(S['아시아'][D3]['low'], True); as_low4 = fmt_list(S['아시아'][D4]['low'], True)

assert cnt('아시아', 'ey0') == 0 and cnt('미주·대양주', 'ey0') == 0, '아시아·미주 복귀 0석이 생겼다 — 본문 문장 확인'
assert S['유럽'][D3]['ey0'] == 1 and S['유럽'][D4]['ey0'] == 1, '유럽 복귀 0석 수가 바뀌었다 — 제목·본문 확인'

to_zero = CH['to_zero']; from_zero = CH['from_zero']; ey_down = CH['ey_down']; ey_up = CH['ey_up']; pr_down = CH['pr_down']; pr_up = CH['pr_up']


def chl(items, key8, key9, unit=''):
    return ', '.join('%s %s %s(%s→%s%s)' % (c['city'], day_of(c['ymd'])[-3:].strip(), c['flt'], c[key8] if c[key8] is not None else '-', c[key9] if c[key9] is not None else '-', unit) for c in items)


prev_link = ('[[LINK:%s | ▶ 앞 글: 2027년 10월 연휴 출발편, 열린 지 이틀 만에 유럽 비즈니스는 28편 중 0편이었어]]\n\n' % PREV_URL) if PREV_URL else ''

BODY = f"""[[TITLE: 2027년 10월 연휴 마일리지 복귀편 | 열린 날 밤에 봤는데 유럽 {tot('유럽')}편 중 0석은 파리 둘뿐이었어]]
[[CATEGORY: Travel > 정보]]

===== ✂️ 여기부터 복사 =====

어제 출발편을 봤으니 오늘은 돌아오는 편이야. 2027년 10월 4일 월요일, 연휴 마지막 날 복귀편이 오늘 아침 9시에 열렸고, 밤 9시 50분부터 10시 사이에 52개 도시에서 인천으로 오는 10월 3일·4일 편 {tot('아시아') + tot('유럽') + tot('미주·대양주')}개를 로그인해서 한 편씩 열어봤어. **결론부터. 복귀편은 출발편보다 훨씬 남아 있었어. 유럽 {tot('유럽')}편 중 일반석 0석은 파리 한 편(3일·4일 각 1번)뿐이고, 아시아 {tot('아시아')}편과 미주·대양주 {tot('미주·대양주')}편은 0석이 없었어.** 대신 프레스티지는 유럽 {tot('유럽')}편 중 {cnt('유럽', 'prok')}편, 미주·대양주 {tot('미주·대양주')}편 중 {cnt('미주·대양주', 'prok')}편에만 남아 있었어.
같은 밤에 어제 본 출발편 {CH['n_out9']}개도 다시 열어봤어. 하루 사이에 바뀐 편이 {CH['n']}개였어.

[[IMG:ai_gate_evening_20261009.png | 연휴 마지막 날 저녁, 유럽 공항 게이트에서 인천행을 기다리는 장면 (AI 생성 이미지, 실제 공항 사진 아님)]]

---

🗓️ 복귀편 10월 4일은 오늘 아침에 열렸고, 10월 5일은 내일이야

대한항공 마일리지 좌석은 출발일 기준 360일 전 아침 9시쯤 열려. 10월 4일 월요일 복귀편은 그래서 오늘 10월 9일에 열렸고, 10월 3일 일요일 복귀편은 어제 열린 거야. 화요일 10월 5일은 내일 아침에 열리니까 오늘 밤엔 전부 미오픈 화면이었어.
오늘 본 건 현지 공항에서 인천으로 오는 편, 성인 1명 편도, 직항만이야. 화면에 잔여가 9석 넘으면 9로만 보여서 「9석 이상」으로 적었어. 시각은 전부 현지 출발 시각이야.

---

🇪🇺 유럽 복귀편은 {tot('유럽')}편 중 0석이 둘뿐이고, 둘 다 파리였어

출발편은 28편 중 9편이 0석이었는데 돌아오는 편은 달랐어. 10월 3일 {n('유럽', D3, 'n')}편 중 0석 {n('유럽', D3, 'ey0')}편, 10월 4일 {n('유럽', D4, 'n')}편 중 0석 {n('유럽', D4, 'ey0')}편이고, 둘 다 파리 KE5902 14시 40분 편이야. 10월 4일에 뜨는 파리 본편 KE902 20시 35분은 9석 이상이었어.
런던·암스테르담·밀라노·이스탄불·빈·리스본은 두 날 다 9석 이상이었어. 프랑크푸르트·마드리드는 3일에만, 로마·프라하·부다페스트는 4일에만 뜨는데 그날은 9석 이상이었고, 취리히는 두 날 다 운항이 없었어. 바르셀로나는 복귀편도 보너스 운임이 안 붙어 있었어.
**프레스티지는 10월 3일 {n('유럽', D3, 'n')}편 전부 0석, 10월 4일은 {n('유럽', D4, 'n')}편 중 {len(S['유럽'][D4]['prok'])}편에 1석씩 남아 있었어.** 남은 건 {eu_prok4}이야. 출발편 28편이 전부 0석이던 것과 비교하면 열린 날 밤에는 아직 몇 자리가 보인 거야.

[[IMG:return_grid_europe_20261009.png | 유럽 14도시 → 인천, 10/3·10/4 편마다 일반석 잔여. 빨간 칸이 0석이야. 직접 만든 그림]]

{eu_table()}

---

🌏 아시아 복귀편 {tot('아시아')}편은 0석이 없었어

10월 3일 {n('아시아', D3, 'n')}편, 10월 4일 {n('아시아', D4, 'n')}편 모두 일반석 0석이 없었어. 9석 아래로 내려간 편만 적으면 10월 3일은 {as_low3}, 10월 4일은 {as_low4}이야. 출발편에서 0석이던 오키나와도 돌아오는 편은 두 날 다 열려 있었어.
프레스티지는 10월 3일 {n('아시아', D3, 'n')}편 중 {n('아시아', D3, 'pr0')}편, 10월 4일 {n('아시아', D4, 'n')}편 중 {n('아시아', D4, 'pr0')}편이 0석이었어. 아시아는 복귀편도 프레스티지가 꽤 남아 있는 쪽이야.

[[IMG:return_grid_asia_20261009.png | 아시아 22도시 → 인천, 10/3·10/4 편마다 일반석 잔여. 직접 만든 그림]]

---

✈️ 미주·대양주 복귀편 {tot('미주·대양주')}편도 일반석은 다 있었고, 프레스티지는 {cnt('미주·대양주', 'prok')}편뿐이었어

미국·캐나다·호주·뉴질랜드 16도시에서 인천으로 오는 편은 10월 3일 {n('미주·대양주', D3, 'n')}편, 4일 {n('미주·대양주', D4, 'n')}편이 전부 9석 이상이었어. 0석도, 9석 아래도 없었어.
**프레스티지는 {tot('미주·대양주')}편 중 {cnt('미주·대양주', 'prok')}편에만 남았어.** {am_prok}이야. LA·뉴욕·샌프란시스코·호놀룰루·라스베이거스·시카고·애틀랜타·댈러스·워싱턴·토론토·시드니는 두 날 다 0석이었어.

[[IMG:return_grid_americas_20261009.png | 미주·대양주 16도시 → 인천, 10/3·10/4 편마다 일반석 잔여. 직접 만든 그림]]

[[IMG:return_prestige_20261009.png | 복귀편 프레스티지가 남은 편 수를 권역별로. 직접 만든 그림]]

---

🔁 어제 본 출발편 {CH['n_out9']}개를 다시 열어보니 {CH['n']}개가 바뀌어 있었어

같은 밤에 어제 오전에 본 출발편을 그대로 다시 봤어. 일반석이 줄어든 편 {len(ey_down)}개, 늘어난 편 {len(ey_up)}개, 0석이 된 편 {len(to_zero)}개, 0석이었다가 다시 열린 편 {len(from_zero)}개야.
{('일반석이 줄어든 편은 ' + chl(ey_down, 'ey8', 'ey9', '석') + '이고, 그중 0석이 된 건 ' + chl(to_zero, 'ey8', 'ey9', '석') + '이야. ') if to_zero else ('일반석이 줄어든 편은 ' + chl(ey_down, 'ey8', 'ey9', '석') + '이야. ' if ey_down else '하루 사이에 일반석이 줄어든 편은 없었어. ')}{('다시 열린 편은 ' + chl(from_zero, 'ey8', 'ey9') + '이야. ') if from_zero else '0석이던 편이 다시 열린 경우도 없었어. '}
{('프레스티지가 줄어든 편은 ' + chl(pr_down, 'pr8', 'pr9') + ', ') if pr_down else '프레스티지가 줄어든 편은 없었고, '}{('늘어난 편은 ' + chl(pr_up, 'pr8', 'pr9') + '이야.') if pr_up else '늘어난 편도 없었어.'}
어제 글에서 「시간을 달리해 다시 보라」고 했는데, 하루 뒤 숫자가 그 말을 그대로 보여 줬어. 왜 늘고 주는지는 모르겠고, 내가 본 건 두 시점의 숫자뿐이야.

[[IMG:out_change_20261009.png | 출발편 중 어제 오전과 오늘 밤 사이에 잔여가 달라진 편. 직접 만든 그림]]

---

🕘 왕복을 묶으려면 어떻게 보면 되나

유럽은 가는 편이 먼저 비어. 가는 편이 9석 이상인 런던·암스테르담·빈·부다페스트는 돌아오는 편도 열려 있어서 왕복이 묶이고, 파리는 가는 10월 1일 KE901 외에는 조합이 어려워. 미주·대양주는 가는 편도 오는 편도 일반석은 넉넉한데 프레스티지는 거의 없어. 아시아는 어느 날이든 묶여.
10월 5일 화요일 복귀편은 내일 아침 9시에 열려. 금요일 출발에 화요일 복귀로 나흘을 다 쓰려면 그때 봐야 해. 오늘 숫자는 10월 9일 밤 한 시점이고, 내일 아침이면 또 달라져 있을 거야.

{prev_link}[[LINK:https://blog.naver.com/baiyan_novembre/224423671841 | ▶ 대한항공 마일리지 좌석은 오전 9시에 열려, 08:59와 09:00을 재봤어]]

[[LINK:https://blog.naver.com/baiyan_novembre/224433381419 | ▶ 대한항공 마일리지 가치, 1마일 10원도 안 되는 날이 있었어]]

#10월연휴마일리지 #2027연휴항공권 #대한항공마일리지 #마일리지항공권 #대한항공보너스항공권 #마일리지복귀편 #유럽마일리지항공권 #대한항공프레스티지 #연휴항공권예약 #마일리지좌석오픈

===== ✂️ 여기까지 =====

# 🚧 작업 메모 — 발행 전 이 아래는 전부 삭제

## 이 글의 원칙

앞 글(출발편)의 짝 글. 질문은 「복귀편이 열렸는데 왕복이 묶이나」 하나. 숫자는 「N편 중 M편」만, 퍼센트·원인 금지(0-9). 범위는 「10/9 밤 한 시점, 현지→인천 직항, 성인 1명 편도」.
본문·표는 `gen_holiday_return_draft.py` 가 `_summary_return.json` 과 복귀편 CSV 에서 뽑는다. 숫자를 손으로 고치지 말고 `build_holiday_return.py` → 이 스크립트 순서로.
썸네일은 마스터 5-4(10/9) 대로 AI 장면(ai_gate_evening_20261009.png), 카드는 두 번째부터. 대표는 1:1로 잘라 지정.

## 근거 자료

`base data/ke_live_2027holiday_return_1009.json`(복귀 10/3·10/4·10/5, 10/5는 미오픈 코드), `base data/ke_live_2027holiday_out_recheck_1009.json`(출발편 재조회), 어제 출발편 3개 json.
이 폴더 `2027년10월연휴_대한항공_마일리지_복귀편별_20261009.csv`, `2027년10월연휴_대한항공_출발편_하루뒤변화_20261009.csv`.
프롬프트·검수는 `image_prompts_ko.md`.

## 발행 전 확인할 것

🚧 앞 글(출발편) 발행 URL 을 `gen_holiday_return_draft.py` 두 번째 인자로 넣어 다시 돌리면 「▶ 앞 글」 링크가 들어간다. 앞 글이 미발행이면 링크 없이 발행(2-4 미발행 글 링크 금지).
🚧 발행 직전 파리 10/4 KE5902 와 런던 10/4 KE908 두 편만 예매 화면에서 눈으로 대조.
🚧 10/10 아침 9시 넘어 10/5 복귀편은 이 글에 덧붙이지 않는다. 필요하면 세 번째 글.

## 사진 배치

| 파일 | 위치 |
|---|---|
| ai_gate_evening_20261009.png | 도입 = 썸네일 (AI 장면, 1:1 대표) |
| return_grid_europe_20261009.png | 🇪🇺 |
| return_grid_asia_20261009.png | 🌏 |
| return_grid_americas_20261009.png | ✈️ |
| return_prestige_20261009.png | ✈️ 끝 |
| out_change_20261009.png | 🔁 |

## 🚫 하지 말 것

🚫 「복귀편은 여유 있다」로 일반화하지 않는다. 열린 날 밤 한 시점.
🚫 늘고 준 이유(취소·배정·대기)를 쓰지 않는다.
🚫 아시아나 숫자 없음. 조회 프로그램·로그인·보유 마일리지·회원 정보 금지.

## 제목 후보

1. 2027년 10월 연휴 마일리지 복귀편 | 열린 날 밤에 봤는데 유럽 {tot('유럽')}편 중 0석은 파리 둘뿐이었어 (현재)
2. 10월 연휴 마일리지 왕복 | 가는 편은 유럽 9편이 0석인데 오는 편은 파리 둘뿐이었어
3. 대한항공 마일리지 연휴 복귀편 | 하루 사이 출발편 {CH['n']}편이 바뀌었어

## 발행 전 체크

본문에서 `[[` 와 `🚧` 검색. 사진 다 넣었으면 `[[IMG` 0개. 첫 사진이 ai_gate_evening_20261009.png 인지. 카테고리는 발행 화면에서 직접.
"""
path = os.path.join(OUT, 'holiday_2027oct_return_post_draft.md')
open(path, 'w', encoding='utf-8').write(BODY)
body = BODY.split('===== ✂️ 여기부터 복사 =====')[1].split('===== ✂️ 여기까지 =====')[0]
print('written', path, '| 본문', len(body.replace(' ', '').replace(chr(10), '')), '자 | IMG', body.count('[[IMG'), '| 표', body.count('|---|') // 2)
