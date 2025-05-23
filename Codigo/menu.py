import tkinter as tk
from tkinter import messagebox
from pacientes import AppPrincipal  # Módulo de pacientes
from medicamentos import MedicamentosApp  # <-- Agregado
from calculator import CalculadoraMedicamentos  # ← Nueva importación


# Paleta de colores
BG = '#041955'
FWG = '#97b4ff'
FG = '#3450a1'

class MenuPrincipal:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Menú Principal")
        self.root.geometry("600x400")
        self.root.configure(bg=BG)

        # Encabezado
        header = tk.Label(self.root, text="Menú principal", bg=FWG, fg=FG,
                          font=("Arial", 16, "bold"), height=2)
        header.pack(fill='x', pady=(0, 40))

        # Botones con lógica
        self.crear_boton("Calculadora de medicamentos", self.abrir_calculadora)
        self.crear_boton("Pacientes", self.abrir_pacientes)
        self.crear_boton("Medicamentos", self.abrir_medicamentos)

        self.root.mainloop()

    def crear_boton(self, texto, comando):
        btn = tk.Button(
            self.root,
            text=texto,
            bg=FWG,
            fg=FG,
            font=("Arial", 12, "bold"),
            relief="solid",
            bd=2,
            activebackground="#cfe0ff",
            activeforeground=FG,
            command=comando
        )
        btn.pack(pady=10, ipadx=40, ipady=10)

    def abrir_calculadora(self):
        ventana_calc = tk.Toplevel(self.root)
        CalculadoraMedicamentos(ventana_calc)  

    def abrir_pacientes(self):
        ventana_pacientes = tk.Toplevel(self.root)
        AppPrincipal(ventana_pacientes)

    def abrir_medicamentos(self):
        ventana_medicamentos = tk.Toplevel(self.root)
        MedicamentosApp(ventana_medicamentos)  # <-- Aquí se lanza el módulo real


