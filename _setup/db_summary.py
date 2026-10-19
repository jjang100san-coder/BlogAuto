import sqlite3
import sys

db = sys.argv[1]
c = sqlite3.connect(db)
rows = c.execute(
    "select name from sqlite_master where type='table' order by name"
).fetchall()
for (t,) in rows:
    n = c.execute("select count(*) from [%s]" % t).fetchone()[0]
    print("%-22s %7d rows" % (t, n))

try:
    lo, hi, n = c.execute(
        "select min(depart_date), max(depart_date), count(distinct depart_date) from award"
    ).fetchone()
    print("\n수집 날짜 범위: %s ~ %s  (%s일)" % (lo, hi, n))
except Exception as e:
    print("\n(award 테이블 조회 불가: %s)" % e)
