$ErrorActionPreference = 'Continue'
$OutputEncoding = [Text.Encoding]::UTF8
$auto = "C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화"
$md   = "C:\Users\user\Desktop\Blog\_1.컨텐츠\여행정보_컨텐츠\261012_마일리지_오픈_9시정각\open0901_post_draft.md"
if (-not (Test-Path $md)) { "초안 없음: $md" | Out-File "$auto\open0901_err.log" -Encoding utf8; exit 1 }
Set-Location $auto
& python -X utf8 "$auto\fill_editor.py" $md *> "$auto\open0901_run.log"