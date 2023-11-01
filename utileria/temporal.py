import xml.etree.ElementTree as ET

# Tu XML en forma de string
xml_string = '''<?xml version="1.0"?>
<diccionario>
 <sentimientos_positivos>
 <palabra> bueno </palabra>
 <palabra> excelente </palabra>
 <palabra> cool </palabra>
 <palabra> satisfecho </palabra>
 </sentimientos_positivos>
 <sentimientos_negativos>
 <palabra> malo </palabra>
 <palabra> pésimo </palabra>
 <palabra> triste </palabra>
 <palabra> molesto </palabra>
 <palabra> decepcionado </palabra>
 <palabra> enojo </palabra>
 </sentimientos_negativos>
</diccionario>'''

# Parsear el XML desde el string
root = ET.fromstring(xml_string)

# Iterar sobre los elementos y mostrar las palabras con su sentimiento
for sentimiento in root:
    for palabra in sentimiento:
        #sentimiento_type = "positivo" if sentimiento.tag == "sentimientos_positivos" else "negativo"

        if sentimiento.tag == "sentimientos_positivos":
            print(f"Palabra: {palabra.text.strip()}, Sentimiento: positivo")
        else:
            print(f"Palabra: {palabra.text.strip()}, Sentimiento: negativo")







from flask import Flask, jsonify
import xml.etree.ElementTree as ET

app = Flask(__name)

# Clase SentimientosDictionary como se definió previamente

@app.route('/devolverMenciones', methods=['GET'])
def devolver_menciones():
    menciones = [msg.get("mencion") for msg in messages_data if "mencion" in msg]

    # Cargar el diccionario desde un archivo
    diccionario = SentimientosDictionary()
    diccionario.cargar_desde_archivo("sentimientos.xml")

    # Contar la frecuencia de cada palabra en menciones
    palabra_frecuencia = {}
    for m in menciones:
        palabras = m.split()
        for palabra in palabras:
            palabra = palabra.lower()  # Convertir a minúsculas para evitar duplicados por diferencias de mayúsculas/minúsculas
            if palabra in palabra_frecuencia:
                palabra_frecuencia[palabra] += 1
            else:
                palabra_frecuencia[palabra] = 1

    # Crear un nuevo XML con las palabras únicas y su frecuencia
    root = ET.Element("palabras_frecuencia")
    for palabra, frecuencia in palabra_frecuencia.items():
        elemento = ET.SubElement(root, "palabra")
        elemento.text = palabra
        elemento.set("frecuencia", str(frecuencia))

    # Convertir el XML en una respuesta XML
    response = app.response_class(
        response=ET.tostring(root, encoding="utf-8").decode("utf-8"),
        status=200,
        mimetype='application/xml'
    )

    return response

if __name__ == '__main__':
    app.run()

