import smtplib
import csv
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os

# KONFIGURASI GMAIL GRATIS
EMAIL = ''  # Email Gmail Anda
PASSWORD = ''  # App Password (bukan password biasa)
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

def enable_gmail_app_password():
    """Panduan: Aktifkan di Google Account > Security > App Passwords"""
    print("Pastikan App Password aktif di: myaccount.google.com/apppasswords")

def send_single_email(to_email, to_name, subject, message, attach_image=None):
    """Kirim 1 email dengan personalisasi"""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Personalisasi
        personalized_msg = message.format(nama=to_name)
        msg.attach(MIMEText(personalized_msg, 'html'))
        
        # Attach gambar jika ada
        if attach_image and os.path.exists(attach_image):
            with open(attach_image, 'rb') as f:
                img = MIMEImage(f.read())
                img.add_header('Content-ID', 'image1')
                msg.attach(img)
        
        # Kirim
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, to_email, msg.as_string())
        server.quit()
        
        print(f"✓ Terkirim ke {to_name} ({to_email})")
        return True
    
    except Exception as e:
        print(f"✗ Error {to_email}: {str(e)}")
        return False

def email_blast(csv_file, subject, message_template, delay=2, image_path=None):
    """Blast ke semua dari CSV"""
    recipients = []
    
    # Baca CSV
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            recipients.append({'nama': row['nama'], 'email': row['email']})
    
    print(f"🚀 Mulai blast ke {len(recipients)} penerima...")
    
    success = 0
    for i, rec in enumerate(recipients, 1):
        if send_single_email(rec['email'], rec['nama'], subject, message_template, image_path):
            success += 1
        
        print(f"Progress: {i}/{len(recipients)}")
        if i < len(recipients):  # Delay antar email (hindari spam detection)
            time.sleep(delay)
    
    print(f"\n🎉 SELESAI! {success}/{len(recipients)} email berhasil terkirim")

# CONTOH PENGGUNAAN
if __name__ == "__main__":
    # File CSV: nama,email
    CSV_FILE = 'gmail.csv'
    
    # Template HTML cantik
    SUBJECT = "🎉 Promo Spesial Anggota - Oktober 2025"
    MESSAGE = """
    <html>
    <body>
        <h2>Halo {nama}!</h2>
        <p><b>Dapatkan diskon 25% untuk event kami!</b></p>
        <p>Tanggal: 25 Oktober 2025 | Tempat: Jakarta Convention Center</p>
        <img src="cid:image1" alt="Event Banner" style="width:100%;max-width:400px;">
        <p><a href="https://bit.ly/daftar-event">DAFTAR SEKARANG</a></p>
        <hr>
        <small>Balas Anjeng untuk berhenti berlangganan | <a href="https://unsubscribe.link">Unsubscribe</a></small>
    </body>
    </html>
    """
    
    # Jalankan blast
    email_blast(CSV_FILE, SUBJECT, MESSAGE, delay=2, image_path='banner.jpg')


    # Kalau menjalankan biasa seperti ini masih akan masuk kategori spam
    # Untuk menghindarinya harus setup acc di Zoho mail untuk SPF/DKIM/DMARC
    # Gunakan email kantor, jangan pribadi
    # Test di mail-tester.com: Kirim email test, dapat skor 9/10+ (SPF/DKIM wajib untuk ini).
    # Contoh nya bisa di lihat di text.txt
    
