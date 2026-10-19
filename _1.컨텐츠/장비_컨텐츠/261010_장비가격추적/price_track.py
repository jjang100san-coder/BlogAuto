# -*- coding: utf-8 -*-
"""다나와 가격 매일 기록 — 캠프라인 등산화 10 + 미즈노 풋살화 10 (2026-10-10 ~ 2026-11-30)

상품 페이지(prod.danawa.com/info/?pcode=)의 구조화 데이터(ld+json AggregateOffer)에서
최저가(lowPrice)와 판매처 수(offerCount)를 읽어 price_log.csv 에 한 줄씩 쌓는다.
다나와 robots.txt 의 Crawl-delay 10 을 지켜 요청 사이 11초를 쉰다. 하루 1회만 돈다.
"""
import csv, json, re, sys, time, datetime as dt, urllib.request as ur
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOG = HERE / "price_log.csv"
RUNLOG = HERE / "price_track_run.log"
END = dt.date(2026, 11, 30)
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

ITEMS = json.loads((HERE / "items.json").read_text(encoding="utf-8"))


def log(msg):
    line = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + msg
    with RUNLOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line, flush=True)


def fetch(pcode):
    url = "https://prod.danawa.com/info/?pcode=%s" % pcode
    t = ur.urlopen(ur.Request(url, headers=UA), timeout=30).read().decode("utf-8", "replace")
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
        s = m.group(1)
        if '"AggregateOffer"' not in s and '"offers"' not in s:
            continue
        name = re.search(r'"name"\s*:\s*"([^"]+)"', s)
        low = re.search(r'"lowPrice"\s*:\s*"?(\d+)', s)
        cnt = re.search(r'"offerCount"\s*:\s*"?(\d+)', s)
        return (name.group(1) if name else ""), (int(low.group(1)) if low else None), (int(cnt.group(1)) if cnt else None)
    return "", None, None


def main():
    today = dt.date.today()
    if today > END and "--force" not in sys.argv:
        log("END 기간 종료(%s) — 실행하지 않음" % END)
        return
    if LOG.exists() and "--force" not in sys.argv:
        with LOG.open(encoding="utf-8-sig") as f:
            if any(r.get("date") == today.isoformat() for r in csv.DictReader(f)):
                log("SKIP 오늘(%s) 기록이 이미 있음" % today)
                return
    new = not LOG.exists()
    ok = bad = 0
    with LOG.open("a", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["date", "time", "group", "pcode", "label", "size", "danawa_name", "low_price", "offer_count", "my_price"])
        for i, it in enumerate(ITEMS):
            if i:
                time.sleep(11)
            try:
                name, low, cnt = fetch(it["pcode"])
                w.writerow([today.isoformat(), dt.datetime.now().strftime("%H:%M"), it["group"], it["pcode"],
                            it["label"], it.get("size", ""), name, low if low is not None else "", cnt if cnt is not None else "",
                            it.get("my_price", "")])
                f.flush()
                ok += 1 if low is not None else 0
                bad += 0 if low is not None else 1
            except Exception as e:
                bad += 1
                log("ERR %s %s %s" % (it["pcode"], it["label"], str(e)[:120]))
    log("DONE %s 성공 %d / 실패 %d" % (today, ok, bad))
    notify(today, ok, bad)


def summary(today, ok, bad):
    """카톡 한 통(200자) — 성공 수, 내 장비 3개 오늘가, 전날보다 바뀐 상품."""
    with LOG.open(encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    days = sorted({r["date"] for r in rows})
    cur = {r["pcode"]: r for r in rows if r["date"] == today.isoformat()}
    prev = {r["pcode"]: r for r in rows if len(days) > 1 and r["date"] == days[-2]}
    head = "✅ 다나와 가격 기록 %d/%d %d/%d" % (today.month, today.day, ok, ok + bad)
    if bad:
        head += " ⚠️실패 %d" % bad
    mine = []
    for it in ITEMS:
        r = cur.get(it["pcode"])
        if it.get("my_price") and r and r["low_price"]:
            short = it.get("short") or it["label"][:8]
            mine.append("%s %s(산 %s)" % (short, format(int(r["low_price"]), ","), format(int(it["my_price"]), ",")))
    moved = []
    for pc, r in cur.items():
        p = prev.get(pc)
        if p and r["low_price"] and p["low_price"] and r["low_price"] != p["low_price"]:
            d = int(r["low_price"]) - int(p["low_price"])
            moved.append("%s %s%s" % (r["label"].split(" (")[0][:8], "+" if d > 0 else "", format(d, ",")))
    lines = [head, "내 것: " + " · ".join(mine)]
    lines.append(("변동 %d: " % len(moved) + " · ".join(moved[:4])) if moved else ("변동 없음" if prev else "첫 기록"))
    lines.append("~11/30 매일 09시")
    return "\n".join(lines)[:200]


def notify(today, ok, bad):
    try:
        sys.path.insert(0, r"C:\Users\user\Desktop\자동화\블로그용\발행판")
        import kakao_send
        text = summary(today, ok, bad)
        r = kakao_send.send(kakao_send.access_token(kakao_send.load()), text)
        log("KAKAO %s" % ("SENT" if r.get("result_code") == 0 else "FAIL " + json.dumps(r, ensure_ascii=False)[:120]))
    except BaseException as e:          # 카톡이 실패해도 기록은 남아 있다
        log("KAKAO ERR %s" % str(e)[:150])


if __name__ == "__main__":
    main()
