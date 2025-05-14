import customtkinter as ctk
import webbrowser

class HeaderComponent:
    def __init__(self, parent, colors, toggle_theme_callback):
        self.parent = parent
        self.colors = colors
        self.toggle_theme_callback = toggle_theme_callback

        # Judul
        self.title_label = ctk.CTkLabel(self.parent, text="RENAMERGED", font=("Poppins", 28, "bold"),
                                        text_color=self.colors["fg"])
        self.title_label.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 10))

        # Frame untuk tombol Donasi dan Ganti Tema
        self.top_button_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.top_button_frame.grid(row=1, column=1, sticky="e", pady=(0, 10))
        self.top_button_frame.grid_columnconfigure(0, weight=0)
        self.top_button_frame.grid_columnconfigure(1, weight=0)

        self.donate_btn = ctk.CTkButton(self.top_button_frame, text="Donasi", command=self.open_donate_link,
                                        fg_color="#E63946", text_color="#FFFFFF",  # Warna merah
                                        font=("Roboto", 12, "bold"), hover_color="#D00000",  # Hover merah lebih gelap
                                        width=120, height=35, border_width=0, corner_radius=15)
        self.donate_btn.grid(row=0, column=0, padx=5)

        self.theme_btn = ctk.CTkButton(self.top_button_frame, text="Ganti Tema", command=self.toggle_theme_callback,
                                       fg_color="#1E3A8A", text_color="#FFFFFF",
                                       font=("Roboto", 12, "bold"), hover_color="#3B82F6",
                                       width=120, height=35, border_width=0, corner_radius=15)
        self.theme_btn.grid(row=0, column=1, padx=5)

    def open_donate_link(self):
        webbrowser.open("https://bit.ly/kiyuris")

    def update_theme(self, colors):
        self.colors = colors
        self.title_label.configure(text_color=self.colors["fg"])
        self.top_button_frame.configure(fg_color="transparent")
        self.donate_btn.configure(fg_color="#E63946", text_color="#FFFFFF", hover_color="#D00000")  # Tetap merah
        self.theme_btn.configure(fg_color="#1E3A8A", text_color=self.colors["button_fg"], hover_color="#3B82F6")