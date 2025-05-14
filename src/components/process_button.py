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

        self.process_btn = ctk.CTkButton(self.parent, text="Proses", command=self.process,
                                         fg_color="#1E3A8A", text_color="#FFFFFF",
                                         font=("Roboto", 12, "bold"), hover_color="#3B82F6",
                                         width=120, height=35, border_width=0, corner_radius=15)
        self.process_btn.grid(row=14, column=0, columnspan=2, pady=(20, 40))

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

        self.process_btn.configure(state="disabled")

        if not output_dir or output_dir.strip() == "":
            output_dir = os.path.join(input_dir, "ProcessedPDFs")
            os.makedirs(output_dir, exist_ok=True)
            self.output_path_var.set(output_dir)

        required_keys = ["use_name", "use_date", "use_reference", "use_faktur"]
        for key in required_keys:
            if not hasattr(self.settings.get(key), 'get'):
                messagebox.showerror("Error", f"Pengaturan {key} tidak valid!")
                self.process_btn.configure(state="normal")
                return

        self.settings["component_order"] = self.mode_selection.get_component_order()
        self.settings["separator"] = self.mode_selection.get_separator()
        self.settings["slash_replacement"] = self.mode_selection.get_slash_replacement()

        log_message(f"Debug: Pengaturan - component_order: {self.settings['component_order']}, "
                    f"use_name: {self.settings['use_name'].get()}, use_date: {self.settings['use_date'].get()}, "
                    f"use_reference: {self.settings['use_reference'].get()}, use_faktur: {self.settings['use_faktur'].get()}, "
                    f"separator: '{self.settings['separator']}', slash_replacement: '{self.settings['slash_replacement']}'", 
                    Fore.CYAN)

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
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")
        finally:
            self.process_btn.configure(state="normal")

    def log_callback(self, message):
        if self.statistics:
            self.statistics.log_message(message)

    def progress_callback(self, stage, current, total_files, total_to_merge, total_to_finalize):
        if stage == "reading":
            percentage = (current / total_files) * 40
        elif stage == "processing":
            percentage = 40 + (current / total_to_merge) * 40
        else:
            percentage = 80 + (current / total_to_finalize) * 20

        percentage = min(max(percentage, 0), 100)
        normalized_progress = percentage / 100

        self.gui.progress_bar.set_progress(normalized_progress)
        self.progress_var.set(normalized_progress)
        self.progress_percentage_var.set(f"{int(percentage)}%")
        self.parent.update_idletasks()
        self.parent.update()
        time.sleep(0.05)