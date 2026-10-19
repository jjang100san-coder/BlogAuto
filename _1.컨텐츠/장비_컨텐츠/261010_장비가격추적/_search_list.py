import re, time, json, sys, urllib.request as ur, urllib.parse as up
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
def get(url):
    return ur.urlopen(ur.Request(url, headers=UA), timeout=25).read().decode("utf-8", "replace")
def search(q, page=1):
    t = get("https://search.danawa.com/dsearch.php?" + up.urlencode({"query": q}))
    items = list(re.finditer(r'id="productItem(\d+)"', t))
    out = []
    for i, m in enumerate(items):
        seg = t[m.start(): items[i+1].start() if i+1 < len(items) else m.start()+30000]
        n = re.search(r'class="prod_name">(.*?)</p>', seg, re.S)
        name = re.sub(r'<[^>]+>|\s+', ' ', n.group(1)).strip() if n else '?'
        name = re.sub(r'\s+', ' ', name)
        prices = re.findall(r'<strong>\s*([\d,]{4,})\s*</strong>', seg)
        spec = re.search(r'class="spec_list">(.*?)</div>', seg, re.S)
        spec = re.sub(r'<[^>]+>|\s+', ' ', spec.group(1)).strip()[:120] if spec else ''
        out.append({"pcode": m.group(1), "name": name, "price": prices[0] if prices else None, "spec": spec})
    return out
res = {}
for q in sys.argv[1:]:
    res[q] = search(q)
    time.sleep(11)
json.dump(res, open("_search_raw.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for q, rows in res.items():
    print("###", q, len(rows))
    for r in rows: print(" ", r["pcode"], r["price"], "|", r["name"][:70], "|", r["spec"][:70])
