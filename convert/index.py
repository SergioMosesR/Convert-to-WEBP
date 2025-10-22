import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
import os
import io
from pathlib import Path

# Coba import cairosvg untuk dukungan SVG
SVG_SUPPORT = False
try:
    from cairosvg import svg2png
    SVG_SUPPORT = True
except ImportError:
    # Menggunakan showinfo agar tidak terlalu mengganggu jika SVG tidak diperlukan
    print("Peringatan: cairosvg tidak terinstal. Konversi SVG tidak didukung! Install dengan: pip install cairosvg")


class WebPConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Converter (WebP, PNG, JPEG)")
        self.root.geometry("600x550") # Sedikit lebih tinggi untuk widget baru
        self.root.resizable(True, True)
        
        # Daftar file yang dipilih
        self.selected_files = []
        
        self.setup_ui()
    
    def setup_ui(self):
        # Frame utama
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # === Pilih file ===
        ttk.Label(main_frame, text="Pilih file gambar (JPG, PNG, SVG, WEBP):").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Button(main_frame, text="Pilih File (Multi-select)", command=self.select_files).grid(row=0, column=1, padx=10, pady=5, columnspan=2, sticky=tk.E)
        
        # === Listbox untuk menampilkan file terpilih ===
        list_frame = ttk.Frame(main_frame)
        list_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        self.file_listbox = tk.Listbox(list_frame, height=10)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        self.file_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.file_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # === Output directory ===
        ttk.Label(main_frame, text="Folder Output:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.output_var = tk.StringVar(value=os.getcwd())
        output_entry = ttk.Entry(main_frame, textvariable=self.output_var, width=50)
        output_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=10, pady=5)
        ttk.Button(main_frame, text="Browse", command=self.select_output_dir).grid(row=2, column=2, padx=10, pady=5)
        
        # === Format Output (BARU) ===
        ttk.Label(main_frame, text="Format Output:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.output_format_var = tk.StringVar(value="WEBP")
        format_combo = ttk.Combobox(main_frame, textvariable=self.output_format_var, values=["WEBP", "PNG", "JPEG"], state="readonly")
        format_combo.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=10, pady=5)
        # Menambahkan binding untuk mengontrol slider kualitas
        format_combo.bind("<<ComboboxSelected>>", self.update_quality_control)

        # === Quality ===
        self.quality_label = ttk.Label(main_frame, text="Kualitas (1-100):")
        self.quality_label.grid(row=4, column=0, sticky=tk.W, pady=5)
        
        self.quality_var = tk.IntVar(value=80)
        self.quality_scale = ttk.Scale(main_frame, from_=1, to=100, variable=self.quality_var, orient=tk.HORIZONTAL)
        self.quality_scale.grid(row=4, column=1, sticky=(tk.W, tk.E), padx=10, pady=5)
        
        self.quality_value_label = ttk.Label(main_frame, textvariable=self.quality_var)
        self.quality_value_label.grid(row=4, column=2, sticky=tk.W, padx=10)
        
        # === Progress bar ===
        self.progress = ttk.Progressbar(main_frame, mode='determinate')
        self.progress.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # === Status label ===
        self.status_var = tk.StringVar(value="Siap konversi...")
        ttk.Label(main_frame, textvariable=self.status_var).grid(row=6, column=0, columnspan=3, pady=5)
        
        # === Tombol konversi (Teks diubah) ===
        ttk.Button(main_frame, text="KONVERSI SEMUA FILE", command=self.convert_all, style='Accent.TButton').grid(row=7, column=0, columnspan=3, pady=20)
        
        # === Hapus file terpilih ===
        ttk.Button(main_frame, text="Hapus Semua File", command=self.clear_files).grid(row=8, column=0, columnspan=3, pady=5)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Panggil sekali di awal untuk mengatur state slider
        self.update_quality_control(None)

    def update_quality_control(self, event):
        """Mengaktifkan/menonaktifkan slider kualitas berdasarkan format output."""
        selected_format = self.output_format_var.get()
        if selected_format == "PNG":
            # PNG (lossless) tidak menggunakan setting kualitas JPEG/WebP
            self.quality_scale.config(state=tk.DISABLED)
            self.quality_label.config(state=tk.DISABLED)
            self.quality_value_label.config(state=tk.DISABLED)
        else:
            # WEBP dan JPEG menggunakan kualitas
            self.quality_scale.config(state=tk.NORMAL)
            self.quality_label.config(state=tk.NORMAL)
            self.quality_value_label.config(state=tk.NORMAL)

    def select_files(self):
        """Memperbarui filetypes untuk menyertakan WEBP."""
        filetypes = [
            ("Image files", "*.jpg *.jpeg *.png *.svg *.webp"),
            ("JPEG", "*.jpg *.jpeg"),
            ("PNG", "*.png"),
            ("SVG", "*.svg"),
            ("WebP", "*.webp"),
            ("All files", "*.*")
        ]
        files = filedialog.askopenfilenames(title="Pilih file gambar", filetypes=filetypes)
        for f in files:
            if f not in self.selected_files:
                self.selected_files.append(f)
                self.file_listbox.insert(tk.END, os.path.basename(f))
        self.status_var.set(f"{len(self.selected_files)} file terpilih.")
    
    def select_output_dir(self):
        dir_path = filedialog.askdirectory(title="Pilih folder output")
        if dir_path:
            self.output_var.set(dir_path)
    
    def clear_files(self):
        self.selected_files.clear()
        self.file_listbox.delete(0, tk.END)
        self.status_var.set("File dibersihkan.")
        self.progress['value'] = 0
    
    def convert_file(self, input_path, target_format, quality):
        """Logika konversi yang dimodifikasi untuk menangani berbagai input/output."""
        output_dir = self.output_var.get()
        base_name = Path(input_path).stem
        output_ext = target_format.lower()
        output_path = os.path.join(output_dir, f"{base_name}.{output_ext}")
        
        input_ext = Path(input_path).suffix.lower()

        # Skip jika format input dan output sama
        if input_ext == f".{output_ext}":
            return False, "Format sama, dilewati."

        img = None
        try:
            # === LANGKAH 1: Buka Gambar (Load Image) ===
            if input_ext == '.svg':
                if not SVG_SUPPORT:
                    return False, "SVG tidak didukung (install cairosvg)."
                with open(input_path, 'rb') as f:
                    svg_data = f.read()
                # Render SVG ke PNG bytes dulu
                png_data = svg2png(bytestring=svg_data, output_width=2048, output_height=2048, dpi=150)
                img = Image.open(io.BytesIO(png_data))
            
            elif input_ext in ['.jpg', '.jpeg', '.png', '.webp']:
                # Buka gambar raster (termasuk .webp)
                img = Image.open(input_path)
            
            else:
                return False, f"Format input tidak didukung: {input_ext}"

            # === LANGKAH 2: Simpan Gambar (Save Image) ===
            
            # Penanganan transparansi jika menyimpan ke JPEG (yang tidak mendukung alpha)
            if target_format == 'JPEG' and img.mode in ('RGBA', 'LA', 'P'):
                # Konversi ke RGB, ganti transparansi dengan latar belakang putih
                img = img.convert('RGB')

            # Simpan berdasarkan format target
            if target_format == 'WEBP':
                img.save(output_path, 'WEBP', quality=quality)
            elif target_format == 'PNG':
                # Kualitas diabaikan untuk PNG
                img.save(output_path, 'PNG')
            elif target_format == 'JPEG':
                img.save(output_path, 'JPEG', quality=quality)
            
            return True, f"Berhasil: {os.path.basename(output_path)}"

        except Exception as e:
            return False, f"Gagal: {str(e)}"
        finally:
            # Pastikan file gambar ditutup
            if img:
                img.close()
    
    def convert_all(self):
        if not self.selected_files:
            messagebox.showerror("Error", "Pilih minimal 1 file!")
            return
        
        output_dir = self.output_var.get()
        if not os.path.exists(output_dir):
            messagebox.showerror("Error", "Folder output tidak valid!")
            return
        
        self.progress['maximum'] = len(self.selected_files)
        self.progress['value'] = 0
        
        # Ambil format target dan kualitas dari UI
        target_format = self.output_format_var.get()
        quality = self.quality_var.get()
        
        success_count = 0
        failed_files = []
        
        for i, input_file in enumerate(self.selected_files):
            self.status_var.set(f"Memproses {i+1}/{len(self.selected_files)}: {os.path.basename(input_file)}")
            self.root.update() # Update UI
            
            success, msg = self.convert_file(input_file, target_format, quality)
            
            if success:
                success_count += 1
            else:
                failed_files.append(f"{os.path.basename(input_file)}: {msg}")
            
            self.progress['value'] = i + 1
        
        self.status_var.set("Selesai!")
        msg = f"Konversi selesai!\nTarget Format: {target_format}\nBerhasil: {success_count}/{len(self.selected_files)}"
        if failed_files:
            msg += f"\nGagal:\n" + "\n".join(failed_files)
        messagebox.showinfo("Hasil", msg)

if __name__ == "__main__":
    # Cek cairosvg saat startup di console
    if not SVG_SUPPORT:
        print("Peringatan: 'cairosvg' tidak ditemukan. Konversi SVG tidak akan berfungsi.")
        print("Install dengan: pip install cairosvg")
        
    root = tk.Tk()
    # Coba gunakan tema yang lebih modern jika ada (opsional)
    try:
        style = ttk.Style(root)
        # Gunakan tema 'clam' atau 'default' jika 'vista' (Windows) atau 'aqua' (Mac) tidak ada
        available_themes = style.theme_names()
        if 'clam' in available_themes:
            style.theme_use('clam')
        if 'vista' in available_themes:
            style.theme_use('vista')
    except Exception:
        pass # Gunakan default jika gagal

    app = WebPConverter(root)
    root.mainloop()