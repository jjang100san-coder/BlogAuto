# -*- coding: utf-8 -*-
import json, sys, re, collections, statistics as st
sys.stdout.reconfigure(encoding="utf-8")
D = json.load(open(sys.argv[1], encoding="utf-8"))
items = [(k, it) for k, v in D['serp'].items() for it in v]
# A. 신선도
pd = [it.get('postdate') or '' for _, it in items]
def ym(s): m = re.match(r'(\d{4})[.\-]?(\d{2})', s.replace(' ', '')); return m.group(1)+'-'+m.group(2) if m else '?'
print("A. 상위30 날짜(월):", collections.Counter(ym(x) for x in pd).most_common(8), "총", len(pd))
# B. 제목 꼴 (검색어별 상위10, 중복 제거)
seen = {}
for k, v in D['serp'].items():
    for it in v[:10]: seen.setdefault(it['link'], (k, it))
T = [it['title'] for _, it in seen.values()]
pat = {'수익 공개·인증·실제': r'공개|인증|실제|현실', '첫 수익': r'첫\s*수익|첫\s*달', '기간(n개월·한 달·일주일)': r'\d+\s*(개월|일|주)|한\s*달|일주일',
       '총정리·방법·꿀팁': r'총정리|정리|방법|꿀팁|가이드', '질문형(?)': r'\?', '금액 숫자(원)': r'\d[\d,]*\s*원', '구분선(|｜:)': r'[|｜]',
       '승인 조건·기준': r'조건|기준', '세금·지급': r'세금|지급|정산|출금'}
print("B. 제목 꼴 (상위10 고유", len(T), "편)")
for n, p in pat.items(): print("  ", n, sum(bool(re.search(p, t)) for t in T))
# C. 본문
P = D['posts']
def rankof(link): return min(it['rank'] for _, it in items if it['link'] == link)
rows = [(rankof(l), p) for l, p in P.items() if p and 'chars' in p]
for name, sel in [('1~3위', lambda r: r <= 3), ('4~10위', lambda r: r > 3)]:
    g = [p for r, p in rows if sel(r)]
    if g: print("C.", name, len(g), "편 | 글자 중앙", st.median(p['chars'] for p in g), "| 사진 중앙", st.median(p['imgs'] for p in g),
               "| 표 있음", sum(p['tables'] > 0 for p in g), "| 광고·협찬 표기", sum(p['ad'] for p in g))
# D. 주장 점검
texts = {l: p['text'] for l, p in P.items() if p and p.get('text')}
title_of = {it['link']: it['title'] for _, it in items}
checks = {
 '✅ 12만5천원 기준': r'12[,.]?5\d{3}\s*원|12만\s*5천|125,000',
 '✅ 8.8%': r'8\.8\s*%',
 '❌ 3.3% (애드포스트에)': r'3\.3\s*%',
 '⚠️ 22% 언급': r'22\s*%',
 '❌ 사업소득으로 신고(개인 애드포스트)': r'애드포스트[^.\n]{0,40}사업소득|사업소득[^.\n]{0,40}애드포스트',
 '✅ 기타소득': r'기타\s*소득',
 '✅ 25일 지급': r'25일',
 '최소 지급 5만': r'5만\s*원|50,000\s*원',
 '옛 표현 「네이버페이 포인트」': r'(네이버\s*페이|Npay|N페이)\s*포인트',
 '「네이버페이 머니」': r'(네이버\s*페이|Npay|N페이)\s*머니',
 '❌ 승인 방문자 숫자 단정(하루 n명)': r'(하루|일)\s*방문자?\s*\d+\s*명\s*(이상|넘)',
 '❌ 승인 글 수 단정(n개 이상)': r'(글|포스팅|게시물)\s*\d+\s*(개|편)\s*이상',
 '클릭당 단가 n원': r'클릭\s*(당|1회)[^.\n]{0,15}\d+\s*원',
 '⚠️ 매달 1일 신청': r'1일[^.\n]{0,10}신청|매달\s*초',
 '고유식별(주민번호) 입력': r'주민(등록)?번호|고유\s*식별',
 '소급': r'소급',
 '분리과세 300만': r'300만',
}
print("D. 주장 점검 (본문", len(texts), "편)")
ex = {}
for n, p in checks.items():
    hits = [l for l, t in texts.items() if re.search(p, t)]
    print("  ", n, len(hits))
    ex[n] = hits
json.dump({n: [(title_of.get(l, ''), l, (re.search(checks[n], texts[l]).group(0)), texts[l][max(0, re.search(checks[n], texts[l]).start()-90): re.search(checks[n], texts[l]).end()+90]) for l in v[:6]] for n, v in ex.items()},
          open(sys.argv[2], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
# E. 실제 수익 숫자 공개
rev = [l for l, t in texts.items() if re.search(r'(수익|수입)[^.\n]{0,20}\d[\d,]*\s*원', t)]
print("E. 본문에 자기 수익 금액(원) 있음:", len(rev), "/", len(texts))
