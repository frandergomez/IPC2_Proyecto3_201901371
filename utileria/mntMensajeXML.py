import xml.etree.ElementTree as ET

class MensajesXMLManager:
    def __init__(self, xml_filename="mensajes.xml"):
        self.xml_filename = xml_filename
        self.tree = self._cargar_xml()

    def _cargar_xml(self):
        try:
            tree = ET.parse(self.xml_filename)
        except FileNotFoundError:
            tree = self._crear_archivo_xml()
        return tree

    def _crear_archivo_xml(self):
        mensajes = ET.Element("MENSAJES")
        tree = ET.ElementTree(mensajes)
        tree.write(self.xml_filename, encoding="utf-8", xml_declaration=True)
        return tree

    def agregar_mensaje(self, fecha, texto):
        root = self.tree.getroot()

        mensaje = ET.Element("MENSAJE")
        fecha_element = ET.Element("FECHA")
        fecha_element.text = fecha
        texto_element = ET.Element("TEXTO")
        texto_element.text = texto

        mensaje.append(fecha_element)
        mensaje.append(texto_element)
        root.append(mensaje)

        self.tree.write(self.xml_filename, encoding="utf-8")

    def leer_mensajes(self):
        mensajes = self.tree.getroot()

        for mensaje in mensajes.findall("MENSAJE"):
            fecha = mensaje.find("FECHA").text
            texto = mensaje.find("TEXTO").text
            print(f"Fecha: {fecha}")
            print(f"Texto: {texto}")
            print()

# Crear una instancia de la clase MensajesXMLManager
#manager = MensajesXMLManager()

# Agregar nuevos mensajes
#nueva_fecha = "Guatemala, 21/01/2023 11:00 hrs."
#nuevo_texto = "Nuevo mensaje 1"
#manager.agregar_mensaje(nueva_fecha, nuevo_texto)

#nueva_fecha = "Guatemala, 21/01/2023 12:00 hrs."
#nuevo_texto = "Nuevo mensaje 2"
#manager.agregar_mensaje(nueva_fecha, nuevo_texto)

# Leer y mostrar los mensajes
#manager.leer_mensajes()
