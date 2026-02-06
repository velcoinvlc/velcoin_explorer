import os
import json
from flask import Flask, jsonify

app = Flask(__name__)

NODE_URL = "https://velcoin.onrender.com"

BLOCKS_FILE = "blocks.json"
WALLET_HISTORY_FILE = "wallet_history.json"

# Asegurarse de que existan los archivos
for f, default in [(BLOCKS_FILE, []), (WALLET_HISTORY_FILE, [])]:
    if not os.path.exists(f):
        with open(f, "w") as file:
            json.dump(default, file)

@app.route("/")
def index():
    return jsonify({"node": NODE_URL, "status": "VelCoin Explorer Online"})

@app.route("/balance/<address>")
def balance(address):
    # Consultamos la wallet sin tocar el nodo
    # Aquí simplemente devolvemos el balance de ejemplo
    # Se podría conectar a tu nodo si quieres balance real en línea
    with open(WALLET_HISTORY_FILE) as f:
        txs = json.load(f)
    balance = 0
    for tx in txs:
        if tx["to"] == address:
            balance += tx["amount"]
        if tx["from"] == address:
            balance -= tx["amount"]
    # Si no hay transacciones, devolvemos un valor grande de ejemplo
    if balance == 0:
        balance = 999971821.27
    return jsonify({"address": address, "balance": balance, "symbol": "VLC"})

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

@app.route("/nodes")
def nodes():
    return jsonify({"seed_nodes": [NODE_URL]})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
