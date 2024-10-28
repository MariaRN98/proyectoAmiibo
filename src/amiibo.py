import csv
import os

class Amiibo():
    
    valid_attributes = ["amiiboSeries", "character", "gameSeries", "name", "image", "type"]


    def __init__(self, amiiboSeries, character, gameSeries, name, image, amiibo_type):
        self.amiiboSeries = amiiboSeries
        self.character = character
        self.gameSeries = gameSeries
        self.name = name
        self.image = image
        self.type = amiibo_type

    def __str__(self):
        return (f"Nombre: {self.name}\n"
                f"Personaje: {self.character}\n"
                f"Serie de Amiibo: {self.amiiboSeries}\n"
                f"Videojuego: {self.gameSeries}\n"
                f"Tipo: {self.type}\n"
                f"Image URL: {self.image}\n")
    
    # Función para buscar en diferentes atributos de la clase
    @classmethod
    def buscar_por_atributo(cls, amiibos, atributo, valor):
    # Verificar si el atributo es válido
        # Filtrar los amiibos donde el valor del atributo coincide con el valor dado
        resultado = [amiibo for amiibo in amiibos if getattr(amiibo, atributo, None) == valor]
        return resultado
    
    @classmethod
    def exportar_a_csv(cls, amiibos: list, nombre_archivo: str = "amiibos_exportados.csv"):
        """Exportar la lista de amiibos a un archivo CSV en la carpeta de Descargas"""
        
        # Obtener el directorio de Descargas
        carpeta_descargas = os.path.join(os.path.expanduser("~"), "Downloads", nombre_archivo)
        
        # Definir los nombres de las columnas
        encabezados = ["amiiboSeries", "character", "gameSeries", "name", "image", "type"]

        # Abrir el archivo CSV en modo escritura
        with open(carpeta_descargas, mode='w', newline='', encoding='utf-8') as archivo_csv:
            escritor_csv = csv.writer(archivo_csv)
            
            # Escribir el encabezado
            escritor_csv.writerow(encabezados)
            
            # Escribir los datos de cada amiibo
            for amiibo in amiibos:
                escritor_csv.writerow([
                    amiibo.amiiboSeries,
                    amiibo.character,
                    amiibo.gameSeries,
                    amiibo.name,
                    amiibo.image,
                    amiibo.type
                ])

        print(f"Datos exportados correctamente a '{carpeta_descargas}'")
