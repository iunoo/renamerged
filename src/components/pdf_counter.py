import customtkinter as ctk
import tkinter as tk
import os
import time
import threading
from threading import Thread

class PDFCounterComponent:
    def __init__(self, parent, colors, input_path_var):
        self.parent = parent
        self.colors = colors
        self.input_path_var = input_path_var
        self.last_checked_path = ""
        self.check_thread = None
        
        # PDF Counter card
        self.counter_card = ctk.CTkFrame(
            self.parent,
            fg_color=self.colors["surface"],
            border_width=1,
            border_color=self.colors["border"],
            corner_radius=16
        )
        self.counter_card.grid(row=2, column=0, sticky="ew", pady=(0, 16), padx=4)
        self.counter_card.grid_columnconfigure(0, weight=1)

        # Content frame
        self.content_frame = ctk.CTkFrame(self.counter_card, fg_color="transparent")
        self.content_frame.pack(fill="x", padx=24, pady=16)
        self.content_frame.grid_columnconfigure(0, weight=0)
        self.content_frame.grid_columnconfigure(1, weight=1)
        self.content_frame.grid_columnconfigure(2, weight=0)

        # PDF icon and label
        self.pdf_icon = ctk.CTkLabel(
            self.content_frame,
            text="📄",
            font=("Inter", 20),
            anchor="w"
        )
        self.pdf_icon.grid(row=0, column=0, sticky="w", padx=(0, 12))

        # Counter text
        self.counter_label = ctk.CTkLabel(
            self.content_frame,
            text="📁 Pilih folder input terlebih dahulu untuk melihat jumlah PDF",
            font=("Inter", 13, "bold"),
            text_color=self.colors["text_muted"],
            anchor="w"
        )
        self.counter_label.grid(row=0, column=1, sticky="ew")

        # Status indicator
        self.status_indicator = ctk.CTkLabel(
            self.content_frame,
            text="⏳",
            font=("Inter", 16),
            anchor="e"
        )
        self.status_indicator.grid(row=0, column=2, sticky="e")

        # Thread management
        self.check_thread = None
        self.stop_flag = threading.Event()
        
        # Bind to path changes
        self.trace_id = self.input_path_var.trace('w', lambda *args: self.schedule_check())
        
    def schedule_check(self):
        """Schedule PDF count check with debouncing"""
        if self.stop_flag.is_set():
            return
            
        # Cancel existing thread if running
        if self.check_thread and self.check_thread.is_alive():
            # Signal existing thread to stop, but don't wait
            # New thread will handle the latest request
            pass
            
        # Small delay to avoid rapid checking while user is typing
        self.check_thread = Thread(target=self._delayed_check, daemon=True)
        self.check_thread.start()
    
    def _delayed_check(self):
        """Delayed check with debouncing"""
        # Check for stop signal during delay
        for _ in range(5):  # 5 x 100ms = 500ms total
            if self.stop_flag.is_set():
                return
            time.sleep(0.1)
        
        # Check again before proceeding
        if not self.stop_flag.is_set():
            self.check_pdf_count()
    
    def check_pdf_count(self):
        """Check and update PDF count for current input path"""
        if self.stop_flag.is_set():
            return
            
        current_path = self.input_path_var.get().strip()
        
        if not current_path:
            if not self.stop_flag.is_set():
                self.update_display("📁 Pilih folder input terlebih dahulu untuk melihat jumlah PDF", "⏳", self.colors["text_muted"])
            return
            
        if current_path == self.last_checked_path:
            return  # No change, no need to recheck
            
        self.last_checked_path = current_path
        
        if not os.path.exists(current_path):
            if not self.stop_flag.is_set():
                self.update_display("❌ Folder tidak ditemukan - Periksa path yang dimasukkan", "⚠️", self.colors["danger"])
            return
            
        if not os.path.isdir(current_path):
            if not self.stop_flag.is_set():
                self.update_display("❌ Path bukan folder yang valid - Pilih folder, bukan file", "⚠️", self.colors["danger"])
            return
        
        try:
            # Check for stop signal before file operations
            if self.stop_flag.is_set():
                return
                
            # Count PDF files
            pdf_files = [f for f in os.listdir(current_path) if f.lower().endswith('.pdf')]
            count = len(pdf_files)
            
            # Check for stop signal before updating display
            if self.stop_flag.is_set():
                return
            
            if count == 0:
                self.update_display("⚠️ Tidak ada file PDF ditemukan di folder ini", "❌", self.colors["warning"])
            elif count == 1:
                self.update_display("✅ 1 file PDF siap diproses", "✅", self.colors["success"])
            else:
                self.update_display(f"✅ {count} file PDF siap diproses", "✅", self.colors["success"])
                
        except PermissionError:
            self.update_display("❌ Tidak ada akses ke folder", "🔒", self.colors["danger"])
        except Exception as e:
            if not self.stop_flag.is_set():
                self.update_display("❌ Error membaca folder", "⚠️", self.colors["danger"])
    
    def stop_monitoring(self):
        """Stop PDF monitoring and clean up resources"""
        self.stop_flag.set()
        
        # Clean up trace callback
        try:
            self.input_path_var.trace_vdelete('w', self.trace_id)
        except:
            pass
        
        # Wait for thread to finish
        if self.check_thread and self.check_thread.is_alive():
            self.check_thread.join(timeout=1.0)
    
    def update_display(self, text, icon, color):
        """Update the display with new information"""
        if self.stop_flag.is_set():
            return
            
        def update_ui():
            if not self.stop_flag.is_set():
                self.counter_label.configure(text=text, text_color=color)
                self.status_indicator.configure(text=icon)
        
        # Schedule UI update on main thread
        self.parent.after(0, update_ui)
    
    def update_theme(self, colors):
        """Update theme colors for all components"""
        self.colors = colors
        
        # Update card styling
        self.counter_card.configure(
            fg_color=self.colors["surface"],
            border_color=self.colors["border"]
        )
        
        # Re-check to update colors properly
        self.check_pdf_count()