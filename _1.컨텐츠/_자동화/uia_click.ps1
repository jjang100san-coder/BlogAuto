# 창(핸들 또는 제목) 안에서 이름이 맞는 컨트롤을 찾아 누른다 — Invoke 패턴, 안 되면 SelectionItem/Toggle
param([int]$Hwnd = 0, [string]$TitleLike = '', [Parameter(Mandatory)][string]$Name, [string]$Type = '')
Add-Type -AssemblyName UIAutomationClient, UIAutomationTypes
$AE = [System.Windows.Automation.AutomationElement]
$TS = [System.Windows.Automation.TreeScope]
$True_ = [System.Windows.Automation.Condition]::TrueCondition
if ($Hwnd) { $roots = @($AE::FromHandle([IntPtr]$Hwnd)) }
else { $roots = @($AE::RootElement.FindAll($TS::Children, $True_) | Where-Object { $_.Current.Name -like $TitleLike }) }
foreach ($root in $roots) {
  foreach ($e in $root.FindAll($TS::Descendants, $True_)) {
    $c = $e.Current
    if ($c.Name -ne $Name) { continue }
    if ($Type -and ($c.ControlType.ProgrammaticName -notlike "*$Type")) { continue }
    foreach ($p in @([System.Windows.Automation.InvokePattern]::Pattern, [System.Windows.Automation.SelectionItemPattern]::Pattern, [System.Windows.Automation.TogglePattern]::Pattern)) {
      $o = $null
      if ($e.TryGetCurrentPattern($p, [ref]$o)) {
        if ($o -is [System.Windows.Automation.InvokePattern]) { $o.Invoke() }
        elseif ($o -is [System.Windows.Automation.SelectionItemPattern]) { $o.Select() }
        else { $o.Toggle() }
        "clicked: $Name ($($c.ControlType.ProgrammaticName)) in $($root.Current.Name)"; return
      }
    }
  }
}
"not found: $Name"
