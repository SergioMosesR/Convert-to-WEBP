# 🖼️ Image Converter (Python + Tkinter)

Aplikasi GUI sederhana berbasis **Tkinter** untuk mengonversi gambar antar format (JPG, JPEG, PNG, SVG, WebP).
Mendukung konversi **ke** WebP dan **dari** WebP.

Mendukung multi-file selection, pengaturan kualitas (untuk WebP/JPEG), serta dukungan SVG menggunakan `cairosvg`.

---

## ✨ Fitur Utama
- ✅ Antarmuka GUI sederhana & interaktif
- ✅ Mendukung format input: `.jpg`, `.jpeg`, `.png`, `.svg`, `.webp`
- ✅ Pilihan format output: **WebP**, **PNG**, **JPEG**
- ✅ Konversi banyak gambar sekaligus (multi-select)
- ✅ Pengaturan kualitas output (1–100) untuk WebP dan JPEG
- ✅ Dukungan konversi **SVG → WebP/PNG/JPEG** (via `cairosvg`)
- ✅ Progress bar dan status proses real-time
- ✅ Pilihan folder output

---

## 🧩 Persyaratan

Pastikan kamu sudah menginstal **Python 3.8+** dan `pip`.

### Instal dependensi:
```bash
pip install pillow
pip install cairosvg   # opsional, hanya untuk konversi SVG
