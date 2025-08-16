@echo off
title Setup Shopify Bulk Importer - First Time Installation
color 0B

echo.
echo ===============================================
echo   SETUP AWAL - SHOPIFY BULK IMPORTER
echo   MyByte International
echo ===============================================
echo.
echo [INFO] Proses setup pertama kali...
echo [INFO] Hanya perlu dijalankan SEKALI saja
echo.

:: Pindah ke direktori aplikasi
cd /d "%~dp0"

:: Cek Python
echo [1/6] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python tidak ditemukan!
    echo [SOLUSI] Install Python dari: https://www.python.org/downloads/
    echo [REMINDER] Jangan lupa centang "Add Python to PATH"
    echo.
    pause
    exit /b 1
) else (
    python --version
    echo [OK] Python terdeteksi
)

echo.
echo [2/6] Checking Git installation...
git --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Git tidak ditemukan (optional)
    echo [INFO] Install Git jika ingin update otomatis dari: https://git-scm.com/
) else (
    git --version
    echo [OK] Git terdeteksi
)

echo.
echo [3/6] Creating virtual environment...
if exist "venv" (
    echo [INFO] Virtual environment sudah ada, skip...
) else (
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Gagal membuat virtual environment!
        pause
        exit /b 1
    )
    echo [OK] Virtual environment dibuat
)

echo.
echo [4/6] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Gagal mengaktifkan virtual environment!
    pause
    exit /b 1
)
echo [OK] Virtual environment aktif

echo.
echo [5/6] Installing dependencies...
echo [INFO] Ini mungkin membutuhkan waktu beberapa menit...
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [ERROR] Gagal install dependencies!
    echo [INFO] Coba jalankan manual: pip install -r requirements.txt
    pause
    exit /b 1
)
echo [OK] Dependencies berhasil diinstall

echo.
echo [6/6] Creating configuration file...
if exist ".env" (
    echo [INFO] File .env sudah ada
    echo [REMINDER] Pastikan kredensial Shopify sudah benar
) else (
    echo [INFO] Membuat file .env template...
    echo SHOPIFY_ACCESS_TOKEN=YOUR_TOKEN_HERE > .env
    echo SHOPIFY_API_KEY=YOUR_API_KEY_HERE >> .env
    echo SHOPIFY_API_SECRET=YOUR_API_SECRET_HERE >> .env
    echo SHOPIFY_SHOP_DOMAIN=jufbtk-ut.myshopify.com >> .env
    echo [OK] File .env template dibuat
)

echo.
echo ===============================================
echo          SETUP SELESAI!
echo ===============================================
echo.
echo [PENTING] Langkah selanjutnya:
echo.
echo 1. Edit file .env dengan kredensial Shopify yang benar
echo    Location: %CD%\.env
echo    Minta kredensial ke admin/supervisor
echo.
echo 2. Double-click START_APP.bat untuk menjalankan aplikasi
echo.
echo 3. Aplikasi akan terbuka di browser secara otomatis
echo    URL: http://localhost:8501
echo.
echo [REMINDER] Setup ini hanya perlu dijalankan SEKALI
echo            Selanjutnya tinggal gunakan START_APP.bat
echo.

:: Buka notepad untuk edit .env
set /p choice="Ingin edit file .env sekarang? (y/n): "
if /i "%choice%"=="y" (
    echo [INFO] Membuka file .env untuk diedit...
    notepad .env
)

echo.
echo [INFO] Setup selesai! Tutup jendela ini atau tekan Enter.
pause >nul