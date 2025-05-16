# login.py
import tkinter as tk
from tkinter import messagebox
from connection import connection

class Login:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Login - MedicalBase")
        self.ventana.geometry("300x200")

        # UI
        tk.Label(self.ventana, text="Usuario:").pack(pady=5)
        self.entry_usuario = tk.Entry(self.ventana)
        self.entry_usuario.pack()

        tk.Label(self.ventana, text="Contraseña:").pack(pady=5)
        self.entry_contrasena = tk.Entry(self.ventana, show="*")
        self.entry_contrasena.pack()

        tk.Button(self.ventana, text="Iniciar sesión", command=self.verificar_login).pack(pady=20)

        self.ventana.mainloop()

    def verificar_login(self):
        usuario = self.entry_usuario.get()
        contrasena = self.entry_contrasena.get()

        conn = connection.getConnection()
        if conn is None:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            return

        try:
            cursor = conn.cursor()
            query = "SELECT * FROM usuarios WHERE usuario = %s AND contraseña = %s"
            cursor.execute(query, (usuario, contrasena))
            resultado = cursor.fetchone()
            conn.close()

            if resultado:
                nombre = resultado[2]
                rol = resultado[3]
                messagebox.showinfo("Acceso permitido", f"¡Bienvenido {nombre} ({rol})!")
                # Aquí podrías abrir una nueva ventana o menú principal
            else:
                messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

# Ejecutar
if __name__ == "__main__":
    Login()
