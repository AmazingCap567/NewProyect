import os
import sys

def ruta_relativa(ruta):
    if getattr(sys, 'frozen', False):
        base = sys._MEIPASS  # carpeta temporal cuando se ejecuta como .exe
    else:
        base = os.path.abspath(".")  # carpeta raíz del proyecto en desarrollo
    return os.path.join(base, ruta)

def obtener_ruta_db():
    return ruta_relativa("database.db")


def buscar_archivo(nombre_parcial, carpeta=".", extensiones=None):
    """Busca el primer archivo que contenga `nombre_parcial` dentro de `carpeta` y tenga una de las extensiones permitidas."""
    carpeta_absoluta = ruta_relativa(carpeta)
    if not os.path.exists(carpeta_absoluta):
        return None

    for archivo in os.listdir(carpeta_absoluta):
        nombre, ext = os.path.splitext(archivo)
        if nombre_parcial.lower() in nombre.lower():
            if extensiones is None or ext.lower() in [e.lower() for e in extensiones]:
                return os.path.join(carpeta_absoluta, archivo)
    return None
