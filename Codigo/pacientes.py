import tkinter as tk
from styles import BG, FWG, CELEST, FG
from nuevoPaciente import NuevoPaciente
from verPaciente import VerPaciente  # 👈 corregido
from editarPaciente import EditarPaciente

class AppPrincipal:
    def __init__(self, root):
        self.root = root
        self.configurar_ventana()
        self.crear_interfaz()

    def configurar_ventana(self):
        self.root.title("Sistema de Pacientes")
        self.root.geometry("500x250")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

    def crear_interfaz(self):
        # Cabecera
        header = tk.Frame(self.root, bg=CELEST, height=60)
        header.pack(fill='x')
        tk.Label(header, text="PACIENTES", font=("Arial", 20, "bold"),
                 bg=CELEST, fg=BG).place(relx=0.5, rely=0.5, anchor='center')
        
        # Botones
        contenedor = tk.Frame(self.root, bg=BG)
        contenedor.pack(pady=40)
        
        self.crear_boton(contenedor, "Nuevo paciente", self.abrir_nuevo)
        self.crear_boton(contenedor, "Editar paciente", self.abrir_editar)
        self.crear_boton(contenedor, "Ver datos", self.abrir_ver)

    def crear_boton(self, parent, texto, comando):
        panel = tk.Frame(parent, bg=FWG, bd=2, relief='solid', width=130, height=60)
        panel.pack(side='left', padx=10)
        panel.pack_propagate(False)
        
        tk.Button(panel, text=texto, command=comando,
                  bg=CELEST, fg=BG, font=("Arial", 10, "bold"),
                  bd=0, activebackground=FWG, activeforeground=FG
        ).pack(expand=True, fill='both')

    def abrir_nuevo(self):
        NuevoPaciente(self.root)

    def abrir_editar(self):
        EditarPaciente(self.root)

    def abrir_ver(self):
        VerPaciente(self.root)  # 👈 corregido

#if __name__ == "__main__":
 #   root = tk.Tk()
  #  app = AppPrincipal(root)
   # root.mainloop()
