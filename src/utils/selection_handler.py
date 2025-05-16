import customtkinter as ctk

class SelectionHandler:
    def __init__(self, colors):
        self.colors = colors
        self.selected_item_frame = None
        self.normal_bg = self.colors["entry_bg"]  # Warna dari tema
        self.selected_bg = "#4CAF50"  # Hijau muda untuk background saat dipilih
        self.hover_bg = "#90CAF9"  # Biru muda untuk hover
        self.selected_border_color = "#FFD700"  # Kuning untuk border saat dipilih
        self.normal_border_color = self.colors["entry_bg"]  # Gunakan warna background agar menyatu

    def select_item(self, item_frame, folder_name=None):
        """Menangani seleksi item dengan mengubah warna background dan border."""
        # Reset warna frame yang sebelumnya dipilih
        if self.selected_item_frame and self.selected_item_frame != item_frame:
            self.selected_item_frame.configure(fg_color=self.normal_bg,
                                               border_color=self.normal_border_color,
                                               border_width=0)  # Nonaktifkan border
        # Set frame baru sebagai yang dipilih
        self.selected_item_frame = item_frame
        self.selected_item_frame.configure(fg_color=self.selected_bg,
                                           border_color=self.selected_border_color,
                                           border_width=2)

    def on_item_enter(self, item_frame):
        """Menangani event saat kursor masuk ke item (hover)."""
        if item_frame != self.selected_item_frame:
            item_frame.configure(fg_color=self.hover_bg)

    def on_item_leave(self, item_frame):
        """Menangani event saat kursor keluar dari item."""
        if item_frame != self.selected_item_frame:
            item_frame.configure(fg_color=self.normal_bg)

    def reset_selection(self):
        """Reset seleksi saat memuat ulang daftar."""
        if self.selected_item_frame:
            self.selected_item_frame.configure(fg_color=self.normal_bg,
                                               border_color=self.normal_border_color,
                                               border_width=0)  # Nonaktifkan border
        self.selected_item_frame = None

    def update_theme(self, colors):
        """Memperbarui warna saat tema berubah."""
        self.colors = colors
        self.normal_bg = self.colors["entry_bg"]  # Update sesuai tema
        self.selected_bg = "#4CAF50"  # Bisa disesuaikan dengan tema kalau perlu
        self.hover_bg = "#90CAF9"
        self.selected_border_color = "#FFD700"
        self.normal_border_color = self.colors["entry_bg"]
        if self.selected_item_frame:
            self.selected_item_frame.configure(fg_color=self.selected_bg,
                                               border_color=self.selected_border_color,
                                               border_width=2)