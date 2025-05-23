import tkinter as tk
from tkinter import messagebox
from database import obtener_un_registro
from connection import connection

class CalculadoraMedicamentos:
    def __init__(self, master=None):
        self.master = master if master else tk.Tk()
        self.master.title("Calculadora de Medicamentos")
        self.master.geometry("400x350")
        self.master.configure(bg="#041955")

        tk.Label(self.master, text="CALCULADORA DE DOSIS", bg="#00d4ff", fg="#000000",
                 font=("Arial", 16, "bold"), pady=10).pack(fill="x", pady=10)

        self.marco = tk.Frame(self.master, bg="#041955")
        self.marco.pack(pady=20)

        self.crear_campo("Nombre del paciente:", "nombre_paciente")
        self.crear_campo("Nombre del medicamento:", "nombre_medicamento")

        tk.Button(self.master, text="Calcular Dosis", command=self.calcular_dosis,
                  font=("Arial", 12), bg="#97b4ff", fg="black").pack(pady=10)

    def crear_campo(self, texto, clave):
        tk.Label(self.marco, text=texto, font=("Arial", 12), bg="#041955", fg="white").pack()
        entrada = tk.Entry(self.marco, font=("Arial", 12), width=30)
        entrada.pack(pady=5)
        setattr(self, clave, entrada)

    def calcular_dosis(self):
        nombre_paciente = self.nombre_paciente.get().strip()
        nombre_medicamento = self.nombre_medicamento.get().strip()

        if not nombre_paciente or not nombre_medicamento:
            messagebox.showerror("Error", "Debe ingresar nombre de paciente y medicamento.")
            return

        # Obtener datos del paciente
        paciente = obtener_un_registro(
            "SELECT * FROM pacientes WHERE nombre = %s", (nombre_paciente,))
        if not paciente:
            messagebox.showerror("Error", "Paciente no encontrado.")
            return

        peso = paciente.get('peso')
        if peso is None:
            messagebox.showerror("Error", "El paciente no tiene peso registrado.")
            return

        # Obtener medicamento y su dosis_x_kg
        conn = connection.getConnection()
        if not conn:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            return

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM medicamentos WHERE nombre_comercial = %s", (nombre_medicamento,))
            medicamento = cursor.fetchone()

            if not medicamento:
                messagebox.showerror("Error", "Medicamento no encontrado.")
                return

            dosis_por_kg = medicamento.get('dosis_x_kg')
            if dosis_por_kg is None:
                messagebox.showerror("Error", "El medicamento no tiene dosis por kg registrada.")
                return

            dosis_total = float(peso) * float(dosis_por_kg)
            messagebox.showinfo("Resultado", f"Dosis total para {nombre_paciente} con {nombre_medicamento}:\n{dosis_total:.2f} mg")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")
        finally:
            conn.close()

