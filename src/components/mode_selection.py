import customtkinter as ctk
import tkinter as tk
from src.components.draggable_component import DraggableComponent
from src.components.tooltip import Tooltip

class ModeSelectionComponent:
    def __init__(self, parent, colors, mode_var, settings, separator_var=None, slash_replacement_var=None):
        self.parent = parent
        self.colors = colors
        self.mode_var = mode_var
        self.settings = settings
        self.separator_var = separator_var
        self.slash_replacement_var = slash_replacement_var
        self.components = []
        self.component_order = []
        self.selected_component = None
        self.tooltips = []

        # Pemetaan untuk konversi display ke nilai aktual
        self.option_mapping = {
            "(spasi)": " ",
            "-": "-",
            "_": "_"
        }
        self.reverse_mapping = {v: k for k, v in self.option_mapping.items()}

        self.mode_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.mode_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))
        ctk.CTkLabel(self.mode_frame, text="Mode Pemrosesan:", font=("Roboto", 12),
                     text_color=self.colors["fg"]).pack(side="left", padx=(0, 10))
        self.mode_menu = ctk.CTkOptionMenu(self.mode_frame, values=["Rename Saja", "Rename dan Merge"],
                                           variable=self.mode_var, command=self.toggle_mode_options,
                                           fg_color="#1E3A8A", text_color="#FFFFFF",
                                           font=("Roboto", 12), width=150, height=35, corner_radius=15)
        self.mode_menu.pack(side="left")

        self.name_components_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.name_components_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))

        ctk.CTkLabel(self.name_components_frame, text="Komponen Nama File (untuk Rename Saja):", font=("Roboto", 12),
                     text_color=self.colors["fg"]).grid(row=0, column=0, sticky="w", padx=(0, 10), pady=(0, 2))

        self.separator_frame = ctk.CTkFrame(self.name_components_frame, fg_color="transparent")
        self.separator_frame.grid(row=2, column=0, sticky="w", padx=(0, 10), pady=(0, 5))
        separator_label = ctk.CTkLabel(self.separator_frame, text="Pemisah Nama File PDF:", font=("Roboto", 12),
                                       text_color=self.colors["fg"])
        separator_label.pack(side="left", padx=(0, 5))
        separator_tooltip_btn = ctk.CTkButton(self.separator_frame, text="?", width=20, height=20,
                                             fg_color="#1E3A8A", text_color="#FFFFFF", font=("Roboto", 10),
                                             corner_radius=10, command=lambda: None)
        separator_tooltip_btn.pack(side="left", padx=(0, 5))
        separator_tooltip = Tooltip(separator_tooltip_btn, "Pilih pemisah untuk memisahkan komponen nama file PDF (misalnya, Nama-Tanggal atau Nama_Tanggal).", self.colors, self, self.tooltips, self.separator_frame)
        self.tooltips.append(separator_tooltip)
        self.separator_menu = ctk.CTkOptionMenu(self.separator_frame, values=["-", "_", "(spasi)"],
                                               variable=self.separator_var, fg_color="#1E3A8A", text_color="#FFFFFF",
                                               font=("Roboto", 12), width=100, height=35, corner_radius=15)
        self.separator_menu.pack(side="left")

        self.slash_replacement_frame = ctk.CTkFrame(self.name_components_frame, fg_color="transparent")
        self.slash_replacement_frame.grid(row=3, column=0, sticky="w", padx=(0, 10), pady=(0, 5))
        slash_label = ctk.CTkLabel(self.slash_replacement_frame, text="Pengganti Garis Miring untuk Referensi:", font=("Roboto", 12),
                                   text_color=self.colors["fg"])
        slash_label.pack(side="left", padx=(0, 5))
        slash_tooltip_btn = ctk.CTkButton(self.slash_replacement_frame, text="?", width=20, height=20,
                                         fg_color="#1E3A8A", text_color="#FFFFFF", font=("Roboto", 10),
                                         corner_radius=10, command=lambda: None)
        slash_tooltip_btn.pack(side="left", padx=(0, 5))
        slash_tooltip = Tooltip(slash_tooltip_btn, "Pilih karakter untuk mengganti garis miring (/) di referensi agar nama file valid (misalnya, Ref/123 jadi Ref_123).", self.colors, self, self.tooltips, self.slash_replacement_frame)
        self.tooltips.append(slash_tooltip)
        self.slash_replacement_menu = ctk.CTkOptionMenu(self.slash_replacement_frame, values=["-", "_", "(spasi)"],
                                                       variable=self.slash_replacement_var, fg_color="#1E3A8A", text_color="#FFFFFF",
                                                       font=("Roboto", 12), width=100, height=35, corner_radius=15)
        self.slash_replacement_menu.pack(side="left")

        self.components_container = ctk.CTkFrame(self.name_components_frame, fg_color="transparent", border_width=2, border_color=self.colors["button_bg"])
        self.components_container.grid(row=4, column=0, columnspan=5, sticky="ew", padx=(10, 10))

        ctk.CTkLabel(self.name_components_frame, text="Klik untuk memilih, lalu gunakan panah kiri/kanan untuk menggeser.", font=("Roboto", 10, "italic"),
                     text_color="#BBBBBB").grid(row=5, column=0, sticky="w", padx=(0, 10), pady=(5, 0))

        self.component_order = [
            ("Nama Lawan Transaksi", self.settings["use_name"]),
            ("Tanggal Faktur Pajak", self.settings["use_date"]),
            ("Referensi", self.settings["use_reference"]),
            ("Nomor Faktur Pajak", self.settings["use_faktur"])
        ]
        self._create_components()

        self.parent.bind("<Left>", self.move_left)
        self.parent.bind("<Right>", self.move_right)

        self.toggle_mode_options(self.mode_var.get())

    def _create_components(self):
        self.components = []
        for text, var in self.component_order:
            if not hasattr(var, 'get'):
                raise ValueError(f"Komponen {text} memiliki variabel yang tidak valid: {var}")
            component = DraggableComponent(self.components_container, text, var, self._on_select, self.colors)
            component.pack(side="left", padx=10, pady=5)
            self.components.append(component)
        self._update_order()

    def _on_select(self, selected_component):
        for component in self.components:
            if component != selected_component:
                component.deselect()
        self.selected_component = selected_component

    def move_left(self, event):
        if self.selected_component and self.mode_var.get() == "Rename Saja":
            current_index = self.components.index(self.selected_component)
            if current_index > 0:
                self.components[current_index], self.components[current_index - 1] = self.components[current_index - 1], self.components[current_index]
                self._refresh_layout()
                self._update_order()

    def move_right(self, event):
        if self.selected_component and self.mode_var.get() == "Rename Saja":
            current_index = self.components.index(self.selected_component)
            if current_index < len(self.components) - 1:
                self.components[current_index], self.components[current_index + 1] = self.components[current_index + 1], self.components[current_index]
                self._refresh_layout()
                self._update_order()

    def _refresh_layout(self):
        for component in self.components:
            component.pack_forget()
        for component in self.components:
            component.pack(side="left", padx=10, pady=5)

    def _update_order(self):
        self.component_order = [(comp.text, comp.variable) for comp in self.components]

    def get_component_order(self):
        return [text for text, _ in self.component_order]

    def get_separator(self):
        """Mengembalikan nilai aktual pemisah berdasarkan pilihan user."""
        return self.option_mapping.get(self.separator_var.get(), "-")

    def get_slash_replacement(self):
        """Mengembalikan nilai aktual pengganti garis miring berdasarkan pilihan user."""
        return self.option_mapping.get(self.slash_replacement_var.get(), "_")

    def toggle_mode_options(self, mode):
        if mode == "Rename Saja":
            self.name_components_frame.grid()
        else:
            self.name_components_frame.grid_remove()

    def update_theme(self, colors):
        self.colors = colors
        for tooltip in self.tooltips:
            tooltip.disable()
        for child in self.mode_frame.winfo_children():
            if isinstance(child, ctk.CTkLabel):
                child.configure(text_color=self.colors["fg"])
        self.mode_menu.configure(fg_color="#1E3A8A", text_color="#FFFFFF")
        for child in self.name_components_frame.winfo_children():
            if isinstance(child, ctk.CTkLabel):
                child.configure(text_color="#BBBBBB" if child.cget("text").startswith("Klik") else self.colors["fg"])
        for child in self.separator_frame.winfo_children():
            if isinstance(child, ctk.CTkLabel):
                child.configure(text_color=self.colors["fg"])
            if isinstance(child, ctk.CTkButton):
                child.configure(fg_color="#1E3A8A", text_color="#FFFFFF")
        for child in self.slash_replacement_frame.winfo_children():
            if isinstance(child, ctk.CTkLabel):
                child.configure(text_color=self.colors["fg"])
            if isinstance(child, ctk.CTkButton):
                child.configure(fg_color="#1E3A8A", text_color="#FFFFFF")
        self.separator_menu.configure(fg_color="#1E3A8A", text_color="#FFFFFF")
        self.slash_replacement_menu.configure(fg_color="#1E3A8A", text_color="#FFFFFF")
        self.components_container.configure(border_color=self.colors["button_bg"])
        for component in self.components:
            component.update_theme(colors)
        for tooltip in self.tooltips:
            tooltip.enable()