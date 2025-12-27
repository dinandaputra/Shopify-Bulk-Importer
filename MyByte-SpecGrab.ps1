# MyByte-SpecGrab.ps1 — FINAL (Storage via Get-PhysicalDisk + GPU fix + RAM total)
$ErrorActionPreference = "Continue"

# ==== Output folder (USB else Desktop) ====
$usb = Get-Volume -ErrorAction SilentlyContinue | Where-Object { $_.DriveType -eq 'Removable' -and $_.DriveLetter } | Select-Object -First 1
$outDir = if ($usb) { "$($usb.DriveLetter):\MyByte_Specs" } else { "$env:USERPROFILE\Desktop\MyByte_Specs" }
New-Item -ItemType Directory -Path $outDir -Force | Out-Null
$outCsv = Join-Path $outDir 'spec_inventory.csv'

# ==== Data dasar ====
$cs    = Get-CimInstance Win32_ComputerSystem -ErrorAction SilentlyContinue
$os    = Get-CimInstance Win32_OperatingSystem -ErrorAction SilentlyContinue
$cpu   = Get-CimInstance Win32_Processor -ErrorAction SilentlyContinue
$bios  = Get-CimInstance Win32_BIOS -ErrorAction SilentlyContinue
$mems  = Get-CimInstance Win32_PhysicalMemory -ErrorAction SilentlyContinue
$gpus  = Get-CimInstance Win32_VideoController -ErrorAction SilentlyContinue
$disks = Get-CimInstance Win32_DiskDrive -ErrorAction SilentlyContinue

# ==== RAM total ====
$ramGB = 0
try { $ramGB = [math]::Round((($mems | Measure-Object -Property Capacity -Sum).Sum) / 1GB,0) } catch {}

# ==== GPU classify (Intel iGPU; AMD iGPU vs dGPU) ====
function Classify-GPU { param($name,$vendor)
  $n="$name"; $v="$vendor"
  if ($v -match 'Intel') { return 'Integrated' }
  if ($v -match 'NVIDIA') { return 'Dedicated' }
  if ($v -match 'AMD|Advanced Micro Devices') {
    $amdIgpu = @(
      'Radeon\s*\(?TM\)?\s*Graphics','Ryzen\s*Graphics','\bVega\b','RX\s*Vega\s*\d+','\bR[34567]\s+Graphics\b'
    ) -join '|'
    $amdDgpu = @('Radeon\s+Pro','\bRX\s*\d{3,4}\b','\bR9\b|\bR7\b(?!\s*Graphics)','\bWX\b','FirePro','Fury','\bXT\b','\bXTX\b') -join '|'
    if ($n -match $amdDgpu) { return 'Dedicated' }
    if ($n -match $amdIgpu) { return 'Integrated' }
    return 'Integrated'  # default aman bila ambigu
  }
  'Dedicated'
}
$igpus=@(); $dgpus=@()
foreach ($g in $gpus) {
  $role = Classify-GPU $g.Name $g.AdapterCompatibility
  if ($role -eq 'Integrated') { $igpus += $g.Name } else { $dgpus += $g.Name }
}
$gpuIntegrated = ($igpus -join '; ')
$gpuDedicated  = ($dgpus -join '; ')

# ==== Display (Size/Res/Hz) ringkas ====
function Get-DiagonalInch([double]$wcm,[double]$hcm){
  if ($wcm -le 0 -or $hcm -le 0) { return $null }
  $win=$wcm/2.54; $hin=$hcm/2.54
  [math]::Round([math]::Sqrt(($win*$win)+($hin*$hin)),1)
}
$displaySummary="Unknown"
try{
  Add-Type -AssemblyName System.Windows.Forms -ErrorAction Stop | Out-Null
  $edid = @(Get-CimInstance -Namespace root\wmi -Class WmiMonitorBasicDisplayParams -ErrorAction SilentlyContinue)
  $diags=@(); foreach($p in $edid){ $diags+=Get-DiagonalInch $p.MaxHorizontalImageSize $p.MaxVerticalImageSize }
  $screens=[System.Windows.Forms.Screen]::AllScreens
  $hz = ($gpus | Where-Object { $_.CurrentRefreshRate -gt 0 } | Select-Object -ExpandProperty CurrentRefreshRate -First 1); if(-not $hz){$hz=60}
  $rows=@()
  for($i=0;$i -lt $screens.Count;$i++){
    $w=$screens[$i].Bounds.Width; $h=$screens[$i].Bounds.Height
    $inch = if($i -lt $diags.Count -and $diags[$i]){"$($diags[$i])`""} else {"Unknown"}
    $rows += "$inch ${w}x$h@$hz`Hz"
  }
  if($rows.Count -gt 0){ $displaySummary = ($rows -join '; ') }
} catch {
  $w=($gpus|Select-Object -ExpandProperty CurrentHorizontalResolution -First 1)
  $h=($gpus|Select-Object -ExpandProperty CurrentVerticalResolution   -First 1)
  $hz=($gpus|Where-Object { $_.CurrentRefreshRate -gt 0 }|Select-Object -ExpandProperty CurrentRefreshRate -First 1); if(-not $hz){$hz=60}
  if($w -and $h){ $displaySummary="Unknown ${w}x$h@$hz`Hz" }
}

# ==== STORAGE via Get-PhysicalDisk (prioritas) ====
function SizeToNice($gb){ if($gb -ge 1000){ "{0}TB" -f [math]::Round($gb/1000,1) } else { "{0}GB" -f [math]::Round($gb,0) } }

$storageSummary = ""
$pd=@()
try { $pd = Get-PhysicalDisk -ErrorAction Stop } catch {}

if ($pd -and $pd.Count -gt 0) {
  # Filter non-USB & disk valid
  $pd = $pd | Where-Object { "$($_.BusType)" -notmatch 'USB' -and $_.Size -gt 0 }

  $parts=@()
  foreach ($p in $pd) {
    $gb = $p.Size/1GB
    $sizeTxt = SizeToNice $gb
    $mt = "$($p.MediaType)"
    # SCM (Optane) → anggap SSD untuk inventori sederhana
    if ($mt -match 'SSD|SolidState|SCM') { $type='SSD' }
    elseif ($mt -match 'HDD') { $type='HDD' }
    else { 
      # Fallback: BusType NVMe/PCIe → SSD, selainnya Unknown
      if ("$($p.BusType)" -match 'NVMe|PCIe') { $type='SSD' } else { $type='Unknown' }
    }
    $parts += "$sizeTxt $type"
  }
  $storageSummary = ($parts -join '; ')
}

# Fallback kalau Get-PhysicalDisk kosong (misal Windows 10 Home tertentu)
if (-not $storageSummary -or $storageSummary -eq "") {
  $diskParts=@()
  foreach($d in $disks){
    if ($d.InterfaceType -eq 'USB' -or "$($d.PNPDeviceID)" -match 'USBSTOR') { continue }
    $gb = if($d.Size){ $d.Size/1GB } else { 0 }
    $sizeTxt = SizeToNice $gb
    $type='Unknown'
    try {
      if ($null -ne $d.RotationRate) {
        if ([int]$d.RotationRate -gt 0) { $type='HDD' } else { $type='SSD' }
      }
    } catch {}
    if ($type -eq 'Unknown') {
      if ("$($d.Model)$($d.PNPDeviceID)" -match 'NVMe|SSD|Solid\s*State|M\.2|PCIe') { $type='SSD' }
      elseif ("$($d.Model)$($d.PNPDeviceID)" -match 'HDD') { $type='HDD' }
    }
    $diskParts += "$sizeTxt $type"
  }
  $storageSummary = ($diskParts -join '; ')
}

# ==== Record & CSV ====
$record = [pscustomobject]@{
  Timestamp            = (Get-Date).ToString('yyyy-MM-dd HH:mm:ss')
  Hostname             = $env:COMPUTERNAME
  Manufacturer         = ($cs.Manufacturer | Select-Object -First 1)
  Model                = ($cs.Model | Select-Object -First 1)
  SerialNumber         = ($bios.SerialNumber | Select-Object -First 1)
  Processor            = ($cpu.Name | Select-Object -First 1)
  RAM_GB               = $ramGB
  Integrated_Graphics  = $gpuIntegrated
  Dedicated_Graphics   = $gpuDedicated
  Display              = $displaySummary
  Storage              = $storageSummary
  OS                   = if ($os) { "$($os.Caption) $($os.OSArchitecture)" } else { "" }
}

if (Test-Path $outCsv) { $record | Export-Csv -Path $outCsv -NoTypeInformation -Append }
else                   { $record | Export-Csv -Path $outCsv -NoTypeInformation }

Write-Host "Done. Saved to: $outCsv"