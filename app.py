from flask import Flask, request, jsonify
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Descargar solo la primera vez
nltk.download('vader_lexicon')

app = Flask(__name__)
analyzer = SentimentIntensityAnalyzer()

@app.route("/analizar", methods=["POST"])
def analizar():
    data = request.get_json()
    textos = data.get("entradas", [])

    resultados = []
    for texto in textos:
        scores = analyzer.polarity_scores(texto)
        comp = scores['compound']

        if comp >= 0.1:
            label = "POSITIVE"
        elif comp <= -0.1:
            label = "NEGATIVE"
        else:
            label = "NEUTRAL"

        resultados.append({
            "texto": texto,
            "resultado": {
                "label": label,
                "score": round(comp, 3)
            }
        })

    return jsonify(resultados)

if __name__ == "__main__":
    app.run()
