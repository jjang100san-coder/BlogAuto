$ErrorActionPreference = "Continue"
$env:PYTHONIOENCODING = "utf-8"
$root = "C:\Users\user\Desktop\Blog\_1.컨텐츠\블로그연대기_컨텐츠\260927_유튜브 영상 분석"
$vs   = "$env:USERPROFILE\.claude\skills\claude-watch-kr\scripts\videoscan.py"
$log  = "$root\_run.log"
$ids = @(
 "BWVGEhf17P8","o3aBEWJPWMA","7IAKPO5hQQM","jy2UnH1AWcA","q6mG21-Mztk","Kky7uh2yvt4",
 "n9HEOEnAc6k","9zw5NeVoo90","H5Vmv1pLdos","uepJ7wDJOnE","NBH1qkQxPjs","K-FQPXahCJI",
 "umdUiY32zZc","4b4SYnPwAjU","Ks_VKWa5qHU","tSwPvQrG7_0","mgkWlLrCU8M","sFoGEKgabeE",
 "Lcu-t-3NyBw","QpQdwWpeDyc","5RSNmZczhvY","5eEiVG7OUd0","AM8GHCwshsQ")
$n = 0
foreach ($id in $ids) {
  $n++
  if (Get-ChildItem $root -Directory -Filter "*_$id" -EA SilentlyContinue) { "SKIP $n $id (already done)" | Out-File $log -Append -Encoding utf8; continue }
  "START $n/$($ids.Count) $id $(Get-Date -f HH:mm:ss)" | Out-File $log -Append -Encoding utf8
  $out = & python $vs "https://www.youtube.com/watch?v=$id" --sub-langs "ko,ko-orig" --whisper-lang ko --no-fallback --blog-root $root 2>&1
  $out | Out-File "$root\_log_$id.txt" -Encoding utf8
  $ready = $out | Select-String "READY" | Select-Object -Last 1
  if ($ready) { "DONE $n $id $ready" | Out-File $log -Append -Encoding utf8 }
  else { "FAIL $n $id :: " + (($out | Select-Object -Last 3) -join " | ") | Out-File $log -Append -Encoding utf8 }
  if ($n -lt $ids.Count) { Start-Sleep -Seconds 130 }
}
"ALLDONE $(Get-Date -f HH:mm:ss)" | Out-File $log -Append -Encoding utf8
