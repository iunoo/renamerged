import customtkinter as ctk
import webbrowser

class HeaderComponent:
    def __init__(self, parent, colors, toggle_theme_callback):
        self.parent = parent
        self.colors = colors
        self.toggle_theme_callback = toggle_theme_callback

        # Main header card
        self.header_card = ctk.CTkFrame(
            self.parent, 
            fg_color=self.colors["surface"],
            border_width=1,
            border_color=self.colors["border"],
            corner_radius=16
        )
        self.header_card.grid(row=0, column=0, sticky="ew", pady=(0, 24), padx=4)
        self.header_card.grid_columnconfigure(0, weight=1)
        self.header_card.grid_columnconfigure(1, weight=0)

        # Title section
        self.title_frame = ctk.CTkFrame(self.header_card, fg_color="transparent")
        self.title_frame.grid(row=0, column=0, sticky="w", padx=24, pady=20)
        
        self.title_label = ctk.CTkLabel(
            self.title_frame, 
            text="🔄 RENAMERGED", 
            font=("Inter", 32, "bold"),
            text_color=self.colors["fg"],
            anchor="w"
        )
        self.title_label.grid(row=0, column=0, sticky="ew")
        
        self.subtitle_label = ctk.CTkLabel(
            self.title_frame, 
            text="Kelola & Organiser File PDF dengan Mudah", 
            font=("Inter", 14),
            text_color=self.colors["text_muted"],
            anchor="w"
        )
        self.subtitle_label.grid(row=1, column=0, sticky="ew", pady=(6, 0))

        # Action buttons frame
        self.action_frame = ctk.CTkFrame(self.header_card, fg_color="transparent")
        self.action_frame.grid(row=0, column=1, sticky="e", padx=24, pady=20)
        
        # Organize buttons in a cleaner layout
        self.donate_btn = ctk.CTkButton(
            self.action_frame, 
            text="💝 Donasi", 
            command=self.open_donate_link,
            fg_color=self.colors["danger"], 
            text_color="#FFFFFF",
            font=("Inter", 12, "bold"), 
            hover_color=self.colors["danger_hover"],
            width=110, 
            height=40, 
            border_width=0, 
            corner_radius=12
        )
        self.donate_btn.grid(row=0, column=0, padx=(0, 8))

        self.contact_btn = ctk.CTkButton(
            self.action_frame, 
            text="📞 Hubungi Dev", 
            command=self.open_contact_link,
            fg_color=self.colors["success"], 
            text_color="#FFFFFF",
            font=("Inter", 12, "bold"), 
            hover_color=self.colors["success_hover"],
            width=130, 
            height=40, 
            border_width=0, 
            corner_radius=12
        )
        self.contact_btn.grid(row=0, column=1, padx=(0, 8))

        self.theme_btn = ctk.CTkButton(
            self.action_frame, 
            text="🌓 Tema", 
            command=self.toggle_theme_callback,
            fg_color=self.colors["secondary"], 
            text_color="#FFFFFF",
            font=("Inter", 12, "bold"), 
            hover_color=self.colors["secondary_hover"],
            width=90, 
            height=40, 
            border_width=0, 
            corner_radius=12
        )
        self.theme_btn.grid(row=0, column=2)

    def open_donate_link(self):
        webbrowser.open("https://bit.ly/kiyuris")
    
    def open_contact_link(self):
        webbrowser.open("https://t.me/iunoin")

    def update_theme(self, colors):
        """Update theme colors for all components"""
        self.colors = colors
        
        # Update card styling
        self.header_card.configure(
            fg_color=self.colors["surface"], 
            border_color=self.colors["border"]
        )
        
        # Update title colors
        self.title_label.configure(text_color=self.colors["fg"])
        self.subtitle_label.configure(text_color=self.colors["text_muted"])
        
        # Update button colors with new theme
        self.donate_btn.configure(
            fg_color=self.colors["danger"], 
            hover_color=self.colors["danger_hover"]
        )
        self.contact_btn.configure(
            fg_color=self.colors["success"], 
            hover_color=self.colors["success_hover"]
        )
        self.theme_btn.configure(
            fg_color=self.colors["secondary"], 
            hover_color=self.colors["secondary_hover"]
        )