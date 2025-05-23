import tkinter as tk
from tkinter import messagebox
from connection import connection

class RegistroUsuario:
    def __init__(self, master=None):
        self.master = master if master else tk.Tk()
        self.master.title("Registrar Usuario")
        self.master.geometry("400x450")
        self.master.configure(bg="#041955")

        tk.Label(self.master, text="REGISTRAR USUARIO", bg="#00d4ff", fg="black",
                 font=("Arial", 16, "bold"), pady=10).pack(fill="x", pady=10)

        self.frame = tk.Frame(self.master, bg="#041955")
        self.frame.pack(pady=20)

        self.campos = {}
        self.crear_entrada("Nombre completo:", "nombre")
        self.crear_entrada("Rol (Admin/Médico/Enfermero):", "rol")
        self.crear_entrada("Usuario:", "usuario")
        self.crear_entrada("Contraseña:", "clave", show="*")
        self.crear_entrada("Confirmar Contraseña:", "confirmar", show="*")

        tk.Button(self.master, text="Registrar", command=self.registrar,
                  bg="#97b4ff", fg="black", font=("Arial", 12)).pack(pady=15)
        tk.Button(self.master, text="Cancelar", command=self.master.destroy,
                  bg="#ff6b6b", fg="black", font=("Arial", 12)).pack()

    def crear_entrada(self, texto, clave, show=None):
        tk.Label(self.frame, text=texto, bg="#041955", fg="white", font=("Arial", 12)).pack()
        entrada = tk.Entry(self.frame, font=("Arial", 12), width=30, show=show)
        entrada.pack(pady=5)
        self.campos[clave] = entrada

    def registrar(self):
        nombre = self.campos["nombre"].get().strip()
        rol = self.campos["rol"].get().strip()
        usuario = self.campos["usuario"].get().strip()
        clave = self.campos["clave"].get()
        confirmar = self.campos["confirmar"].get()

        if not all([nombre, rol, usuario, clave, confirmar]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        if clave != confirmar:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return

        if rol not in ['Admin', 'Médico', 'Enfermero']:
            messagebox.showerror("Error", "El rol debe ser: Admin, Médico o Enfermero")
            return

        conn = connection.getConnection()
        if conn is None:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            return

        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO usuarios (nombre, rol, usuario, contraseña)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (nombre, rol, usuario, clave))
            conn.commit()
            messagebox.showinfo("Éxito", f"Usuario '{usuario}' registrado correctamente")
            self.master.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al registrar: {e}")
        finally:
            if conn:
                conn.close()
