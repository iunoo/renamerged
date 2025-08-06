import customtkinter as ctk
import tkinter as tk

class DraggableComponent(ctk.CTkFrame):
    def __init__(self, parent, text, variable, on_select_callback, colors, width=250, height=48):
        super().__init__(
            parent, 
            fg_color=colors["surface"],
            border_width=2, 
            border_color=colors["border"],
            corner_radius=12, 
            width=width, 
            height=height
        )
        self.text = text
        self.variable = variable
        self.on_select_callback = on_select_callback
        self.colors = colors
        self.is_selected = False

        # Main container with better spacing
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=12, pady=10)
        self.content_frame.grid_columnconfigure(1, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        # Checkbox with modern styling
        self.checkbox = ctk.CTkCheckBox(
            self.content_frame, 
            text="",
            variable=self.variable,
            width=20,
            height=20,
            corner_radius=4,
            border_width=2,
            fg_color=self.colors["primary"],
            hover_color=self.colors["primary_hover"],
            border_color=self.colors["border_light"]
        )
        self.checkbox.grid(row=0, column=0, padx=(0, 16), sticky="w")

        # Label with improved typography and alignment
        self.label = ctk.CTkLabel(
            self.content_frame, 
            text=self.text,
            font=("Inter", 12, "bold"),
            text_color=self.colors["fg"],
            anchor="w",
            justify="left"
        )
        self.label.grid(row=0, column=1, sticky="ew", pady=1)

        # Selection indicator with proper alignment
        self.indicator = ctk.CTkLabel(
            self.content_frame,
            text="",
            font=("Inter", 14),
            width=24,
            anchor="center"
        )
        self.indicator.grid(row=0, column=2, padx=(12, 0), sticky="e")

        # Bind events
        self.bind("<Button-1>", self.select)
        self.content_frame.bind("<Button-1>", self.select)
        self.checkbox.bind("<Button-1>", self.select)
        self.label.bind("<Button-1>", self.select)

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.content_frame.bind("<Enter>", self.on_enter)
        self.content_frame.bind("<Leave>", self.on_leave)
        self.checkbox.bind("<Enter>", self.on_enter)
        self.checkbox.bind("<Leave>", self.on_leave)
        self.label.bind("<Enter>", self.on_enter)
        self.label.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        """Handle mouse enter - show hover effect"""
        if not self.is_selected:
            self.configure(
                fg_color=self.colors["surface_light"],
                border_color=self.colors["primary_hover"]
            )

    def on_leave(self, event):
        """Handle mouse leave - reset hover effect"""
        if not self.is_selected:
            self.configure(
                fg_color=self.colors["surface"],
                border_color=self.colors["border"]
            )

    def select(self, event):
        """Handle component selection"""
        if not self.is_selected:
            self.is_selected = True
            self.configure(
                fg_color=self.colors["primary"],
                border_color=self.colors["accent"]
            )
            self.label.configure(text_color="#FFFFFF")
            self.indicator.configure(text="🎯")
            self.on_select_callback(self)
        return "break"

    def deselect(self):
        """Deselect the component"""
        self.is_selected = False
        self.configure(
            fg_color=self.colors["surface"],
            border_color=self.colors["border"]
        )
        self.label.configure(text_color=self.colors["fg"])
        self.indicator.configure(text="")

    def update_theme(self, colors):
        """Update component colors when theme changes"""
        self.colors = colors
        
        if self.is_selected:
            self.configure(
                fg_color=self.colors["primary"],
                border_color=self.colors["accent"]
            )
            self.label.configure(text_color="#FFFFFF")
        else:
            self.configure(
                fg_color=self.colors["surface"],
                border_color=self.colors["border"]
            )
            self.label.configure(text_color=self.colors["fg"])
            
        # Update checkbox colors
        self.checkbox.configure(
            fg_color=self.colors["primary"],
            hover_color=self.colors["primary_hover"],
            border_color=self.colors["border_light"]
        )