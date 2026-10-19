# 대본에서 같은 말 반복 찾기 — python repeat_check.py <narration\EP\script.txt> (qa_clip ③-3 이 부른다)
# (10/11 사용자: 「~위에 ~위에 두 번 나와서 듣기 이상」「영어처럼 한글도 같은 단어 두 번을 꺼린다」 — 지침 6-1-2)
#  ① 한 줄(한 장면) 안에서 같은 말 줄기가 두 번 → 고칠 것
#  ② 바로 다음 줄 첫머리까지 같은 말 줄기 → 볼 것(이어 듣기 때문)
#  ③ 「-아 보고 … -아 보며」처럼 같은 보조 동사가 한 줄에 두 번 → 고칠 것
import re, sys

# 말 줄기 = 어절에서 뒤 조사·어미를 떼어 낸 앞부분
TAIL = sorted(['은', '는', '이', '가', '을', '를', '에', '에서', '에선', '엔', '으로', '로', '와', '과', '도', '만', '까지', '부터',
               '이야', '야', '이었어', '였어', '었어', '았어', '했어', '어', '아', '고', '며', '면', '서', '지', '게', '든', '이든',
               '처럼', '보다', '마다', '이나', '나', '의', '께', '한테', '라고', '이라고', '였다', '이다', '다'], key=len, reverse=True)
SKIP = {'그', '이', '저', '너', '나', '내', '것', '거', '수', '때', '더', '안', '못', '잘', '다', '또', '좀', '꼭', '한', '두', '날',
        '편', '중', '전', '뒤', '앞', '명', '일', '월', '년', '억', '만', '원', '건', '층', '그램', '병', '선수', '감독', '분', '개', '시', '엔', '킬로', '하나', '둘', '셋', '넷', '다섯', '여섯', '일곱', '여덟', '아홉', '석', '열', '세', '네', '어디', '언제', '무엇', '왜', '그런데', '그래서', '그리고', '그러니까', '대신', '혹시', '알려줘', '댓글로', '너는', '나는'}
AUX = ['보고', '보며', '보는', '본', '봤어', '봐']


def stem(w):
    w = re.sub(r'[,.?!·「」\'"]', '', w)
    if re.fullmatch(r'[\d.,~%]+\w{0,2}', w):
        return ''   # 숫자는 따로 셈하지 않는다
    for t in TAIL:
        if w.endswith(t) and len(w) - len(t) >= 1:
            return w[:-len(t)]
    return w


def check(lines):
    out = []
    for n, line in enumerate(lines):
        words = line.split()
        st = [stem(w) for w in words]
        seen = {}
        for i, s in enumerate(st):
            if len(s) < 1 or s in SKIP or words[i] in SKIP:
                continue
            if s in seen:
                a, b = words[seen[s]], words[i]
                between = ' '.join(words[seen[s] + 1:i])
                pun = i == seen[s] + 1 and re.search(r'(였던|이었던|였어|이었어)', b)   # 「계획표는, 계획표였던 거지」 같은 말장난
                if (a.endswith('?') and b.endswith('?') and '아니면' in between) or (a.endswith('든') and b.endswith('든')) or pun:
                    continue   # 일부러 맞춘 대구(「A 챙겨? 아니면 B 챙겨?」「싼 스틱이든 비싼 스틱이든」)는 반복으로 치지 않는다
                out.append(('고칠 것', n, '「%s」 두 번: %s … %s' % (s, words[seen[s]], words[i]), line))
            else:
                seen[s] = i
        aux = [w for w in words if re.sub(r'[,.?!]', '', w) in AUX]
        if len(aux) >= 2:
            out.append(('고칠 것', n, '보조 동사 「보다」 %d번: %s' % (len(aux), ' · '.join(aux)), line))
        if n + 1 < len(lines):
            nxt = [stem(w) for w in lines[n + 1].split()[:4]]
            tail = [s for s in st[-4:] if s and s not in SKIP]
            for s in tail:
                if s in nxt:
                    out.append(('볼 것', n, '「%s」 다음 줄 첫머리에 또' % s, line + ' / ' + lines[n + 1]))
    return out


if __name__ == '__main__':
    lines = [l.strip() for l in open(sys.argv[1], encoding='utf-8') if l.strip()]
    res = check(lines)
    for kind, n, msg, line in res:
        print('%s  n%02d  %s\n        %s' % (kind, n, msg, line))
    print('반복 %d건(고칠 것 %d)' % (len(res), sum(1 for r in res if r[0] == '고칠 것')))
