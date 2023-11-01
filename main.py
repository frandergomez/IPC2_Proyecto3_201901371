import xml.etree.ElementTree as ET

from flask import Flask, request, jsonify, make_response

from flask_cors import CORS

from utileria.mntConfiguracionXML import SentimientosDictionary
from utileria.mntMensajeXML import MensajesXMLManager

from collections import defaultdict
import re
from datetime import datetime



app = Flask(__name__)
CORS(app)

# Datos donde almacenar los mensajes procesados en formato XML
messages_data = []





@app.route('/grabarMensaje', methods=['POST'])
def grabar_mensaje():
    if 'file' not in request.files:
        return jsonify({
            "message": "No se ha enviado un archivo, intente de nuevo"
        })
    file = request.files['file']
    file_contents = file.read().decode('utf-8')

    # Crear una instancia de la clase MensajesXMLManager
    manager = MensajesXMLManager()


    # Analizar el XML desde la cadena
    root = ET.fromstring(file_contents)

    # Iterar a través de los mensajes e imprimir <FECHA> y <TEXTO>
    for mensaje in root.findall(".//MENSAJE"):
        fecha = mensaje.find("FECHA").text
        texto = mensaje.find("TEXTO").text
        print(f"Fecha: {fecha}")
        print(f"Texto: {texto}")
        print()
        # Agregar un nuevo mensaje
        nueva_fecha = fecha
        nuevo_texto = texto
        manager.agregar_mensaje(nueva_fecha, nuevo_texto)


    return jsonify({
        "message": "El mensaje fue grabado con éxito"
    })




@app.route('/grabarConfiguracion', methods=['POST'])
def grabar_configuracion():
    if 'file' not in request.files:
        return jsonify({
            "message": "No se ha enviado un archivo, intente de nuevo"
        })
    file = request.files['file']
    file_contents = file.read().decode('utf-8')
    messages_data.append({"config": file_contents})


    # Crear un diccionario de sentimientos
    diccionario = SentimientosDictionary()
    # Cargar el diccionario desde un archivo (o crearlo si no existe)
    diccionario.cargar_desde_archivo("sentimientos.xml")

    # Parsear el XML desde el string
    root = ET.fromstring(file_contents)

    # Iterar sobre los elementos y mostrar las palabras con su sentimiento
    for sentimiento in root:
        for palabra in sentimiento:
            # sentimiento_type = "positivo" if sentimiento.tag == "sentimientos_positivos" else "negativo"

            if sentimiento.tag == "sentimientos_positivos":
                print(f"Palabra: {palabra.text.strip()}, Sentimiento: positivo")
                diccionario.agregar_palabra(palabra.text.strip(), "positivo")
            else:
                print(f"Palabra: {palabra.text.strip()}, Sentimiento: negativo")
                diccionario.agregar_palabra(palabra.text.strip(), "negativo")




    # Guardar el diccionario en un archivo
    diccionario.guardar_en_archivo("sentimientos.xml")


    return jsonify({
        "message": "La configuración del servidor fue grabada con éxito"
    })

@app.route('/limpiarDatos', methods=['POST'])
def limpiar_datos():
    messages_data.clear()
    return jsonify({"message": "Datos limpiados exitosamente"})

@app.route('/devolverMenciones', methods=['GET'])
def devolver_menciones():
    # Cargar el diccionario desde un archivo
    diccionario = SentimientosDictionary()
    diccionario.cargar_desde_archivo("sentimientos.xml")

    # Obtener todas las palabras del diccionario
    palabras_unicas = set()
    palabras_repetidas = {}
    for sentimiento in [diccionario.sentimientos_positivos, diccionario.sentimientos_negativos]:
        for palabra_element in sentimiento:
            palabra = palabra_element.text.strip().lower()  # Convertir a minúsculas para evitar duplicados
            if palabra in palabras_unicas:
                if palabra in palabras_repetidas:
                    palabras_repetidas[palabra] += 1
                else:
                    palabras_repetidas[palabra] = 2  # La primera repetición
            else:
                palabras_unicas.add(palabra)

    # Crear un nuevo XML con las palabras únicas y su frecuencia
    root = ET.Element("diccionario")
    for palabra in palabras_unicas:
        elemento = ET.SubElement(root, "palabra")
        elemento.text = palabra
        if palabra in palabras_repetidas:
            elemento.set("repeticiones", str(palabras_repetidas[palabra]))

    # Convertir el XML en una respuesta XML
    response = make_response(ET.tostring(root, encoding="utf-8").decode("utf-8"))
    response.headers['Content-Type'] = 'application/xml'


    return response



@app.route('/devolverHashtags', methods=['GET'])
def get_hashtags_by_date():
    # Cargamos el archivo XML
    tree = ET.parse('mensajes.xml')
    root = tree.getroot()

    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    if start_date_str is None or end_date_str is None:
        return "Debe proporcionar las fechas de inicio y fin en el formato dd/MM/AAAA", 400

    start_date = datetime.strptime(start_date_str, '%d/%m/%Y').date()
    end_date = datetime.strptime(end_date_str, '%d/%m/%Y').date()

    hashtags_by_date = defaultdict(lambda: defaultdict(int))

    for mensaje in root.findall('MENSAJE'):
        fecha_element = mensaje.find('FECHA')
        fecha_text = fecha_element.text
        fecha = get_fecha(fecha_text)
        if fecha and start_date <= fecha <= end_date:
            texto_element = mensaje.find('TEXTO')
            hashtags = get_hashtags(texto_element.text)
            for hashtag in hashtags:
                hashtags_by_date[fecha][hashtag] += 1

    response = make_response(generate_xml_response(hashtags_by_date))
    response.headers["Content-Type"] = "application/xml"
    return response

def generate_xml_response(hashtags_by_date):
    root = ET.Element("hashtags")

    for fecha, hashtags in hashtags_by_date.items():
        dia_element = ET.SubElement(root, "dia")
        fecha_element = ET.SubElement(dia_element, "fecha")
        fecha_element.text = fecha.strftime('%d/%m/%Y')

        for hashtag, count in hashtags.items():
            hashtag_element = ET.SubElement(dia_element, "hashtag")
            titulo_element = ET.SubElement(hashtag_element, "titulo")
            titulo_element.text = "#" + hashtag + "#"
            numeromensaje_element = ET.SubElement(hashtag_element, "numeromensaje")
            numeromensaje_element.text = str(count)

    return ET.tostring(root, encoding="unicode")
def get_hashtags(text):
    hashtags = re.findall(r'#\w+#', text)
    return list(set(hashtag.lower() for hashtag in hashtags))  # Utilizamos un conjunto para eliminar duplicados

def get_fecha(text):
    date_match = re.search(r'(\d{2}/\d{2}/\d{4})', text)
    if date_match:
        return datetime.strptime(date_match.group(1), '%d/%m/%Y').date()
    return None




if __name__ == '__main__':
    app.run(debug=True)