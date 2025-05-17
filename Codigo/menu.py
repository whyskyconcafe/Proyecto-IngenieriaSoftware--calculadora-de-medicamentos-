#menu.py
import tkinter as tk

class menu:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Menu - Medication Registration System")
        self.ventana.geometry("300x200")

        #UI
        tk.Label(self.ventana, text="Menu").pack(pady=5)
        self.buttom__Menu=tk.Button()
