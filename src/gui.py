import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import requests
from amiibo import Amiibo

class AmiiboApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Amiibo App")
        self.amiibos = []

        # Configuración de la interfaz
        tk.Label(root, text="Buscar por columna:").grid(row=0, column=0, padx=10, pady=5)
        self.columna_var = tk.StringVar(value="name")
        tk.Entry(root, textvariable=self.columna_var).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(root, text="Valor a buscar:").grid(row=1, column=0, padx=10, pady=5)
        self.valor_var = tk.StringVar()
        tk.Entry(root, textvariable=self.valor_var).grid(row=1, column=1, padx=10, pady=5)

        tk.Button(root, text="Buscar", command=self.buscar).grid(row=2, column=0, padx=10, pady=5)
        tk.Button(root, text="Exportar a CSV", command=self.exportar).grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        # Configurar el Treeview para mostrar los amiibos
        self.tree = ttk.Treeview(root, columns=("Amiibo Series", "Character", "Game Series", "Name", "Image", "Type"), show='headings')
        self.tree.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # Definir encabezados
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        # Cargar datos automáticamente al iniciar la aplicación
        self.cargar_datos()

    def cargar_datos(self):
        url = "https://raw.githubusercontent.com/matthewlyons/amiibo-database/master/db/amiibo.json"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Verifica si hay un error HTTP
            data = response.json()
            self.amiibos = [Amiibo(item['amiiboSeries'], item['character'], item['gameSeries'], 
                                   item['name'], item['image'], item['type']) for item in data]
            #messagebox.showinfo("Cargar Datos", "Datos cargados correctamente.")
            self.mostrar_datos()  # Llamar a la función para mostrar datos en la tabla
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de Carga", f"No se pudieron cargar los datos:\n{e}")

    def mostrar_datos(self):
        # Limpiar el Treeview antes de mostrar nuevos datos
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Insertar los datos en el Treeview
        for amiibo in self.amiibos:
            self.tree.insert("", "end", values=(amiibo.amiiboSeries, amiibo.character, amiibo.gameSeries,
                                                 amiibo.name, amiibo.image, amiibo.type))

    def buscar(self):
        columna = self.columna_var.get()
        valor = self.valor_var.get()

        # Verificar si la columna es un atributo válido de la clase Amiibo
        if columna not in Amiibo.valid_attributes:
            messagebox.showwarning("Atributo no válido", f"El atributo '{columna}' no existe.")
            return

        if not self.amiibos:
            messagebox.showwarning("Sin Datos", "Primero debes cargar los datos.")
            return

        resultado = Amiibo.buscar_por_atributo(self.amiibos, columna, valor)
        self.mostrar_resultados(resultado)



    def mostrar_resultados(self, resultados):
        # Limpiar el Treeview antes de mostrar nuevos resultados
        for row in self.tree.get_children():
            self.tree.delete(row)

        if resultados:
            for amiibo in resultados:
                self.tree.insert("", "end", values=(amiibo.amiiboSeries, amiibo.character, amiibo.gameSeries,
                                                     amiibo.name, amiibo.image, amiibo.type))
        else:
            messagebox.showinfo("Resultados de Búsqueda", "No se encontraron resultados.")

    def exportar(self):
        if not self.amiibos:
            messagebox.showwarning("Sin Datos", "Primero debes cargar los datos.")
            return
        ruta_csv = Amiibo.exportar_a_csv(self.amiibos)
        messagebox.showinfo("Exportar a CSV", f"Datos exportados a {ruta_csv}")
