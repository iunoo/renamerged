import customtkinter as ctk
import tkinter as tk
import os
from tkinter import filedialog
from src.pdf.pdf_utils import validate_pdf
from src.components.custom_pdf_dialog import CustomPDFDialog

class FileInputOutputComponent:
    def __init__(self, parent, colors, input_path_var, output_path_var):
        self.parent = parent
        self.colors = colors
        self.input_path_var = input_path_var
        self.output_path_var = output_path_var

        # File paths card
        self.file_paths_card = ctk.CTkFrame(
            self.parent,
            fg_color=self.colors["surface"],
            border_width=1,
            border_color=self.colors["border"],
            corner_radius=16
        )
        self.file_paths_card.grid(row=1, column=0, sticky="ew", pady=(0, 16), padx=4)
        self.file_paths_card.grid_columnconfigure(0, weight=1)

        # Card header
        self.card_header = ctk.CTkLabel(
            self.file_paths_card,
            text="📁 Lokasi File",
            font=("Inter", 18, "bold"),
            text_color=self.colors["fg"],
            anchor="w"
        )
        self.card_header.grid(row=0, column=0, sticky="ew", padx=24, pady=(20, 16))

        # Input folder section
        self.input_section = ctk.CTkFrame(self.file_paths_card, fg_color="transparent")
        self.input_section.grid(row=1, column=0, sticky="ew", padx=24, pady=(0, 20))
        self.input_section.grid_columnconfigure(0, weight=1)

        self.input_label = ctk.CTkLabel(
            self.input_section,
            text="📂 Folder Input PDF",
            font=("Inter", 13, "bold"),
            text_color=self.colors["fg"],
            anchor="w"
        )
        self.input_label.grid(row=0, column=0, sticky="w", pady=(0, 4))
        
        # Add instruction for input folder
        self.input_instruction = ctk.CTkLabel(
            self.input_section,
            text="💡 Bisa langsung paste path lokasi PDF disini",
            font=("Inter", 10, "italic"),
            text_color=self.colors["text_muted"],
            anchor="w"
        )
        self.input_instruction.grid(row=1, column=0, sticky="w", pady=(0, 8))

        self.input_frame = ctk.CTkFrame(self.input_section, fg_color="transparent")
        self.input_frame.grid(row=2, column=0, sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.input_entry = ctk.CTkEntry(
            self.input_frame,
            textvariable=self.input_path_var,
            height=44,
            fg_color=self.colors["entry_bg"],
            text_color=self.colors["entry_fg"],
            border_width=1,
            border_color=self.colors["border"],
            corner_radius=12,
            font=("Inter", 12),
            placeholder_text="Pilih folder yang berisi file PDF..."
        )
        self.input_entry.grid(row=0, column=0, sticky="ew", padx=(0, 12))

        self.browse_input_btn = ctk.CTkButton(
            self.input_frame,
            text="🔍 Browse",
            command=self.browse_input,
            fg_color=self.colors["primary"],
            text_color="#FFFFFF",
            font=("Inter", 12, "bold"),
            hover_color=self.colors["primary_hover"],
            width=100,
            height=44,
            border_width=0,
            corner_radius=12
        )
        self.browse_input_btn.grid(row=0, column=1)

        # Output folder section
        self.output_section = ctk.CTkFrame(self.file_paths_card, fg_color="transparent")
        self.output_section.grid(row=2, column=0, sticky="ew", padx=24, pady=(0, 24))
        self.output_section.grid_columnconfigure(0, weight=1)

        self.output_label = ctk.CTkLabel(
            self.output_section,
            text="💾 Folder Output (Opsional)",
            font=("Inter", 13, "bold"),
            text_color=self.colors["fg"],
            anchor="w"
        )
        self.output_label.grid(row=0, column=0, sticky="w", pady=(0, 10))

        self.output_frame = ctk.CTkFrame(self.output_section, fg_color="transparent")
        self.output_frame.grid(row=1, column=0, sticky="ew")
        self.output_frame.grid_columnconfigure(0, weight=1)

        self.output_entry = ctk.CTkEntry(
            self.output_frame,
            textvariable=self.output_path_var,
            height=44,
            fg_color=self.colors["entry_bg"],
            text_color=self.colors["entry_fg"],
            border_width=1,
            border_color=self.colors["border"],
            corner_radius=12,
            font=("Inter", 12),
            placeholder_text="Default: ProcessedPDFs di folder input"
        )
        self.output_entry.grid(row=0, column=0, sticky="ew", padx=(0, 12))

        self.browse_output_btn = ctk.CTkButton(
            self.output_frame,
            text="🔍 Browse",
            command=self.browse_output,
            fg_color=self.colors["primary"],
            text_color="#FFFFFF",
            font=("Inter", 12, "bold"),
            hover_color=self.colors["primary_hover"],
            width=100,
            height=44,
            border_width=0,
            corner_radius=12
        )
        self.browse_output_btn.grid(row=0, column=1)

        # Process button section - aligned with browse buttons
        self.process_section = ctk.CTkFrame(self.file_paths_card, fg_color="transparent")
        self.process_section.grid(row=3, column=0, sticky="ew", padx=24, pady=(16, 24))
        self.process_section.grid_columnconfigure(0, weight=1)
        self.process_section.grid_columnconfigure(1, weight=0)

        # Process button frame for better alignment
        self.process_frame = ctk.CTkFrame(self.process_section, fg_color="transparent")
        self.process_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 0))
        self.process_frame.grid_columnconfigure(0, weight=1)
        
        # Large process button - centered but prominent
        self.process_btn = ctk.CTkButton(
            self.process_frame,
            text="🚀 Mulai Proses",
            command=None,  # Will be set by main GUI
            fg_color=self.colors["primary"],
            text_color="#FFFFFF",
            font=("Inter", 16, "bold"),
            hover_color=self.colors["primary_hover"],
            width=200,
            height=56,
            border_width=0,
            corner_radius=16
        )
        self.process_btn.grid(row=0, column=0, pady=8)

    def browse_input(self):
        popup = ctk.CTkToplevel(self.parent)
        popup.title("Pilih Folder Input PDF")
        popup.geometry("600x400")
        popup.transient(self.parent)
        popup.grab_set()

        main_frame = ctk.CTkFrame(popup)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        folder_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        folder_frame.pack(fill="x", pady=(0, 10))
        folder_path_var = ctk.StringVar()
        folder_entry = ctk.CTkEntry(folder_frame, textvariable=folder_path_var, width=400,
                                    fg_color=self.colors["entry_bg"], text_color=self.colors["entry_fg"],
                                    border_width=0, corner_radius=10)
        folder_entry.pack(side="left", padx=(0, 5))
        browse_btn = ctk.CTkButton(folder_frame, text="Browse", command=lambda: self._browse_folder(popup, folder_path_var),
                                   fg_color="#1E3A8A", text_color="#FFFFFF", hover_color="#3B82F6",
                                   font=("Roboto", 12, "bold"), width=120, height=35, border_width=0, corner_radius=15)
        browse_btn.pack(side="left", padx=(5, 0))

        total_pdf_var = ctk.StringVar(value="Total PDF Terdeteksi: 0")
        total_pdf_label = ctk.CTkLabel(main_frame, textvariable=total_pdf_var, font=("Roboto", 12))
        total_pdf_label.pack(anchor="w", padx=5)

        preview_frame = ctk.CTkFrame(main_frame)
        preview_frame.pack(fill="both", expand=True)
        ctk.CTkLabel(preview_frame, text="Pratinjau File PDF:", font=("Roboto", 12)).pack(anchor="w", padx=5)
        file_list = ctk.CTkTextbox(preview_frame, height=200)
        file_list.pack(fill="both", expand=True, padx=5, pady=5)
        file_list.configure(state="disabled")

        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill="x", pady=(10, 0))
        cancel_btn = ctk.CTkButton(button_frame, text="Batal", command=popup.destroy)
        cancel_btn.pack(side="right", padx=5)
        select_btn = ctk.CTkButton(button_frame, text="Pilih", command=lambda: self._select_folder(popup, folder_path_var))
        select_btn.pack(side="right", padx=5)

        trace_id = folder_path_var.trace("w", lambda *args: self._update_preview(folder_path_var, file_list, total_pdf_var))
        
        # Store trace ID for cleanup when popup is destroyed
        def cleanup_trace():
            try:
                folder_path_var.trace_vdelete("w", trace_id)
            except:
                pass
        
        popup.protocol("WM_DELETE_WINDOW", lambda: (cleanup_trace(), popup.destroy()))
        popup.update_idletasks()

    def _browse_folder(self, popup, folder_path_var):
        dialog = CustomPDFDialog(popup, self.colors)
        folder = dialog.get_selected_folder()
        if folder:
            folder_path_var.set(folder)

    def _update_preview(self, folder_path_var, file_list, total_pdf_var):
        folder = folder_path_var.get()
        file_list.configure(state="normal")
        file_list.delete("1.0", tk.END)
        if folder and os.path.isdir(folder):
            pdf_files = [f for f in os.listdir(folder) if f.endswith('.pdf') and validate_pdf(os.path.join(folder, f))]
            count = len(pdf_files)
            total_pdf_var.set(f"Total PDF Terdeteksi: {count}")
            for pdf_file in pdf_files:
                file_list.insert(tk.END, f"{pdf_file}\n")
        else:
            total_pdf_var.set("Total PDF Terdeteksi: 0")
        file_list.configure(state="disabled")

    def _select_folder(self, popup, folder_path_var):
        folder = folder_path_var.get()
        if folder:
            self.input_path_var.set(folder)
        popup.destroy()

    def browse_output(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_path_var.set(folder)

    def update_theme(self, colors):
        """Update theme colors for all components"""
        self.colors = colors
        
        # Update card styling
        self.file_paths_card.configure(
            fg_color=self.colors["surface"],
            border_color=self.colors["border"]
        )
        
        # Update labels
        self.card_header.configure(text_color=self.colors["fg"])
        self.input_label.configure(text_color=self.colors["fg"])
        self.input_instruction.configure(text_color=self.colors["text_muted"])
        self.output_label.configure(text_color=self.colors["fg"])
        
        # Update entries
        self.input_entry.configure(
            fg_color=self.colors["entry_bg"],
            text_color=self.colors["entry_fg"],
            border_color=self.colors["border"]
        )
        self.output_entry.configure(
            fg_color=self.colors["entry_bg"],
            text_color=self.colors["entry_fg"],
            border_color=self.colors["border"]
        )
        
        # Update buttons
        self.browse_input_btn.configure(
            fg_color=self.colors["primary"],
            hover_color=self.colors["primary_hover"]
        )
        self.browse_output_btn.configure(
            fg_color=self.colors["primary"],
            hover_color=self.colors["primary_hover"]
        )
        
        # Update process button if exists
        if hasattr(self, 'process_btn'):
            self.process_btn.configure(
                fg_color=self.colors["primary"],
                hover_color=self.colors["primary_hover"]
            )
    
    def set_process_command(self, command):
        """Set command for the process button"""
        if hasattr(self, 'process_btn'):
            self.process_btn.configure(command=command)