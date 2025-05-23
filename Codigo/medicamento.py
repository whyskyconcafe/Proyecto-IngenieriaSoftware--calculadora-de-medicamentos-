# medicamento.py
class Medicamento:
    def __init__(self, id_medicamento=None, nombre_comercial="", principio_activo="", concentracion="", 
                 presentacion="", via_administracion="", fabricante="", dosis_x_kg=""):
        self.id_medicamento = id_medicamento
        self.nombre_comercial = nombre_comercial
        self.principio_activo = principio_activo
        self.concentracion = concentracion
        self.presentacion = presentacion
        self.via_administracion = via_administracion
        self.fabricante = fabricante
        self.dosis_x_kg = dosis_x_kg