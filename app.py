import os
import json
import requests
from flask import Flask, jsonify

app = Flask(__name__)

# URL de tu nodo online
NODE_URL = "https://velcoin.onrender.com"

# Archivos locales para guardar datos
BLOCKS_FILE = "blocks.json"
WALLET_HISTORY_FILE = "wallet_history.json"

# Crear archivos si no existen
for f, default in [(BLOCKS_FILE, []), (WALLET_HISTORY_FILE, [])]:
    if not os.path.exists(f):
        with open(f, "w") as file:
            json.dump(default, file)

def fetch_blocks_from_node():
    try:
        # Intentamos traer bloques del nodo
        resp = requests.get(f"{NODE_URL}/chain")
        if resp.status_code == 200:
            blocks = resp.json()
            with open(BLOCKS_FILE, "w") as f:
                json.dump(blocks, f)
            return blocks
        else:
            return json.load(open(BLOCKS_FILE))
    except Exception:
        return json.load(open(BLOCKS_FILE))

def fetch_transactions_from_node():
    try:
        resp = requests.get(f"{NODE_URL}/transactions")
        if resp.status_code == 200:
            txs = resp.json()
            with open(WALLET_HISTORY_FILE, "w") as f:
                json.dump(txs, f)
            return txs
        else:
            return json.load(open(WALLET_HISTORY_FILE))
    except Exception:
        return json.load(open(WALLET_HISTORY_FILE))

@app.route("/")
def index():
    return jsonify({"node": NODE_URL, "status": "VelCoin Explorer Online"})

@app.route("/balance/<address>")
def balance(address):
    txs = fetch_transactions_from_node()
    balance = 0
    for tx in txs:
        if tx.get("to") == address:
            balance += tx.get("amount", 0)
        if tx.get("from") == address:
            balance -= tx.get("amount", 0)
    return jsonify({"address": address, "balance": balance, "symbol": "VLC"})

@app.route("/blocks")
def blocks():
    blocks = fetch_blocks_from_node()
    return jsonify(blocks)

@app.route("/transactions")
def transactions():
    txs = fetch_transactions_from_node()
    return jsonify(txs)

@app.route("/nodes")
def nodes():
    return jsonify({"seed_nodes": [NODE_URL]})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
