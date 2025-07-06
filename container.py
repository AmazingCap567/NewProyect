from tkinter import *
import tkinter as tk
from ventas import Ventas
from inventario import Inventario
from clientes import Clientes
from vendedores import Vendedores
from proveedor import Proveedor
from informacion import Informacion 
import sys 
import os 

class Container(tk.Frame):
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador = controlador
        self.pack()
        self.place(x=0, y=0, width=1100, height=650)
        self.widgets()
        self.frames = {}
        self.buttons = []
        for i in (Ventas, Inventario, Clientes, Vendedores, Proveedor, Informacion):
            frame = i(self)
            self.frames[i] = frame
            frame.pack()
            frame.config(bg="#C6D9E3", highlightbackground= "gray", highlightthickness=1)
            frame.place(x=0, y=40, width= 1100, height=610)
        self.show_frames(Ventas)

    def show_frames(self, container):
        frame = self.frames[container]
        frame.tkraise()

    def ventas(self):
        self.show_frames(Ventas)

    def inventario(self):
        self.show_frames(Inventario)

    def clientes(self):
        self.show_frames(Clientes)

    def vendedores(self):
        self.show_frames(Vendedores)

    def proveedor(self):
        self.show_frames(Proveedor)

    def informacion(self):
        self.show_frames(Informacion)

    def widgets(self):
        frame2 = tk.Frame(self)
        frame2.place(x=0, y=0, width=1100, height=40)

        self.btn_ventas = Button(frame2, fg="black", text="Ventas", font="sans 16 bold", command=self.ventas)
        self.btn_ventas.place(x=0, y=0, width=184, height=40)
        
        self.btn_inventario = Button(frame2, fg="black", text="Inventario", font="sans 16 bold", command=self.inventario)
        self.btn_inventario.place(x=184, y=0, width=184, height=40)
        
        self.btn_clientes = Button(frame2, fg="black", text="Clientes", font="sans 16 bold", command=self.clientes)
        self.btn_clientes.place(x=369, y=0, width=184, height=40)
        
        self.btn_vendedores = Button(frame2, fg="black", text="Vendedores", font="sans 16 bold", command=self.vendedores)
        self.btn_vendedores.place(x=554, y=0, width=184, height=40)
        
        self.btn_proveedor = Button(frame2, fg="black", text="Proveedor", font="sans 16 bold", command=self.proveedor)
        self.btn_proveedor.place(x=739, y=0, width=184, height=40)
        
        self.btn_informacion = Button(frame2, fg="black", text="Informacion", font="sans 16 bold", command=self.informacion)
        self.btn_informacion.place(x=923, y=0, width=184, height=40)
        self.buttons = [self.btn_ventas, self.btn_inventario, self.btn_clientes, self.btn_vendedores, self.btn_proveedor, self.btn_informacion]

