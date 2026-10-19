"""로그인 쿠키가 프로필에 저장됐는지만 본다. 값은 읽지 않는다(암호화돼 있고 필요도 없다)."""
import shutil
import sqlite3
import sys
import tempfile
from pathlib import Path

src = Path(sys.argv[1])
tmp = Path(tempfile.gettempdir()) / "cookies_readonly.db"
shutil.copy2(src, tmp)  # 크롬이 잠가 둘 수 있어 사본으로 연다

con = sqlite3.connect(tmp)
rows = con.execute(
    "select name, host_key, expires_utc from cookies where host_key like '%naver.com%'"
).fetchall()
con.close()
tmp.unlink(missing_ok=True)

names = {r[0] for r in rows}
need = {"NID_AUT", "NID_SES"}

print("naver.com 쿠키 %d개" % len(rows))
for n in sorted(need):
    print("  %-8s %s" % (n, "있음" if n in names else "없음"))
print("\n판정:", "로그인 상태" if need <= names else "로그인 안 됨")
sys.exit(0 if need <= names else 1)
