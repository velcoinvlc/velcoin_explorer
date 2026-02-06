import os
import json
import requests
from flask import Flask, jsonify

app = Flask(__name__)

NODE_URL = "https://velcoin.onrender.com"

BLOCKS_FILE = "blocks.json"
WALLET_HISTORY_FILE = "wallet_history.json"

# Asegurarse de que existan los archivos locales
for f, default in [(BLOCKS_FILE, []), (WALLET_HISTORY_FILE, [])]:
    if not os.path.exists(f):
        with open(f, "w") as file:
            json.dump(default, file)

def fetch_node_data(endpoint):
    """Consulta el nodo y devuelve JSON si existe, si no devuelve lista vacía"""
    try:
        r = requests.get(f"{NODE_URL}/{endpoint}", timeout=5)
        r.raise_for_status()
        return r.json()
    except requests.RequestException:
        # Si falla, devolvemos lista vacía
        return []

@app.route("/")
def index():
    return jsonify({"node": NODE_URL, "status": "VelCoin Explorer Online"})

@app.route("/balance/<address>")
def balance(address):
    # Consultar todas las transacciones del nodo
    txs = fetch_node_data("transactions")
    balance = 0
    for tx in txs:
        if tx["to"] == address:
            balance += tx["amount"]
        if tx["from"] == address:
            balance -= tx["amount"]
    return jsonify({"address": address, "balance": balance, "symbol": "VLC"})

@app.route("/blocks")
def blocks():
    # Trae bloques del nodo
    blocks = fetch_node_data("chain")
    return jsonify(blocks)

@app.route("/transactions")
def transactions():
    txs = fetch_node_data("transactions")
    return jsonify(txs)

@app.route("/nodes")
def nodes():
    # Solo devuelve el nodo principal
    return jsonify({"seed_nodes": [NODE_URL]})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
