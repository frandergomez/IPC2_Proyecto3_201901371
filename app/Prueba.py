from flask import Flask, request, jsonify, Response
import xml.etree.ElementTree as ET
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Datos donde almacenar los mensajes procesados en formato XML
messages_data = []
messages_data2 = []

@app.route('/grabarMensaje', methods=['POST'])
def grabar_mensaje():
    if 'file' not in request.files:
        return jsonify({
            "message": "No se ha enviado un archivo, intente de nuevo"
        })

    file = request.files['file']
    file_contents = file.read().decode('utf-8')

    # Procesar el archivo XML y extraer la información requerida
    root = ET.fromstring(file_contents)
    fecha = root.find('TIEMPO/FECHA').text.strip()
    msj_recibidos = root.find('TIEMPO/MSJ_RECIBIDOS').text.strip()
    usr_mencionados = root.find('TIEMPO/USR_MENCIONADOS').text.strip()
    hash_incluidos = root.find('TIEMPO/HASH_INCLUIDOS').text.strip()

    # Almacenar la información en un diccionario
    message_info = {
        "FECHA": fecha,
        "MSJ_RECIBIDOS": msj_recibidos,
        "USR_MENCIONADOS": usr_mencionados,
        "HASH_INCLUIDOS": hash_incluidos
    }

    # Agregar la información al registro de mensajes
    messages_data.append(message_info)

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

    # Procesar el archivo XML y almacenar los datos en un diccionario
    config_data = {}
    root = ET.fromstring(file_contents)

    # Procesar las secciones del archivo XML
    for section in root:
        section_name = section.tag
        config_data[section_name] = {}

        for word_element in section:
            word = word_element.text.strip()
            count = len(list(word_element))
            config_data[section_name][word] = count

    # Agregar la información al registro de configuración
    messages_data2.append(config_data)

    return jsonify({
        "message": "La configuración del servidor fue grabada con éxito"
    })



@app.route('/limpiarDatos', methods=['POST'])
def limpiar_datos():
    messages_data.clear()
    messages_data2.clear()
    return jsonify({"message": "Datos limpiados exitosamente"})


@app.route('/devolverHashtags', methods=['GET'])
def devolver_hashtags():
    # Crear un elemento XML con la información almacenada en messages_data
    xml_response = ET.Element("MENSAJES_RECIBIDOS")
    for message_info in messages_data:
        tiempo = ET.SubElement(xml_response, "TIEMPO")
        fecha = ET.SubElement(tiempo, "FECHA")
        fecha.text = message_info["FECHA"]
        msj_recibidos = ET.SubElement(tiempo, "MSJ_RECIBIDOS")
        msj_recibidos.text = message_info["MSJ_RECIBIDOS"]
        usr_mencionados = ET.SubElement(tiempo, "USR_MENCIONADOS")
        usr_mencionados.text = message_info["USR_MENCIONADOS"]
        hash_incluidos = ET.SubElement(tiempo, "HASH_INCLUIDOS")
        hash_incluidos.text = message_info["HASH_INCLUIDOS"]

    # Generar una respuesta XML
    response = ET.tostring(xml_response, encoding="utf-8")
    return Response(response, content_type='application/xml')


@app.route('/devolverMenciones', methods=['GET'])
def devolver_menciones():
    if not messages_data2:
        return jsonify({"menciones": "No hay datos de configuración almacenados"})

    word_counts = {}
    xml_response = ET.Element("CONFIG_RECIBIDA")

    for section_name, words in messages_data2[-1].items():
        section = ET.Element(section_name)
        section_words = set()  # Usamos un conjunto para evitar duplicados en la salida
        for word in words:
            if word not in section_words:
                section_words.add(word)
                word_counts[word] = word_counts.get(word, 0) + 1
                word_element = ET.Element("palabra")
                word_element.text = word
                section.append(word_element)
        xml_response.append(section)

    for word, count in word_counts.items():
        section = ET.Element("conteo_" + word)
        palabra_element = ET.Element("palabra")
        palabra_element.text = word
        section.append(palabra_element)
        conteo_element = ET.Element("conteo")
        conteo_element.text = str(count)
        section.append(conteo_element)
        xml_response.append(section)

    response = ET.tostring(xml_response, encoding="utf-8")
    return Response(response, content_type='application/xml')





if __name__ == '__main__':
    app.run(debug=True)