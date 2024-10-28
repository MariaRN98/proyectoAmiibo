import tkinter as tk
from gui import Gui

# Crear la ventana raíz
root = tk.Tk()
# Crear instancia de la interfaz AmiiboApp
app = Gui(root)
# Ejecutar la aplicación
root.mainloop()