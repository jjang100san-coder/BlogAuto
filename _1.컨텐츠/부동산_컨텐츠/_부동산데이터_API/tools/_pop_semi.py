import re_common as C, json, collections
K=C.datago_key_q()
pts=["202210","202304","202310","202404","202410","202504","202510","202604","202609"]
def pop(stdg,ym,lv):
    u=f"https://apis.data.go.kr/1741000/stdgPpltnHhStus/selectStdgPpltnHhStus?serviceKey={K}&stdgCd={stdg}&srchFrYm={ym}&srchToYm={ym}&lv={lv}&regSeCd=1&type=JSON&numOfRows=1000&pageNo=1"
    d=C.get_json(u,timeout=120)["Response"]; it=(d.get("items") or {}).get("item") or []
    return it if isinstance(it,list) else [it]
res=collections.defaultdict(dict)
for ym in pts:
    rows=pop("4159100000",ym,3)
    if not any(x.get("stdgNm")=="남양읍" for x in rows): rows=pop("4159000000",ym,3)   # 2026.2 이전은 옛 화성시 코드
    for x in rows:
        nm=x["stdgNm"]
        if nm in("남양읍","새솔동"):
            r=res[nm].setdefault(ym,[0,0]); r[0]+=int(x["totNmprCnt"]); r[1]+=int(x["hhCnt"])
    sw=[0,0]
    for g in C.SUWON:
        x=pop(g+"00000",ym,6)[0]; sw[0]+=int(x["totNmprCnt"]); sw[1]+=int(x["hhCnt"])
    res["수원 4개 구"][ym]=sw
    print(ym,{k:v.get(ym) for k,v in res.items()},flush=True)
json.dump(res,open("_pop_semi.json","w",encoding="utf-8"),ensure_ascii=False)
print("ALL DONE",flush=True)
