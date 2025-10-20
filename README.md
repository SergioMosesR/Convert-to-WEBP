# 🖼️ Image to WebP Converter (Python + Tkinter)

Aplikasi GUI sederhana berbasis **Tkinter** untuk mengonversi gambar dari berbagai format (JPG, JPEG, PNG, SVG) ke **WebP**.  
Mendukung multi-file selection, pengaturan kualitas, serta dukungan SVG menggunakan `cairosvg`.

---

## ✨ Fitur Utama
- ✅ Antarmuka GUI sederhana & interaktif
- ✅ Mendukung format gambar: `.jpg`, `.jpeg`, `.png`, `.svg`
- ✅ Konversi banyak gambar sekaligus (multi-select)
- ✅ Pengaturan kualitas output (1–100)
- ✅ Dukungan konversi **SVG → WebP** (via `cairosvg`)
- ✅ Progress bar dan status proses real-time
- ✅ Pilihan folder output

---

## 🧩 Persyaratan

Pastikan kamu sudah menginstal **Python 3.8+** dan `pip`.

### Instal dependensi:
```bash
pip install pillow
pip install cairosvg   # opsional, hanya untuk konversi SVG
