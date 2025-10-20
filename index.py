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
    messagebox.showwarning("Peringatan", "cairosvg tidak terinstal. Konversi SVG tidak didukung!\nInstall dengan: pip install cairosvg")

class WebPConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to WebP Converter")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Daftar file yang dipilih
        self.selected_files = []
        
        self.setup_ui()
    
    def setup_ui(self):
        # Frame utama
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Pilih file
        ttk.Label(main_frame, text="Pilih file gambar (JPEG, JPG, PNG, SVG):").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Button(main_frame, text="Pilih File (Multi-select)", command=self.select_files).grid(row=0, column=1, padx=10, pady=5)
        
        # Listbox untuk menampilkan file terpilih
        list_frame = ttk.Frame(main_frame)
        list_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        self.file_listbox = tk.Listbox(list_frame, height=10)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        self.file_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.file_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Output directory
        ttk.Label(main_frame, text="Folder Output:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.output_var = tk.StringVar(value=os.getcwd())
        output_entry = ttk.Entry(main_frame, textvariable=self.output_var, width=50)
        output_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=10, pady=5)
        ttk.Button(main_frame, text="Browse", command=self.select_output_dir).grid(row=2, column=2, padx=10, pady=5)
        
        # Quality
        ttk.Label(main_frame, text="Kualitas WebP (1-100):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.quality_var = tk.IntVar(value=80)
        quality_scale = ttk.Scale(main_frame, from_=1, to=100, variable=self.quality_var, orient=tk.HORIZONTAL)
        quality_scale.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=10, pady=5)
        ttk.Label(main_frame, textvariable=self.quality_var).grid(row=3, column=2, sticky=tk.W, padx=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='determinate')
        self.progress.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Status label
        self.status_var = tk.StringVar(value="Siap konversi...")
        ttk.Label(main_frame, textvariable=self.status_var).grid(row=5, column=0, columnspan=3, pady=5)
        
        # Tombol konversi
        ttk.Button(main_frame, text="KONVERSI SEMUA KE WEBP", command=self.convert_all, style='Accent.TButton').grid(row=6, column=0, columnspan=3, pady=20)
        
        # Hapus file terpilih
        ttk.Button(main_frame, text="Hapus Semua File", command=self.clear_files).grid(row=7, column=0, columnspan=3, pady=5)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
    
    def select_files(self):
        filetypes = [
            ("Image files", "*.jpg *.jpeg *.png *.svg"),
            ("JPEG", "*.jpg *.jpeg"),
            ("PNG", "*.png"),
            ("SVG", "*.svg"),
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
    
    def convert_to_webp(self, input_path, quality):
        output_dir = self.output_var.get()
        base_name = Path(input_path).stem
        output_path = os.path.join(output_dir, f"{base_name}.webp")
        
        # Skip jika sudah .webp
        if Path(input_path).suffix.lower() == '.webp':
            return False, "Sudah WebP, dilewati."
        
        try:
            ext = Path(input_path).suffix.lower()
            if ext in ['.jpg', '.jpeg', '.png']:
                with Image.open(input_path) as img:
                    img.save(output_path, 'WEBP', quality=quality)
            elif ext == '.svg':
                if not SVG_SUPPORT:
                    return False, "SVG tidak didukung (install cairosvg)."
                with open(input_path, 'rb') as f:
                    svg_data = f.read()
                # Render SVG ke PNG bytes (dpi=96 default, bisa diubah)
                png_data = svg2png(bytestring=svg_data, output_width=2048, output_height=2048, dpi=150)  # Ukuran besar untuk kualitas baik
                img = Image.open(io.BytesIO(png_data))
                img.save(output_path, 'WEBP', quality=quality)
            else:
                return False, f"Format tidak didukung: {ext}"
            return True, f"Berhasil: {os.path.basename(output_path)}"
        except Exception as e:
            return False, f"Gagal: {str(e)}"
    
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
        quality = self.quality_var.get()
        
        success_count = 0
        failed_files = []
        
        for i, input_file in enumerate(self.selected_files):
            self.status_var.set(f"Memproses {i+1}/{len(self.selected_files)}: {os.path.basename(input_file)}")
            self.root.update()
            
            success, msg = self.convert_to_webp(input_file, quality)
            if success:
                success_count += 1
            else:
                failed_files.append(f"{os.path.basename(input_file)}: {msg}")
            
            self.progress['value'] = i + 1
        
        self.status_var.set("Selesai!")
        msg = f"Konversi selesai!\nBerhasil: {success_count}/{len(self.selected_files)}"
        if failed_files:
            msg += f"\nGagal:\n" + "\n".join(failed_files)
        messagebox.showinfo("Hasil", msg)

if __name__ == "__main__":
    root = tk.Tk()
    app = WebPConverter(root)
    root.mainloop()