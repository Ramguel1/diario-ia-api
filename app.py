from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# URL pública del modelo de análisis de sentimiento
API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"

@app.route("/analizar", methods=["POST"])
def analizar():
    data = request.get_json()
    textos = data.get("entradas", [])

    resultados = []
    for texto in textos:
        try:
            response = requests.post(API_URL, json={"inputs": texto})
            respuesta_json = response.json()

            if isinstance(respuesta_json, list):
                salida = respuesta_json[0]
            else:
                salida = {"error": respuesta_json}

        except Exception as e:
            salida = {"error": str(e)}

        resultados.append({
            "texto": texto,
            "resultado": salida
        })

    return jsonify(resultados)

if __name__ == "__main__":
    app.run()
