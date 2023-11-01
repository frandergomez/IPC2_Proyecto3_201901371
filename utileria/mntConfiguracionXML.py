import xml.etree.ElementTree as ET
import os

class SentimientosDictionary:
    def __init__(self):
        self.tree = ET.ElementTree(ET.Element("diccionario"))
        self.root = self.tree.getroot()
        self.sentimientos_positivos = ET.SubElement(self.root, "sentimientos_positivos")
        self.sentimientos_negativos = ET.SubElement(self.root, "sentimientos_negativos")

    def agregar_palabra(self, palabra, sentimiento):
        if sentimiento == "positivo":
            elemento = ET.SubElement(self.sentimientos_positivos, "palabra")
        elif sentimiento == "negativo":
            elemento = ET.SubElement(self.sentimientos_negativos, "palabra")
        elemento.text = palabra

    def guardar_en_archivo(self, archivo):
        self.tree.write(archivo, encoding="utf-8", xml_declaration=True)

    def cargar_desde_archivo(self, archivo):
        if os.path.exists(archivo):
            self.tree = ET.parse(archivo)
            self.root = self.tree.getroot()
            self.sentimientos_positivos = self.root.find("sentimientos_positivos")
            self.sentimientos_negativos = self.root.find("sentimientos_negativos")
        else:
            # Si el archivo no existe, crea un diccionario vacío
            self.tree = ET.ElementTree(ET.Element("diccionario"))
            self.root = self.tree.getroot()
            self.sentimientos_positivos = ET.SubElement(self.root, "sentimientos_positivos")
            self.sentimientos_negativos = ET.SubElement(self.root, "sentimientos_negativos")

    def __str__(self):
        return ET.tostring(self.root, encoding="utf-8").decode("utf-8")

# Crear un diccionario de sentimientos
# diccionario = SentimientosDictionary()
# diccionario.agregar_palabra("bueno", "positivo")
# diccionario.agregar_palabra("excelente", "positivo")
# diccionario.agregar_palabra("cool", "positivo")
# diccionario.agregar_palabra("satisfecho", "positivo")
# diccionario.agregar_palabra("malo", "negativo")
# diccionario.agregar_palabra("pésimo", "negativo")
# diccionario.agregar_palabra("triste", "negativo")
# diccionario.agregar_palabra("molesto", "negativo")
# diccionario.agregar_palabra("decepcionado", "negativo")
# diccionario.agregar_palabra("enojo", "negativo")

# Cargar el diccionario desde un archivo (o crearlo si no existe)
# diccionario.cargar_desde_archivo("sentimientos.xml")

# Imprimir el diccionario cargado
# print(diccionario)

# Ejemplo de cómo agregar una nueva palabra
# diccionario.agregar_palabra("feliz", "positivo")
# diccionario.guardar_en_archivo("sentimientos.xml")

