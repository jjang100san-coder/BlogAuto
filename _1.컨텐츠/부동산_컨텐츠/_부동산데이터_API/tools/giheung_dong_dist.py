# -*- coding: utf-8 -*-
"""기흥구 법정동별 「수원 영통구까지 거리」 — 브이월드 경계(읍면동 LT_C_ADEMD_INFO·시군구 LT_C_ADSIGG_INFO).
거리 = 법정동 경계 중심점 → 영통구 경계(가장 가까운 꼭짓점) 직선 거리(km). 영통구와 맞닿으면 0에 가깝다.
결과: _giheung_dong_dist.json (동 이름·중심 좌표·거리·영통과 맞닿음 여부). 단지 정보는 없다."""
import json, math, os, sys, urllib.request, urllib.parse
sys.path.insert(0, r"C:\Users\user\Desktop\자동화\블로그용\Keyword_Reader")
from radar.core.store import load_settings
_S = load_settings(); KEY = _S["vworld_key"]; DOM = _S.get("vworld_domain") or "localhost"
HERE = os.path.dirname(os.path.abspath(__file__))


def feats(data, flt):
    q = dict(service="data", request="GetFeature", data=data, key=KEY, format="json", size="100",
             geometry="true", attribute="true", crs="EPSG:4326", attrFilter=flt, domain=DOM)
    u = "https://api.vworld.kr/req/data?" + urllib.parse.urlencode(q)
    d = json.loads(urllib.request.urlopen(u, timeout=60).read().decode("utf-8"))
    st = d["response"]["status"]
    if st != "OK": raise SystemExit(f"{data} {flt} → {st} {d['response'].get('error')}")
    return d["response"]["result"]["featureCollection"]["features"]


def rings(geom):
    t, c = geom["type"], geom["coordinates"]
    polys = [c] if t == "Polygon" else c
    return [ring for poly in polys for ring in poly]


def km(a, b):
    lon1, lat1 = a; lon2, lat2 = b
    x = (lon2 - lon1) * math.cos(math.radians((lat1 + lat2) / 2)) * 111.32
    y = (lat2 - lat1) * 110.57
    return math.hypot(x, y)


yt = feats("LT_C_ADSIGG_INFO", "sig_cd:=:41117")
ypts = [p for f in yt for r in rings(f["geometry"]) for p in r]
emd = feats("LT_C_ADEMD_INFO", "emd_cd:like:41463")
out = []
for f in emd:
    pts = [p for r in rings(f["geometry"]) for p in r]
    cx = sum(p[0] for p in pts) / len(pts); cy = sum(p[1] for p in pts) / len(pts)
    dmin_edge = min(km(p, q) for p in pts[::3] for q in ypts[::3])      # 경계끼리 최소 거리(맞닿음 판정)
    dcen = min(km((cx, cy), q) for q in ypts)                            # 중심 → 영통 경계
    out.append(dict(dong=f["properties"].get("emd_kor_nm"), code=f["properties"].get("emd_cd"),
                    center=[round(cx, 5), round(cy, 5)], km_center_to_yeongtong=round(dcen, 2),
                    touches=dmin_edge < 0.15))
out.sort(key=lambda r: r["km_center_to_yeongtong"])
for r in out: print(r)
json.dump(out, open(os.path.join(HERE, "_giheung_dong_dist.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
