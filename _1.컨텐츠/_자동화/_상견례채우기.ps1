$ErrorActionPreference = 'Continue'
$OutputEncoding = [Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"
$auto = "C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화"
$md   = "C:\Users\user\Desktop\Blog\_1.컨텐츠\둘이서_컨텐츠\260926_상견례ppt\sanggyeonrye_ppt\sanggyeonrye_ppt_draft.md"
if (-not (Test-Path $md)) { "초안 없음: $md" | Out-File "$auto\sgr_err.log" -Encoding utf8; exit 1 }
Set-Location $auto
& python "$auto\fill_editor.py" $md *> "$auto\sgr_run.log"