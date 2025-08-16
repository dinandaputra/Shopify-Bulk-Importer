# ✅ CHECKLIST VERIFIKASI INSTALASI BERHASIL

## 📋 CHECKLIST SEBELUM INSTALASI

### ✅ Persiapan Sistem
- [ ] Komputer Windows 10/11
- [ ] Koneksi internet stabil
- [ ] Hak akses Administrator
- [ ] Ruang disk minimal 2GB kosong
- [ ] Browser modern (Chrome/Firefox/Edge)

### ✅ Software Requirement
- [ ] Python 3.8+ terinstall dan ditambahkan ke PATH
- [ ] Git for Windows terinstall
- [ ] Command Prompt dapat diakses

## 📋 CHECKLIST SELAMA INSTALASI

### ✅ Langkah 1: Verifikasi Python
```bash
python --version
pip --version
```
- [ ] Python version 3.8+ muncul
- [ ] pip version muncul tanpa error

### ✅ Langkah 2: Verifikasi Git
```bash
git --version
```
- [ ] Git version muncul

### ✅ Langkah 3: Clone Repository
```bash
cd C:\Projects
git clone https://github.com/dinandahp/shopify-bulk-importer.git
cd shopify-bulk-importer
```
- [ ] Folder shopify-bulk-importer terbuat
- [ ] File streamlit_app.py ada di folder

### ✅ Langkah 4: Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```
- [ ] Folder venv terbuat
- [ ] Command prompt menampilkan (venv) di awal

### ✅ Langkah 5: Install Dependencies
```bash
pip install -r requirements.txt
```
- [ ] Semua package terinstall tanpa error
- [ ] Tidak ada pesan "FAILED" atau "ERROR"

### ✅ Langkah 6: Konfigurasi File
```bash
dir .env
```
- [ ] File .env ada di folder project
- [ ] File .env berisi kredensial Shopify yang benar
- [ ] SHOPIFY_SHOP_DOMAIN = jufbtk-ut.myshopify.com

## 📋 CHECKLIST SETELAH INSTALASI

### ✅ Test Aplikasi
```bash
streamlit run streamlit_app.py
```
- [ ] Command berjalan tanpa error
- [ ] Browser terbuka otomatis
- [ ] URL menampilkan: http://localhost:8501
- [ ] Halaman aplikasi Shopify Bulk Importer muncul

### ✅ Test Interface
- [ ] Menu "Smartphone Entry" dapat diakses
- [ ] Menu "Laptop Entry" dapat diakses
- [ ] Form input muncul dengan benar
- [ ] Dropdown brand dan model berfungsi

### ✅ Test Koneksi Shopify
- [ ] Tidak ada error "Invalid credentials" 
- [ ] Tidak ada error "Access denied"
- [ ] Status koneksi menunjukkan "Connected"

### ✅ Test Produk Dummy
- [ ] Buat produk test sederhana
- [ ] Produk berhasil dibuat di Shopify
- [ ] Produk muncul di Admin Shopify dengan status "Draft"

## 🔧 TROUBLESHOOTING COMMON ISSUES

### ❌ Python tidak ditemukan
**Solusi:**
1. Install ulang Python dengan centang "Add to PATH"
2. Restart Command Prompt
3. Atau tambahkan manual ke PATH environment

### ❌ Git tidak ditemukan
**Solusi:**
1. Install Git for Windows
2. Pilih opsi "Git from command line"
3. Restart Command Prompt

### ❌ Virtual environment error
**Solusi:**
```bash
python -m pip install --upgrade pip
python -m pip install virtualenv
python -m virtualenv venv
```

### ❌ Package install gagal
**Solusi:**
```bash
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt
```

### ❌ Streamlit tidak bisa start
**Solusi:**
```bash
pip install --upgrade streamlit
streamlit run streamlit_app.py --server.port=8080
```

### ❌ API Shopify error
**Solusi:**
1. Cek file .env kredensial benar
2. Cek koneksi internet
3. Cek permissions di Shopify Admin

## ✅ VERIFIKASI FINAL

### 🎯 Aplikasi Siap Produksi Jika:
- [ ] ✅ Instalasi berhasil tanpa error
- [ ] ✅ Interface berjalan lancar
- [ ] ✅ Koneksi Shopify sukses
- [ ] ✅ Test produk berhasil dibuat
- [ ] ✅ Data tersimpan di Shopify Admin
- [ ] ✅ Handle produk terbuat dengan format yang benar
- [ ] ✅ Metafield tersimpan dengan benar

## 📞 BANTUAN TEKNIS

Jika masih ada masalah setelah mengikuti checklist:

1. **Cek Log Error**: Lihat pesan error di Command Prompt
2. **Restart Aplikasi**: Tutup dan buka ulang Command Prompt
3. **Cek Koneksi**: Pastikan internet dan firewall tidak memblokir
4. **Hubungi IT Support**: Dengan screenshot error message

---

**🎉 SELAMAT! APLIKASI SHOPIFY BULK IMPORTER SIAP DIGUNAKAN!**