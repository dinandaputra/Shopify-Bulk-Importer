@echo off
title Shopify Bulk Importer - MyByte International
color 0A

echo.
echo ===============================================
echo     SHOPIFY BULK IMPORTER - MYBYTE INTL
echo ===============================================
echo.
echo [INFO] Memulai aplikasi...

:: Pindah ke direktori aplikasi
cd /d "%~dp0"

:: Cek apakah virtual environment ada
if not exist "venv\Scripts\activate.bat" (
    echo.
    echo [ERROR] Virtual environment tidak ditemukan!
    echo [SOLUSI] Jalankan SETUP_FIRST_TIME.bat terlebih dahulu
    echo.
    pause
    exit /b 1
)

:: Aktifkan virtual environment
echo [INFO] Mengaktifkan virtual environment...
call venv\Scripts\activate.bat

:: Cek apakah Streamlit terinstall
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo.
    echo [ERROR] Dependencies belum terinstall!
    echo [SOLUSI] Jalankan SETUP_FIRST_TIME.bat terlebih dahulu
    echo.
    pause
    exit /b 1
)

:: Cek apakah file .env ada
if not exist ".env" (
    echo.
    echo [WARNING] File .env tidak ditemukan!
    echo [INFO] Membuat file .env template...
    echo SHOPIFY_ACCESS_TOKEN=YOUR_TOKEN_HERE > .env
    echo SHOPIFY_API_KEY=YOUR_API_KEY_HERE >> .env
    echo SHOPIFY_API_SECRET=YOUR_API_SECRET_HERE >> .env
    echo SHOPIFY_SHOP_DOMAIN=jufbtk-ut.myshopify.com >> .env
    echo.
    echo [ACTION REQUIRED] Edit file .env dengan kredensial Shopify yang benar!
    echo [LOCATION] %CD%\.env
    echo.
    echo Tekan Enter setelah file .env sudah diedit...
    pause >nul
)

:: Mulai aplikasi
echo.
echo [INFO] Memulai Shopify Bulk Importer...
echo [INFO] Aplikasi akan terbuka di browser secara otomatis
echo [INFO] URL: http://localhost:8501
echo.
echo ===============================================
echo     APLIKASI SIAP DIGUNAKAN!
echo ===============================================
echo.
echo [TIPS] Tekan Ctrl+C untuk menghentikan aplikasi
echo [TIPS] Tutup terminal ini untuk keluar sepenuhnya
echo.

:: Jalankan Streamlit
streamlit run streamlit_app.py --server.headless true

:: Jika aplikasi berhenti
echo.
echo [INFO] Aplikasi telah dihentikan.
echo [INFO] Tutup jendela ini atau tekan Enter untuk keluar.
pause >nul