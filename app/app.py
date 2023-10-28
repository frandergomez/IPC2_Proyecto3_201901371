from flask import Flask, request, jsonify

from flask_cors import CORS

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
    messages_data.append({"message": file_contents, "hashtag": "example_hashtag"})
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
    return jsonify({
        "message": "La configuración del servidor fue grabada con éxito"
    })
