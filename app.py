from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Puedes usar "sentiment-analysis" o probar otro pipeline más personalizado
modelo = pipeline("sentiment-analysis")

@app.route("/analizar", methods=["POST"])
def analizar():
    data = request.get_json()
    textos = data.get("entradas", [])
    
    resultados = []
    for texto in textos:
        analisis = modelo(texto)[0]
        resultados.append({
            "texto": texto,
            "resultado": analisis
        })

    return jsonify(resultados)

if __name__ == "__main__":
    app.run()
