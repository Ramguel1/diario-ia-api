from flask import Flask, request, jsonify
from textblob import TextBlob

app = Flask(__name__)

@app.route("/analizar", methods=["POST"])
def analizar():
    data = request.get_json()
    textos = data.get("entradas", [])

    resultados = []
    for texto in textos:
        tb = TextBlob(texto)
        polaridad = tb.sentiment.polarity

        # Ajustamos el umbral para que sea menos estricto
        if polaridad >= 0.1:
            label = "POSITIVE"
        elif polaridad <= -0.1:
            label = "NEGATIVE"
        else:
            label = "NEUTRAL"

        resultados.append({
            "texto": texto,
            "resultado": {
                "label": label,
                "score": round(abs(polaridad), 3)
            }
        })

    return jsonify(resultados)

if __name__ == "__main__":
    app.run()
