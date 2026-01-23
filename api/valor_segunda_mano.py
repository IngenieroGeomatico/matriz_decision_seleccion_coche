import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import pandas as pd
import os
from urllib.parse import quote
import random
import time
import unicodedata
import re

# Lista de User-Agents para rotar

USER_AGENTS = [
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:110.0) Gecko/20100101 Firefox/110.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13.5; rv:112.0) Gecko/20100101 Firefox/112.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 18_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36"
]

def generar_sleep(TIME_SLEEP_BASE = 1, max=0.5, min=-0.5):
    time.sleep(TIME_SLEEP_BASE + random.uniform(min, max))

# Función para generar headers aleatorios
def generar_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Host": "www.ciudaddelautomovil.es",
        "Referer":"www.ciudaddelautomovil.es",
        "Origin":"https://www.ciudaddelautomovil.es"

    }


# Session con reintentos para evitar fallos por desconexiones temporales
SESSION = requests.Session()
RETRY_STRATEGY = Retry(
    total=5,
    backoff_factor=0.5,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "OPTIONS"],
)
ADAPTER = HTTPAdapter(max_retries=RETRY_STRATEGY)
SESSION.mount("https://", ADAPTER)
SESSION.mount("http://", ADAPTER)

# ----------------------------
# Función principal
# ----------------------------

def obtener_valor_segunda_mano_todos(fiabilidad_dict):

    def obtener_marca_desde_fiabilidad(name, dict_fiabilidad):

        def normalizar_texto(texto):
            texto = texto.lower()
            texto = unicodedata.normalize("NFD", texto)
            texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
            texto = re.sub(r"[-_]", " ", texto)
            texto = re.sub(r"\s+", " ", texto)
            return texto.strip()

        name_norm = normalizar_texto(name)

        # Normalizamos las marcas y las ordenamos por longitud (desc)
        marcas_norm = sorted(
            ((normalizar_texto(marca), marca) for marca in dict_fiabilidad.keys()),
            key=lambda x: len(x[0]),
            reverse=True
        )

        for marca_norm, marca_original in marcas_norm:
            if marca_norm in name_norm:
                return marca_original, dict_fiabilidad[marca_original]

        return None, None

    resultados = []

    page = 1
    page_size = 24
    reintentos = 5
    r_r = 0
    r_r2 = 0
    while True:
        print(f" ------------- página: {page}")
        url_finder = f"https://www.ciudaddelautomovil.es/coches-segunda-mano/?marca=0&modelo=0&carroceria=0&combustible=0&transmision=0&concesionario=0&precio=0;150000&year=2007;2026&kilometraje=0;240000&potencia=66;560&vista=grid&page={page}&psize={page_size}&ordenar=precio-asc"
        
        generar_sleep()
        try:
            r = SESSION.get(url_finder, headers=generar_headers(), timeout=60)
            r.raise_for_status()
        except requests.RequestException as e:
            print(f"Error al obtener la página {page}: {e}")
            r_r += 1
            if r_r >= reintentos:
                break
            generar_sleep(TIME_SLEEP_BASE = 10, max=3, min=-0.5)
            
        soup = BeautifulSoup(r.text, "html.parser")
        # Buscar todas las tarjetas de coches (revisar clase real en el HTML)
        cards = soup.find_all("h4", class_="product-title") 
        if not cards:
            break

        for c in cards:
            json_propiedades= {}
            json_propiedades["href"] = c.find("a").get("href")
            json_propiedades["ref"] = json_propiedades["href"].split("/")[4]
            json_propiedades["slug_version"] = json_propiedades["ref"] + "_" + json_propiedades["href"].split("/")[3]
            json_propiedades["name"] = c.find("a").text.strip() 
            marca, marca2 = obtener_marca_desde_fiabilidad(json_propiedades["name"], fiabilidad_dict)
            json_propiedades["marca"] = marca

            if len(cards) == 1:
                existe = any(json_["href"] == json_propiedades["href"] for json_ in resultados)
                if existe:
                    break

            print(json_propiedades["name"])

            url_vehic = f"https://www.ciudaddelautomovil.es{json_propiedades["href"]}"

            generar_sleep()
            try:
                r2 = SESSION.get(url_vehic, headers=generar_headers(), timeout=10)
                r2.raise_for_status()
            except requests.RequestException as e:
                r_r2 += 1
                print(f"Error {r_r2} al obtener la página {json_propiedades['name']}: {e}")
                if r_r2 >= reintentos:
                    break
                generar_sleep(TIME_SLEEP_BASE = 10, max=3, min=-0.5)

            soup2 = BeautifulSoup(r2.text, "html.parser")
            # Buscar todas las tarjetas de coches (revisar clase real en el HTML)
            cards2_1 = soup2.find("h1", class_="theme lowercase") 
            if not cards2_1:
                break

            json_propiedades["precio"] = float(cards2_1.text.replace('\xa0', ' ').replace('€', '').replace('.', '').replace('ahora ','').strip())

            cards2_2 = soup2.find_all("li", class_="list-group-item row details-data") 
            if not cards2_2:
                break

            for c2_2 in cards2_2:
                c2_2_split = c2_2.text.replace('\n','').split(":")
                if not c2_2_split[0]:
                    continue
                json_propiedades[c2_2_split[0].strip()] = c2_2_split[1].strip()

            resultados.append(json_propiedades)

        if len(cards) < page_size:
            break

        page += 1
    
    for obj in resultados:
        obj.pop("href", None)

    # ----------------------------
    # Guardar CSV
    # ----------------------------
    os.makedirs("data", exist_ok=True)
    df = pd.DataFrame(resultados)
    df.to_csv("data/coches_segunda_mano.csv", index=False)
    print(f"CSV guardado en data/coches_segunda_mano.csv")
    return df



if __name__ == "__main__":
    fiabilidad_csv = pd.read_csv("data/fiabilidad_marcas.csv")
    # Diccionario con claves en minúsculas
    fiabilidad_dict = dict(zip(fiabilidad_csv.marca.str.lower(), fiabilidad_csv.fiabilidad))
    obtener_valor_segunda_mano_todos(fiabilidad_dict)
