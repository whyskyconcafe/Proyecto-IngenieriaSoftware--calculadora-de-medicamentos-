# menu_principal.py
import tkinter as tk

# Paleta
BG = '#041955'
FWG = '#97b4ff'
FG = '#3450a1'

class MenuPrincipal:
    def __init__(self):
        root = tk.Tk()
        root.title("Menú Principal")
        root.geometry("600x400")
        root.configure(bg=BG)

        header = tk.Label(root, text="Menú principal", bg=FWG, fg=FG,
                          font=("Helvetica", 16, "bold"), height=2)
        header.pack(fill='x', pady=(0, 40))

        def create_rounded_button(master, text):
            btn = tk.Canvas(master, width=250, height=60, bg=BG, highlightthickness=0)
            btn.create_oval(0, 0, 250, 60, fill=FWG, outline=FG, width=3)
            btn.create_text(125, 30, text=text, font=("Helvetica", 12, "bold"), fill=FG)
            btn.pack(pady=10)
            return btn

        create_rounded_button(root, "Calculadora de medicamentos")
        create_rounded_button(root, "Pacientes")
        create_rounded_button(root, "Medicamentos")

        root.mainloop()
