# 게시물 꾸러미를 「휴대폰과 연결」로 갤럭시에 보낸다 — 윈도우 기본 기능만(탐색기 공유 → 폰), 설치 없음
# 사용: powershell -File post_send.ps1 -Dir "<_오늘의게시물\yymmdd-n>"   (꾸러미 하나만이면 그 꾸러미 폴더)
#
# 꾸러미마다 한 동작(10/8 사용자 결정 — 화면을 뺏는 시간은 꾸러미당 5초 안):
#   1) 그 꾸러미 폴더의 사진(1-1.jpg …)과 글(1-게시물.txt) — 이름은 post_pack 이 「꾸러미 번호-사진 순서」로 지어 둔다(10/8)
#   2) 그 폴더를 탐색기로 열어 전부 선택 → [공유] → 폰(「내 폰」 또는 「Galaxy …」) 한 번 → 탐색기 닫고 쓰던 창을 다시 앞으로
#   3) 그 꾸러미 글을 PC 클립보드에 — 「기기 간 복사·붙여넣기」로 폰 키보드 「클립보드 기록」에 꾸러미마다 따로 쌓인다
#   → 45초 쉬고 다음 꾸러미. 사용자는 PC 에서 파일 번호를 보고 폰 앱에서 사진을 고른다(갤럭시 갤러리 순서는 도착 순이라 섞일 수 있음)
# 주의: 「휴대폰과 연결」 창에는 문자·은행 알림이 보인다 — 그 창 내용은 읽지도 남기지도 않는다.
#       공유 창을 연 채 실패하면 그 창이 멈춰 남고 이후 공유가 안 열린다 → 실패 때 Esc 로 닫는다(그래도 남으면 탐색기 재시작, 10/8)
param([Parameter(Mandatory)][string]$Dir)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName UIAutomationClient, UIAutomationTypes
Add-Type @"
using System; using System.Runtime.InteropServices;
public class FgWin {
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int n);
  [DllImport("user32.dll")] public static extern void keybd_event(byte b, byte s, uint f, UIntPtr e);
}
"@
$AE = [System.Windows.Automation.AutomationElement]; $TS = [System.Windows.Automation.TreeScope]
$T = [System.Windows.Automation.Condition]::TrueCondition
$hdrCond = New-Object System.Windows.Automation.PropertyCondition($AE::AutomationIdProperty, 'SharePickerHeaderText')
$liCond = New-Object System.Windows.Automation.PropertyCondition($AE::ControlTypeProperty, [System.Windows.Automation.ControlType]::ListItem)

function Alt-Tap { [FgWin]::keybd_event(0x12, 0, 0, [UIntPtr]::Zero); [FgWin]::keybd_event(0x12, 0, 2, [UIntPtr]::Zero) }
function Press($e) {
  $o = $null
  if ($e.TryGetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern, [ref]$o)) { $o.Invoke(); return }
  if ($e.TryGetCurrentPattern([System.Windows.Automation.SelectionItemPattern]::Pattern, [ref]$o)) { $o.Select(); return }
  throw "누를 수 없음: $($e.Current.Name)"
}

function Send-One([string]$pack, [string]$stageRoot) {
  # 1) 보낼 파일: 꾸러미 폴더의 사진(1-1.jpg …)과 글(1-게시물.txt). 이름은 post_pack 이 이미 「꾸러미-순서」로 지어 둠(10/8). 태그.txt 는 PC 메모라 안 보냄
  $stage = $pack
  $want = @(Get-ChildItem $pack -File | Where-Object { $_.Extension -eq '.jpg' -or $_.Name -like '*게시물.txt' } | ForEach-Object Name)
  $n = $want.Count
  if ($n -eq 0) { "건너뜀(파일 없음): $pack"; return }

  # 2) 공유 한 번
  $before = [FgWin]::GetForegroundWindow()
  $sh = New-Object -ComObject Shell.Application
  $sh.Open($stage); Start-Sleep -Seconds 2
  $w = $null
  for ($i = 0; $i -lt 10 -and -not $w; $i++) {
    $w = $sh.Windows() | Where-Object { try { $_.Document.Folder.Self.Path -eq $stage } catch { $false } } | Select-Object -Last 1
    if (-not $w) { Start-Sleep -Milliseconds 500 }
  }
  if (-not $w) { throw "탐색기 창을 못 찾음: $stage" }
  $first = $true
  foreach ($it in $w.Document.Folder.Items()) {
    if ($want -notcontains (Split-Path $it.Path -Leaf)) { continue }
    if ($first) { $w.Document.SelectItem($it, 1 + 4 + 8 + 16); $first = $false } else { $w.Document.SelectItem($it, 1) }
  }
  if ($w.Document.SelectedItems().Count -ne $n) { $w.Quit(); throw "선택 실패($($w.Document.SelectedItems().Count)/$n)" }
  Alt-Tap; [FgWin]::ShowWindow([IntPtr]$w.HWND, 9) | Out-Null; [FgWin]::SetForegroundWindow([IntPtr]$w.HWND) | Out-Null
  Start-Sleep -Milliseconds 600
  $share = $AE::FromHandle([IntPtr]$w.HWND).FindFirst($TS::Descendants,
    (New-Object System.Windows.Automation.PropertyCondition($AE::NameProperty, '공유')))
  if (-not $share) { $w.Quit(); throw '탐색기 [공유] 버튼 없음' }
  Press $share
  $target = $null
  for ($i = 0; $i -lt 20 -and -not $target; $i++) {
    Start-Sleep -Milliseconds 500
    foreach ($top in $AE::RootElement.FindAll($TS::Children, $T)) {
      if ($top.Current.ClassName -ne 'ApplicationFrameWindow') { continue }
      $hdr = $null; try { $hdr = $top.FindFirst($TS::Descendants, $hdrCond) } catch {}
      if (-not $hdr) { continue }   # 공유 창만 본다(다른 앱 창을 통째로 뒤지면 시간 초과)
      foreach ($e in $top.FindAll($TS::Descendants, $liCond)) {
        $nm = $e.Current.Name
        if ($nm -eq '내 폰' -or $nm -like 'Galaxy*') { $target = $e; break }   # 폰 이름은 설정에 따라 바뀜
      }
      if ($target) { break }
    }
  }
  if (-not $target) {
    [FgWin]::keybd_event(0x1B, 0, 0, [UIntPtr]::Zero); [FgWin]::keybd_event(0x1B, 0, 2, [UIntPtr]::Zero)
    $w.Quit()
    throw '공유 창에서 폰 항목(「내 폰」/「Galaxy …」)을 못 찾음 — 「휴대폰과 연결」 연결 확인. 공유가 계속 안 열리면 탐색기 재시작'
  }
  Press $target
  "보냄: " + (Split-Path $pack -Leaf) + " 파일 ${n}개 → " + $target.Current.Name
  Start-Sleep -Seconds 2
  $w.Quit()
  if ($before -ne [IntPtr]::Zero) { Alt-Tap; [FgWin]::SetForegroundWindow($before) | Out-Null }   # 쓰던 창을 다시 앞으로

  # 3) 이 꾸러미 글을 클립보드에
  $txt = Get-ChildItem $pack -File -Filter '*게시물.txt' | Select-Object -First 1 -ExpandProperty FullName
  if ($txt) {
    Set-Clipboard -Value ' '; Start-Sleep -Milliseconds 400
    Set-Clipboard -Value (Get-Content $txt -Raw -Encoding UTF8)
    "클립보드: " + (Split-Path $pack -Leaf)
  }
}

$Dir = (Resolve-Path $Dir).Path
$packs = @(Get-ChildItem $Dir -Directory | Where-Object { $_.Name -ne '_보내기' } | Sort-Object Name | ForEach-Object FullName)
if ($packs.Count -eq 0) { $packs = @($Dir) }
$stageRoot = ''
function Restart-Explorer {
  # 10/11·10/15: 세션 첫 공유에서 FindAll 시간 초과(공유 창이 빈 채 멈춤) → 탐색기 재시작으로만 풀렸다. 꾸러미 탐색기 창은 먼저 닫는다
  $sh = New-Object -ComObject Shell.Application
  foreach ($w in @($sh.Windows())) { try { if ($w.Document.Folder.Self.Path -like '*_오늘의게시물*') { $w.Quit() } } catch {} }
  Stop-Process -Name explorer -Force -ErrorAction SilentlyContinue; Start-Sleep -Seconds 3
  if (-not (Get-Process explorer -ErrorAction SilentlyContinue)) { Start-Process explorer.exe }
  Start-Sleep -Seconds 8; "탐색기 재시작"
}

for ($k = 0; $k -lt $packs.Count; $k++) {
  try { Send-One $packs[$k] $stageRoot }
  catch {
    if ("$_" -notlike '*FindAll*' -and "$_" -notlike '*timed out*' -and "$_" -notlike '*폰 항목*') { throw }
    "공유 창 멈춤($($_.Exception.Message.Split([char]10)[0])) → 탐색기 재시작 후 한 번 더"
    Restart-Explorer
    Send-One $packs[$k] $stageRoot
  }
  if ($k -lt $packs.Count - 1) { Start-Sleep -Seconds 45 }   # 앞 꾸러미 전송이 끝날 틈 — 6초면 겹쳐서 「보내기 실패」(10/8)
}
