import json
from datetime import datetime

wallet_file = "wallet_history.json"

# Leer histórico
try:
    with open(wallet_file, "r") as f:
        history = json.load(f)
except FileNotFoundError:
    history = []

# Agregar 2 tx de prueba
tx1 = {
    "txid": f"tx{len(history)+1:04}",
    "from": "6d627bb087faa32a00ed18749af72185de31a038",
    "to": "abcdef1234567890abcdef1234567890abcd",
    "amount": 1000.0,
    "timestamp": datetime.utcnow().isoformat()
}

tx2 = {
    "txid": f"tx{len(history)+2:04}",
    "from": "abcdef1234567890abcdef1234567890abcd",
    "to": "6d627bb087faa32a00ed18749af72185de31a038",
    "amount": 500.0,
    "timestamp": datetime.utcnow().isoformat()
}

history.extend([tx1, tx2])

with open(wallet_file, "w") as f:
    json.dump(history, f, indent=2)

print(f"wallet_history.json actualizado con {len([tx1,tx2])} transacciones de prueba")
