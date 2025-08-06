import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

class FilenameWarningDialog:
    def __init__(self, parent, colors, long_filenames_count):
        self.parent = parent
        self.colors = colors
        self.long_filenames_count = long_filenames_count
        self.user_choice = None
        
    def show_warning(self):
        """Tampilkan dialog peringatan sederhana untuk filename panjang"""
        
        # Buat top-level window
        self.dialog = ctk.CTkToplevel(self.parent)
        self.dialog.title("Peringatan: Nama File Terlalu Panjang")
        self.dialog.geometry("520x350")
        self.dialog.resizable(False, False)
        
        # Center window
        self.dialog.transient(self.parent)
        self.dialog.grab_set()  # Make modal
        
        # Configure colors
        self.dialog.configure(fg_color=self.colors.get("bg", "#1a1a1a"))
        
        # Main frame
        main_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Warning icon and title
        title_label = ctk.CTkLabel(
            main_frame, 
            text="⚠️ Nama File Terlalu Panjang", 
            font=("Roboto", 18, "bold"),
            text_color="#FFA500"
        )
        title_label.pack(pady=(0, 15))
        
        # Problem explanation 
        problem_label = ctk.CTkLabel(
            main_frame,
            text=f"Ditemukan {self.long_filenames_count} file dengan REFERENSI terlalu panjang.\n\nReferensi yang panjang menyebabkan nama file melebihi batas\nWindows (260 karakter) dan proses akan gagal.",
            font=("Roboto", 12),
            text_color=self.colors.get("fg", "#ffffff"),
            justify="center"
        )
        problem_label.pack(pady=(0, 15))
        
        # Solution info
        frame_bg_color = self.colors.get("frame_bg", "#2d2d2d")  # Default fallback color
        info_frame = ctk.CTkFrame(main_frame, fg_color=frame_bg_color, corner_radius=10)
        info_frame.pack(fill="x", pady=(0, 20))
        
        info_text = (
            "✅ Solusi Otomatis (Sesuai Aturan Script):\n"
            "• Nama perusahaan dan tanggal tetap utuh\n"
            "• Referensi dipotong otomatis dengan tanda '...'\n"
            "• Maksimal 150 karakter per nama file\n"
            "• File akan berhasil dibuat tanpa error\n"
            "• Berlaku untuk SEMUA file dalam proses ini"
        )
        
        info_label = ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=("Roboto", 11),
            text_color=self.colors.get("fg", "#ffffff"),
            justify="left"
        )
        info_label.pack(padx=15, pady=15)
        
        # Buttons dengan spacing yang lebih baik
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(20, 10))
        
        # Cancel button (kiri)
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="❌ Batal",
            font=("Roboto", 12, "bold"),
            fg_color="#FF4444",
            hover_color="#CC3333",
            width=120,
            height=40,
            command=self.cancel_action
        )
        cancel_btn.pack(side="left", padx=(20, 10))
        
        # OK button (kanan) 
        ok_btn = ctk.CTkButton(
            button_frame,
            text="✅ OK, Sesuaikan & Lanjutkan",
            font=("Roboto", 12, "bold"),
            fg_color="#00AA00",
            hover_color="#008800",
            width=200,
            height=40,
            command=self.ok_action
        )
        ok_btn.pack(side="right", padx=(10, 20))
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (520 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (350 // 2)
        self.dialog.geometry(f"520x350+{x}+{y}")
        
        # Wait for user response
        self.dialog.wait_window()
        
        return self.user_choice
    
    def ok_action(self):
        """User memilih OK untuk melanjutkan dengan pemotongan otomatis"""
        self.user_choice = "ok"
        self.dialog.destroy()
    
    def cancel_action(self):
        """User memilih untuk membatalkan"""
        self.user_choice = "cancel"
        self.dialog.destroy()