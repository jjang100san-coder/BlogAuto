param(
    [Parameter(Mandatory = $true)][string]$Zip,
    [Parameter(Mandatory = $true)][string]$Dest
)

Add-Type -AssemblyName System.IO.Compression.FileSystem

$z = [System.IO.Compression.ZipFile]::OpenRead($Zip)
$n = 0
$skipped = @()
try {
    foreach ($e in $z.Entries) {
        $target = Join-Path $Dest $e.FullName
        if ($e.FullName.EndsWith('/')) {
            New-Item -ItemType Directory -Force -Path $target | Out-Null
            continue
        }
        $dir = Split-Path $target -Parent
        if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
        try {
            [System.IO.Compression.ZipFileExtensions]::ExtractToFile($e, $target, $true)
            $n++
        } catch {
            $skipped += "$($e.FullName)  --  $($_.Exception.Message)"
        }
    }
} finally {
    $z.Dispose()
}

Write-Output "EXTRACTED $n  ->  $Dest"
if ($skipped.Count -gt 0) {
    Write-Output "SKIPPED $($skipped.Count):"
    $skipped | Select-Object -First 20 | ForEach-Object { "  $_" }
}
