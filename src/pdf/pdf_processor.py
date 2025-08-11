import os
import shutil
from src.utils.utils import log_message, Fore
from src.pdf.pdf_utils import validate_pdf, extract_info_from_pdf, merge_pdfs


def process_pdfs(input_directory, output_directory=None, progress_callback=None, log_callback=None, settings=None, cancel_flag=None):
    """Memproses file PDF dengan mode Rename dan Merge."""
    if output_directory is None or output_directory.strip() == "":
        output_directory = os.path.join(input_directory, "ProcessedPDFs")  # Kembali ke ProcessedPDFs
    os.makedirs(output_directory, exist_ok=True)

    # Tahap 1: Perhitungan file PDF dengan memory management
    try:
        pdf_files = [f for f in os.listdir(input_directory) if f.lower().endswith('.pdf')]
    except (PermissionError, FileNotFoundError) as e:
        log_message(f"❌ Error accessing input directory: {str(e)}", Fore.RED, log_callback=log_callback)
        return {"processed": 0, "renamed": 0, "merged": 0, "errors": 1}
    
    total_files = len(pdf_files)
    log_message(f"Total file ditemukan: {total_files}", Fore.CYAN, log_callback=log_callback)
    
    # Memory management: Process in batches if too many files
    max_batch_size = 50  # Process max 50 files at once
    if total_files > max_batch_size:
        log_message(f"⚠️ Memproses {total_files} file dalam batch ({max_batch_size} file per batch)", Fore.YELLOW, log_callback=log_callback)

    # Inisialisasi variabel statistik
    processed_files = 0
    error_files = 0
    renamed_files = 0  # Jumlah file yang hanya diganti nama (gagal digabungkan)
    merged_files = 0   # Jumlah file individual yang diganti nama dan digabungkan

    # Ambil urutan komponen dari pengaturan
    component_order = settings.get("component_order", None)

    # Process files in batches to manage memory
    files_by_idtku = {}
    batch_count = 0
    
    for i in range(0, total_files, max_batch_size):
        batch_files = pdf_files[i:i + max_batch_size]
        batch_count += 1
        
        if total_files > max_batch_size:
            log_message(f"📦 Memproses batch {batch_count}: {len(batch_files)} file", Fore.CYAN, log_callback=log_callback)
        
        for filename in batch_files:
            # Check for cancellation
            if cancel_flag and cancel_flag.is_set():
                log_message("🛑 Proses dibatalkan oleh user", Fore.YELLOW, log_callback=log_callback)
                return processed_files, renamed_files, merged_files, error_files
                
            pdf_path = os.path.join(input_directory, filename)
            
            # Check file accessibility
            if not os.path.isfile(pdf_path) or not os.access(pdf_path, os.R_OK):
                error_files += 1
                renamed_files += 1
                log_message(f"⚠️ File {filename} tidak dapat diakses, dilewati.", Fore.YELLOW, log_callback=log_callback)
                continue
                
            if not validate_pdf(pdf_path):
                error_files += 1
                renamed_files += 1
                log_message(f"⚠️ File {filename} korup atau tidak valid, dilewati.", Fore.YELLOW, log_callback=log_callback)
                continue

            try:
                id_tku_seller, partner_name, faktur_number, date, reference = extract_info_from_pdf(pdf_path, log_callback)

                if partner_name == "Nama tidak ditemukan":
                    log_message(f"⚠️ Nama tidak ditemukan di {filename}, dilewati.", Fore.YELLOW, log_callback=log_callback)
                    renamed_files += 1
                    continue

                if id_tku_seller not in files_by_idtku:
                    files_by_idtku[id_tku_seller] = []
                files_by_idtku[id_tku_seller].append((pdf_path, partner_name, faktur_number, date, reference))
                
            except MemoryError:
                log_message(f"⚠️ Memory error processing {filename}, skipping...", Fore.YELLOW, log_callback=log_callback)
                error_files += 1
                renamed_files += 1
                continue
            except Exception as e:
                error_files += 1
                renamed_files += 1
                log_message(f"❌ Error membaca {filename}: {str(e)}", Fore.RED, log_callback=log_callback)

            processed_files += 1
            if progress_callback:
                progress_callback("reading", processed_files, total_files, 0, 0)

    # Hitung total file yang akan digabungkan
    total_to_merge = sum(len(files) for id_tku, files in files_by_idtku.items())
    total_to_finalize = total_to_merge  # Jumlah file yang akan difinalisasi sama dengan yang digabungkan
    processed_files_for_merging = 0
    processed_files_for_finalizing = 0

    # Tahap 2: Pemrosesan (merging)
    processed_files = 0
    total_to_process = len(files_by_idtku)
    for id_tku_seller, files in files_by_idtku.items():
        # Check for cancellation
        if cancel_flag and cancel_flag.is_set():
            log_message("🛑 Proses dibatalkan oleh user", Fore.YELLOW, log_callback=log_callback)
            break
        # Buat folder berdasarkan ID TKU dengan race condition protection
        idtku_folder = os.path.join(output_directory, id_tku_seller)
        try:
            os.makedirs(idtku_folder, exist_ok=True)
        except (OSError, FileExistsError) as e:
            # Handle race condition where folder is created by another process
            if not os.path.isdir(idtku_folder):
                log_message(f"⚠️ Error creating folder {idtku_folder}: {str(e)}", Fore.YELLOW, log_callback=log_callback)
                # Try alternative path
                idtku_folder = os.path.join(output_directory, f"{id_tku_seller}_alt")
                os.makedirs(idtku_folder, exist_ok=True)

        # Kelompokkan file berdasarkan Nama Partner
        files_by_partner = {}
        for pdf_path, partner_name, faktur_number, date, reference in files:
            if partner_name not in files_by_partner:
                files_by_partner[partner_name] = []
            files_by_partner[partner_name].append((pdf_path, partner_name, faktur_number, date, reference))

        # Proses setiap file secara individual
        for partner_name, partner_files in files_by_partner.items():
            for file in partner_files:
                pdf_path, _, _, _, _ = file
                processed_files_for_merging += 1
                if progress_callback:
                    progress_callback("processing", processed_files_for_merging, total_files, total_to_merge, total_to_finalize)

            # Buat nama file output (hanya menggunakan Nama Partner)
            output_filename = f"{partner_name}.pdf"
            output_path = os.path.join(idtku_folder, output_filename)

            # Merge file PDF
            merged_files += len(partner_files)  # Hitung jumlah file individual yang digabungkan
            merge_pdfs([file[0] for file in partner_files], output_path, log_callback)

        processed_files += 1

    # Tahap 3: Finalisasi
    if progress_callback:
        progress_callback("finalizing", 0, total_files, total_to_merge, total_to_finalize)

    # Simulasi finalisasi untuk setiap file yang digabungkan
    for i in range(total_to_finalize):
        # Check for cancellation
        if cancel_flag and cancel_flag.is_set():
            break
            
        processed_files_for_finalizing += 1
        if progress_callback:
            progress_callback("finalizing", processed_files_for_finalizing, total_files, total_to_merge, total_to_finalize)
    
    # Ensure final progress callback shows 100%
    if progress_callback and not (cancel_flag and cancel_flag.is_set()):
        progress_callback("finalizing", total_to_finalize, total_files, total_to_merge, total_to_finalize)

    # Log hasil akhir
    log_message("\n📊 Hasil Akhir:", Fore.CYAN, log_callback=log_callback)
    log_message(f"📝 Total file diproses   : {total_files}", Fore.CYAN, log_callback=log_callback)
    log_message(f"📂 File yang hanya diganti nama: {renamed_files}", Fore.BLUE, log_callback=log_callback)
    log_message(f"✅ File yang diganti nama dan digabung: {merged_files}", Fore.GREEN, log_callback=log_callback)
    log_message(f"❌ Total error           : {error_files}\n", Fore.RED, log_callback=log_callback)
    log_message("✨ Selesai", Fore.GREEN, log_callback=log_callback)

    return total_files, renamed_files, merged_files, error_files