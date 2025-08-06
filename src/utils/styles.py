class Theme:
    def __init__(self):
        # Modern color palette untuk tema dark
        self.dark = {
            "bg": "#0F172A",           # Slate-900 - Background utama
            "fg": "#F8FAFC",           # Slate-50 - Text utama
            "surface": "#1E293B",      # Slate-800 - Card/surface
            "surface_light": "#334155", # Slate-700 - Surface hover
            "primary": "#6366F1",      # Indigo-500 - Primary button
            "primary_hover": "#4F46E5", # Indigo-600 - Primary hover
            "secondary": "#8B5CF6",    # Violet-500 - Secondary
            "secondary_hover": "#7C3AED", # Violet-600 - Secondary hover
            "success": "#10B981",      # Emerald-500 - Success
            "success_hover": "#059669", # Emerald-600 - Success hover
            "danger": "#EF4444",       # Red-500 - Danger
            "danger_hover": "#DC2626", # Red-600 - Danger hover
            "warning": "#F59E0B",      # Amber-500 - Warning
            "info": "#06B6D4",         # Cyan-500 - Info
            "border": "#475569",       # Slate-600 - Borders
            "border_light": "#64748B", # Slate-500 - Light borders
            "text_muted": "#94A3B8",   # Slate-400 - Muted text
            "accent": "#F472B6",       # Pink-400 - Accent color
            
            # Legacy compatibility
            "entry_bg": "#1E293B",
            "entry_fg": "#F8FAFC", 
            "button_bg": "#6366F1",
            "button_fg": "#F8FAFC",
            "button_hover_bg": "#4F46E5",
            "listbox_bg": "#1E293B",
            "listbox_fg": "#F8FAFC",
            "log_bg": "#1E293B",
            "log_fg": "#F8FAFC",
            "status_fg": "#F8FAFC",
        }

        # Modern color palette untuk tema light  
        self.light = {
            "bg": "#FFFFFF",           # White - Background utama
            "fg": "#0F172A",           # Slate-900 - Text utama
            "surface": "#F8FAFC",      # Slate-50 - Card/surface
            "surface_light": "#F1F5F9", # Slate-100 - Surface hover
            "primary": "#6366F1",      # Indigo-500 - Primary button
            "primary_hover": "#4F46E5", # Indigo-600 - Primary hover
            "secondary": "#8B5CF6",    # Violet-500 - Secondary
            "secondary_hover": "#7C3AED", # Violet-600 - Secondary hover
            "success": "#10B981",      # Emerald-500 - Success
            "success_hover": "#059669", # Emerald-600 - Success hover
            "danger": "#EF4444",       # Red-500 - Danger
            "danger_hover": "#DC2626", # Red-600 - Danger hover
            "warning": "#F59E0B",      # Amber-500 - Warning
            "info": "#06B6D4",         # Cyan-500 - Info
            "border": "#E2E8F0",       # Slate-200 - Borders
            "border_light": "#CBD5E1", # Slate-300 - Light borders
            "text_muted": "#64748B",   # Slate-500 - Muted text
            "accent": "#EC4899",       # Pink-500 - Accent color
            
            # Legacy compatibility
            "entry_bg": "#F8FAFC",
            "entry_fg": "#0F172A",
            "button_bg": "#6366F1", 
            "button_fg": "#FFFFFF",
            "button_hover_bg": "#4F46E5",
            "listbox_bg": "#F8FAFC",
            "listbox_fg": "#0F172A",
            "log_bg": "#F8FAFC",
            "log_fg": "#0F172A",
            "status_fg": "#0F172A",
        }

        # Modern typography system
        self.fonts = {
            "title": ("Inter", 28, "bold"),         # Judul utama
            "heading": ("Inter", 20, "bold"),       # Sub-heading
            "subheading": ("Inter", 16, "bold"),    # Sub-heading kecil
            "body": ("Inter", 12),                  # Body text
            "body_bold": ("Inter", 12, "bold"),     # Body text bold
            "caption": ("Inter", 10),               # Caption/small text
            "button": ("Inter", 12, "bold"),        # Button text
            "code": ("JetBrains Mono", 11),         # Monospace code
        }
        
        # Legacy font compatibility
        self.title_font = self.fonts["title"]
        self.label_font = self.fonts["body"]
        self.button_font = self.fonts["button"]
        self.listbox_font = self.fonts["caption"]
        
        # Spacing system (8px base unit)
        self.spacing = {
            "xs": 4,    # 0.5 unit
            "sm": 8,    # 1 unit  
            "md": 16,   # 2 units
            "lg": 24,   # 3 units
            "xl": 32,   # 4 units
            "2xl": 48,  # 6 units
        }
        
        # Border radius system
        self.radius = {
            "sm": 6,    # Small radius
            "md": 10,   # Medium radius  
            "lg": 16,   # Large radius
            "xl": 20,   # Extra large radius
            "full": 999 # Fully rounded
        }

    def get_colors(self, theme):
        """Mengembalikan warna berdasarkan tema yang dipilih."""
        if theme == "dark":
            return self.dark
        else:
            return self.light