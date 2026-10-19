# -*- coding: utf-8 -*-
"""블로그 통계 「조회수 순위」 엑셀 → 글 유형별 합·중앙값. 유형은 제목 규칙으로 나눈다(위에서부터 먼저 맞는 것)."""
import openpyxl, sys, statistics as st, warnings
warnings.filterwarnings("ignore"); sys.stdout.reconfigure(encoding="utf-8")
RULES = [
 ("블로그연대기", ["애드포스트", "유입경로"]),
 ("해 봤더니(절차·생활)", ["대한항공 통합", "가족 등록", "가격 협상", "퇴직연금", "민음사빵", "특약", "임장", "토지거래", "한정선", "상견례", "마운자로", "코딩", "내집마련"]),
 ("마일리지 측정", ["마일리지"]),  # 경비 글은 아래 규칙보다 먼저 걸러짐 ↓
 ("등산 장비 실패담", ["등산화", "배낭", "밴티지"]),
 ("등산 코스·산 찾기", ["등산코스", "산 찾기", "퇴근 후 등산"]),
 ("축구 결과·기타", ["결과", "후기, 골은", "찜찜", "모레노 감독", "토트넘", "0-0", "1-4"]),
 ("축구 프리뷰", ["전망", "명단", "일정", "중계", "8강 한국 vs", "카타르전 9월 15일 저녁"]),
 ("농구 선수", ["프로필"]),
 ("책", ["줄거리", "요약 후기", "달리기를 말할", "노벨문학상", "문학동네"]),
 ("국내 맛집", ["담가화로"]),
 ("경제·환율·부동산", ["환전", "아파트값"]),
 ("국내 축제·계절·나들이", ["축제", "문화제", "꽃별", "단풍 절정", "화담숲", "세미원", "경주 1박", "니지모리"]),
 ("연예·기타", ["심수봉"]),
]
def kind(t):
    if "경비" in t: return "해외여행기·숙소·경비"
    for k, ws in RULES:
        if any(w in t for w in ws): return k
    return "해외여행기·숙소·경비"
def load(p):
    ws = openpyxl.load_workbook(p).active
    return [(r[1], int(r[2]), r[3][:10]) for r in ws.iter_rows(values_only=True) if r[0] and str(r[0]).isdigit()]
def summary(rows, new_from):
    g = {}
    for t, v, d in rows: g.setdefault(kind(t), []).append((v, d, t))
    tot = sum(v for _, v, _ in rows); out = []
    for k, xs in g.items():
        vs = [v for v, _, _ in xs]; top = max(xs)
        out.append((sum(vs), k, len(vs), st.median(vs), sum(v >= 20 for v in vs), sum(d >= new_from for _, d, _ in xs), top[2].split("|")[0].strip()[:20], top[0]))
    return tot, sorted(out, reverse=True)
if __name__ == "__main__":
    for p, nf in zip(sys.argv[1::2], sys.argv[2::2]):
        tot, out = summary(load(p), nf); print(f"\n## {p.split(chr(92))[-1][:30]}  합계 {tot}")
        for s, k, n, md, g20, nw, tt, tv in out:
            print(f"{k:14s} 편{n:3d} 합{s:5d}({s*100/tot:4.1f}%) 중앙{md:6.1f} 20↑{g20:2d} 기간내발행{nw:2d} 최고:{tt} {tv}")
    if "-v" in sys.argv: pass
