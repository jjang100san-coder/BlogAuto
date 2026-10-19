import re_common as C, json, collections, os, time
K=C.datago_key_q()
months=C.months_back("202609",48)
cache="_pop_cache.json"; done=json.load(open(cache,encoding="utf-8")) if os.path.exists(cache) else {}
def pop(stdg,fr,to,lv):
    k=f"{stdg}_{fr}_{to}_{lv}"
    if k in done: return done[k]
    u=f"https://apis.data.go.kr/1741000/stdgPpltnHhStus/selectStdgPpltnHhStus?serviceKey={K}&stdgCd={stdg}&srchFrYm={fr}&srchToYm={to}&lv={lv}&regSeCd=1&type=JSON&numOfRows=1000&pageNo=1"
    d=C.get_json(u,timeout=90)["Response"]; it=(d.get("items") or {}).get("item") or []
    it=it if isinstance(it,list) else [it]
    it=[dict(stdgNm=x.get("stdgNm"),statsYm=x.get("statsYm"),pop=int(x.get("totNmprCnt") or 0),hh=int(x.get("hhCnt") or 0)) for x in it]
    done[k]=it; json.dump(done,open(cache,"w",encoding="utf-8"),ensure_ascii=False); return it
res=collections.defaultdict(dict)
for i in range(0,len(months),3):
    fr,to=months[i],months[min(i+2,len(months)-1)]
    for x in pop("4159100000",fr,to,3):
        if x["stdgNm"] in("남양읍","새솔동"):
            r=res[x["stdgNm"]].setdefault(x["statsYm"],[0,0]); r[0]+=x["pop"]; r[1]+=x["hh"]
    for g,n in C.SUWON.items():
        for x in pop(g+"00000",fr,to,6): res["수원"+n][x["statsYm"]]=[x["pop"],x["hh"]]
    print("window",fr,to,flush=True)
out={k:dict(sorted(v.items())) for k,v in res.items()}
json.dump(out,open("_pop_2210_2609.json","w",encoding="utf-8"),ensure_ascii=False)
print("ALL DONE",flush=True)
