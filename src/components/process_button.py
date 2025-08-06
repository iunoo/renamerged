import customtkinter as ctk
import tkinter as tk
import os
import time
from tkinter import messagebox
from src.pdf.pdf_processor import process_pdfs as process_pdfs_merge
from src.pdf.pdf_processor_rename import process_pdfs as process_pdfs_rename
from src.utils.utils import log_message, Fore

class ProcessButtonComponent:
    def __init__(self, parent, colors, input_path_var, output_path_var, mode_var, settings, progress_var, progress_percentage_var, statistics, output_location, mode_selection, gui):
        self.parent = parent
        self.colors = colors
        self.input_path_var = input_path_var
        self.output_path_var = output_path_var
        self.mode_var = mode_var
        self.settings = settings
        self.progress_var = progress_var
        self.progress_percentage_var = progress_percentage_var
        self.statistics = statistics
        self.output_location = output_location
        self.mode_selection = mode_selection
        self.gui = gui

        # No UI creation - this component now only provides logic
        # The actual button is created in FileInputOutputComponent

    def process(self):
        input_dir = self.input_path_var.get()
        output_dir = self.output_path_var.get()
        mode = self.mode_var.get()

        if not input_dir or not isinstance(input_dir, str):
            messagebox.showerror("Error", "Pilih folder input terlebih dahulu!")
            return
        if not os.path.isdir(input_dir):
            messagebox.showerror("Error", "Folder input tidak valid! Pilih folder yang benar.")
            return

        self.set_button_state("disabled")

        if not output_dir or output_dir.strip() == "":
            output_dir = os.path.join(input_dir, "ProcessedPDFs")
            os.makedirs(output_dir, exist_ok=True)
            self.output_path_var.set(output_dir)

        required_keys = ["use_name", "use_date", "use_reference", "use_faktur"]
        for key in required_keys:
            if not hasattr(self.settings.get(key), 'get'):
                messagebox.showerror("Error", f"Pengaturan {key} tidak valid!")
                self.set_button_state("normal")
                return

        self.settings["component_order"] = self.mode_selection.get_component_order()
        self.settings["separator"] = self.mode_selection.get_separator()
        self.settings["slash_replacement"] = self.mode_selection.get_slash_replacement()

        log_message(f"Debug: Pengaturan - component_order: {self.settings['component_order']}, "
                    f"use_name: {self.settings['use_name'].get()}, use_date: {self.settings['use_date'].get()}, "
                    f"use_reference: {self.settings['use_reference'].get()}, use_faktur: {self.settings['use_faktur'].get()}, "
                    f"separator: '{self.settings['separator']}', slash_replacement: '{self.settings['slash_replacement']}'", 
                    Fore.CYAN)

        # Check for long filenames before processing
        from src.utils.filename_checker import check_long_filenames
        from src.components.filename_warning_dialog import FilenameWarningDialog
        
        has_long_filenames, long_filenames, sample_filenames = check_long_filenames(input_dir, self.settings, self.log_callback)
        
        if has_long_filenames:
            # Show simple warning dialog
            dialog = FilenameWarningDialog(self.parent, self.gui.colors, len(long_filenames))
            user_choice = dialog.show_warning()
            
            if user_choice == "cancel":
                log_message("Proses dibatalkan oleh user karena filename terlalu panjang", Fore.YELLOW, log_callback=self.log_callback)
                self.set_button_state("normal")
                return
            elif user_choice == "ok":
                # Set default max length (150 karakter - apply for all)
                self.settings["max_filename_length"] = 150
                log_message(f"User memilih melanjutkan dengan penyesuaian referensi otomatis (max 150 karakter, berlaku untuk semua file)", Fore.CYAN, log_callback=self.log_callback)

        self.statistics.reset()
        self.progress_var.set(0)
        self.progress_percentage_var.set("0%")
        self.gui.progress_bar.set_progress(0)
        self.parent.update_idletasks()

        try:
            if mode == "Rename dan Merge":
                total, renamed, merged, errors = process_pdfs_merge(input_dir, output_dir, self.progress_callback, self.log_callback, self.settings)
            else:
                total, renamed, merged, errors = process_pdfs_rename(input_dir, output_dir, self.progress_callback, self.log_callback, self.settings)

            self.statistics.update_statistics(total, renamed, merged, errors)
            self.output_location.set_output_path(output_dir)

        except Exception as e:
            error_message = self.get_detailed_error_message(e)
            messagebox.showerror("Error", error_message)
            log_message(f"Error detail: {str(e)}", Fore.RED, log_callback=self.log_callback)
        finally:
            self.process_btn.configure(state="normal")

    def log_callback(self, message):
        if self.statistics:
            self.statistics.log_message(message)

    def progress_callback(self, stage, current, total_files, total_to_merge, total_to_finalize):
        if stage == "reading":
            percentage = (current / max(total_files, 1)) * 40  # Prevent division by zero
        elif stage == "processing":
            percentage = 40 + (current / max(total_to_merge, 1)) * 40  # Prevent division by zero
        else:
            percentage = 80 + (current / max(total_to_finalize, 1)) * 20  # Prevent division by zero

        percentage = min(max(percentage, 0), 100)
        normalized_progress = percentage / 100

        self.gui.progress_bar.set_progress(normalized_progress)
        self.progress_var.set(normalized_progress)
        self.progress_percentage_var.set(f"{int(percentage)}%")
        self.parent.update_idletasks()
        self.parent.update()
        time.sleep(0.05)
    
    def get_detailed_error_message(self, exception):
        """Memberikan pesan error yang lebih jelas untuk user"""
        error_str = str(exception).lower()
        
        if "permission denied" in error_str or "access is denied" in error_str:
            return (f"❌ Error Akses File:\n"
                   f"Tidak dapat mengakses file atau folder.\n\n"
                   f"Solusi:\n"
                   f"• Tutup file PDF yang sedang terbuka\n"
                   f"• Pastikan folder tidak readonly\n"
                   f"• Jalankan sebagai administrator\n"
                   f"• Periksa antivirus yang mungkin memblokir\n\n"
                   f"Detail: {str(exception)}")
        
        elif "no such file or directory" in error_str or "cannot find" in error_str:
            return (f"❌ Error File Tidak Ditemukan:\n"
                   f"File atau folder yang dipilih tidak ada.\n\n"
                   f"Solusi:\n"
                   f"• Periksa apakah folder input masih ada\n"
                   f"• Pilih ulang folder input\n"
                   f"• Pastikan tidak ada file yang dipindah/dihapus\n\n"
                   f"Detail: {str(exception)}")
        
        elif "memory" in error_str or "out of memory" in error_str:
            return (f"❌ Error Memori:\n"
                   f"Tidak cukup memori untuk memproses file.\n\n"
                   f"Solusi:\n"
                   f"• Tutup aplikasi lain yang tidak perlu\n"
                   f"• Proses file dalam batch yang lebih kecil\n"
                   f"• Restart aplikasi jika perlu\n\n"
                   f"Detail: {str(exception)}")
        
        elif "corrupted" in error_str or "invalid pdf" in error_str:
            return (f"❌ Error File PDF Rusak:\n"
                   f"Ada file PDF yang rusak atau tidak valid.\n\n"
                   f"Solusi:\n"
                   f"• Periksa file PDF secara manual\n"
                   f"• Pisahkan file yang bermasalah\n"
                   f"• Coba repair PDF dengan tools lain\n\n"
                   f"Detail: {str(exception)}")
        
        elif "filename too long" in error_str or "path too long" in error_str:
            return (f"❌ Error Nama File Terlalu Panjang:\n"
                   f"Nama file hasil melebihi batas Windows (260 karakter).\n\n"
                   f"Solusi:\n"
                   f"• Gunakan referensi yang lebih pendek\n"
                   f"• Pindah ke folder dengan path lebih pendek\n"
                   f"• Aktifkan 'Long Path Support' di Windows\n\n"
                   f"Detail: {str(exception)}")
        
        elif "division by zero" in error_str:
            return (f"❌ Error Perhitungan Progress:\n"
                   f"Terjadi kesalahan dalam menghitung progress.\n\n"
                   f"Solusi:\n"
                   f"• Pastikan ada file PDF di folder input\n"
                   f"• Coba restart aplikasi\n"
                   f"• Pilih ulang folder input\n\n"
                   f"Detail: {str(exception)}")
        
        else:
            return (f"❌ Error Tidak Terduga:\n"
                   f"Terjadi kesalahan yang tidak diketahui.\n\n"
                   f"Solusi:\n"
                   f"• Restart aplikasi\n"
                   f"• Periksa file log untuk detail\n"
                   f"• Hubungi developer jika masalah berlanjut\n\n"
                   f"Detail: {str(exception)}")

    def set_button_state(self, state):
        """Enable or disable the process button through GUI reference"""
        if hasattr(self.gui, 'file_input_output') and hasattr(self.gui.file_input_output, 'process_btn'):
            self.gui.file_input_output.process_btn.configure(state=state)