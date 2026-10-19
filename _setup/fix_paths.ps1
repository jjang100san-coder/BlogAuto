# 운영 문서의 옛 PC 경로를 새 PC 기준으로 고친다.
# docs\superpowers\ (작업 기록) 와 콘텐츠 초안은 건드리지 않는다 - 과거 기록이다.

$root = "C:\Users\user\Desktop\Blog"

$targets = @(
    "$root\영상분석\설치.md"
    "$root\영상분석\영상분석 코드\claude-watch-kr-배포\claude-watch-kr\references\other-pc.md"
    "$root\영상분석\영상분석 코드\claude-watch-kr-배포\claude-watch-kr\references\setup-windows.md"
    "$root\네이버 블로그\_자동화\SETUP.md"
    "$root\네이버 블로그\_템플릿\초안작성_프롬프트.md"
    "$root\네이버 블로그\마일리지_수집기\README.md"
    "$root\네이버 블로그\마일리지_수집기\skill\SKILL.md"
    "$root\projects\ke-award-sin\skill\SKILL.md"
    "$root\projects\ke-award-sin\README.md"
)

$map = [ordered]@{
    'D:\Base_JBS\개인\네이버 블로그'  = 'C:\Users\user\Desktop\Blog\네이버 블로그'
    'D:/Base_JBS/개인/네이버 블로그'  = 'C:/Users/user/Desktop/Blog/네이버 블로그'
    'C:\Users\admin\projects'        = 'C:\Users\user\Desktop\Blog\projects'
    '/c/Users/admin/projects'        = '/c/Users/user/Desktop/Blog/projects'
    'C:\Users\admin\.claude'         = 'C:\Users\user\.claude'
    'Settings 탭'                     = '설정 탭'
    '"Remember API keys on this PC"' = '"이 PC에서 API 키 기억하기 (Windows DPAPI 암호화)"'
    "'Remember API keys'"            = "'이 PC에서 API 키 기억하기'"
}

$enc = New-Object System.Text.UTF8Encoding($false)

foreach ($f in $targets) {
    if (-not (Test-Path $f)) { Write-Output "SKIP (없음)  $f"; continue }
    $text = [System.IO.File]::ReadAllText($f, [System.Text.Encoding]::UTF8)
    $orig = $text
    $hits = @()
    foreach ($k in $map.Keys) {
        if ($text.Contains($k)) {
            $n = ([regex]::Matches($text, [regex]::Escape($k))).Count
            $hits += "$k ($n)"
            $text = $text.Replace($k, $map[$k])
        }
    }
    if ($text -ne $orig) {
        [System.IO.File]::WriteAllText($f, $text, $enc)
        Write-Output "FIXED  $($f.Replace("$root\",''))"
        $hits | ForEach-Object { "         $_" }
    } else {
        Write-Output "무변경  $($f.Replace("$root\",''))"
    }
}
