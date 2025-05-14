import customtkinter as ctk
import tkinter as tk

class Tooltip:
    def __init__(self, widget, text, colors, parent, tooltips, container):
        self.widget = widget
        self.text = text
        self.colors = colors
        self.parent = parent  # ModeSelectionComponent untuk akses tooltips
        self.tooltips = tooltips  # Daftar tooltip lain
        self.container = container  # Frame yang berisi widget (untuk binding Motion)
        self.tooltip_window = None
        self.show_id = None
        self.hide_id = None
        self.enabled = True
        self.widget.bind("<Enter>", self.schedule_show)
        self.widget.bind("<Leave>", self.schedule_hide)
        self.container.bind("<Motion>", self.check_motion)

    def schedule_show(self, event):
        if not self.enabled or self.tooltip_window:
            return
        if self.hide_id:
            self.widget.after_cancel(self.hide_id)
            self.hide_id = None
        # Hancurkan tooltip lain yang aktif
        for other_tooltip in self.tooltips:
            if other_tooltip != self and other_tooltip.tooltip_window:
                other_tooltip.hide_tooltip()
        self.show_id = self.widget.after(100, self.show_tooltip)

    def show_tooltip(self):
        if not self.enabled or self.tooltip_window:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20
        self.tooltip_window = ctk.CTkToplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        label = ctk.CTkLabel(self.tooltip_window, text=self.text, font=("Roboto", 10),
                             fg_color=self.colors["entry_bg"], text_color=self.colors["fg"],
                             corner_radius=5, padx=5, pady=2)
        label.pack()
        self.show_id = None

    def schedule_hide(self, event):
        if not self.tooltip_window:
            return
        if self.show_id:
            self.widget.after_cancel(self.show_id)
            self.show_id = None
        self.hide_id = self.widget.after(500, self.hide_tooltip)

    def hide_tooltip(self):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None
            self.hide_id = None

    def check_motion(self, event):
        """Periksa apakah kursor masih di dalam widget."""
        if not self.tooltip_window or not self.enabled:
            return
        widget_x = self.widget.winfo_rootx()
        widget_y = self.widget.winfo_rooty()
        widget_width = self.widget.winfo_width()
        widget_height = self.widget.winfo_height()
        cursor_x = event.x_root
        cursor_y = event.y_root
        if not (widget_x <= cursor_x <= widget_x + widget_width and
                widget_y <= cursor_y <= widget_y + widget_height):
            self.schedule_hide(event)

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False
        self.hide_tooltip()

    def update_theme(self, colors):
        self.colors = colors
        # Tooltip akan otomatis menggunakan warna baru saat dibuat ulang