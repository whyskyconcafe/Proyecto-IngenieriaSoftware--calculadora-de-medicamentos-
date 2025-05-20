import tkinter as tk
from tkinter import messagebox
from connection import connection
from menu import MenuPrincipal


# Colores de la nueva paleta
BG   = '#041955'
FWG  = '#97b4ff'
FG   = '#3450a1'
CELEST = "#00d4ff"

class Login:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Login - Medication Registration System")
        self.ventana.geometry("600x500")
        self.ventana.configure(bg=BG)

        # Encabezado con color CELEST
        encabezado = tk.Frame(self.ventana, bg=CELEST, height=80)
        encabezado.pack(fill=tk.X)
        tk.Label(encabezado, text="Bienvenido", bg=CELEST, fg="black", font=("Arial", 16)).pack(pady=20)

        # Campo de Usuario
        self.crear_campo("Usuario:", 120, "usuario")

        # Campo de Contraseña
        self.crear_campo("Contraseña: ", 200, "contrasena", es_contrasena=True)

        # Botón de Iniciar sesión
        boton_login = tk.Button(
            self.ventana,
            text="Iniciar sesión",
            bg=CELEST,
            fg="black",
            font=("Arial", 12),
            command=self.verificar_login,
            bd=2,
            relief="ridge",
            activebackground=FG
        )
        boton_login.place(relx=0.5, y=300, anchor="center", width=160, height=60)
        boton_login.config(highlightbackground="black", highlightthickness=1)

        self.ventana.mainloop()

    def crear_campo(self, texto, y, atributo, es_contrasena=False):
        # Marco de fondo (simula borde redondeado)
        marco = tk.Frame(self.ventana, bg=FWG, bd=2, relief="solid")
        marco.place(relx=0.5, y=y, anchor="center", width=400, height=70)
        tk.Label(marco, text=texto, bg=FWG, fg="black", anchor="w", font=("Arial", 12)).place(x=10, y=10)

        entrada = tk.Entry(marco, font=("Arial", 11), relief="flat", justify="left", show="*" if es_contrasena else "")
        entrada.place(x=120, y=10, width=200, height=30)

        if atributo == "usuario":
            self.entry_usuario = entrada
        else:
            self.entry_contrasena = entrada

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
                nombre = resultado[1]
                rol = resultado[2]
                messagebox.showinfo("Acceso permitido", f"¡Bienvenido {nombre} ({rol})!")
                
                self.ventana.destroy()  # Cierra login
                MenuPrincipal()         # Abre menú principal

            else:
                messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

if __name__ == "__main__":
    Login()
