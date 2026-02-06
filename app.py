import os
import json
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

NODE_URL = "https://velcoin.onrender.com"

BLOCKS_FILE = "blocks.json"
WALLET_HISTORY_FILE = "wallet_history.json"

# Asegurarse de que existan los archivos locales
for f, default in [(BLOCKS_FILE, []), (WALLET_HISTORY_FILE, [])]:
    if not os.path.exists(f):
        with open(f, "w") as file:
            json.dump(default, file)

@app.route("/")
def index():
    return jsonify({"node": NODE_URL, "status": "VelCoin Explorer Online"})

@app.route("/balance/<address>")
def balance(address):
    try:
        # Consultar balance real del nodo
        r = requests.get(f"{NODE_URL}/balance/{address}")
        r.raise_for_status()
        return jsonify(r.json())
    except Exception as e:
        # fallback a historial local
        with open(WALLET_HISTORY_FILE) as f:
            txs = json.load(f)
        balance = 0
        for tx in txs:
            if tx["to"] == address:
                balance += tx["amount"]
            if tx["from"] == address:
                balance -= tx["amount"]
        return jsonify({"address": address, "balance": balance, "symbol": "VLC", "note": "fallback local"})

@app.route("/blocks")
def blocks():
    with open(BLOCKS_FILE) as f:
        blocks = json.load(f)
    return jsonify(blocks)

@app.route("/transactions")
def transactions():
    with open(WALLET_HISTORY_FILE) as f:
        txs = json.load(f)
    return jsonify(txs)

@app.route("/register_tx", methods=["POST"])
def register_tx():
    data = request.get_json()
    required_fields = ["txid", "from", "to", "amount", "timestamp"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "missing fields"}), 400

    # Leer wallet_history.json
    with open(WALLET_HISTORY_FILE) as f:
        txs = json.load(f)
    # Evitar tx duplicadas
    if any(tx["txid"] == data["txid"] for tx in txs):
        return jsonify({"message": "transaction already registered"}), 200

    txs.append(data)
    with open(WALLET_HISTORY_FILE, "w") as f:
        json.dump(txs, f, indent=2)
    return jsonify({"message": "transaction registered"}), 201

@app.route("/nodes")
def nodes():
    return jsonify({"seed_nodes": [NODE_URL]})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
