import customtkinter as ctk
from frontend.gui_app import DigitalLibraryApp

if __name__ == "__main__":
   
    root_window = ctk.CTk()
    
    app = DigitalLibraryApp(root_window)
    
    root_window.mainloop()