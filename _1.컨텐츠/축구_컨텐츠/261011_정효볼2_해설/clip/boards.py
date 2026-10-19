# dots.json(개념도에서 뽑은 점) → 움직이는 전술판 장면. 왼쪽 칸(①) 배치에서 오른쪽 칸(②) 배치로 바뀐 점만 움직인다
import json, os, math
D = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dots.json'), encoding='utf-8'))


def morph(f, t0=0.8, t1=3.2):
    L, R = D[f]['L'], D[f]['R']
    players, moves = {}, []
    for team in ('kor', 'opp'):
        a = [p for p in L if p[0] == team]; b = [p for p in R if p[0] == team]
        used = set(); pairs = []
        for i, p in enumerate(a):   # 같은 자리 먼저
            for j, q in enumerate(b):
                if j not in used and math.dist(p[1:], q[1:]) < 0.02:
                    used.add(j); pairs.append((p, q)); break
            else:
                pairs.append((p, None))
        rest = [q for j, q in enumerate(b) if j not in used]
        for k, (p, q) in enumerate(pairs):   # 남은 건 가까운 것끼리
            if q is None and rest:
                q = min(rest, key=lambda r: math.dist(p[1:], r[1:])); rest.remove(q); pairs[k] = (p, q)
        for n, (p, q) in enumerate(pairs):
            pid = '%s%d' % (team, n)
            players[pid] = (team, p[1], p[2], None)
            if q and math.dist(p[1:], q[1:]) >= 0.02:
                moves.append((pid, t0, t1, (q[1], q[2])))
    return players, moves


def close_in(f, ball, t0=0.6, t1=2.6, push=0.09):
    """한 칸만 쓰는 장면 — 공 둘레 선수들이 바깥에서 공 쪽으로 좁혀 들어온다(역압박)."""
    players, moves = {}, []
    for n, p in enumerate(D[f]['L']):
        team, x, y = p
        pid = '%s%d' % (team, n)
        d = math.dist((x, y), ball)
        if team == 'kor' and d < 0.45:
            k = (d + push) / max(d, 1e-3)
            sx, sy = ball[0] + (x - ball[0]) * k, ball[1] + (y - ball[1]) * k
            players[pid] = (team, round(sx, 3), round(sy, 3), None); moves.append((pid, t0, t1, (x, y)))
        else:
            players[pid] = (team, x, y, None)
    return players, moves
