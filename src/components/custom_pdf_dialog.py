import customtkinter as ctk
import os
import tkinter as tk
import threading
from src.utils.selection_handler import SelectionHandler

class CustomPDFDialog:
    def __init__(self, parent, colors):
        self.parent = parent
        self.colors = colors
        self.selected_folder = None
        self.current_path = os.path.expanduser("~")  # Mulai dari home directory
        self.loading = False  # Flag untuk thread loading
        self.dialog_open = True  # Flag untuk cek apakah dialog masih terbuka
        self.cache = {}  # Cache untuk menyimpan daftar file per path
        self.batch_size = 100  # Jumlah item yang dimuat per batch
        self.current_items = []  # Item yang sedang ditampilkan
        self.current_index = 0  # Indeks untuk lazy loading

        # Inisialisasi SelectionHandler
        self.selection_handler = SelectionHandler(self.colors)

        # Setup dialog
        self.dialog = ctk.CTkToplevel(self.parent)
        self.dialog.title("Pilih Folder PDF")
        self.dialog.geometry("900x600")
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        self.dialog.protocol("WM_DELETE_WINDOW", self._on_closing)

        # Main frame
        self.main_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Path and navigation frame
        self.nav_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.nav_frame.pack(fill="x", pady=(0, 10))
        self.path_var = ctk.StringVar(value=self.current_path)
        self.path_entry = ctk.CTkEntry(self.nav_frame, textvariable=self.path_var, width=600,
                                       fg_color=self.colors["entry_bg"], text_color=self.colors["entry_fg"],
                                       border_width=0, corner_radius=10, font=("Roboto", 12))
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.up_btn = ctk.CTkButton(self.nav_frame, text="⬆ Up", command=self._go_up,
                                    fg_color="#1E3A8A", text_color="#FFFFFF", hover_color="#3B82F6",
                                    font=("Roboto", 12, "bold"), width=100, height=35,
                                    border_width=0, corner_radius=15)
        self.up_btn.pack(side="right")

        # File list frame
        self.file_frame = ctk.CTkScrollableFrame(self.main_frame, fg_color=self.colors["entry_bg"], corner_radius=10)
        self.file_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Label untuk loading
        self.loading_label = ctk.CTkLabel(self.file_frame, text="Memuat...", font=("Roboto", 12),
                                          text_color=self.colors["fg"])
        self.loading_label.pack(pady=10)

        # Load more button (akan ditampilkan jika ada item yang belum dimuat)
        self.load_more_btn = ctk.CTkButton(self.file_frame, text="Load More", command=self._load_more,
                                           fg_color="#1E3A8A", text_color="#FFFFFF", hover_color="#3B82F6",
                                           font=("Roboto", 12, "bold"), width=120, height=35,
                                           border_width=0, corner_radius=15)

        # Buttons
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.pack(fill="x", pady=(10, 0))
        self.select_folder_btn = ctk.CTkButton(self.button_frame, text="Select this Folder",
                                               command=self._select_folder,
                                               fg_color="#1E3A8A", text_color="#FFFFFF", hover_color="#3B82F6",
                                               font=("Roboto", 12, "bold"), width=120, height=35,
                                               border_width=0, corner_radius=15)
        self.select_folder_btn.pack(side="right", padx=5)
        self.cancel_btn = ctk.CTkButton(self.button_frame, text="Batal", command=self._on_closing,
                                        fg_color="#1E3A8A", text_color="#FFFFFF", hover_color="#3B82F6",
                                        font=("Roboto", 12, "bold"), width=120, height=35,
                                        border_width=0, corner_radius=15)
        self.cancel_btn.pack(side="right", padx=5)

        # Bind path entry untuk update file list saat path berubah
        self.path_trace_id = self.path_var.trace("w", self._on_path_changed)

        # Mulai thread untuk memuat file list
        self._load_file_list_async()

    def _on_closing(self):
        """Dipanggil saat dialog ditutup."""
        self.dialog_open = False
        # Clean up trace callback
        try:
            self.path_var.trace_vdelete("w", self.path_trace_id)
        except:
            pass
        self.dialog.destroy()

    def _on_path_changed(self, *args):
        """Dipanggil saat path berubah, memulai thread untuk memuat file list."""
        if not self.loading and self.dialog_open:
            self._load_file_list_async()

    def _load_file_list_async(self):
        """Memuat daftar file secara asinkronus menggunakan thread."""
        if self.loading or not self.dialog_open:
            return
        self.loading = True
        self.current_items = []
        self.current_index = 0
        self.selection_handler.reset_selection()  # Reset seleksi saat memuat ulang
        self.loading_label.configure(text="Memuat...")
        self.loading_label.pack(pady=10)
        self.load_more_btn.pack_forget()
        self.file_frame.update_idletasks()

        # Mulai thread untuk memuat file
        thread = threading.Thread(target=self._fetch_file_list)
        thread.daemon = True  # Thread berhenti saat aplikasi ditutup
        thread.start()

    def _fetch_file_list(self):
        """Mengambil daftar file dan folder di thread terpisah, lalu update UI di main thread."""
        self.current_path = self.path_var.get()
        if not os.path.isdir(self.current_path):
            if self.dialog_open:
                self.dialog.after(0, self._update_ui, [], [], "Path tidak valid!")
            self.loading = False
            return

        try:
            # Gunakan os.scandir untuk efisiensi
            folders = []
            files = []
            if self.current_path in self.cache:
                # Gunakan cache jika path sudah pernah dimuat
                folders, files = self.cache[self.current_path]
            else:
                with os.scandir(self.current_path) as entries:
                    for entry in entries:
                        if not self.dialog_open:
                            break
                        if entry.is_dir():
                            folders.append(entry.name)
                        elif entry.name.endswith('.pdf'):
                            files.append(entry.name)
                folders.sort()
                files.sort()
                self.cache[self.current_path] = (folders, files)  # Simpan ke cache
            error_msg = None
        except Exception as e:
            folders = []
            files = []
            error_msg = f"Error: {str(e)}"

        # Jadwalkan update UI di main thread
        if self.dialog_open:
            self.current_items = folders + files
            self.current_index = 0
            self.dialog.after(0, self._update_ui, folders, files, error_msg)
        self.loading = False

    def _update_ui(self, folders, files, error_msg):
        """Memperbarui UI dengan daftar file dan folder di main thread."""
        if not self.dialog_open:
            return

        # Hapus semua item di file_frame kecuali loading label dan load more button
        for widget in self.file_frame.winfo_children():
            if widget != self.loading_label and widget != self.load_more_btn:
                widget.destroy()

        if error_msg:
            ctk.CTkLabel(self.file_frame, text=error_msg, font=("Roboto", 12),
                         text_color=self.colors["fg"]).pack(pady=10)
        else:
            # Tampilkan batch berikutnya
            start_index = self.current_index
            end_index = min(self.current_index + self.batch_size, len(self.current_items))
            for i in range(start_index, end_index):
                item = self.current_items[i]
                is_folder = i < len(folders)
                item_frame = ctk.CTkFrame(self.file_frame, fg_color=self.colors["entry_bg"])
                item_frame.pack(fill="x", pady=2)
                item_label = ctk.CTkLabel(item_frame, text=f"📁 {item}" if is_folder else f"📄 {item}",
                                          font=("Roboto", 12), text_color=self.colors["fg"], anchor="w")
                item_label.pack(side="left", fill="x", expand=True)
                if is_folder:
                    # Bind klik sekali untuk seleksi
                    item_label.bind("<Button-1>", lambda e, f=item_frame, n=item: self.selection_handler.select_item(f, n))
                    # Bind double-click untuk navigasi
                    item_label.bind("<Double-1>", lambda e, f=item: self._navigate_folder(f))
                    # Bind hover events
                    item_label.bind("<Enter>", lambda e, f=item_frame: self.selection_handler.on_item_enter(f))
                    item_label.bind("<Leave>", lambda e, f=item_frame: self.selection_handler.on_item_leave(f))
                    # Bind klik dan hover pada frame juga
                    item_frame.bind("<Button-1>", lambda e, f=item_frame, n=item: self.selection_handler.select_item(f, n))
                    item_frame.bind("<Double-1>", lambda e, f=item: self._navigate_folder(f))
                    item_frame.bind("<Enter>", lambda e, f=item_frame: self.selection_handler.on_item_enter(f))
                    item_frame.bind("<Leave>", lambda e, f=item_frame: self.selection_handler.on_item_leave(f))

            self.current_index = end_index

            # Tampilkan tombol Load More jika masih ada item yang belum dimuat
            if self.current_index < len(self.current_items):
                self.load_more_btn.pack(pady=10)
            else:
                self.load_more_btn.pack_forget()

        # Sembunyikan loading label
        self.loading_label.pack_forget()
        self.file_frame.update_idletasks()

    def _load_more(self):
        """Memuat batch berikutnya dari item."""
        if not self.dialog_open:
            return
        folders = [item for item in self.current_items if item in self.cache.get(self.current_path, ([], []))[0]]
        files = [item for item in self.current_items if item in self.cache.get(self.current_path, ([], []))[1]]
        self._update_ui(folders, files, None)

    def _navigate_folder(self, folder_name):
        """Navigasi ke folder yang dipilih."""
        if folder_name == "..":
            new_path = os.path.dirname(self.current_path)
        else:
            new_path = os.path.join(self.current_path, folder_name)
        self.current_path = new_path
        self.path_var.set(new_path)

    def _go_up(self):
        """Navigasi ke folder induk."""
        self._navigate_folder("..")

    def _select_folder(self):
        if os.path.isdir(self.current_path):
            self.selected_folder = self.current_path
        self._on_closing()

    def get_selected_folder(self):
        self.dialog.wait_window()
        return self.selected_folder