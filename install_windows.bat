@echo off
echo ================================================
echo SHOPIFY BULK IMPORTER - INSTALASI OTOMATIS
echo ================================================
echo.

echo [1/6] Membuat folder project...
cd /d C:\
if not exist "Projects" mkdir Projects
cd Projects
echo ✓ Folder Projects dibuat di C:\Projects

echo.
echo [2/6] Clone repository...
if exist "shopify-bulk-importer" (
    echo Repository sudah ada, melakukan update...
    cd shopify-bulk-importer
    git pull
) else (
    git clone https://github.com/dinandahp/shopify-bulk-importer.git
    cd shopify-bulk-importer
)
echo ✓ Repository berhasil di-clone/update

echo.
echo [3/6] Membuat virtual environment...
python -m venv venv
echo ✓ Virtual environment berhasil dibuat

echo.
echo [4/6] Mengaktifkan virtual environment...
call venv\Scripts\activate
echo ✓ Virtual environment aktif

echo.
echo [5/6] Install dependencies...
pip install --upgrade pip
pip install -r requirements.txt
echo ✓ Dependencies berhasil diinstall

echo.
echo [6/6] Setup file konfigurasi...
if not exist ".env" (
    echo SHOPIFY_ACCESS_TOKEN=YOUR_TOKEN_HERE > .env
    echo SHOPIFY_API_KEY=YOUR_API_KEY_HERE >> .env
    echo SHOPIFY_API_SECRET=YOUR_API_SECRET_HERE >> .env
    echo SHOPIFY_SHOP_DOMAIN=jufbtk-ut.myshopify.com >> .env
    echo ✓ File .env dibuat - JANGAN LUPA EDIT KREDENSIAL!
) else (
    echo ✓ File .env sudah ada
)

echo.
echo ================================================
echo INSTALASI SELESAI!
echo ================================================
echo.
echo LANGKAH SELANJUTNYA:
echo 1. Edit file .env dengan kredensial Shopify yang benar
echo 2. Jalankan: run_app.bat
echo 3. Aplikasi akan terbuka di browser
echo.
echo File instalasi tersimpan di: %CD%
echo.
pause