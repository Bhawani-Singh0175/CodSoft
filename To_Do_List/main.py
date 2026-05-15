import customtkinter as ctk
from ui.main_window import MainWindow
import sys
import os

# Add the project root to python path to resolve modules correctly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    # CustomTkinter base configuration
    ctk.set_default_color_theme("green") # Base theme, though we override colors
    
    app = MainWindow()
    app.mainloop()
