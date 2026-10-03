import json
from pathlib import Path

class ArchivoServicio:
    def leer_json(self, ruta):
        with Path(ruta).open("r", encoding="utf-8") as archivo:
            return json.load(archivo)

    def guardar_json(self, ruta, datos):
        ruta = Path(ruta)
        ruta.parent.mkdir(parents=True, exist_ok=True)
        with ruta.open("w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=4)
