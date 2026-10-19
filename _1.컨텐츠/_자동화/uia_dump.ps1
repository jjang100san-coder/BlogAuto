# 창 하나의 UI Automation 트리에서 버튼·목록 항목 이름을 뽑는다(윈도우 기본 기능, 설치 없음)
param([int]$Hwnd = 0, [string]$TitleLike = '', [int]$Max = 400)
Add-Type -AssemblyName UIAutomationClient, UIAutomationTypes
$AE = [System.Windows.Automation.AutomationElement]
if ($Hwnd) { $root = $AE::FromHandle([IntPtr]$Hwnd) }
else {
  $cond = [System.Windows.Automation.Condition]::TrueCondition
  $root = $AE::RootElement.FindAll([System.Windows.Automation.TreeScope]::Children, $cond) |
    Where-Object { $_.Current.Name -like $TitleLike } | Select-Object -First 1
}
if (-not $root) { 'no root'; return }
"ROOT: " + $root.Current.Name + " | " + $root.Current.ClassName
$all = $root.FindAll([System.Windows.Automation.TreeScope]::Descendants, [System.Windows.Automation.Condition]::TrueCondition)
$n = 0
foreach ($e in $all) {
  $c = $e.Current
  $t = $c.ControlType.ProgrammaticName -replace 'ControlType\.', ''
  if ($t -in @('Button', 'ListItem', 'MenuItem', 'SplitButton', 'Hyperlink', 'Text') -and $c.Name) {
    "{0} | {1} | {2}" -f $t, $c.Name, $c.AutomationId
    $n++; if ($n -ge $Max) { break }
  }
}
