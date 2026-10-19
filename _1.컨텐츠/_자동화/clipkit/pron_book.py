# 피해야 할 발음 장부 — 클립 지침 6-1-3 (10/11 사용자 제안: 「반복해서 걸리는 받침·단어로 피해야 할 발음 데이터를 쌓자」)
#   장부: clipkit\pron_book.json   (낱말 · 들린 말 · 횟수 · 바꾼 말 · 메모)
#   쌓기: narr_pick.py 가 녹음마다 받아쓰기와 자막을 맞춰 보고, 어긋난 낱말을 자동으로 더한다(kind=stt)
#         사용자가 귀로 지적한 건 add 로 더한다(kind=user — 더 무겁게 본다)
#   쓰기: 녹음 전에 python pron_book.py check <narration\EP\script.txt>  (qa_clip ③-4 도 부른다)
#
#   python pron_book.py check <script.txt>
#   python pron_book.py add <낱말> --heard 들린말 --fix 바꾼말 --note "메모"
#   python pron_book.py list
import os, re, sys, json, difflib, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.join(HERE, 'pron_book.json')

# 낱말이 아니라 꼴(패턴)로 걸리는 것 — 장부와 같이 본다
PATTERNS = [
    (r'(?<![가-힣])(?:사고|재고|가고|쓰고|타고|차고|자고)(?=[\s,.])', '짧은 동사 + -고 → 다른 낱말(사고=accident, 재고=창고 물건)로 들린다. 무엇을·어떻게를 붙여 풀기(6-1-2)'),
    (r'(?<![가-힣])[일이삼사오육칠팔구]?[십백]이(?:라고|야|에요|었어)', '숫자 끝 「이」 + 조사 → 「오십이라고」가 「50이라고」로 들린다. 「오십이 눈금」처럼 숫자 뒤에 낱말을 두기'),
    (r'[가-힣]+(?:얬|앴|옜)', '「하얬어」류 겹받침·이중모음 과거형 — 소리 엔진이 못 읽는다. 다른 말로'),
    # 모호한 말 — 뜻이 둘 이상이거나 기준이 안 보인다(6-1-2, 10/11 사용자: 「찾는 사람이 거의 없는」「재 보는 데」)
    (r'찾는 사람', '모호: 무슨 기준으로 「찾는」? → 「한 달 검색량 110」처럼 기준과 숫자로'),
    (r'(?<!늘려 )(?<!길이를 )(?<!무게를 )(?<![가-힣])재 ?(?:보|봤|볼)', '모호: 「재 보다」= 측정? 체험? → 「무게를 달아」「길이를 재」처럼 무엇을, 또는 「측정하는」'),
    (r'하늘이 열', '모호(비유): 「하늘이 열렸다」→ 「비가 그쳤다」「맑아졌다」'),
    (r'같은 날', '모호: 어느 날인지 → 「4일」처럼 날짜로'),
    (r'(?<![가-힣])숫자는', '모호: 무슨 숫자? → 「남은 좌석은」처럼 대상으로'),
    (r'출발편', '모호: 복귀편 이야기 중엔 출발편=어느 쪽? → 「가는 편」「오는 편」'),
    (r'읽어 줄', '모호(비유): 무엇을 읽어 주나 → 「작품 이야기를 들려줄」'),
]


def load():
    if os.path.exists(BOOK):
        return json.load(open(BOOK, encoding='utf-8'))
    return {'entries': {}}


def save(b):
    json.dump(b, open(BOOK, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


def _add(b, word, heard, kind, ep='', note='', fix=''):
    e = b['entries'].setdefault(word, {'heard': {}, 'count': 0, 'user': 0, 'fix': '', 'note': '', 'eps': [],
                                       'first': datetime.date.today().isoformat()})
    e['count'] += 1
    if kind == 'user':
        e['user'] += 1
    if heard:
        e['heard'][heard] = e['heard'].get(heard, 0) + 1
    if fix:
        e['fix'] = fix
    if note:
        e['note'] = note
    if ep and ep not in e['eps']:
        e['eps'].append(ep)


NORM = lambda s: re.sub(r'[\s,.?!·~「」"\'()]', '', s)


def log_mismatch(cap, heard, ep=''):
    """자막(cap)과 받아쓰기(heard)를 글자로 맞춰 보고, 어긋난 곳이 걸친 자막 낱말을 장부에 더한다."""
    words = cap.split()
    spans, pos = [], 0
    for w in words:
        n = len(NORM(w)); spans.append((pos, pos + n, w)); pos += n
    a, h = NORM(cap), NORM(heard)
    b = load(); got = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, h, autojunk=False).get_opcodes():
        if op == 'equal':
            continue
        hit = [s for s in spans if s[0] < max(i2, i1 + 1) and s[1] > i1]
        if not hit:
            continue
        w0, w1 = hit[0][0], hit[-1][1]
        word = ' '.join(re.sub(r'[,.?!「」]', '', s[2]) for s in hit)
        if len(hit) == 1:
            import repeat_check   # 「대영박물관은」→「대영박물관」: 조사를 떼야 다른 대본에서도 걸린다
            word = repeat_check.stem(word) or word
        if re.fullmatch(r'[\d.,%~a-zA-Z ]+', NORM(word)):
            continue   # 숫자·영문 꼴 차이는 받아쓰기 표기 문제
        hd = h[max(0, j1 - (i1 - w0)):j2 + (w1 - i2)]
        if NORM(word) == hd or len(NORM(word)) < 2 or re.fullmatch(r'[\d.,%~]+\w?', hd or '0'):
            continue   # 한 글자 낱말(줄맞춤 오차)·한글 수사→아라비아 숫자(「두」→2)는 받아쓰기 표기라 빼다
        _add(b, word, hd, 'stt', ep); got.append((word, hd))
    save(b)
    return got


def check(lines, min_count=1):
    """대본 줄마다 장부 낱말·꼴이 있으면 경고 [(줄, 낱말, 들린 말, 바꾼 말·메모)]."""
    b = load()['entries']; out = []
    for n, line in enumerate(lines):
        for w, e in b.items():
            hit = re.search(r'(?<![가-힣])' + re.escape(w), line) if len(w) <= 2 else (w in line)   # 「택」이 「주택」에 걸리지 않게(10/11)
            if (e['count'] >= min_count or e['user']) and hit:
                heard = ', '.join('%s×%d' % kv for kv in sorted(e['heard'].items(), key=lambda kv: -kv[1])[:3])
                tip = ' → '.join(x for x in [e.get('fix', ''), e.get('note', '')] if x)
                out.append((n, w, heard, ('사용자 지적 ' if e['user'] else '') + '%d회' % e['count'] + (' · ' + tip if tip else '')))
        for rx, msg in PATTERNS:
            for mm in re.finditer(rx, line):
                out.append((n, mm.group(0), '', msg))
    return out


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'list'
    if cmd == 'check':
        lines = [l.strip() for l in open(sys.argv[2], encoding='utf-8') if l.strip()]
        res = check(lines)
        for n, w, heard, tip in res:
            print('n%02d  「%s」%s  %s' % (n, w, ('  들린 말: ' + heard) if heard else '', tip))
        print('발음 주의 %d건' % len(res))
    elif cmd == 'add':
        a = sys.argv[2:]; word = a[0]
        get = lambda k: a[a.index(k) + 1] if k in a else ''
        b = load(); _add(b, word, get('--heard'), 'user', get('--ep'), get('--note'), get('--fix')); save(b)
        print('더함:', word)
    else:
        for w, e in sorted(load()['entries'].items(), key=lambda kv: (-kv[1]['user'], -kv[1]['count'])):
            print('%-12s %2d회%s  들린: %s  %s %s' % (w, e['count'], '(사용자)' if e['user'] else '',
                  ', '.join(e['heard']), e.get('fix', ''), e.get('note', '')))
