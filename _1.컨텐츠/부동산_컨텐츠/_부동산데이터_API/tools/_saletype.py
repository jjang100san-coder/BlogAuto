# -*- coding: utf-8 -*-
"""K-apt 단지 기본정보로 분양/임대/혼합 비중과 시행사(LH 등)를 본다 — 남양·새솔·수원 4개 구.
결과: _saletype.json (단지 이름은 내부 확인용, 블로그에는 집계만)"""
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import re_common as C

K = C.datago_key_q()
LIST = "https://apis.data.go.kr/1613000/AptListService4/getSigunguAptList4?ServiceKey={k}&sigunguCode={s}&pageNo={p}&numOfRows=100"
INFO = "https://apis.data.go.kr/1613000/AptBasisInfoServiceV5/getAphusBassInfoV5?ServiceKey={k}&kaptCode={c}"


def items(txt):
    d = json.loads(txt)
    body = d.get("response", {}).get("body", {})
    it = body.get("items") or []
    if isinstance(it, dict):
        it = it.get("item") or []
    return [it] if isinstance(it, dict) else it, int(body.get("totalCount") or 0)


def apt_list(sigungu):
    out, p = [], 1
    while True:
        it, tot = items(C.get(LIST.format(k=K, s=sigungu, p=p)))
        out += it
        if len(out) >= tot or not it:
            return out
        p += 1


def info(code):
    err = None
    for n in range(5):                      # 429 는 쉬었다가 다시 (간격을 점점 늘린다)
        time.sleep(1.0 + 10 * n)
        try:
            d = json.loads(C.get(INFO.format(k=K, c=code)))
            it = d.get("response", {}).get("body", {}).get("item")
            if it:
                return it
            err = "빈 응답"
        except Exception as e:
            err = str(e)
    return {"_err": err}


def main():
    groups = {"41591": None, "41111": "장안구", "41113": "권선구", "41115": "팔달구", "41117": "영통구"}
    res = {}
    args = sys.argv[1:]
    outname = None
    if "--out" in args:
        i = args.index("--out"); outname = args[i + 1]; del args[i:i + 2]
    for sg in (args or groups):
        lst = apt_list(sg)
        print(sg, "단지", len(lst), flush=True)
        with ThreadPoolExecutor(1) as ex:
            infos = list(ex.map(info, [a["kaptCode"] for a in lst]))
        rows = []
        for a, i in zip(lst, infos):
            rows.append(dict(code=a.get("kaptCode"), name=a.get("kaptName"), as3=a.get("as3"), as4=a.get("as4"), bjd=a.get("bjdCode"),
                             sale=i.get("codeSaleNm"), use=i.get("kaptUsedate"), hh=i.get("kaptdaCnt"), dong=i.get("kaptDongCnt"),
                             builder=i.get("kaptBcompany"), developer=i.get("kaptAcompany"), err=i.get("_err")))
        res[sg] = rows
    out = C.HERE / (outname or ("_saletype.json" if not args or args == ["41591"] else "_saletype_suwon.json"))
    out.write_text(json.dumps(res, ensure_ascii=False, indent=0), encoding="utf-8")
    print("DONE")


if __name__ == "__main__":
    main()
