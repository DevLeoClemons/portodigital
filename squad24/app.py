from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from main import GerarCriativoIA
import os

app = Flask(__name__)
CORS(app)

OUTPUT_PATH = "post.png"


def get_criativo():
    try:
        return GerarCriativoIA(), None
    except ValueError as e:
        return None, str(e)


@app.route("/")
def index():
    return send_file("index.html")


@app.route("/gerar", methods=["POST"])
def gerar():

    dados = request.json

    if not dados or "tema" not in dados:
        return jsonify({"erro": "Campo 'tema' é obrigatório"}), 400

    criativo, erro = get_criativo()

    if erro:
        return jsonify({"erro": erro}), 500

    criativo.consolidate_creative(
        ideia_prompt=dados["tema"],
        output_path=OUTPUT_PATH,
        brand=dados.get("brand", "")
    )

    return send_file(OUTPUT_PATH, mimetype="image/png")


if __name__ == "__main__":
    app.run(debug=True)