$ErrorActionPreference = 'Continue'
$OutputEncoding = [Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"
$auto = "C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화"
$md   = "C:\Users\user\Desktop\Blog\_1.컨텐츠\다시묵고싶은곳_컨텐츠\261004_대구 프라나 호텔\draft_daegu_prana_hotel.md"
if (-not (Test-Path $md)) { "초안 없음: $md" | Out-File "$auto\_fill_prana.err.log" -Encoding utf8; exit 1 }
Set-Location $auto
& python "$auto\fill_editor.py" $md *> "$auto\_fill_prana.log"
