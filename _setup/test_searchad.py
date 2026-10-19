"""네이버 검색광고 API 실연동 확인. 저장된 설정을 그대로 쓰고 키 값은 출력하지 않는다."""
import json
import sys
from pathlib import Path

sys.path.insert(0, r"C:\Users\user\Desktop\Blog\키워드레이더")
import searchad as SA  # noqa: E402

conf = SA.load_conf()
print("설정 상태:", "준비됨" if SA.conf_ready(conf) else "미완성")
print("  api_key  :", "있음" if conf["api_key"] else "없음")
print("  secret   :", "있음" if conf["secret"] else "없음")
print("  customer :", conf["customer"])

if not SA.conf_ready(conf):
    sys.exit("설정이 비어 있어 호출하지 않습니다.")

print("\n검색광고 keywordstool 실호출 …")
rows = SA.call_keywordstool(conf, ["싱가포르여행"])
print("연관 키워드 %d개 수신\n" % len(rows))

print("%-20s %10s %10s" % ("키워드", "PC검색", "모바일검색"))
for r in rows[:8]:
    print("%-20s %10s %10s" % (r.get("relKeyword"),
                               r.get("monthlyPcQcCnt"),
                               r.get("monthlyMobileQcCnt")))

# settings.json 의 AI 공급자도 같이 확인
sp = Path(__import__("os").environ["LOCALAPPDATA"]) / "ContentTrendRadar" / "settings.json"
if sp.exists():
    s = json.loads(sp.read_text(encoding="utf-8"))
    print("\nAI 공급자 :", s.get("ai_provider"))
    print("AI 모델   :", s.get("ai_model"))
    print("AI 키     :", "있음" if s.get("ai_key") else "없음")
