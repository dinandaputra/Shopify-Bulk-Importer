@echo off
title Stop Shopify Bulk Importer
color 0C

echo.
echo ===============================================
echo     STOP SHOPIFY BULK IMPORTER
echo ===============================================
echo.

:: Cari dan hentikan proses Streamlit
echo [INFO] Mencari proses Streamlit yang sedang berjalan...

:: Hentikan proses streamlit
tasklist | find /i "python.exe" >nul
if not errorlevel 1 (
    echo [INFO] Menghentikan proses Python/Streamlit...
    
    :: Hentikan proses yang menggunakan port 8501
    for /f "tokens=5" %%a in ('netstat -aon ^| find ":8501" ^| find "LISTENING"') do (
        echo [INFO] Menghentikan proses dengan PID: %%a
        taskkill /F /PID %%a >nul 2>&1
    )
    
    :: Hentikan semua proses streamlit
    taskkill /F /IM "streamlit.exe" >nul 2>&1
    taskkill /F /IM "python.exe" /FI "WINDOWTITLE eq *streamlit*" >nul 2>&1
    
    echo [OK] Proses berhasil dihentikan
) else (
    echo [INFO] Tidak ada proses Streamlit yang sedang berjalan
)

:: Cek apakah port 8501 masih digunakan
echo.
echo [INFO] Checking port 8501...
netstat -an | find ":8501" >nul
if not errorlevel 1 (
    echo [WARNING] Port 8501 masih digunakan oleh proses lain
    echo [INFO] Anda mungkin perlu restart komputer jika ada masalah
) else (
    echo [OK] Port 8501 sudah bebas
)

echo.
echo ===============================================
echo     APLIKASI BERHASIL DIHENTIKAN
echo ===============================================
echo.
echo [INFO] Shopify Bulk Importer telah dihentikan
echo [INFO] Anda bisa menjalankan lagi dengan START_APP.bat
echo.
echo [TIPS] Jika masih ada masalah:
echo        1. Restart browser
echo        2. Tunggu 10 detik sebelum start ulang
echo        3. Restart komputer jika perlu
echo.

timeout /t 3 /nobreak >nul
echo [INFO] Jendela akan tertutup dalam 3 detik...
timeout /t 3 /nobreak >nul