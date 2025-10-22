import pywhatkit as pwk
import pyautogui
import csv
import time
import os

# Konfigurasi PyAutoGUI
pyautogui.FAILSAFE = True  # Gerakkan mouse ke kiri atas untuk stop
pyautogui.PAUSE = 0.5  # Jeda kecil antar aksi

def send_whatsapp_message(phone, message, wait_time=10):
    """Kirim pesan WhatsApp dengan auto-enter"""
    try:
        phone = phone.replace(' ', '').replace('-', '')
        if not phone.startswith('+62'):
            phone = '+62' + phone.lstrip('0')
        
        # Kirim pesan via PyWhatKit
        pwk.sendwhatmsg_instantly(phone, message, wait_time=wait_time, tab_close=False)
        
        # Simulasi tekan Enter
        time.sleep(2)  # Tunggu WhatsApp Web siap
        pyautogui.press('enter')
        print(f"✓ Pesan untuk {phone} dikirim otomatis")
        
        # Tutup tab setelah kirim
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'w')
        
        return True
    
    except Exception as e:
        print(f"✗ Error untuk {phone}: {str(e)}")
        with open('log_gagal_wa.txt', 'a', encoding='utf-8') as log:
            log.write(f"{phone}: {str(e)}\n")
        return False

def whatsapp_blast_pengumuman(csv_file, message_template, batch_size=5, delay=20):
    recipients = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            recipients.append({
                'nama': row['nama'],
                'phone': row['phone']
            })
    
    print(f"🚀 Mulai blast ke {len(recipients)} peserta lolos...")
    
    success = 0
    for i in range(0, len(recipients), batch_size):
        batch = recipients[i:i + batch_size]
        for rec in batch:
            message = message_template.format(nama=rec['nama'])
            
            if send_whatsapp_message(rec['phone'], message, wait_time=delay):
                success += 1
            
            print(f"Progress: {i + batch.index(rec) + 1}/{len(recipients)}")
            time.sleep(delay)
        
        if i + batch_size < len(recipients):
            print(f"Batch {i//batch_size + 1} selesai. Istirahat 5 menit...")
            time.sleep(300)  # 5 menit
    
    print(f"🎉 SELESAI! {success}/{len(recipients)} pesan berhasil diproses")

# CONTOH
if __name__ == "__main__":
    CSV_FILE = 'wa.csv'
    MESSAGE_TEMPLATE = """
    Selamat {nama}!
    ini cuman test auto🫱🏻‍🫲🏿
    """
    
    print("Buka WhatsApp Web dan scan QR code sebelum mulai!")
    time.sleep(10)  # Waktu untuk scan QR
    whatsapp_blast_pengumuman(CSV_FILE, MESSAGE_TEMPLATE, batch_size=5, delay=20)
    
    
