import tkinter as tk
from tkinter import ttk, messagebox
from database import ejecutar_consulta
from styles import BG, FG, FWG, CELEST, ERROR

class NuevoPaciente(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Registrar Nuevo Paciente")
        self.geometry("650x750")
        self.configure(bg=BG)
        self.resizable(False, False)
        
        # Configurar grid principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.crear_widgets()
        self.centrar_ventana()

    def centrar_ventana(self):
        self.update_idletasks()
        ancho = self.winfo_width()
        alto = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f'+{x}+{y}')

    def crear_widgets(self):
        # Frame principal
        main_frame = tk.Frame(self, bg=BG)
        main_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # Título
        lbl_titulo = tk.Label(
            main_frame, 
            text="NUEVO REGISTRO DE PACIENTE",
            font=("Arial", 14, "bold"),
            bg=BG,
            fg=CELEST
        )
        lbl_titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Campos del formulario
        campos = [
            ("Nombre completo:", "entry_nombre", "varchar(100)", True),
            ("Edad:", "entry_edad", "int(11)", True),
            ("Peso (kg):", "entry_peso", "float", False),
            ("Estatura (m):", "entry_estatura", "float", False),
            ("Tipo de sangre:", "entry_tipo_sangre", "varchar(5)", False),
            ("Alergias conocidas:", "entry_alergias", "text", False),
            ("Informe médico inicial:", "entry_informe", "text", False)
        ]

        for i, (label_text, entry_name, tipo_dato, obligatorio) in enumerate(campos, start=1):
            # Frame para cada campo
            field_frame = tk.Frame(main_frame, bg=BG)
            field_frame.grid(row=i, column=0, columnspan=2, pady=5, sticky="ew")
            
            # Etiqueta
            lbl_text = f"{label_text} {'(OBLIGATORIO)' if obligatorio else ''}"
            lbl = tk.Label(
                field_frame,
                text=lbl_text,
                bg=BG,
                fg=FWG,
                font=("Arial", 10),
                anchor="w"
            )
            lbl.pack(side=tk.TOP, fill=tk.X)
            
            # Tooltip con tipo de dato
            self.crear_tooltip(lbl, f"Tipo de dato: {tipo_dato}")
            
            # Campo de entrada
            if "text" in tipo_dato:
                entry = tk.Text(
                    field_frame,
                    height=4,
                    bg=FG,
                    fg='white',
                    insertbackground=FWG,
                    wrap=tk.WORD,
                    font=("Arial", 10),
                    padx=5,
                    pady=5
                )
                scroll = tk.Scrollbar(field_frame, command=entry.yview)
                entry.configure(yscrollcommand=scroll.set)
                entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
                scroll.pack(side=tk.RIGHT, fill=tk.Y)
            else:
                entry = tk.Entry(
                    field_frame,
                    bg=FG,
                    fg='white',
                    insertbackground=FWG,
                    font=("Arial", 10),
                    width=30
                )
                entry.pack(fill=tk.X)
            
            setattr(self, entry_name, entry)

        # Frame para botones
        btn_frame = tk.Frame(main_frame, bg=BG)
        btn_frame.grid(row=len(campos)+2, column=0, columnspan=2, pady=(20, 0))

        # Botón Guardar
        btn_guardar = tk.Button(
            btn_frame,
            text="GUARDAR REGISTRO",
            command=self.validar_datos,
            bg=CELEST,
            fg=BG,
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8,
            bd=0,
            activebackground=FWG,
            activeforeground=FG
        )
        btn_guardar.pack(side=tk.LEFT, padx=10)

        # Botón Limpiar
        btn_limpiar = tk.Button(
            btn_frame,
            text="LIMPIAR FORMULARIO",
            command=self.limpiar_formulario,
            bg=FG,
            fg=FWG,
            font=("Arial", 10),
            padx=15,
            pady=8,
            bd=0,
            activebackground=CELEST,
            activeforeground=BG
        )
        btn_limpiar.pack(side=tk.LEFT, padx=10)

        # Botón Cancelar
        btn_cancelar = tk.Button(
            btn_frame,
            text="CANCELAR",
            command=self.destroy,
            bg=ERROR,
            fg='white',
            font=("Arial", 10),
            padx=15,
            pady=8,
            bd=0,
            activebackground=FWG
        )
        btn_cancelar.pack(side=tk.RIGHT, padx=10)

    def crear_tooltip(self, widget, text):
        tooltip = tk.Toplevel(widget)
        tooltip.withdraw()
        tooltip.wm_overrideredirect(True)
        
        def enter(event):
            x = widget.winfo_rootx() + 25
            y = widget.winfo_rooty() + 20
            tooltip.geometry(f"+{x}+{y}")
            tk.Label(tooltip, text=text, bg="#FFFFE0", relief="solid", 
                    borderwidth=1, padx=5, pady=2).pack()
            tooltip.deiconify()
        
        def leave(event):
            tooltip.withdraw()
        
        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)

    def limpiar_formulario(self):
        for attr_name in dir(self):
            if attr_name.startswith('entry_'):
                widget = getattr(self, attr_name)
                if isinstance(widget, tk.Entry):
                    widget.delete(0, tk.END)
                elif isinstance(widget, tk.Text):
                    widget.delete('1.0', tk.END)

    def validar_datos(self):
        # Obtener valores
        nombre = self.entry_nombre.get().strip()
        edad = self.entry_edad.get().strip()
        peso = self.entry_peso.get().strip()
        estatura = self.entry_estatura.get().strip()
        tipo_sangre = self.entry_tipo_sangre.get().strip().upper()
        alergias = self.entry_alergias.get('1.0', tk.END).strip()
        informe = self.entry_informe.get('1.0', tk.END).strip()

        # Validaciones
        errores = []

        # Nombre obligatorio
        if not nombre:
            errores.append("El nombre completo es obligatorio")
        
        # Validar edad
        if edad:
            try:
                edad_int = int(edad)
                if edad_int <= 0 or edad_int > 120:
                    errores.append("La edad debe ser entre 1 y 120 años")
            except ValueError:
                errores.append("La edad debe ser un número entero válido")
        else:
            edad_int = None

        # Validar peso
        if peso:
            try:
                peso_float = float(peso)
                if peso_float <= 0 or peso_float > 300:
                    errores.append("El peso debe ser entre 0.1 y 300 kg")
            except ValueError:
                errores.append("El peso debe ser un número válido")
        else:
            peso_float = None

        # Validar estatura
        if estatura:
            try:
                estatura_float = float(estatura)
                if estatura_float <= 0 or estatura_float > 2.5:
                    errores.append("La estatura debe ser entre 0.1 y 2.5 metros")
            except ValueError:
                errores.append("La estatura debe ser un número válido")
        else:
            estatura_float = None

        # Validar tipo de sangre
        if tipo_sangre and not self.validar_tipo_sangre(tipo_sangre):
            errores.append("Tipo de sangre inválido. Formatos válidos: A+, B-, O+, etc.")

        # Mostrar errores si hay
        if errores:
            mensaje_error = "Por favor corrija los siguientes errores:\n\n" + "\n• ".join(errores)
            messagebox.showerror("Error de validación", mensaje_error, parent=self)
            return

        # Si todo está bien, guardar
        self.guardar_paciente(
            nombre=nombre,
            edad=edad_int,
            peso=peso_float,
            estatura=estatura_float,
            tipo_sangre=tipo_sangre if tipo_sangre else None,
            alergias=alergias if alergias else None,
            informe=informe if informe else None
        )

    def validar_tipo_sangre(self, tipo_sangre):
        if len(tipo_sangre) not in (2, 3):
            return False
        
        grupo = tipo_sangre[:-1]
        rh = tipo_sangre[-1]
        
        grupos_validos = ['A', 'B', 'AB', 'O']
        rh_validos = ['+', '-']
        
        return grupo.upper() in grupos_validos and rh in rh_validos

    def guardar_paciente(self, **datos):
        query = """
        INSERT INTO pacientes (
            nombre, edad, peso, estatura, 
            tipo_sangre, alergias, informe
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        valores = (
            datos['nombre'],
            datos['edad'],
            datos['peso'],
            datos['estatura'],
            datos['tipo_sangre'],
            datos['alergias'],
            datos['informe']
        )

        try:
            if ejecutar_consulta(query, valores):
                messagebox.showinfo(
                    "Registro exitoso",
                    "Paciente registrado correctamente en la base de datos",
                    parent=self
                )
                self.limpiar_formulario()
                self.destroy()
                
        except Exception as e:
            messagebox.showerror(
                "Error en la base de datos",
                f"No se pudo guardar el registro:\n{str(e)}",
                parent=self
            )

if __name__ == "__main__":
    root = tk.Tk()
    app = NuevoPaciente(root)
    root.mainloop()