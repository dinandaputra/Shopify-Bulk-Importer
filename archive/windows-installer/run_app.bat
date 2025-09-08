@echo off
echo ================================================
echo SHOPIFY BULK IMPORTER - JALANKAN APLIKASI
echo ================================================
echo.

cd /d C:\Projects\shopify-bulk-importer

echo Mengaktifkan virtual environment...
call venv\Scripts\activate

echo.
echo Memulai aplikasi Streamlit...
echo Aplikasi akan terbuka di browser secara otomatis
echo Tekan Ctrl+C untuk menghentikan aplikasi
echo.

streamlit run streamlit_app.py

pause