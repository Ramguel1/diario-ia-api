from flask import Flask, request, jsonify
from textblob import TextBlob

app = Flask(__name__)

@app.route("/analizar", methods=["POST"])
def analizar():
    data = request.get_json()
    textos = data.get("entradas", [])

    resultados = []
    for texto in textos:
        try:
            tb = TextBlob(texto)

            # Traducir a inglés
            texto_en = tb.translate(to="en")
            tb_en = TextBlob(str(texto_en))

            polaridad = tb_en.sentiment.polarity

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

        except Exception as e:
            resultados.append({
                "texto": texto,
                "resultado": {
                    "error": str(e)
                }
            })

    return jsonify(resultados)

if __name__ == "__main__":
    app.run()
