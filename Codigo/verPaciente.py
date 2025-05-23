import tkinter as tk
from tkinter import ttk, messagebox
from database import ejecutar_consulta, obtener_un_registro
from styles import BG, FG, FWG, CELEST

class VerPaciente(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Ver Datos del Paciente")
        self.geometry("600x550")
        self.configure(bg=BG)

        self.pacientes = []  # Lista de pacientes para el combobox
        self.crear_widgets()
        self.cargar_lista_pacientes()

    def crear_widgets(self):
        frame = tk.Frame(self, bg=BG)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(frame, text="Seleccione un paciente:",
                 bg=BG, fg=FWG, font=("Arial", 12)).pack(pady=(0, 10))

        self.combo = ttk.Combobox(frame, state="readonly", font=("Arial", 11))
        self.combo.pack(fill=tk.X, pady=(0, 10))
        self.combo.bind("<<ComboboxSelected>>", self.seleccionar_paciente)

        tk.Button(frame, text="BUSCAR", command=self.buscar_paciente,
                  bg=CELEST, fg=BG, font=("Arial", 10, "bold")).pack(pady=(0, 20))

        self.info_text = tk.Text(frame, height=20, bg=FG, fg="white", wrap=tk.WORD)
        self.info_text.pack(fill=tk.BOTH, expand=True)
        self.info_text.config(state=tk.DISABLED)

    def cargar_lista_pacientes(self):
        resultado = ejecutar_consulta("SELECT id, nombre FROM pacientes", fetch=True)
        if resultado:
            self.pacientes = resultado
            opciones = [f"{p['id']} - {p['nombre']}" for p in self.pacientes]
            self.combo['values'] = opciones
        else:
            messagebox.showinfo("Información", "No hay pacientes registrados", parent=self)

    def seleccionar_paciente(self, event):
        self.buscar_paciente()

    def buscar_paciente(self):
        seleccion = self.combo.get()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un paciente", parent=self)
            return

        try:
            id_paciente = int(seleccion.split(" - ")[0])
        except (IndexError, ValueError):
            messagebox.showerror("Error", "Selección inválida", parent=self)
            return

        paciente = obtener_un_registro("SELECT * FROM pacientes WHERE id = %s", (id_paciente,))
        if not paciente:
            messagebox.showerror("Error", "Paciente no encontrado", parent=self)
            return

        self.mostrar_paciente(paciente)

    def mostrar_paciente(self, p):
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete("1.0", tk.END)
        datos = (
            f"ID: {p['id']}\n"
            f"Nombre: {p['nombre']}\n"
            f"Edad: {p['edad']}\n"
            f"Peso: {p['peso']} kg\n"
            f"Estatura: {p['estatura']} m\n"
            f"Tipo de sangre: {p['tipo_sangre']}\n"
            f"Alergias: {p['alergias']}\n"
            f"Informe médico: {p['informe']}\n"
            f"Fecha de registro: {p['fecha_registro']}\n"
        )
        self.info_text.insert(tk.END, datos)
        self.info_text.config(state=tk.DISABLED)

