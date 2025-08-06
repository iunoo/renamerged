import json
import os
from src.utils.utils import log_message, Fore

class SettingsManager:
    def __init__(self, settings_file="user_settings.json"):
        self.settings_file = settings_file
        self.default_settings = {
            "mode": "Rename Saja",
            "use_name": True,
            "use_date": True,
            "use_reference": True,
            "use_faktur": True,
            "separator": "-",
            "slash_replacement": "_",
            "component_order": [
                "Nama Lawan Transaksi",
                "Tanggal Faktur Pajak", 
                "Referensi",
                "Nomor Faktur Pajak"
            ],
            "last_input_directory": "",
            "last_output_directory": "",
            "theme": "dark"
        }
    
    def load_settings(self, log_callback=None):
        """Load user settings dari file, atau gunakan default jika file tidak ada"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                
                # Merge dengan default untuk key yang hilang
                merged_settings = self.default_settings.copy()
                merged_settings.update(settings)
                
                log_message("Settings user berhasil dimuat", Fore.GREEN, log_callback=log_callback)
                return merged_settings
            else:
                log_message("File settings tidak ditemukan, menggunakan default", Fore.YELLOW, log_callback=log_callback)
                return self.default_settings.copy()
                
        except Exception as e:
            log_message(f"Error loading settings: {str(e)}, menggunakan default", Fore.RED, log_callback=log_callback)
            return self.default_settings.copy()
    
    def save_settings(self, settings_dict, log_callback=None):
        """Simpan user settings ke file"""
        try:
            # Konversi settings GUI ke format yang bisa disimpan
            saveable_settings = {}
            
            for key, value in settings_dict.items():
                if hasattr(value, 'get'):  # Tkinter variable
                    saveable_settings[key] = value.get()
                else:
                    saveable_settings[key] = value
            
            # Simpan ke file dengan pretty formatting
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(saveable_settings, f, indent=2, ensure_ascii=False)
            
            log_message("Settings user berhasil disimpan", Fore.GREEN, log_callback=log_callback)
            return True
            
        except Exception as e:
            log_message(f"Error saving settings: {str(e)}", Fore.RED, log_callback=log_callback)
            return False
    
    def get_default_settings(self):
        """Return default settings"""
        return self.default_settings.copy()
    
    def reset_settings(self, log_callback=None):
        """Reset settings ke default dan hapus file"""
        try:
            if os.path.exists(self.settings_file):
                os.remove(self.settings_file)
            log_message("Settings berhasil direset ke default", Fore.GREEN, log_callback=log_callback)
            return True
        except Exception as e:
            log_message(f"Error reset settings: {str(e)}", Fore.RED, log_callback=log_callback)
            return False