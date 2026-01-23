import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from urllib.parse import quote
import random
import time

from  api.api_request import robust_get, crear_session_robusta, generar_sleep, generar_user_agent

# Lista de User-Agents para rotar
USER_AGENTS = generar_user_agent()


# Función para generar headers aleatorios
def generar_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Host": "www.quecochemecompro.com",
        "Alt-Used": "www.quecochemecompro.com",

    }

# Session con reintentos para evitar fallos por desconexiones temporales
SESSION = crear_session_robusta()

# ----------------------------
# Función principal
# ----------------------------


def obtener_valor_mercado_quecochemecompro():
    resultados = []

    page = 1
    while True:

        url_finder = f"https://www.quecochemecompro.com/components/finder/?page={page}&search_type=vn&per_page=30&is_embed=false&is_stock=true"

        generar_sleep()
        try:
            r = robust_get(session=SESSION, url=url_finder, headers=generar_headers(), timeout=60)
        except requests.RequestException as e:
            print(f"Error al obtener la página {page}: {e}")
            break

        soup = BeautifulSoup(r.text, "html.parser")
        # Buscar todas las tarjetas de coches (revisar clase real en el HTML)
        cards = soup.find_all("a", class_="block text-gray-darkest no-underline truncate w-52 absolute-link font-bold") 
        if not cards:
            break

        for c in cards:
           
            href = c.get("href") 
            marca_modelo = href.split("/")[2].split("-") 
            marca_tag = marca_modelo[0]  # clase aproximada
            modelo_tag =  "-".join(marca_modelo[1:])  # clase aproximada
            if not marca_modelo:
                continue

            marca = marca_tag.strip()
            modelo = modelo_tag.strip()
            slug = f"{marca}-{modelo}"

            print(f"----- {slug} -----")

            # ----------------------
            # Obtener versiones con precios y características
            # ----------------------
            v_page = 1
            while True:
                generar_sleep()
                try:

                    url_versions = f"https://www.quecochemecompro.com/components/versions_table/?page={v_page}&slug={quote(slug)}&search_type=vn&per_page=30"

                    try:
                        r_v = robust_get(session=SESSION, url=url_versions, headers=generar_headers(), timeout=60)
                    except requests.RequestException as e:
                        print(f"Error en versiones de {slug} página {v_page}")
                        break

                    soup_v = BeautifulSoup(r_v.text, "html.parser")
                    version_rows = soup_v.find_all("tr", attrs={"data-url": True})  # ajustar clase real
                    if not version_rows:
                        break

                    for row in version_rows:
                        # Nombre completo de la versión
                        nombre = row.find("td", class_=["uppercase", "font-bold"]) or row.find("div", class_=["uppercase", "font-bold"])
                        nombre = nombre.text.strip()

                        # Etiqueta medioambiental (la letra dentro del alt del <img>)
                        env_label_img = row.find("img", alt=True)
                        etiqueta_medioambiental = env_label_img["alt"].replace("Etiqueta medioambiental ", "") if env_label_img else None

                        # Consumo (puede venir con coma, '5,5 l/100Km')
                        consumo_td = row.find_all("td")[4]  # quinta columna
                        
                        consumo_text = consumo_td.text.strip().replace(" l/100Km", "").replace(",", ".")
                        try:
                            consumo = float(consumo_text)
                        except:
                            consumo = None

                        # Potencia (CV)
                        potencia_td = row.find_all("td")[3]
                        try:
                            potencia = int(potencia_td.text.strip())
                        except:
                            potencia = None

                        # Año (si está disponible en la tabla, aquí usamos la columna 2 como ejemplo)
                        anio_td = row.find_all("td")[2]
                        try:
                            anio = int(anio_td.text.strip())
                        except:
                            anio = None

                        # Combustible (6ª columna)
                        combustible_td = row.find_all("td")[5]
                        combustible = combustible_td.text.strip() if combustible_td else None

                        # Precio (el valor dentro del span data-value="price")
                        precio_span = row.find("span", {"data-value": "price"})
                        if precio_span:
                            precio_text = precio_span.text.strip().replace(" €", "").replace(".", "").replace(",", ".")
                            try:
                                precio = float(precio_text)
                            except:
                                precio = None
                        else:
                            precio = None

                        # URL/slug de la versión
                        url_version = row["data-url"]
                        slug_version = url_version.strip("/").split("/")[-1]

                        resultados.append({
                            "nombre": nombre,
                            "marca": marca,
                            "modelo": modelo,
                            "slug_version": slug_version,
                            "precio": precio,
                            "combustible": combustible,
                            "potencia": potencia,
                            "consumo": consumo,
                            "anio": anio,
                            "etiqueta_medioambiental": etiqueta_medioambiental,
                            "url_version": url_version
                        })

                    v_page += 1
                    generar_sleep()

                except IndexError:
                        generar_sleep()
                        continue

        page += 1


        generar_sleep()  # evitar bloqueos

    # ----------------------------
    # Guardar CSV
    # ----------------------------
    os.makedirs("data", exist_ok=True)
    df = pd.DataFrame(resultados)
    df.to_csv("data/coches_quecochemecompro.csv", index=False)
    print(f"CSV guardado en data/coches_quecochemecompro.csv")
    return df

