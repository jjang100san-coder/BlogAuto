"""09-17 재구현분 검증 - 실제 API 를 부르지 않고 폴백 경로만 확인한다."""
import sys
import types
from argparse import Namespace
from pathlib import Path

SKILL = Path.home() / ".claude" / "skills" / "claude-watch-kr" / "scripts"
sys.path.insert(0, str(SKILL))
import bridge_engine as b  # noqa: E402

OUT = Path(__file__).resolve().parent / "_t"
URL = "https://www.youtube.com/watch?v=tpoV4u_fd3s"

FAKE_TRANSCRIPT = {"segments": [{"start": 0, "end": 600, "text": "ㄱ"}]}


def args(**kw):
    base = dict(capture=URL, out=str(OUT), max_frames=24,
                dry_run=True, no_gemini=False)
    base.update(kw)
    return Namespace(**base)


def run(name, expect, *, transcript, gemini, no_gemini=False):
    b.fetch_transcript = (lambda *a, **k: transcript) if transcript else \
        _raiser("자막 서버 500")
    b.analyze_video_gemini = (lambda *a, **k: gemini) if gemini else \
        _raiser("HTTP 429: quota exceeded")
    b._load_keys = lambda: ("fake-gemini", "fake-yep")
    code = b.capture_cli(args(no_gemini=no_gemini))
    ok = "PASS" if code == expect else "FAIL"
    print("[%s] %s  (exit=%s, 기대=%s)" % (ok, name, code, expect))
    return ok == "PASS"


def _raiser(msg):
    def f(*a, **k):
        raise RuntimeError(msg)
    return f


results = []

print("--- 1. Gemini 429 -> 그리드 폴백 (죽지 않아야 한다) ---")
results.append(run("Gemini 실패시 그리드 폴백", b.EXIT_OK,
                   transcript=FAKE_TRANSCRIPT, gemini=None))

print("\n--- 2. 자막 없음 + Gemini 없음 -> 유료 호출 전 중단 ---")
results.append(run("길이 추정 실패시 중단", b.EXIT_UNAVAILABLE,
                   transcript=None, gemini=None, no_gemini=True))

print("\n--- 3. 자막 없음 + Gemini 있음 -> Gemini 길이로 진행 ---")
results.append(run("자막만 없을 때는 진행", b.EXIT_OK, transcript=None,
                   gemini={"captures": [{"timestamp_seconds": 300,
                                         "importance": 90,
                                         "category": "chart",
                                         "reason": "표"}],
                           "summary": "요약"}))

print("\n--- 4. analysis.json 조건부 저장 ---")
OUT.mkdir(parents=True, exist_ok=True)
stale = OUT / "analysis.json"
stale.write_text("{}", encoding="utf-8")
stale.unlink()
b.fetch_transcript = lambda *a, **k: FAKE_TRANSCRIPT
b.analyze_video_gemini = _raiser("429")
b._load_keys = lambda: ("fake-gemini", "")  # yep 키 없음 -> 프레임 건너뜀
b.capture_cli(args(dry_run=False, max_frames=6))
man = __import__("json").loads((OUT / "manifest.json").read_text(encoding="utf-8"))
no_file = not stale.exists()
zero = man["api_calls"]["gemini"] == 0
deg = "gemini" in man["degraded"]
print("[%s] analysis.json 미생성        (%s)" % ("PASS" if no_file else "FAIL", no_file))
print("[%s] api_calls.gemini == 0       (%s)" % ("PASS" if zero else "FAIL", man["api_calls"]))
print("[%s] degraded 에 gemini 기록      (%s)" % ("PASS" if deg else "FAIL", man["degraded"]))
results += [no_file, zero, deg]

print("\n%d/%d PASS" % (sum(1 for r in results if r in (True, "PASS")), len(results)))
sys.exit(0 if all(r in (True, "PASS") for r in results) else 1)
