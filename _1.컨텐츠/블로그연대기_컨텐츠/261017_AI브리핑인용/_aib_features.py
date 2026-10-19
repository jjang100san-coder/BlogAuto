# -*- coding: utf-8 -*-
r"""AI 브리핑 출처(인용) 블로그 글 vs 같은 검색어 상위 블로그 글(미인용) 본문 특징 비교 (2026-10-17).
레이더 판정(reviewdata.classify_post) 포함. 본문은 스크래치에만 저장, 결과엔 블로거 이름 없이 집계만.
사용: python _aib_features.py <aib.json> <bodies 저장.json> <집계 출력.json>"""
import sys, json, io, re, time, statistics as st, collections, urllib.request as ur
sys.path.insert(0, r"C:\Users\user\Desktop\자동화\블로그용\Keyword_Reader")
sys.stdout.reconfigure(encoding="utf-8")
import reviewdata as R
A = json.load(open(sys.argv[1], encoding="utf-8")); BODY, OUT = sys.argv[2], sys.argv[3]
UA = "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Mobile Safari/537.36"
try: B = json.load(open(BODY, encoding="utf-8"))
except Exception: B = {}
jobs = []
for row in A:
    if not row.get("ai"): continue
    cited = row["src_blogs"]
    for k in cited: jobs.append((row["q"], k, "인용"))
    for k in row["org_blogs"][:10]:
        if k not in cited: jobs.append((row["q"], k, "미인용"))
for i, (q, k, g) in enumerate(jobs):
    if k in B: continue
    try:
        h = ur.urlopen(ur.Request("https://m.blog.naver.com/" + k, headers={"User-Agent": UA}), timeout=20).read().decode("utf-8", "replace")
        t = R.extract_post_text(h); lab, why = R.classify_post(t, h)
        seg = h[h.find("se-main-container"):] if "se-main-container" in h else h
        m = re.search(r"(\d{4})\.\s?(\d{1,2})\.\s?(\d{1,2})\.\s?\d{1,2}:\d{2}", h)
        ti = re.search(r'og:title" content="([^"]+)"', h)
        heads = [re.sub(r"<[^>]+>", "", x).strip() for x in re.findall(r'se-section-sectionTitle.*?<p[^>]*>(.*?)</p>', seg, re.S)]
        B[k] = dict(text=t[:30000], label=lab, title=ti.group(1) if ti else "", date="%s-%02d-%02d" % (m.group(1), int(m.group(2)), int(m.group(3))) if m else "",
                    img=seg.count("se-image-resource"), table=seg.count('class="se-table'), heads=heads[:40], quote=seg.count("se-quotation"),
                    video=bool(re.search(r"se-module-video|se-video", seg)), map=bool(re.search(r"se-module-map|se-placesMap", seg)), oglink=seg.count("se-module-oglink"))
    except Exception as e:
        B[k] = dict(err=str(e)[:60])
    if i % 40 == 0: json.dump(B, io.open(BODY, "w", encoding="utf-8"), ensure_ascii=False); print(i, len(jobs), flush=True)
    time.sleep(0.4)
json.dump(B, io.open(BODY, "w", encoding="utf-8"), ensure_ascii=False)

def words(q): return [w for w in re.split(r"\s+", q) if w]
def ngrams(s, n=6): s = re.sub(r"\s+", "", s); return {s[i:i+n] for i in range(len(s) - n + 1)}
def feat(q, k, brief):
    v = B.get(k, {});  t = v.get("text", "")
    if not t: return None
    ws = words(q); title = v["title"]
    first = t[:300]
    qhead = sum(1 for h in v["heads"] if h.endswith("?") or re.search(r"(나요|까요|뭔가요|인가요|할까|언제|어디|얼마|방법)", h))
    nums = len(re.findall(r"\d[\d,\.]*\s*(원|엔|달러|%|분|시간|km|kg|cm|mm|개|명|편|장|일|월|년|시)", t))
    # 브리핑 문장과 겹친 6글자 조각이 본문 어디에 몰렸나(앞 1/3·중간·뒤)
    bg = ngrams(brief); pos = []
    ts = re.sub(r"\s+", "", t)
    for i in range(0, max(0, len(ts) - 6), 3):
        if ts[i:i+6] in bg: pos.append(i / max(1, len(ts)))
    return dict(chars=len(t), title_has_all=all(w.lower() in title.lower() for w in ws), title_starts=title.replace(" ", "").lower().startswith(q.replace(" ", "").lower()),
                first_has_all=all(w.lower() in first.lower() for w in ws), heads=len(v["heads"]), qheads=qhead, table=v["table"], img=v["img"], nums=nums,
                nums_per_1k=round(nums * 1000 / max(1, len(t)), 1), label=v["label"], video=v["video"], map=v["map"], date=v["date"],
                overlap=len(pos), overlap_front=sum(1 for p in pos if p < 1/3), overlap_mid=sum(1 for p in pos if 1/3 <= p < 2/3), overlap_back=sum(1 for p in pos if p >= 2/3))
rows = []
for row in A:
    if not row.get("ai"): continue
    for k in row["src_blogs"]:
        f = feat(row["q"], k, row["brief"]);  f and rows.append(dict(q=row["q"], kind=row["kind"], g="인용", mine=k.startswith("baiyan_novembre/"), **f))
    for r_, k in enumerate(row["org_blogs"][:10], 1):
        if k in row["src_blogs"]: continue
        f = feat(row["q"], k, row["brief"]);  f and rows.append(dict(q=row["q"], kind=row["kind"], g="미인용", rank=r_, mine=k.startswith("baiyan_novembre/"), **f))
S = {"검색어": len(A), "AI 브리핑 뜸": sum(bool(r.get("ai")) for r in A), "내 글 인용": sum(bool(r.get("cited_mine")) for r in A),
     "브리핑 출처 블로그": sum(len(r.get("src_blogs", [])) for r in A if r.get("ai")), "브리핑 출처 블로그 밖": sum(len(r.get("src_other", [])) for r in A if r.get("ai"))}
def summ(xs):
    if not xs: return {}
    med = lambda key: st.median(x[key] for x in xs)
    cnt = lambda fn: sum(1 for x in xs if fn(x))
    return {"글": len(xs), "글자 중앙값": med("chars"), "사진 중앙값": med("img"), "소제목 중앙값": med("heads"), "질문꼴 소제목 있는 글": cnt(lambda x: x["qheads"] > 0),
            "표 있는 글": cnt(lambda x: x["table"] > 0), "숫자+단위 1천자당 중앙값": med("nums_per_1k"), "제목에 검색어 낱말 전부": cnt(lambda x: x["title_has_all"]),
            "제목이 검색어로 시작": cnt(lambda x: x["title_starts"]), "첫 300자에 검색어 낱말 전부": cnt(lambda x: x["first_has_all"]),
            "체험단·협찬": cnt(lambda x: x["label"] == "ad"), "내돈내산": cnt(lambda x: x["label"] == "self"), "영상": cnt(lambda x: x["video"]), "지도": cnt(lambda x: x["map"]),
            "2026년 9월 이후 글": cnt(lambda x: x["date"] >= "2026-09"), "2026년 글": cnt(lambda x: x["date"] >= "2026"),
            "브리핑과 겹친 조각 중앙값": med("overlap"), "겹친 조각 앞/중/뒤 합": [sum(x["overlap_front"] for x in xs), sum(x["overlap_mid"] for x in xs), sum(x["overlap_back"] for x in xs)]}
S["인용"] = summ([r for r in rows if r["g"] == "인용"]); S["미인용(상위 10 중)"] = summ([r for r in rows if r["g"] == "미인용"])
S["내 글(미인용)"] = [dict(q=r["q"], rank=r.get("rank"), chars=r["chars"], heads=r["heads"], qheads=r["qheads"], table=r["table"], title_starts=r["title_starts"]) for r in rows if r["mine"]]
S["검색어별"] = [dict(q=r["q"], kind=r["kind"], ai=r.get("ai"), 블로그출처=len(r.get("src_blogs", [])), 그밖출처=len(r.get("src_other", [])), 내순위=r.get("mine_rank")) for r in A]
json.dump(dict(summary=S, rows=rows), io.open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(S, ensure_ascii=False, indent=1))
