import re_common as C
K = C.datago_key_q()
pts = ["202210","202304","202310","202404","202410","202504","202510","202604","202609"]
def pop(stdg, ym, lv):
    u = (f"https://apis.data.go.kr/1741000/stdgPpltnHhStus/selectStdgPpltnHhStus?serviceKey={K}&stdgCd={stdg}"
         f"&srchFrYm={ym}&srchToYm={ym}&lv={lv}&regSeCd=1&type=JSON&numOfRows=1000&pageNo=1")
    d = C.get_json(u, timeout=120)["Response"]; it = (d.get("items") or {}).get("item") or []
    return it if isinstance(it, list) else [it]
