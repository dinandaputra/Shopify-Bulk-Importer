@echo off
setlocal
REM Jalankan PowerShell tanpa profil, bypass policy, dan PAUSE di akhir
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0MyByte-SpecGrab.ps1"
echo.
echo Selesai. Tekan tombol apa saja untuk menutup...
pause >nul