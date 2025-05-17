# login.py
import tkinter as tk
from tkinter import messagebox
from connection import connection

class Login:
    def __init__(self):#crear ventana
        self.ventana = tk.Tk()#define la ventana
        self.ventana.title("Login - MedicalBase")#titulo de la ventana
        self.ventana.geometry("300x200")#dimeciones de la ventana

        # UI
        tk.Label(self.ventana, text="Usuario:").pack(pady=5)#crea el texto de usuario (pady es para dar espacio)
        self.entry_usuario = tk.Entry(self.ventana)#entrada de datos de usuario
        self.entry_usuario.pack()#lo agrega en pantalla

        tk.Label(self.ventana, text="Contraseña:").pack(pady=5)#crea el texto de contraseña
        self.entry_contrasena = tk.Entry(self.ventana, show="*")#show=* es para que se vean * en ves de la contraseña
        self.entry_contrasena.pack()#lo agrega en pantalla

        tk.Button(self.ventana, text="Iniciar sesión", command=self.verificar_login).pack(pady=20)# boton de verificado

        self.ventana.mainloop() #bucle de ventana

    #verificar contraseña con la base de datos
    def verificar_login(self):
        #estos dos obtienen la informacion de los campos
        usuario = self.entry_usuario.get()
        contrasena = self.entry_contrasena.get()

        #conexion con la base de datos
        conn = connection.getConnection()
        #por si no hay conexion
        if conn is None:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            return

        #recordar siempre usar try y catch cada vez que se intenta algo con la base de datos (por si falla)
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
                # Aquí podrías abrir una nueva ventana o menú principal
            else:
                messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

# Ejecutar
if __name__ == "__main__":
    Login()
