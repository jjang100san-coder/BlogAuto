# 우루과이전 프리뷰 자동 업로드
# 한글 경로를 명령행 인수로 넘기면 콘솔 코드페이지 때문에 깨질 때가 있어
# (2026-09-27 실측: _1.컨텐츠 -> _1.而⑦뀗痢?), 경로를 이 파일 안에 박아둔다.
$ErrorActionPreference = 'Continue'
$OutputEncoding = [Text.Encoding]::UTF8

$auto = "C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화"
$md   = "C:\Users\user\Desktop\Blog\_1.컨텐츠\축구_컨텐츠\260927_우루과이전프리뷰\uruguay-preview\draft_korea_uruguay_preview.md"

if (-not (Test-Path $md)) {
    "초안 없음: $md" | Out-File "$auto\uru_err.log" -Encoding utf8
    exit 1
}

Set-Location $auto
& python "$auto\fill_editor.py" $md *> "$auto\uru_run.log"
