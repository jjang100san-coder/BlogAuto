# 허브글 채우기 — 한글 경로를 인수로 넘기면 PowerShell 콘솔 코드페이지 때문에
# 깨질 때가 있다(2026-09-26 실측: _1.컨텐츠 -> _1.而⑦뀗痢? 로 망가져 FileNotFoundError).
# 경로를 이 파일 안에 UTF-8 BOM 으로 박아두고 실행한다.
$ErrorActionPreference = 'Continue'
$OutputEncoding = [Text.Encoding]::UTF8

$auto = "C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화"
$md   = "C:\Users\user\Desktop\Blog\_1.컨텐츠\축구_컨텐츠\260926_남은경기_요약\amatch-broadcast\draft_amatch_broadcast.md"

if (-not (Test-Path $md)) { "초안 없음: $md" | Out-File "$auto\hub_err.log" -Encoding utf8; exit 1 }

Set-Location $auto
& python "$auto\fill_editor.py" $md *> "$auto\hub_run.log"
