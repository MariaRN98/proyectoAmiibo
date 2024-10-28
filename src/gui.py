import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import requests
from amiibo import Amiibo

class Gui:
    def __init__(self, root):
        self.root = root
        self.root.title("Amiibo App")
        self.amiibos = []

        # Configuración de la interfaz
        self.filtros_frame = tk.Frame(root)
        self.filtros_frame.grid(row=0, column=0, padx=10, pady=10)

        # Crear campos de búsqueda para cada columna
        self.columnas = Amiibo.valid_attributes  # Usar los atributos válidos de Amiibo
        
        self.filtro_vars = {}
        for idx, columna in enumerate(self.columnas):
            tk.Label(self.filtros_frame, text=f"{columna}:").grid(row=idx, column=0, padx=5, pady=5)
            entry_var = tk.StringVar()
            entry = tk.Entry(self.filtros_frame, textvariable=entry_var)
            entry.grid(row=idx, column=1, padx=5, pady=5)
            self.filtro_vars[columna] = entry_var  # Guardar solo el valor de entrada

        tk.Button(root, text="Buscar", command=self.buscar).grid(row=len(self.columnas), column=0, padx=10, pady=5)
        tk.Button(root, text="Restablecer", command=self.restablecer).grid(row=len(self.columnas), column=1, padx=10, pady=5)
        tk.Button(root, text="Exportar a CSV", command=self.exportar).grid(row=len(self.columnas), column=2, padx=10, pady=5)

        # Configurar el Treeview para mostrar los amiibos
        self.tree = ttk.Treeview(root, columns=("Amiibo Series", "Character", "Game Series", "Name", "Image", "Type"), show='headings')
        self.tree.grid(row=len(self.columnas) + 1, column=0, columnspan=3, padx=10, pady=10)

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
            messagebox.showinfo("Cargar Datos", "Datos cargados correctamente.")
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
        # Obtener los criterios de búsqueda
        filtros = {}
        for columna, entry_var in self.filtro_vars.items():
            valor = entry_var.get().strip()
            if valor:  # Solo agregar si hay valor
                filtros[columna] = valor

        if not filtros:
            messagebox.showwarning("Sin Filtros", "Por favor, ingrese al menos un filtro.")
            return

        # Filtrar los amiibos según los criterios
        resultado = self.amiibos
        for columna, valor in filtros.items():
            resultado = [amiibo for amiibo in resultado if getattr(amiibo, columna, None) == valor]

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

    def restablecer(self):
        # Limpiar todos los campos de entrada
        for entry_var in self.filtro_vars.values():
            entry_var.set("")  # Limpiar el contenido de la entrada

        # Mostrar todos los amiibos de nuevo
        self.mostrar_datos()

    def exportar(self):
        if not self.amiibos:
            messagebox.showwarning("Sin Datos", "Primero debes cargar los datos.")
            return
        ruta_csv = Amiibo.exportar_a_csv(self.amiibos)
        messagebox.showinfo("Exportar a CSV", f"Datos exportados a {ruta_csv}") 