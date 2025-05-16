import pdfplumber
import re
import os
import shutil
from datetime import datetime
from colorama import Fore, Style, init
import time

init(autoreset=True)
LOG_FILE = "log.txt"

def log_message(message, color=Fore.WHITE, include_timestamp=True):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}" if include_timestamp else message
    
    print(f"{color}{log_entry}")
    
    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(log_entry + "\n")

def welcome_message():
    print(Fore.MAGENTA + "==============================================")
    print(Fore.CYAN + "✨ Selamat Datang di PDF Renamer ✨")
    print(Fore.CYAN + "📜 Script by Syahbandi")
    print(Fore.CYAN + "🌐 Original Repositori : https://github.com/mikhailovnasy/renamerged")
    print(Fore.CYAN + "🖥️ Jika ada kendala silahkan hubungi saya di Telegram https://t.me/prasasona")
    print(Fore.MAGENTA + "==============================================")
    time.sleep(2)

def extract_info_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = "".join(page.extract_text() + "\n" for page in pdf.pages if page.extract_text())

    id_tku_match = re.search(r'#?(\d{22})', text)
    id_tku = id_tku_match.group(1).strip() if id_tku_match else None

    partner_match = re.search(r'Pembeli Barang Kena Pajak\s*/\s*Penerima Jasa Kena Pajak:\s*Nama\s*:\s*(.+?)\s*Alamat', text, re.DOTALL)
    partner_name = partner_match.group(1).strip().title() if partner_match else "Nama tidak ditemukan"

    date_match = re.search(r'(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})', text)
    month_dict = {"Januari":"01",
                   "Februari":"02",
                   "Maret":"03",
                   "April":"04",
                   "Mei":"05",
                   "Juni":"06",
                   "Juli":"07",
                   "Agustus":"08",
                   "September":"09",
                   "Oktober":"10",
                   "November":"11",
                   "Desember":"12"
                  }
    date = f"{date_match.group(1)}-{month_dict.get(date_match.group(2), '00')}-{date_match.group(3)}" if date_match else "Tanggal tidak ditemukan"

    faktur_match = re.search(r'Faktur Pajak:\s*(\d+)', text)
    faktur_number = faktur_match.group(1).strip() if faktur_match else "Faktur tidak ditemukan"

    ref_match = re.search(r'Referensi:\s*([^)]*)', text)
    reference = ref_match.group(1).strip() if ref_match and ref_match.group(1).strip() else "---Tidak Ada Referensi---"

    return id_tku, partner_name, faktur_number, date, reference

def rename_pdf_files(input_directory, use_reference, use_faktur):
    output_directory = os.path.join(input_directory, "RenamedPDFs")
    os.makedirs(output_directory, exist_ok=True)
    
    pdf_files = [f for f in os.listdir(input_directory) if f.endswith('.pdf')]
    total_files = len(pdf_files)
    processed_files = 0
    error_files = 0
    
    log_message(f"Total file ditemukan: {total_files}", Fore.CYAN)
    
    for filename in pdf_files:
        pdf_path = os.path.join(input_directory, filename)
        try:
            id_tku, partner_name, faktur_number, date, reference = extract_info_from_pdf(pdf_path)
            
            if not id_tku:
                log_message(f"ID TKU tidak ditemukan di {filename}, dilewati.", Fore.YELLOW)
                continue
                
            tku_folder = os.path.join(output_directory, id_tku)
            os.makedirs(tku_folder, exist_ok=True)
            
            parts = [partner_name]
            if use_faktur == 'Y':
                parts.append(faktur_number)
            parts.append(date)
            if use_reference == 'Y':
                parts.append(reference)
            
            new_filename = " ".join(parts) + ".pdf"
            dest_path = os.path.join(tku_folder, new_filename)
            
            counter = 1
            while os.path.exists(dest_path):
                new_filename = f"{' '.join(parts)} ({counter}).pdf"
                dest_path = os.path.join(tku_folder, new_filename)
                counter += 1
            
            shutil.copy(pdf_path, dest_path)
            processed_files += 1
            
            # Format log khusus
            log_message(f"✅ Berhasil: {filename}", Fore.GREEN)
            log_message(f"🚀 Dipidahkan : {new_filename}", Fore.CYAN, include_timestamp=True)
            log_message(f"📁 Folder : {id_tku}", Fore.YELLOW, include_timestamp=True)
            log_message("", include_timestamp=False)  # Baris kosong
            
        except Exception as e:
            error_files += 1
            log_message(f"Error processing {filename}: {str(e)}", Fore.RED)
    
     # Format hasil akhir di CMD
    print(Fore.CYAN + "\n📊 Hasil Akhir:")
    print(Fore.CYAN + f"📝 Total sampel   : {total_files}")
    print(Fore.GREEN + f"✅ Total diproses : {processed_files}")
    print(Fore.RED + f"❌ Total error    : {error_files}\n")
    time.sleep(1)
    print(Fore.GREEN + "✨ Selesai")
    time.sleep(1)
    
    print(Fore.CYAN + "🤗 Jika Skrip ini bermanfaat dengan senang hati")
    print(Fore.CYAN + "🎁 Donasi scan QRIS Link : https://bit.ly/kiyuris")
    print(Fore.CYAN + "😄 Terimakasih")
    
    # Format hasil akhir
    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write("\nHasil Akhir:\n")
        log_file.write("    Total sampel    : {}\n".format(total_files))
        log_file.write("    Total diproses    : {}\n".format(processed_files))
        log_file.write("    Total error    : {}\n\n".format(error_files))
        log_file.write("END\n\n")

def main():
    welcome_message()
    input_directory = input(Fore.MAGENTA + "Masukkan path folder tempat file PDF: ").strip()
    
    if not os.path.isdir(input_directory):
        log_message("Path tidak valid, pastikan benar!", Fore.RED)
        return
    
    use_reference = input(Fore.MAGENTA + "Apakah ingin pakai referensi? (Y/N) (Default Y): ").strip().upper() or 'Y'
    use_faktur = input(Fore.MAGENTA + "Apakah ingin pakai nomor faktur? (Y/N) (Default Y): ").strip().upper() or 'Y'
    
    rename_pdf_files(input_directory, use_reference, use_faktur)

if __name__ == "__main__":
    main()
