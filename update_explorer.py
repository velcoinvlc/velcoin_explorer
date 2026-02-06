import requests
import json
from datetime import datetime

def update_explorer_from_node(node_url, blocks_file, history_file):
    print(f"Actualizando explorer desde nodo {node_url} a {datetime.now()}")

    # Bloques
    try:
        r = requests.get(f"{node_url}/chain")
        r.raise_for_status()
        with open(blocks_file, "w") as f:
            json.dump(r.json(), f, indent=2)
        print(f"Archivo {blocks_file} generado con {len(r.json())} bloques.")
    except requests.HTTPError:
        print("Endpoint /chain no disponible: 404")
        with open(blocks_file, "w") as f:
            json.dump([], f)

    # Transacciones / wallet history
    try:
        r = requests.get(f"{node_url}/transactions")
        r.raise_for_status()
        with open(history_file, "w") as f:
            json.dump(r.json(), f, indent=2)
        print(f"Archivo {history_file} generado.")
    except requests.HTTPError:
        print("Endpoint /transactions no disponible: 404")
        with open(history_file, "w") as f:
            json.dump([], f)
