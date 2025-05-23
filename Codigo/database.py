import mysql.connector
from tkinter import messagebox

def conectar():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="medicalbase"
        )
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error de conexión a MySQL: {err}")
        return None

def ejecutar_consulta(query, parametros=None, fetch=False):
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)  # Para obtener resultados como diccionarios
            cursor.execute(query, parametros or ())
            
            if fetch:
                return cursor.fetchall()  # Devuelve múltiples registros
            else:
                conn.commit()
                return True
                
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error en consulta: {err}")
            return False
        finally:
            conn.close()

# Nueva función específica para obtener un solo registro
def obtener_un_registro(query, parametros=None):
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, parametros or ())
            return cursor.fetchone()  # Devuelve solo un registro
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error en consulta: {err}")
            return None
        finally:
            conn.close()