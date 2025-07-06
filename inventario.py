import sqlite3
from tkinter import *
import tkinter as tk 
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import threading
import os

class Inventario(tk.Frame):
    def __init__(self, padre):
        super().__init__(padre)
        self.verificar_estructura_bd()
        self.widgets()
        self.articulos_combobox()
        self.cargar_articulos()
        self.timer_articulos = None
        self.image_folder = "fotos"
        if not os.path.exists(self.image_folder):
            os.makedirs(self.image_folder)
        
        # Variables para la cuadrícula
        self.row = 0
        self.column = 0

    def verificar_estructura_bd(self):
        try:
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("PRAGMA table_info(articulos)")
                columns = [col[1] for col in cur.fetchall()]
                if 'image_path' not in columns:
                    cur.execute("ALTER TABLE articulos ADD COLUMN image_path TEXT")
                    con.commit()
        except sqlite3.Error as e:
            print(f"Error al verificar estructura BD: {e}")

    def widgets(self):
        canvas_articulos = tk.LabelFrame(self, text="Artículos", font="arial 14 bold", bg="#C6D9E3")
        canvas_articulos.place(x=300, y=10, width=700, height=500)

        self.canvas = tk.Canvas(canvas_articulos, bg="#C6D9E3")
        self.scrollbar = tk.Scrollbar(canvas_articulos, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#C6D9E3")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        lblframe_buscar = LabelFrame(self, text="Buscar", font="arial 14 bold", bg="#C6D9E3")
        lblframe_buscar.place(x=10, y=10, width=280, height=80)

        self.comboboxbuscar = ttk.Combobox(lblframe_buscar, font="arial 12")
        self.comboboxbuscar.place(x=5, y=5, width=260, height=40)
        self.comboboxbuscar.bind("<<ComboboxSelected>>", self.on_combobox_select)
        self.comboboxbuscar.bind("<KeyRelease>", self.filtrar_articulos)

        lblframe_seleccion = LabelFrame(self, text="Seleccion", font="arial 14 bold", bg="#C6D9E3")
        lblframe_seleccion.place(x=10, y=95, width=280, height=190)

        self.label1 = tk.Label(lblframe_seleccion, text="Artículo", font="arial 12", bg="#C6D9E3", wraplength=300)
        self.label1.place(x=5, y=5)

        self.label2 = tk.Label(lblframe_seleccion, text="Precio", font="arial 12", bg="#C6D9E3")
        self.label2.place(x=5, y=40)

        self.label3 = tk.Label(lblframe_seleccion, text="Costo", font="arial 12", bg="#C6D9E3")
        self.label3.place(x=5, y=70)

        self.label4 = tk.Label(lblframe_seleccion, text="Stock", font="arial 12", bg="#C6D9E3")
        self.label4.place(x=5, y=100)

        self.label5 = tk.Label(lblframe_seleccion, text="Estado", font="arial 12", bg="#C6D9E3")
        self.label5.place(x=5, y=130)

        lblframe_botones = LabelFrame(self, bg="#C6D9E3", text="Opciones", font="arial 14 bold")
        lblframe_botones.place(x=10, y=290, width=280, height=300)

        btn1 = tk.Button(lblframe_botones, text="Agregar", font="arial 14 bold", command=self.agregar_articulos)
        btn1.place(x=20, y=20, width=180, height=40)

        btn2 = tk.Button(lblframe_botones, text="Editar", font="arial 14 bold", command=self.editar_articulo)
        btn2.place(x=20, y=80, width=180, height=40)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif")])
        if file_path:
            try:
                image = Image.open(file_path)
                image = image.resize((200, 200), Image.LANCZOS)
                image_name = os.path.basename(file_path)
                image_save_path = os.path.join(self.image_folder, image_name)
                image.save(image_save_path)

                self.image_tk = ImageTk.PhotoImage(image)
                self.product_image = self.image_tk
                self.image_path = image_save_path

                img_label = tk.Label(self.frameimg, image=self.image_tk)
                img_label.place(x=0, y=0, width=200, height=200)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar la imagen: {str(e)}")

    def articulos_combobox(self):
        try:
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("SELECT articulo FROM articulos")
                self.articulos = [row[0] for row in cur.fetchall()]
                self.comboboxbuscar['values'] = self.articulos
        except sqlite3.Error as e:
            print("Error al cargar los artículos:", e)
            messagebox.showerror("Error", "No se pudo cargar la lista de artículos")
    
    def cargar_articulos(self, filtro=None):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        query = "SELECT articulo, precio, image_path FROM articulos"
        params = []

        if filtro:
            query += " WHERE articulo LIKE ?"
            params.append(f'%{filtro}%')

        try:
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute(query, params)
                articulos = cur.fetchall()

                self.row = 0
                self.column = 0

                for articulo, precio, image_path in articulos:
                    self.mostrar_articulo_individual(articulo, precio, image_path)

        except sqlite3.Error as e:
            print("Error al cargar artículos:", e)
            messagebox.showerror("Error", "No se pudieron cargar los artículos")

    def mostrar_articulo_individual(self, articulo, precio, image_path):
        # Frame contenedor
        article_frame = tk.Frame(
            self.scrollable_frame, 
            bg="white", 
            relief="groove", 
            bd=2,
            padx=5,
            pady=5
        )
        article_frame.grid(
            row=self.row, 
            column=self.column, 
            padx=10, 
            pady=10, 
            sticky="nsew"
        )
        
        # Manejo de imágenes
        img_path = image_path if image_path and os.path.exists(image_path) else "fotos/default.png"
        
        try:
            img = Image.open(img_path)
            img = img.resize((150, 150), Image.LANCZOS)
            photo_img = ImageTk.PhotoImage(img)
            
            img_label = tk.Label(
                article_frame, 
                image=photo_img, 
                bg="white"
            )
            img_label.image = photo_img  # Mantener referencia
            img_label.pack(pady=(0, 5))
            
        except Exception as e:
            print(f"Error cargando imagen {img_path}: {e}")
            error_label = tk.Label(
                article_frame, 
                text="Imagen no disponible",
                bg="white",
                fg="red"
            )
            error_label.pack(pady=(0, 5))
        
        # Nombre del artículo
        nombre_label = tk.Label(
            article_frame,
            text=articulo,
            bg="white",
            font=("Arial", 10, "bold"),
            wraplength=140
        )
        nombre_label.pack()
        
        # Precio
        precio_text = f"Precio: ${float(precio):.2f}" if precio else "Precio: N/D"
        precio_label = tk.Label(
            article_frame,
            text=precio_text,
            bg="white",
            font=("Arial", 9)
        )
        precio_label.pack()
        
        # Configurar grid
        self.column += 1
        if self.column >= 3:  # 4 columnas por fila
            self.column = 0
            self.row += 1

    def agregar_articulos(self):
        top = tk.Toplevel(self)
        top.title("Agregar Artículo")
        top.geometry("700x400+200+50")
        top.config(bg="#C6D9E3")
        top.resizable(False, False)

        top.transient(self.master)
        top.grab_set()
        top.focus_set()
        top.lift()

        tk.Label(top, text="Artículos", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=20, width=80, height=25)
        entry_articulos = ttk.Entry(top, font="arial 12 bold")
        entry_articulos.place(x=120, y=20, width=250, height=30)

        tk.Label(top, text="Precio", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=60, width=80, height=25)
        entry_precio = ttk.Entry(top, font="arial 12 bold")
        entry_precio.place(x=120, y=60, width=250, height=30)

        tk.Label(top, text="Costo", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=100, width=80, height=25)
        entry_costo = ttk.Entry(top, font="arial 12 bold")
        entry_costo.place(x=120, y=100, width=250, height=30)

        tk.Label(top, text="Stock", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=140, width=80, height=25)
        entry_stock = ttk.Entry(top, font="arial 12 bold")
        entry_stock.place(x=120, y=140, width=250, height=30)

        tk.Label(top, text="Estado", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=180, width=80, height=25)
        entry_estado = ttk.Entry(top, font="arial 12 bold")
        entry_estado.place(x=120, y=180, width=250, height=30)

        self.frameimg = tk.Frame(top, bg="white", highlightbackground="gray", highlightthickness=1)
        self.frameimg.place(x=440, y=30, width=200, height=200)

        btnimage = tk.Button(top, text="Cargar imagen", font="arial 12 bold", command=self.load_image)
        btnimage.place(x=470, y=260, width=150, height=40)

        def guardar():
            articulo = entry_articulos.get()
            precio = entry_precio.get()
            costo = entry_costo.get()
            stock = entry_stock.get()
            estado = entry_estado.get()

            if not articulo or not precio or not costo or not stock or not estado:
                messagebox.showerror("Error", "Todos los campos deben ser completados")
                return
            
            try:
                precio = float(precio)
                costo = float(costo)
                stock = int(stock)
            except ValueError:
                messagebox.showerror("Error", "Precio, costo y stock deben ser números válidos")
                return
            
            image_path = getattr(self, 'image_path', "fotos/default.png")

            try:
                with sqlite3.connect("database.db") as con:
                    cur = con.cursor()
                    cur.execute("""
                        INSERT INTO articulos (articulo, precio, costo, stock, estado, image_path)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (articulo, precio, costo, stock, estado, image_path))
                    con.commit()
                messagebox.showinfo("Éxito", "Artículo agregado correctamente")
                top.destroy()
                self.cargar_articulos()
                self.articulos_combobox()
            except sqlite3.Error as e:
                print("Error al cargar el artículo", e)
                messagebox.showerror("Error", "Error al guardar el artículo")

        tk.Button(top, text="Guardar", font="arial 12 bold", command=guardar).place(x=50, y=260, width=150, height=40)
        tk.Button(top, text="Cancelar", font="arial 12 bold", command=top.destroy).place(x=260, y=260, width=150, height=40)

    def on_combobox_select(self, event):
        self.actualizar_label()

    def actualizar_label(self, event=None):
        articulo_seleccionado = self.comboboxbuscar.get()

        try:
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("SELECT articulo, precio, costo, stock, estado FROM articulos WHERE articulo=?", (articulo_seleccionado,))
                resultado = cur.fetchone()

                if resultado is not None:
                    articulo, precio, costo, stock, estado = resultado

                    self.label1.config(text=f"Artículo: {articulo}")
                    self.label2.config(text=f"Precio: {precio}")
                    self.label3.config(text=f"Costo: {costo}")
                    self.label4.config(text=f"Stock: {stock}")
                    self.label5.config(text=f"Estado: {estado}")

                    if estado.lower() == "activo":
                        self.label5.config(fg="green")
                    elif estado.lower() == "inactivo":
                        self.label5.config(fg="red")
                    else:
                        self.label5.config(fg="black")
                else:
                    self.label1.config(text="Artículo: No encontrado")
                    self.label2.config(text="Precio: N/A")
                    self.label3.config(text="Costo: N/A")
                    self.label4.config(text="Stock: N/A")
                    self.label5.config(text="Estado: N/A", fg="black")

        except sqlite3.Error as e:
            print("Error al obtener los datos del artículo:", e)
            messagebox.showerror("Error", "Error al obtener los datos del artículo")

    def filtrar_articulos(self, event=None):
        typed = self.comboboxbuscar.get()

        try:
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("SELECT articulo FROM articulos WHERE articulo LIKE ?", (f"%{typed}%",))
                data = [row[0] for row in cur.fetchall()]
        except sqlite3.Error as e:
            print("Error al filtrar artículos:", e)
            return

        if data:
            self.comboboxbuscar['values'] = data
        else:
            self.comboboxbuscar['values'] = ['No se encontraron resultados']

        self.cargar_articulos(filtro=typed)

    def editar_articulo(self):
        selected_item = self.comboboxbuscar.get()

        if not selected_item:
            messagebox.showerror("Error", "Selecciona un artículo para editar")
            return

        try:
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("SELECT articulo, precio, costo, stock, estado, image_path FROM articulos WHERE articulo=?", (selected_item,))
                resultado = cur.fetchone()
        except sqlite3.Error as e:
            print("Error al consultar el artículo:", e)
            messagebox.showerror("Error", "No se pudo cargar el artículo")
            return

        if not resultado:
            messagebox.showerror("Error", "Artículo no encontrado")
            return

        top = tk.Toplevel(self)
        top.title("Editar Artículo")
        top.geometry("700x400+200+50")
        top.config(bg="#C6D9E3")
        top.resizable(False, False)

        top.transient(self.master)
        top.grab_set()
        top.focus_set()
        top.lift()

        articulo, precio, costo, stock, estado, image_path = resultado

        # Campos de entrada
        tk.Label(top, text="Artículo: ", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=20, width=80, height=25)
        entry_articulo = ttk.Entry(top, font="arial 12 bold")
        entry_articulo.place(x=120, y=20, width=250, height=30)
        entry_articulo.insert(0, articulo)

        tk.Label(top, text="Precio: ", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=60, width=80, height=25)
        entry_precio = ttk.Entry(top, font="arial 12 bold")
        entry_precio.place(x=120, y=60, width=250, height=30)
        entry_precio.insert(0, precio)

        tk.Label(top, text="Costo: ", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=100, width=80, height=25)
        entry_costo = ttk.Entry(top, font="arial 12 bold")
        entry_costo.place(x=120, y=100, width=250, height=30)
        entry_costo.insert(0, costo)

        tk.Label(top, text="Stock: ", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=140, width=80, height=25)
        entry_stock = ttk.Entry(top, font="arial 12 bold")
        entry_stock.place(x=120, y=140, width=250, height=30)
        entry_stock.insert(0, stock)

        tk.Label(top, text="Estado: ", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=180, width=80, height=25)
        entry_estado = ttk.Entry(top, font="arial 12 bold")
        entry_estado.place(x=120, y=180, width=250, height=30)
        entry_estado.insert(0, estado)

        # Imagen actual
        self.frameimg = tk.Frame(top, bg="white", highlightbackground="gray", highlightthickness=1)
        self.frameimg.place(x=440, y=30, width=200, height=200)

        if image_path and os.path.exists(image_path):
            image = Image.open(image_path)
            image = image.resize((200, 200), Image.LANCZOS)
            self.product_image = ImageTk.PhotoImage(image)
            self.image_path = image_path
            image_label = tk.Label(self.frameimg, image=self.product_image)
            image_label.pack(expand=True, fill="both")

        btnimagen = tk.Button(top, text="Cargar Imagen", font="arial 12 bold", command=self.load_image)
        btnimagen.place(x=470, y=260, width=150, height=40)

        def guardar():
            nuevo_articulo = entry_articulo.get()
            nuevo_precio = entry_precio.get()
            nuevo_costo = entry_costo.get()
            nuevo_stock = entry_stock.get()
            nuevo_estado = entry_estado.get()

            if not nuevo_articulo or not nuevo_precio or not nuevo_costo or not nuevo_stock or not nuevo_estado:
                messagebox.showerror("Error", "Todos los campos deben ser completados")
                return

            try:
                nuevo_precio = float(nuevo_precio)
                nuevo_costo = float(nuevo_costo)
                nuevo_stock = int(nuevo_stock)
            except ValueError:
                messagebox.showerror("Error", "Precio, costo y stock deben ser números válidos")
                return

            nuevo_image_path = getattr(self, 'image_path', image_path)

            try:
                with sqlite3.connect("database.db") as con:
                    cur = con.cursor()
                    cur.execute("""
                        UPDATE articulos 
                        SET articulo=?, precio=?, costo=?, stock=?, estado=?, image_path=? 
                        WHERE articulo=?
                    """, (nuevo_articulo, nuevo_precio, nuevo_costo, nuevo_stock, nuevo_estado, nuevo_image_path, selected_item))
                    con.commit()
            except sqlite3.Error as e:
                print("Error al guardar el artículo editado:", e)
                messagebox.showerror("Error", "No se pudo editar el artículo")
                return

            self.articulos_combobox()
            self.cargar_articulos(filtro=nuevo_articulo)
            top.destroy()
            messagebox.showinfo("Éxito", "Artículo editado exitosamente")

        tk.Button(top, text="Guardar", font="arial 12 bold", command=guardar).place(x=260, y=260, width=150, height=40)
        tk.Button(top, text="Cancelar", font="arial 12 bold", command=top.destroy).place(x=50, y=260, width=150, height=40)