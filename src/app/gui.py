import customtkinter as ctk
import tkinter as tk
import threading
from src.utils.styles import Theme
from src.utils.settings_manager import SettingsManager
from src.components.header import HeaderComponent
from src.components.mode_selection import ModeSelectionComponent
from src.components.file_input_output import FileInputOutputComponent
from src.components.file_list import FileListComponent
from src.components.progress_bar import ProgressBarComponent
from src.components.statistics import StatisticsComponent
from src.components.output_location import OutputLocationComponent
from src.components.process_button import ProcessButtonComponent

def run_gui():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    VERSION = "2.0.3"  # Ganti dengan versi yang diinginkan
    root.title(f"RENAMERGED v{VERSION} - Rename & Merge PDFs")
    root.geometry("1000x900")
    root.resizable(True, True)
    root.minsize(1000, 900)
    app = RenamergedGUI(root)
    root.mainloop()

class RenamergedGUI:
    def __init__(self, root):
        self.root = root
        self.theme = Theme()
        self.settings_manager = SettingsManager()
        
        # Load user settings
        saved_settings = self.settings_manager.load_settings()
        
        self.current_theme = saved_settings.get("theme", "dark")
        self.colors = self.theme.get_colors(self.current_theme)
        self.mode_var = ctk.StringVar(value=saved_settings.get("mode", "Rename dan Merge"))
        self.input_path_var = tk.StringVar(value=saved_settings.get("last_input_directory", ""))
        self.output_path_var = tk.StringVar(value=saved_settings.get("last_output_directory", ""))
        
        # Setup auto-save untuk perubahan settings dengan throttling
        self.mode_var.trace('w', lambda *args: self._throttled_save())
        self.input_path_var.trace('w', lambda *args: self._throttled_save())
        self.output_path_var.trace('w', lambda *args: self._throttled_save())
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_percentage_var = tk.StringVar(value="0%")
        self.separator_var = tk.StringVar(value=saved_settings.get("separator", "-"))
        self.slash_replacement_var = tk.StringVar(value=saved_settings.get("slash_replacement", "_"))
        
        # Auto-save untuk separator dan slash replacement dengan throttling
        self.separator_var.trace('w', lambda *args: self._throttled_save())
        self.slash_replacement_var.trace('w', lambda *args: self._throttled_save())

        self.settings = {
            "use_name": tk.BooleanVar(value=saved_settings.get("use_name", True)),
            "use_date": tk.BooleanVar(value=saved_settings.get("use_date", True)),
            "use_reference": tk.BooleanVar(value=saved_settings.get("use_reference", True)),
            "use_faktur": tk.BooleanVar(value=saved_settings.get("use_faktur", True)),
            "component_order": saved_settings.get("component_order", None)
        }
        
        # Auto-save untuk checkbox settings dengan throttling
        self._save_timer = None
        for key, var in self.settings.items():
            if hasattr(var, 'trace'):  # Hanya untuk StringVar, BooleanVar, dll
                var.trace('w', lambda *args: self._throttled_save())

        self.main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        self.main_frame.grid_rowconfigure(0, weight=0)
        self.main_frame.grid_rowconfigure(1, weight=0)
        self.main_frame.grid_rowconfigure(2, weight=0)
        self.main_frame.grid_rowconfigure(3, weight=0)
        self.main_frame.grid_rowconfigure(4, weight=0)
        self.main_frame.grid_rowconfigure(5, weight=0)
        self.main_frame.grid_rowconfigure(6, weight=0)
        self.main_frame.grid_rowconfigure(7, weight=0)
        self.main_frame.grid_rowconfigure(8, weight=0)
        self.main_frame.grid_rowconfigure(9, weight=0)
        self.main_frame.grid_rowconfigure(10, weight=0)
        self.main_frame.grid_rowconfigure(11, weight=0)
        self.main_frame.grid_rowconfigure(12, weight=0)
        self.main_frame.grid_rowconfigure(13, weight=0)
        self.main_frame.grid_rowconfigure(14, weight=0)
        self.main_frame.grid_rowconfigure(15, weight=0)
        self.main_frame.grid_rowconfigure(16, weight=0)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=0)

        self.header = HeaderComponent(self.main_frame, self.colors, self.switch_theme)
        self.mode_selection = ModeSelectionComponent(self.main_frame, self.colors, self.mode_var, self.settings, self.separator_var, self.slash_replacement_var)
        self.file_input_output = FileInputOutputComponent(self.main_frame, self.colors, self.input_path_var, self.output_path_var)
        self.file_list = FileListComponent(self.main_frame, self.colors, self.input_path_var)
        self.progress_bar = ProgressBarComponent(self.main_frame, self.colors, self.progress_var, self.progress_percentage_var)
        self.statistics = StatisticsComponent(self.main_frame, self.colors)
        self.output_location = OutputLocationComponent(self.main_frame, self.colors)
        self.process_button = ProcessButtonComponent(
            self.main_frame, self.colors, self.input_path_var, self.output_path_var,
            self.mode_var, self.settings, self.progress_var, self.progress_percentage_var,
            self.statistics, self.output_location, self.mode_selection, self
        )

        self.copyright_label = ctk.CTkLabel(self.main_frame, text="© 2025 Renamerged - All Rights Reserved",
                                            font=("Roboto", 10), text_color=self.colors["fg"])
        self.copyright_label.grid(row=16, column=0, columnspan=2, pady=(10, 20), sticky="s")

        self.root.bind("<Left>", lambda event: self.mode_selection.move_left(event))
        self.root.bind("<Right>", lambda event: self.mode_selection.move_right(event))
        
        # Setup window close handler untuk save settings
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def switch_theme(self):
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        ctk.set_appearance_mode(self.current_theme)
        self.colors = self.theme.get_colors(self.current_theme)
        self.root.configure(bg=self.colors["bg"])
        self.main_frame.configure(fg_color=self.colors["bg"])
        self.header.update_theme(self.colors)
        self.mode_selection.update_theme(self.colors)
        self.file_input_output.update_theme(self.colors)
        self.file_list.update_theme(self.colors)
        self.progress_bar.update_theme(self.colors)
        self.statistics.update_theme(self.colors)
        self.output_location.update_theme(self.colors)
        self.process_button.update_theme(self.colors)
        self.copyright_label.configure(text_color=self.colors["fg"])
        
        # Auto-save setelah ganti tema (langsung tanpa throttling)
        self.save_current_settings()
    
    def _throttled_save(self):
        """Save settings dengan delay untuk menghindari terlalu sering save"""
        if self._save_timer:
            self._save_timer.cancel()
        
        self._save_timer = threading.Timer(1.0, self.save_current_settings)  # Delay 1 detik
        self._save_timer.start()
    
    def save_current_settings(self):
        """Simpan settings saat ini ke file"""
        current_settings = {
            "theme": self.current_theme,
            "mode": self.mode_var,
            "last_input_directory": self.input_path_var,
            "last_output_directory": self.output_path_var,
            "separator": self.separator_var,
            "slash_replacement": self.slash_replacement_var,
            "use_name": self.settings["use_name"],
            "use_date": self.settings["use_date"],
            "use_reference": self.settings["use_reference"],
            "use_faktur": self.settings["use_faktur"],
            "component_order": self.settings.get("component_order", None)
        }
        
        return self.settings_manager.save_settings(current_settings)
    
    def on_closing(self):
        """Handler ketika aplikasi ditutup - save settings terlebih dahulu"""
        try:
            # Cancel any pending timer and save immediately
            if self._save_timer:
                self._save_timer.cancel()
            self.save_current_settings()
        except Exception as e:
            print(f"Error saving settings on close: {str(e)}")
        finally:
            self.root.destroy()