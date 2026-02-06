import os
import json
import requests
from flask import Flask, jsonify

app = Flask(__name__)

# URL del nodo VelCoin
NODE_URL = "https://velcoin.onrender.com"

@app.route("/")
def index():
    return jsonify({"node": NODE_URL, "status": "VelCoin Explorer Online"})

@app.route("/balance/<address>")
def balance(address):
    """
    Consulta el balance de una wallet directamente desde el nodo.
    """
    try:
        resp = requests.get(f"{NODE_URL}/balance/{address}", timeout=5)
        resp.raise_for_status()
        return jsonify(resp.json())
    except requests.RequestException as e:
        return jsonify({"error": "No se pudo obtener balance del nodo", "details": str(e)}), 500

@app.route("/transactions")
def transactions():
    """
    Obtiene todas las transacciones del nodo directamente desde /ledger.
    """
    try:
        resp = requests.get(f"{NODE_URL}/ledger", timeout=5)
        resp.raise_for_status()
        return jsonify(resp.json())
    except requests.RequestException as e:
        return jsonify({"error": "No se pudo obtener transacciones del nodo", "details": str(e)}), 500

@app.route("/blocks")
def blocks():
    """
    Retorna los bloques locales del explorer (opcional, solo demo)
    """
    blocks_file = "blocks.json"
    if not os.path.exists(blocks_file):
        with open(blocks_file, "w") as f:
            json.dump([], f)
    with open(blocks_file) as f:
        blocks = json.load(f)
    return jsonify(blocks)

@app.route("/nodes")
def nodes():
    """
    Lista los nodos semilla. Para ahora solo nuestro nodo principal.
    """
    return jsonify({"seed_nodes": [NODE_URL]})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
