from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# URL del modelo de análisis de sentimiento en HuggingFace
API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"

# Si no tienes una API Key, deja esto vacío. Para uso gratuito no es obligatorio.
HEADERS = {}


@app.route("/analizar", methods=["POST"])
def analizar():
    data = request.get_json()
    textos = data.get("entradas", [])

    resultados = []
    for texto in textos:
        response = requests.post(API_URL, headers=HEADERS, json={"inputs": texto})

        try:
            result = response.json()
            if isinstance(result, list):
                output = result[0]
            else:
                output = {"error": result}
        except Exception as e:
            output = {"error": str(e)}

        resultados.append({
            "texto": texto,
            "resultado": output
        })

    return jsonify(resultados)

if __name__ == "__main__":
    app.run()
