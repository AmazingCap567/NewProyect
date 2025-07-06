from tkinter import *
from tkinter import ttk
from login import Login
from login import Registro
from container import Container
import sys
import os

# 🔧 Función para obtener ruta relativa al ejecutable o script
def ruta_relativa(ruta):
    if getattr(sys, 'frozen', False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.abspath(".")
    return os.path.join(base, ruta)

# 🔧 Ruta base global para uso en otras partes
RUTA_BASE = ruta_relativa("")  # puedes usar esto en otros módulos si lo importas

class Manager(Tk):
    def __init__(self, *args, **kwagrs):
        super().__init__(*args, **kwagrs)
        self.title("Ferretería V1.0")
        self.geometry("1100x650+120+20")
        self.resizable(False, False)

        # Aquí podrías verificar si las carpetas necesarias existen
        self.verificar_estructura_directorios()

        container = Frame(self)
        container.pack(side=TOP, fill=BOTH, expand=True)
        container.configure(bg="#C6D9E3")

        self.frames = {}
        for i in (Login, Registro, Container):
            frame = i(container, self)
            self.frames[i] = frame 

        self.show_frame(Login)

        self.style = ttk.Style()
        self.style.theme_use("clam")

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()

    def verificar_estructura_directorios(self):
        carpetas = ["fotos", "Facturas"]
        for carpeta in carpetas:
            ruta = ruta_relativa(carpeta)
            if not os.path.exists(ruta):
                os.makedirs(ruta)
                print(f"[INFO] Carpeta creada: {ruta}")

def main():
    app = Manager()
    app.mainloop()

if __name__ == "__main__":
    main()
