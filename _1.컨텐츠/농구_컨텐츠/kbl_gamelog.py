# -*- coding: utf-8 -*-
r"""KBL 선수 경기별 기록 받기 — 농구 지침 5장(2026-10-18).

KBL 홈페이지 「경기별」 탭이 부르는 주소를 그대로 쓴다(브라우저 없이 curl·urllib 로 받아짐, 10/18 확인).
  경기별: https://kbl-api.sports2i.com/api/v1/players/categories/game/<시즌>/48/<선수번호>
  평균  : https://kbl-api.sports2i.com/api/v1/players/categories/avg/<시즌>/<선수번호>
  팀 이름: https://kbl-api.sports2i.com/api/v1/code/codes/1  (seasonCode 로 거름)
시즌 49 = 2026-27 정규리그.

쓰기:
  python kbl_gamelog.py 291375 291667 --since 20261018
  → 화면에 경기 표(마크다운)와 KBL 경기당 평균, _kbl_gamelog\<오늘>_<선수번호>.json 저장.
평균은 KBL 이 낸 값을 그대로 옮긴다(계산하지 않음, 마스터 0-4).
"""
import argparse, datetime, json, os, sys, urllib.request

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "_kbl_gamelog")
API = "https://kbl-api.sports2i.com/api/v1"
HDR = {"Referer": "https://www.kbl.or.kr/", "Origin": "https://www.kbl.or.kr", "User-Agent": "Mozilla/5.0"}
NAMES = {"291220": "변준형", "291375": "이우석", "291857": "문유현", "291667": "문정현", "290993": "최준용", "291846": "에디 다니엘", "290787": "이승현"}
WEEK = "월화수목금토일"


def get(url):
    req = urllib.request.Request(url, headers=HDR)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def teams(season):
    d = get(f"{API}/code/codes/1")
    rows = d.get("data", d) if isinstance(d, dict) else d
    return {t["teamCode"]: t["teamName2"] for t in rows if t.get("seasonCode") == season}


def mmss(sec):
    return f"{sec // 60}:{sec % 60:02d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("players", nargs="+")
    ap.add_argument("--season", type=int, default=49)
    ap.add_argument("--since", default="")
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    tm = teams(a.season)
    today = datetime.date.today().strftime("%Y%m%d")
    for pno in a.players:
        g = get(f"{API}/players/categories/game/{a.season}/48/{pno}")
        games = sorted(g.get("RegularGameRecords", []), key=lambda x: x["gameDate"])
        avg = {r["columnName"]: r["columnValue"] for r in get(f"{API}/players/categories/avg/{a.season}/{pno}")}
        json.dump({"games": games, "avg": avg, "teams": tm}, open(os.path.join(OUT, f"{today}_{pno}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        name = NAMES.get(pno, pno)
        print(f"\n## {name} ({pno}) — {a.season}시즌 정규리그 {len(games)}경기")
        print("| 날짜 | 소속 | 상대 | 결과 | 출전 | 득점 | 리바운드 | 어시스트 | 스틸 | 3점 | +/- | DD |")
        print("|---|---|---|---|---|---|---|---|---|---|---|---|")
        for x in games:
            if a.since and x["gameDate"] < a.since:
                continue
            dt = datetime.datetime.strptime(x["gameDate"], "%Y%m%d").date()
            res = ("승" if x["win"] else "패" if x["loss"] else "무") + f" {x['score']}-{x['awayScore']}"
            print(f"| {dt.month}.{dt.day}({WEEK[dt.weekday()]}) | {tm.get(x['teamCode'], x['teamCode'])} | {tm.get(x['awayTeam'], x['awayTeam'])} | {res} | {mmss(x['playSec'])} | {x['pts']} | {x['rb']} | {x['aS']} | {x['sT']} | {x['threep']}/{x['threepA']} | {x['margin']:+d} | {x['dd2']} |")
        keys = [("SCORE", "득점"), ("RB", "리바운드"), ("A_S", "어시스트"), ("S_T", "스틸")]
        have = [f"{lab} {float(avg[k]):.1f}" for k, lab in keys if k in avg]
        print(f"- KBL 경기당 평균: {' · '.join(have) if have else '(평균 항목 이름 확인 필요: ' + ', '.join(list(avg)[:12]) + ')'}")
        if a.since and not any(x["gameDate"] >= a.since for x in games):
            print(f"- ⏳ {a.since} 이후 경기가 아직 없다(경기 전이거나 기록 미반영)")


if __name__ == "__main__":
    main()
