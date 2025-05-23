import tkinter as tk
from tkinter import ttk, messagebox
from database import obtener_un_registro, ejecutar_consulta
from styles import BG, FG, FWG, CELEST, ERROR

class EditarPaciente(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Editor de Pacientes")
        self.geometry("800x600")
        self.configure(bg=BG)
        
        # Variables
        self.paciente_actual = None
        
        # Interface
        self.crear_widgets()
        self.cargar_lista_pacientes()

    def crear_widgets(self):
        # Frame principal
        main_frame = tk.Frame(self, bg=BG)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Lista de pacientes (izquierda)
        lista_frame = tk.LabelFrame(main_frame, text=" Lista de Pacientes ", 
                                bg=BG, fg=CELEST, font=("Arial", 12, "bold"))
        lista_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Treeview + Scrollbar en un sub-frame
        tree_container = tk.Frame(lista_frame, bg=BG)
        tree_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Treeview
        self.tree = ttk.Treeview(tree_container, columns=("ID", "Nombre"), show="headings", height=20)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nombre", width=200, anchor="w")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Buscar por ID (derecha)
        buscar_frame = tk.LabelFrame(main_frame, text=" Buscar Paciente por ID ", 
                                bg=BG, fg=CELEST, font=("Arial", 12, "bold"))
        buscar_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        tk.Label(buscar_frame, text="Ingrese ID del paciente:", 
                bg=BG, fg=FWG).pack(pady=(10, 5))
        
        self.id_entry = tk.Entry(buscar_frame, font=("Arial", 12))
        self.id_entry.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(buscar_frame, text="BUSCAR", command=self.buscar_paciente,
                bg=CELEST, fg=BG, font=("Arial", 10, "bold")).pack(pady=10)
        
        # Formulario de edición (oculto inicialmente)
        self.form_frame = tk.LabelFrame(main_frame, text=" Editar Paciente ", 
                                    bg=BG, fg=CELEST, font=("Arial", 12, "bold"))
        self.crear_formulario()
        
        # Botones de acción (ocultos inicialmente)
        self.btn_frame = tk.Frame(main_frame, bg=BG)
        tk.Button(self.btn_frame, text="GUARDAR CAMBIOS", command=self.guardar_cambios,
                bg="#2ECC71", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(self.btn_frame, text="CANCELAR", command=self.cancelar_edicion,
                bg=ERROR, fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)

    
    def crear_formulario(self):
        campos = [
            ("Nombre:", "nombre"),
            ("Edad:", "edad"), 
            ("Peso (kg):", "peso"),
            ("Estatura (m):", "estatura"),
            ("Tipo de sangre:", "tipo_sangre"),
            ("Alergias:", "alergias"),
            ("Informe médico:", "informe")
        ]
        
        self.entries = {}
        
        for i, (label, field) in enumerate(campos):
            row = tk.Frame(self.form_frame, bg=BG)
            row.pack(fill=tk.X, padx=5, pady=5)
            
            tk.Label(row, text=label, width=15, anchor="e", 
                   bg=BG, fg=FWG).pack(side=tk.LEFT)
            
            if field in ["alergias", "informe"]:
                entry = tk.Text(row, height=4, bg=FG, fg="white",
                              insertbackground=FWG, wrap=tk.WORD)
                scroll = ttk.Scrollbar(row, command=entry.yview)
                entry.configure(yscrollcommand=scroll.set)
                entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
                scroll.pack(side=tk.RIGHT, fill=tk.Y)
            else:
                entry = tk.Entry(row, bg=FG, fg="white", 
                               insertbackground=FWG)
                entry.pack(fill=tk.X, expand=True)
            
            self.entries[field] = entry

    def cargar_lista_pacientes(self):
        # Limpiar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener pacientes de la base de datos
        query = "SELECT id, nombre FROM pacientes ORDER BY nombre ASC"
        pacientes = ejecutar_consulta(query, fetch=True)
        
        if pacientes:
            for paciente in pacientes:
                self.tree.insert("", tk.END, values=(paciente["id"], paciente["nombre"]))


    def buscar_paciente(self):
        id_paciente = self.id_entry.get().strip()
        
        if not id_paciente:
            messagebox.showwarning("Advertencia", "Ingrese un ID válido", parent=self)
            return
            
        try:
            id_paciente = int(id_paciente)
        except ValueError:
            messagebox.showerror("Error", "El ID debe ser un número", parent=self)
            return
            
        paciente = obtener_un_registro("SELECT * FROM pacientes WHERE id = %s", (id_paciente,))
        
        if not paciente:
            messagebox.showerror("Error", "No se encontró el paciente", parent=self)
            return
            
        self.mostrar_datos_paciente(paciente)

    def mostrar_datos_paciente(self, paciente):
        self.paciente_actual = paciente
        
        # Mostrar frame del formulario
        self.form_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        self.btn_frame.pack(pady=10)
        
        # Llenar campos
        for field, entry in self.entries.items():
            if isinstance(entry, tk.Text):
                entry.delete("1.0", tk.END)
                entry.insert("1.0", paciente.get(field, ""))
            else:
                entry.delete(0, tk.END)
                entry.insert(0, str(paciente.get(field, "")))

    def guardar_cambios(self):
        if not self.paciente_actual:
            return
            
        nuevos_datos = {}
        
        # Validar campos
        try:
            nuevos_datos["nombre"] = self.entries["nombre"].get()
            if not nuevos_datos["nombre"]:
                raise ValueError("El nombre es obligatorio")
                
            nuevos_datos["edad"] = int(self.entries["edad"].get()) if self.entries["edad"].get() else None
            nuevos_datos["peso"] = float(self.entries["peso"].get()) if self.entries["peso"].get() else None
            nuevos_datos["estatura"] = float(self.entries["estatura"].get()) if self.entries["estatura"].get() else None
            nuevos_datos["tipo_sangre"] = self.entries["tipo_sangre"].get() or None
            nuevos_datos["alergias"] = self.entries["alergias"].get("1.0", tk.END).strip() or None
            nuevos_datos["informe"] = self.entries["informe"].get("1.0", tk.END).strip() or None
            
        except ValueError as e:
            messagebox.showerror("Error", f"Dato inválido: {str(e)}", parent=self)
            return
            
        # Actualizar en BD
        query = """
        UPDATE pacientes SET
            nombre = %s,
            edad = %s,
            peso = %s,
            estatura = %s,
            tipo_sangre = %s,
            alergias = %s,
            informe = %s
        WHERE id = %s
        """
        
        valores = (
            nuevos_datos["nombre"],
            nuevos_datos["edad"],
            nuevos_datos["peso"],
            nuevos_datos["estatura"],
            nuevos_datos["tipo_sangre"],
            nuevos_datos["alergias"],
            nuevos_datos["informe"],
            self.paciente_actual["id"]
        )
        
        if ejecutar_consulta(query, valores):
            messagebox.showinfo("Éxito", "Datos actualizados correctamente", parent=self)
            self.cancelar_edicion()
            self.cargar_lista_pacientes()

    def cancelar_edicion(self):
        self.form_frame.pack_forget()
        self.btn_frame.pack_forget()
        self.id_entry.delete(0, tk.END)
        self.paciente_actual = None

if __name__ == "__main__":
    root = tk.Tk()
    app = EditarPaciente(root)
    root.mainloop()