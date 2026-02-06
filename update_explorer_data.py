import json
import requests
from datetime import datetime

NODE_URL = "https://velcoin.onrender.com"

# Ejemplo de balance
address = "6d627bb087faa32a00ed18749af72185de31a038"
try:
    r = requests.get(f"{NODE_URL}/balance/{address}")
    bal = r.json()
    print("Balance ejemplo:", bal)
except:
    print("No se pudo obtener balance desde el nodo.")

# Inicializa archivos locales si no existen
for file in ["blocks.json", "wallet_history.json"]:
    try:
        with open(file, "r") as f:
            pass
    except FileNotFoundError:
        with open(file, "w") as f:
            f.write("[]")

# Esto deja archivos vacíos pero listos para llenarse automáticamente
