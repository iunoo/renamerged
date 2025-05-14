import pdfplumber
import re
import os
import shutil
from pypdf import PdfWriter
from src.utils.utils import log_message, Fore

def validate_pdf(pdf_path):
    """Memvalidasi apakah file PDF dapat dibaca (tidak korup)."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            if pdf.pages:
                return True
        return False
    except Exception as e:
        return False

def extract_info_from_pdf(pdf_path, log_callback=None):
    """Mengambil informasi dari PDF: ID TKU, Nama Partner, Nomor Faktur, Tanggal, dan Referensi."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = "".join(page.extract_text() + "\n" for page in pdf.pages if page.extract_text())

        partner_match = re.search(r'Pembeli Barang Kena Pajak\s*/\s*Penerima Jasa Kena Pajak:\s*Nama\s*:\s*(.+?)\s*Alamat', text, re.DOTALL)
        partner_name = partner_match.group(1).strip().title() if partner_match else "Nama tidak ditemukan"

        id_tku_seller_match = re.search(r'#?(\d{22})', text)
        id_tku_seller = id_tku_seller_match.group(1).strip() if id_tku_seller_match else "IDTKU_Tidak_Ditemukan"

        date_match = re.search(r'(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})', text)
        month_dict = {
            "Januari": "01", "Februari": "02", "Maret": "03", "April": "04", "Mei": "05", "Juni": "06",
            "Juli": "07", "Agustus": "08", "September": "09", "Oktober": "10", "November": "11", "Desember": "12"
        }
        date = f"{date_match.group(1)}-{month_dict.get(date_match.group(2), '00')}-{date_match.group(3)}" if date_match else "Tanggal tidak ditemukan"

        # Perbaiki regex untuk nomor faktur
        faktur_match = re.search(r'Faktur Pajak:\s*([\w\d\-/]+)', text, re.IGNORECASE)
        faktur_number = faktur_match.group(1).strip() if faktur_match else "NoFaktur"
        if faktur_number == "":
            faktur_number = "NoFaktur"
        log_message(f"Debug: Ekstraksi nomor faktur dari {os.path.basename(pdf_path)}: '{faktur_number}'", Fore.CYAN, log_callback=log_callback)

        ref_match = re.search(r'Referensi:\s*([^)]*)', text)
        reference = ref_match.group(1).strip() if ref_match and ref_match.group(1).strip() else ""

        return id_tku_seller, partner_name, faktur_number, date, reference
    except Exception as e:
        if log_callback:
            log_callback(f"❌ Error membaca {os.path.basename(pdf_path)}: {str(e)}")
        raise

def generate_filename(partner_name, faktur_number, date, reference, settings, component_order=None, separator="-", slash_replacement="_"):
    """Membuat nama file berdasarkan urutan komponen dari GUI dengan pemisah dan pengganti garis miring."""
    invalid_chars = '<>:"/\\|?*'
    if any(char in separator for char in invalid_chars) or any(char in slash_replacement for char in invalid_chars):
        log_message(f"Error: Pemisah '{separator}' atau pengganti garis miring '{slash_replacement}' mengandung karakter tidak valid!", Fore.RED)
        raise ValueError("Pemisah atau pengganti garis miring mengandung karakter tidak valid!")

    if reference and "/" in reference:
        reference = reference.replace("/", slash_replacement)

    parts = []
    component_values = {
        "Nama Lawan Transaksi": (partner_name, settings.get("use_name")),
        "Tanggal Faktur Pajak": (date, settings.get("use_date")),
        "Referensi": (reference if reference else "NoRef", settings.get("use_reference")),
        "Nomor Faktur Pajak": (faktur_number, settings.get("use_faktur"))
    }

    log_message(f"Debug: Komponen yang dipilih - {[(name, var.get() if hasattr(var, 'get') else False) for name, (_, var) in component_values.items()]}", Fore.CYAN)

    if component_order:
        for component_name in component_order:
            value, var = component_values.get(component_name, ("", None))
            if var and hasattr(var, 'get') and var.get():
                # Validasi nilai untuk Nomor Faktur Pajak
                if component_name == "Nomor Faktur Pajak" and value == "NoFaktur":
                    log_message(f"Debug: Mengabaikan Nomor Faktur Pajak karena tidak valid: {value}", Fore.YELLOW)
                    continue
                parts.append(value)
                log_message(f"Debug: Menambahkan komponen {component_name}: {value}", Fore.CYAN)
    else:
        for key, (value, var) in component_values.items():
            if var and hasattr(var, 'get') and var.get():
                # Validasi nilai untuk Nomor Faktur Pajak
                if key == "Nomor Faktur Pajak" and value == "NoFaktur":
                    log_message(f"Debug: Mengabaikan Nomor Faktur Pajak karena tidak valid: {value}", Fore.YELLOW)
                    continue
                parts.append(value)
                log_message(f"Debug: Menambahkan komponen default {key}: {value}", Fore.CYAN)

    if not parts:
        parts.append("unnamed")
        log_message("Debug: Tidak ada komponen yang dipilih, menggunakan 'unnamed'", Fore.YELLOW)

    return separator.join(parts) + ".pdf"

def copy_file_with_unique_name(source_path, destination_path, log_callback=None):
    """Menyalin file ke lokasi tujuan dengan menambahkan nomor unik jika file sudah ada."""
    counter = 1
    original_destination = destination_path
    while os.path.exists(destination_path):
        base, ext = os.path.splitext(original_destination)
        destination_path = f"{base} ({counter}){ext}"
        counter += 1

    shutil.copy(source_path, destination_path)
    log_message(f"📂 {os.path.basename(destination_path)} dipindahkan ke {os.path.dirname(destination_path)}", Fore.BLUE, log_callback=log_callback)
    return 1

def merge_pdfs(pdf_paths, output_path, log_callback=None):
    """Menggabungkan beberapa file PDF menjadi satu file."""
    try:
        merger = PdfWriter()
        for pdf_path in pdf_paths:
            merger.append(pdf_path)
        merger.write(output_path)
        merger.close()
        log_message(f"✅ File digabungkan ke {output_path}", Fore.GREEN, log_callback=log_callback)
    except Exception as e:
        log_message(f"❌ Gagal merge {os.path.basename(output_path)}: {str(e)}", Fore.RED, log_callback=log_callback)
        raise