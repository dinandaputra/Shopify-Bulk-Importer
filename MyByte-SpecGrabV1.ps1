# MyByte-SpecGrab.ps1
# Ambil spesifikasi ringkas laptop untuk inventory MyByte

# ==== Pilih folder output: USB kalau ada, selain itu Desktop ====
$usb = Get-Volume -ErrorAction SilentlyContinue | Where-Object { $_.DriveType -eq 'Removable' -and $_.DriveLetter } | Select-Object -First 1
$outDir = if ($usb) { "$($usb.DriveLetter):\MyByte_Specs" } else { "$env:USERPROFILE\Desktop\MyByte_Specs" }
New-Item -ItemType Directory -Path $outDir -Force | Out-Null
$outCsv = Join-Path $outDir 'spec_inventory.csv'

# ==== Kumpulkan data inti ====
$cs   = Get-CimInstance Win32_ComputerSystem
$os   = Get-CimInstance Win32_OperatingSystem
$cpu  = Get-CimInstance Win32_Processor
$bios = Get-CimInstance Win32_BIOS
$mems = Get-CimInstance Win32_PhysicalMemory
$gpus = Get-CimInstance Win32_VideoController -ErrorAction SilentlyContinue
$disks= Get-CimInstance Win32_DiskDrive -ErrorAction SilentlyContinue

# ==== RAM total (GB) ====
$ramTotalGB = [math]::Round( ( ($mems | Measure-Object -Property Capacity -Sum).Sum ) / 1GB, 0 )

# ==== GPU Integrated vs Dedicated ====
$gpuList = @()
if ($gpus) {
  $gpuList = $gpus | ForEach-Object {
    $vendor = $_.AdapterCompatibility
    $venid  = $_.PNPDeviceID
    $type   = if ($vendor -match 'Intel' -or $venid -match 'VEN_8086') { 'Integrated' } else { 'Dedicated' }
    [pscustomobject]@{
      Name   = $_.Name
      Type   = $type
    }
  }
}
$gpuIntegrated = ($gpuList | Where-Object Type -eq 'Integrated' | Select-Object -ExpandProperty Name -ErrorAction SilentlyContinue) -join '; '
$gpuDedicated  = ($gpuList | Where-Object Type -eq 'Dedicated'  | Select-Object -ExpandProperty Name -ErrorAction SilentlyContinue) -join '; '

# ==== Display (Size, Resolution, Refresh Rate) ====
Add-Type -AssemblyName System.Windows.Forms | Out-Null

function Get-DiagonalInch($wcm, $hcm) {
  if (-not $wcm -or -not $hcm -or $wcm -eq 0 -or $hcm -eq 0) { return $null }
  $win = $wcm / 2.54
  $hin = $hcm / 2.54
  return [math]::Round( [math]::Sqrt( ($win*$win) + ($hin*$hin) ), 1 )
}

$edidParams = @( Get-CimInstance -Namespace root\wmi -ClassName WmiMonitorBasicDisplayParams -ErrorAction SilentlyContinue )
$diagonals = @()
foreach ($p in $edidParams) {
  $diagonals += Get-DiagonalInch $p.MaxHorizontalImageSize $p.MaxVerticalImageSize
}

$screens = [System.Windows.Forms.Screen]::AllScreens
$adapterRates = @()
if ($gpus) { $adapterRates = $gpus | ForEach-Object { $_.CurrentRefreshRate } }
$defaultHz = ($adapterRates | Where-Object { $_ -gt 0 } | Select-Object -First 1)
if (-not $defaultHz) { $defaultHz = 60 }

$displayStrings = @()
for ($i=0; $i -lt $screens.Count; $i++) {
  $scr = $screens[$i]
  $w = $scr.Bounds.Width
  $h = $scr.Bounds.Height
  $hz = $defaultHz
  $inch = $null
  if ($i -lt $diagonals.Count -and $diagonals[$i]) { $inch = $diagonals[$i] }
  $sizeTxt = if ($inch) { "$inch`"" } else { "Unknown" }
  $displayStrings += "$sizeTxt ${w}x$h@$hz`Hz"
}
$displaySummary = $displayStrings -join '; '

# ==== Storage ====
$diskSummaries = @()
if ($disks) {
  foreach ($d in $disks) {
    $sz = if ($d.Size) { [math]::Round($d.Size/1GB,0) } else { $null }
    $iface = $d.InterfaceType
    if (-not $iface -and $d.Model -match 'NVMe') { $iface = 'NVMe' }
    $one = if ($sz) { "$sz`GB" } else { "Unknown" }
    if ($iface) { $one += " $iface" }
    if ($d.Model) { $one += " - $($d.Model.Trim())" }
    $diskSummaries += $one
  }
}
$storageSummary = $diskSummaries -join '; '

# ==== Buat record ====
$record = [pscustomobject]@{
  Timestamp             = (Get-Date).ToString('yyyy-MM-dd HH:mm:ss')
  Hostname              = $env:COMPUTERNAME
  Manufacturer          = $cs.Manufacturer
  Model                 = $cs.Model
  SerialNumber          = $bios.SerialNumber
  Processor             = $cpu.Name
  RAM_GB                = $ramTotalGB
  Integrated_Graphics   = $gpuIntegrated
  Dedicated_Graphics    = $gpuDedicated
  Display               = $displaySummary
  Storage               = $storageSummary
}

# ==== Simpan ke CSV (append kalau sudah ada) ====
if (Test-Path $outCsv) {
  $record | Export-Csv -Path $outCsv -NoTypeInformation -Append
} else {
  $record | Export-Csv -Path $outCsv -NoTypeInformation
}

Write-Host "Done. Saved to: $outCsv"