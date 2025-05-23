# medicamentos.py
import tkinter as tk
from tkinter import ttk, messagebox
from connection import connection
from medicamento import Medicamento

class MedicamentosApp:
    def __init__(self, master=None):
        self.master = master if master else tk.Tk()
        self.master.title("Sistema de Medicamentos")
        self.master.geometry("800x600")
        self.master.configure(bg='#041955') 

        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 12), padding=10, borderwidth=0)
        self.style.configure('TLabel', background='#041955', foreground='white', font=('Arial', 12))
        self.style.configure('TEntry', font=('Arial', 12), padding=5)
        
        self.crear_menu_principal()
        
    def crear_menu_principal(self):
        self.limpiar_pantalla()
        
        marco_principal = tk.Frame(self.master, bg='#041955')
        marco_principal.pack(expand=True, fill='both', padx=50, pady=50)
        
        tk.Label(marco_principal, text="MEDICAMENTOS", font=('Arial', 24, 'bold'), 
                bg="#00d4ff", fg="#000000", pady=20).pack()
        
        marco_botones = tk.Frame(marco_principal, bg='#041955')
        marco_botones.pack(expand=True)
        
        botones = [
            ("Nuevo Medicamento", self.mostrar_nuevo_medicamento),
            ("Editar Medicamento", self.mostrar_menu_editar),
            ("Ver Medicamento", self.mostrar_menu_ver)
        ]
        
        for texto, comando in botones:
            tk.Button(marco_botones, text=texto, command=comando,
                     bg='#97b4ff', fg='black', font=('Arial', 12), 
                     width=25, height=2, bd=0, activebackground='#97b4ff').pack(pady=10)
        
        tk.Button(marco_principal, text="Salir", command=self.master.destroy,
                 bg='#00d4ff', fg='black', font=('Arial', 12), 
                 bd=0, padx=20, pady=5, activebackground='#00d4ff').pack(side='bottom', pady=20)

    def mostrar_nuevo_medicamento(self):
        self.limpiar_pantalla()
        
        marco_principal = tk.Frame(self.master, bg='#041955')
        marco_principal.pack(expand=True, fill='both', padx=50, pady=30)
        
        tk.Label(marco_principal, text="NUEVO MEDICAMENTO", font=('Arial', 20, 'bold'), 
                bg="#00d4ff", fg="#000000", pady=10).pack()
        
        marco_formulario = tk.Frame(marco_principal, bg='#041955')
        marco_formulario.pack(expand=True)
        
        campos = [
            "Nombre Comercial:", "Principio Activo:", "Concentracion:", 
            "Presentacion:", "Via Administracion:", "Fabricante:", "dosis_x_kg:"
        ]
        
        self.entradas = {}
        for i, campo in enumerate(campos):
            tk.Label(marco_formulario, text=campo, bg='#041955', fg='white', 
                    font=('Arial', 12)).grid(row=i, column=0, sticky='e', padx=10, pady=5)
            entrada = tk.Entry(marco_formulario, font=('Arial', 12), width=30, bd=2, relief='flat')
            entrada.grid(row=i, column=1, padx=10, pady=5)
            self.entradas[campo.split(":")[0].lower().replace(" ", "_")] = entrada
        
        marco_botones = tk.Frame(marco_principal, bg='#041955')
        marco_botones.pack(side='bottom', pady=20)
        
        tk.Button(marco_botones, text="Guardar", command=self.guardar_medicamento,
                 bg='#00d4ff', fg='black', font=('Arial', 12), 
                 bd=0, padx=20, pady=5, activebackground="#00d4ff").pack(side='left', padx=10)
        tk.Button(marco_botones, text="Cancelar", command=self.crear_menu_principal,
                 bg='#97b4ff', fg='black', font=('Arial', 12), 
                 bd=0, padx=20, pady=5, activebackground='#97b4ff').pack(side='left', padx=10)
    
    def guardar_medicamento(self):
        datos = {key: entry.get() for key, entry in self.entradas.items()}
        
        if not all(datos.values()):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        medicamento = Medicamento(
            nombre_comercial=datos['nombre_comercial'],
            principio_activo=datos['principio_activo'],
            concentracion=datos['concentracion'],
            presentacion=datos['presentacion'],
            via_administracion=datos['via_administracion'],
            fabricante=datos['fabricante'],
            dosis_x_kg=datos['dosis_x_kg']
        )
        
        conn = connection.getConnection()
        if conn is None:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            return
        
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO medicamentos 
                (nombre_comercial, principio_activo, concentracion, presentacion, via_administracion, fabricante, dosis_x_kg) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                medicamento.nombre_comercial,
                medicamento.principio_activo,
                medicamento.concentracion,
                medicamento.presentacion,
                medicamento.via_administracion,
                medicamento.fabricante,
                medicamento.dosis_x_kg
            ))


            conn.commit()
            messagebox.showinfo("Éxito", "Medicamento registrado correctamente")
            self.crear_menu_principal()
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al guardar: {e}")
        finally:
            if conn:
                conn.close()
    
    def mostrar_menu_editar(self):
        self.limpiar_pantalla()
        
        marco_principal = tk.Frame(self.master, bg='#041955')
        marco_principal.pack(expand=True, fill='both', padx=50, pady=30)
        
        tk.Label(marco_principal, text="EDITAR MEDICAMENTO", font=('Arial', 20, 'bold'), 
                bg="#00d4ff", fg="#000000", pady=10).pack()
        
        marco_lista = tk.Frame(marco_principal, bg='#041955')
        marco_lista.pack(fill='both', expand=True)
        
        medicamentos = self.obtener_medicamentos()
        
        if not medicamentos:
            tk.Label(marco_lista, text="No hay medicamentos registrados", 
                    bg='#041955', fg='white', font=('Arial', 12)).pack(pady=20)
            tk.Button(marco_principal, text="Regresar", command=self.crear_menu_principal,
                    bg='#97b4ff', fg='black', font=('Arial', 12), 
                    bd=0, padx=20, pady=5, activebackground='#97b4ff').pack(side='bottom', pady=20)
            return
        
        estilo_tabla = ttk.Style()
        estilo_tabla.configure("Treeview", 
                             background="#97b4ff",
                             foreground="black",
                             fieldbackground="#97b4ff",
                             font=('Arial', 11))
        estilo_tabla.configure("Treeview.Heading", 
                             background="#3450a1",
                             foreground="black",
                             font=('Arial', 12, 'bold'))
        estilo_tabla.map("Treeview", background=[('selected', '#3450a1')])
        
        tabla = ttk.Treeview(marco_lista, columns=('id', 'nombre', 'principio'), show='headings')
        tabla.heading('id', text='ID')
        tabla.heading('nombre', text='Nombre Comercial')
        tabla.heading('principio', text='Principio Activo')
        
        for med in medicamentos:
            tabla.insert('', 'end', values=(med.id_medicamento, med.nombre_comercial, med.principio_activo))
        
        tabla.pack(fill='both', expand=True, padx=10, pady=10)
        
        marco_botones = tk.Frame(marco_principal, bg='#041955')
        marco_botones.pack(side='bottom', pady=20)
        
        tk.Button(marco_botones, text="Editar Seleccionado", 
                 command=lambda: self.editar_medicamento_seleccionado(tabla),
                 bg='#00d4ff', fg='black', font=('Arial', 12), 
                 bd=0, padx=20, pady=5, activebackground='#00d4ff').pack(side='left', padx=10)
        tk.Button(marco_botones, text="Eliminar Seleccionado", 
                 command=lambda: self.eliminar_medicamento_seleccionado(tabla),
                 bg='#ff6b6b', fg='black', font=('Arial', 12), 
                 bd=0, padx=20, pady=5, activebackground='#ff6b6b').pack(side='left', padx=10)
        tk.Button(marco_botones, text="Regresar", command=self.crear_menu_principal,
                 bg='#97b4ff', fg='black', font=('Arial', 12), 
                 bd=0, padx=20, pady=5, activebackground='#97b4ff').pack(side='left', padx=10)
    
    def editar_medicamento_seleccionado(self, tabla):
        seleccionado = tabla.focus()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Por favor seleccione un medicamento")
            return
        
        item = tabla.item(seleccionado)
        medicamento_id = item['values'][0]
        
        conn = connection.getConnection()
        if conn is None:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            return
        
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM medicamentos WHERE id_medicamento = %s"
            cursor.execute(query, (medicamento_id,))
            resultado = cursor.fetchone()
            
            if resultado:
                medicamento = Medicamento(
                    id_medicamento=resultado['id_medicamento'],
                    nombre_comercial=resultado['nombre_comercial'],
                    principio_activo=resultado['principio_activo'],
                    concentracion=resultado['concentracion'],
                    presentacion=resultado['presentacion'],
                    via_administracion=resultado['via_administracion'],
                    fabricante=resultado['fabricante'],
                    dosis_x_kg=resultado['dosis_x_kg']
                )
                self.mostrar_formulario_edicion(medicamento)
            else:
                messagebox.showerror("Error", "Medicamento no encontrado")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")
        finally:
            if conn:
                conn.close()
    
    def mostrar_formulario_edicion(self, medicamento):
        self.limpiar_pantalla()
        
        marco_principal = tk.Frame(self.master, bg='#041955')
        marco_principal.pack(expand=True, fill='both', padx=50, pady=30)
        
        tk.Label(marco_principal, text="EDITAR MEDICAMENTO", font=('Arial', 20, 'bold'), 
                bg='#00d4ff', fg="#000000", pady=10).pack()
        
        marco_formulario = tk.Frame(marco_principal, bg='#041955')
        marco_formulario.pack(expand=True)
        
        campos = [
            "ID Medicamento:", "Nombre Comercial:", "Principio Activo:", "Concentracion:", 
            "Presentacion:", "Via Administracion:", "Fabricante:", "dosis_x_kg"
        ]
        
        self.entradas_edicion = {}
        for i, campo in enumerate(campos):
            tk.Label(marco_formulario, text=campo, bg='#041955', fg='white', 
                    font=('Arial', 12)).grid(row=i, column=0, sticky='e', padx=10, pady=5)
            
            if campo == "ID Medicamento:":
                entrada = tk.Entry(marco_formulario, font=('Arial', 12), width=30, state='readonly')
                entrada.insert(0, medicamento.id_medicamento)
            else:
                entrada = tk.Entry(marco_formulario, font=('Arial', 12), width=30, bd=2, relief='flat')
                nombre_campo = campo.split(":")[0].lower().replace(" ", "_")
                if hasattr(medicamento, nombre_campo):
                    entrada.insert(0, getattr(medicamento, nombre_campo))
            
            entrada.grid(row=i, column=1, padx=10, pady=5)
            self.entradas_edicion[campo.split(":")[0].lower().replace(" ", "_")] = entrada
        
        marco_botones = tk.Frame(marco_principal, bg='#041955')
        marco_botones.pack(side='bottom', pady=20)
        
        tk.Button(marco_botones, text="Guardar Cambios", 
                 command=lambda: self.actualizar_medicamento(medicamento.id_medicamento),
                 bg='#00d4ff', fg='black', font=('Arial', 12), 
                 bd=0, padx=20, pady=5, activebackground='#00d4ff').pack(side='left', padx=10)
        tk.Button(marco_botones, text="Cancelar", command=self.mostrar_menu_editar,
                 bg='#97b4ff', fg='black', font=('Arial', 12), 
                 bd=0, padx=20, pady=5, activebackground='#97b4ff').pack(side='left', padx=10)
    
    def actualizar_medicamento(self, medicamento_id):
        datos = {key: entry.get() for key, entry in self.entradas_edicion.items() if key != 'id_medicamento'}
        
        if not all(datos.values()):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        conn = connection.getConnection()
        if conn is None:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            return
        
        try:
            cursor = conn.cursor()
            query = """
                UPDATE medicamentos SET 
                nombre_comercial = %s, 
                principio_activo = %s, 
                concentracion = %s, 
                presentacion = %s, 
                via_administracion = %s, 
                fabricante = %s,
                dosis_x_kg = %s
                WHERE id_medicamento = %s
            """
            cursor.execute(query, (
                datos['nombre_comercial'],
                datos['principio_activo'],
                datos['concentracion'],
                datos['presentacion'],
                datos['via_administracion'],
                datos['fabricante'],
                datos['dosis_x_kg'],
                medicamento_id
            ))
            conn.commit()
            messagebox.showinfo("Éxito", "Medicamento actualizado correctamente")
            self.mostrar_menu_editar()
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al actualizar: {e}")
        finally:
            if conn:
                conn.close()
    
    def eliminar_medicamento_seleccionado(self, tabla):
        seleccionado = tabla.focus()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Por favor seleccione un medicamento")
            return
        
        item = tabla.item(seleccionado)
        medicamento_id = item['values'][0]
        medicamento_nombre = item['values'][1]
        
        confirmar = messagebox.askyesno(
            "Confirmar Eliminación", 
            f"¿Está seguro que desea eliminar el medicamento '{medicamento_nombre}'?"
        )
        
        if not confirmar:
            return
        
        conn = connection.getConnection()
        if conn is None:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            return
        
        try:
            cursor = conn.cursor()
            query = "DELETE FROM medicamentos WHERE id_medicamento = %s"
            cursor.execute(query, (medicamento_id,))
            conn.commit()
            messagebox.showinfo("Éxito", "Medicamento eliminado correctamente")
            self.mostrar_menu_editar()
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al eliminar: {e}")
        finally:
            if conn:
                conn.close()
    
    def mostrar_menu_ver(self):
        self.limpiar_pantalla()
        
        marco_principal = tk.Frame(self.master, bg='#041955')
        marco_principal.pack(expand=True, fill='both', padx=50, pady=30)
        
        tk.Label(marco_principal, text="VER MEDICAMENTOS", font=('Arial', 20, 'bold'), 
                bg='#00d4ff', fg="#000000", pady=10).pack()
        
        marco_lista = tk.Frame(marco_principal, bg='#041955')
        marco_lista.pack(fill='both', expand=True)
        
        medicamentos = self.obtener_medicamentos()
        
        if not medicamentos:
            tk.Label(marco_lista, text="No hay medicamentos registrados", 
                    bg='#041955', fg='white', font=('Arial', 12)).pack(pady=20)
            tk.Button(marco_principal, text="Regresar", command=self.crear_menu_principal,
                    bg='#97b4ff', fg='black', font=('Arial', 12), 
                    bd=0, padx=20, pady=5, activebackground='#97b4ff').pack(side='bottom', pady=20)
            return
        
        estilo_tabla = ttk.Style()
        estilo_tabla.configure("Treeview", 
                             background="#97b4ff",
                             foreground="black",
                             fieldbackground="#97b4ff",
                             font=('Arial', 11))
        estilo_tabla.configure("Treeview.Heading", 
                             background="#3450a1",
                             foreground="black",
                             font=('Arial', 12, 'bold'))
        estilo_tabla.map("Treeview", background=[('selected', '#3450a1')])
        
        tabla = ttk.Treeview(marco_lista, columns=('id', 'nombre', 'principio'), show='headings')
        tabla.heading('id', text='ID')
        tabla.heading('nombre', text='Nombre Comercial')
        tabla.heading('principio', text='Principio Activo')
        
        for med in medicamentos:
            tabla.insert('', 'end', values=(med.id_medicamento, med.nombre_comercial, med.principio_activo))
        
        tabla.pack(fill='both', expand=True, padx=10, pady=10)
        
        marco_botones = tk.Frame(marco_principal, bg='#041955')
        marco_botones.pack(side='bottom', pady=20)
        
        tk.Button(marco_botones, text="Ver Detalles", 
                 command=lambda: self.ver_detalles_medicamento(tabla),
                 bg='#00d4ff', fg='black', font=('Arial', 12), 
                 bd=0, padx=20, pady=5, activebackground="#00d4ff").pack(side='left', padx=10)
        tk.Button(marco_botones, text="Regresar", command=self.crear_menu_principal,
                 bg='#97b4ff', fg='black', font=('Arial', 12), 
                 bd=0, padx=20, pady=5, activebackground='#97b4ff').pack(side='left', padx=10)
    
    def ver_detalles_medicamento(self, tabla):
        seleccionado = tabla.focus()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Por favor seleccione un medicamento")
            return
        
        item = tabla.item(seleccionado)
        medicamento_id = item['values'][0]
        
        conn = connection.getConnection()
        if conn is None:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            return
        
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM medicamentos WHERE id_medicamento = %s"
            cursor.execute(query, (medicamento_id,))
            resultado = cursor.fetchone()
            
            if resultado:
                self.mostrar_ventana_detalles(resultado)
            else:
                messagebox.showerror("Error", "Medicamento no encontrado")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")
        finally:
            if conn:
                conn.close()
    
    def mostrar_ventana_detalles(self, datos_medicamento):
        ventana_detalles = tk.Toplevel(self.master)
        ventana_detalles.title("Detalles del Medicamento")
        ventana_detalles.geometry("500x430")
        ventana_detalles.configure(bg='#041955')
        
        tk.Label(ventana_detalles, text=f"DETALLES: {datos_medicamento['nombre_comercial']}", 
                font=('Arial', 16, 'bold'), bg='#00d4ff', fg="#000000", pady=10).pack()
        
        marco_detalles = tk.Frame(ventana_detalles, bg='#041955')
        marco_detalles.pack(fill='both', expand=True, padx=20, pady=10)
        
        campos = [
            ("ID Medicamento:", datos_medicamento['id_medicamento']),
            ("Nombre Comercial:", datos_medicamento['nombre_comercial']),
            ("Principio Activo:", datos_medicamento['principio_activo']),
            ("Concentracion:", datos_medicamento['concentracion']),
            ("Presentacion:", datos_medicamento['presentacion']),
            ("Via Administracion:", datos_medicamento['via_administracion']),
            ("Fabricante:", datos_medicamento['fabricante']),
            ("Dosis por kg:", datos_medicamento['dosis_x_kg'])
        ]
        
        for i, (etiqueta, valor) in enumerate(campos):
            tk.Label(marco_detalles, text=etiqueta, bg='#041955', fg='white', 
                    font=('Arial', 12, 'bold')).grid(row=i, column=0, sticky='e', padx=10, pady=5)
            tk.Label(marco_detalles, text=valor, bg='#041955', fg='#97b4ff', 
                    font=('Arial', 12)).grid(row=i, column=1, sticky='w', padx=10, pady=5)
        
        tk.Button(ventana_detalles, text="Cerrar", command=ventana_detalles.destroy,
                 bg='#97b4ff', fg='black', font=('Arial', 12), 
                 bd=0, padx=20, pady=5, activebackground='#97b4ff').pack(side='bottom', pady=20)
    
    def obtener_medicamentos(self):
        conn = connection.getConnection()
        if conn is None:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            return []
        
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM medicamentos ORDER BY nombre_comercial"
            cursor.execute(query)
            resultados = cursor.fetchall()
            
            medicamentos = []
            for resultado in resultados:
                medicamento = Medicamento(
                    id_medicamento=resultado['id_medicamento'],
                    nombre_comercial=resultado['nombre_comercial'],
                    principio_activo=resultado['principio_activo'],
                    concentracion=resultado['concentracion'],
                    presentacion=resultado['presentacion'],
                    via_administracion=resultado['via_administracion'],
                    fabricante=resultado['fabricante'],
                    dosis_x_kg=resultado['dosis_x_kg']
                )
                medicamentos.append(medicamento)
            
            return medicamentos
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al obtener medicamentos: {e}")
            return []
        finally:
            if conn:
                conn.close()
    
    def limpiar_pantalla(self):
        for widget in self.master.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = MedicamentosApp()
    app.master.mainloop()