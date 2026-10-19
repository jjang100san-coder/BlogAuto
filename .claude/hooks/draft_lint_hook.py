# -*- coding: utf-8 -*-
"""PostToolUse(Write|Edit) 훅 — 초안 md 를 저장할 때마다 draft_lint.py 를 돌려 ❌ 면 Claude 에게 되돌린다 (마스터 2-11)."""
import json, os, re, subprocess, sys
try:
    data = json.loads(sys.stdin.buffer.read().decode("utf-8", "replace") or "{}")
except Exception:
    sys.exit(0)
f = (data.get("tool_input") or {}).get("file_path") or (data.get("tool_response") or {}).get("filePath") or ""
name = os.path.basename(f)
if not f.lower().endswith(".md") or "_템플릿" in f or not re.search(r"(_draft|^draft_|^초안_)", name, re.I):
    sys.exit(0)
LINT = r"C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\draft_lint.py"
env = dict(os.environ, PYTHONIOENCODING="utf-8")
r = subprocess.run([sys.executable, LINT, f], capture_output=True, env=env)
out = (r.stdout + r.stderr).decode("utf-8", "replace").strip()
if r.returncode != 0:
    sys.stderr.buffer.write(("[draft_lint ❌ — 마스터 2-11 강제 검사] 고치기 전엔 초안이 끝난 게 아니다(fill_editor 도 막힌다).\n" + out + "\n").encode("utf-8"))
    sys.exit(2)
if "⚠" in out:
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": "[draft_lint 경고]\n" + out}}, ensure_ascii=False))
sys.exit(0)
