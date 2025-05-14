import customtkinter as ctk
import tkinter as tk
from src.utils.styles import Theme
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
    root.title("RENAMERGED - Rename & Merge PDFs")
    root.geometry("1000x900")
    root.resizable(True, True)
    root.minsize(1000, 900)
    app = RenamergedGUI(root)
    root.mainloop()

class RenamergedGUI:
    def __init__(self, root):
        self.root = root
        self.theme = Theme()
        self.current_theme = "dark"
        self.colors = self.theme.get_colors(self.current_theme)
        self.mode_var = ctk.StringVar(value="Rename dan Merge")
        self.input_path_var = tk.StringVar()
        self.output_path_var = tk.StringVar()
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_percentage_var = tk.StringVar(value="0%")
        self.separator_var = tk.StringVar(value="(spasi)")  # Ubah default ke "(spasi)"
        self.slash_replacement_var = tk.StringVar(value="(spasi)")  # Ubah default ke "(spasi)"

        self.settings = {
            "use_name": tk.BooleanVar(value=True),
            "use_date": tk.BooleanVar(value=True),
            "use_reference": tk.BooleanVar(value=True),
            "use_faktur": tk.BooleanVar(value=True),
            "component_order": None
        }

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