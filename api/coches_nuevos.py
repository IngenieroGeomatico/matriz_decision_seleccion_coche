import requests
import json

BASE_URL = "https://carapi.app/api"

def obtener_coches_nuevos(anio_min=2020, limite=50):
    coches = []

    # La API devuelve lista directa, no "data"
    marcas = requests.get(f"{BASE_URL}/makes").json()

    for marca in marcas["data"]:

        marca_id = marca["id"]
        marca_nombre = marca["name"]

        # Modelos también devuelven lista directa
        page = 1
        pages = 99
        while True:
            if page > pages:
                break
            filtro = [{"field": "year", "op": ">=", "val": anio_min}]
            r = requests.get(
                f"{BASE_URL}/models/v2",
                params={
                    "make_id": marca_id,
                    "limit": limite,
                    "page": page,
                    "json": json.dumps(filtro)
                }
            )

            modelos = r.json()
            pages = modelos["collection"]["pages"]

            for m in modelos["data"]:
                coches.append({
                    "marca": marca_nombre,
                    "modelo": m["name"],
                    "anio": ">= " + str(anio_min),
                    "tipo": "nuevo"
                })

            page += 1  # siguiente página

    return coches
