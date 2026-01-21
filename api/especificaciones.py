import requests
import pandas as pd
import os

BASE_URL = "https://carapi.app/api"

def obtener_especificaciones(marca, modelo, anio):
    """
    Obtiene consumo y potencia usando los endpoints /engines/v2 y /mileages/v2
    """
    try:
        # 1️⃣ Buscar modelos exactos
        filtro_modelo = f'[{{"field": "make", "op": "=", "val": "{marca}"}},' \
                        f'{{"field": "model", "op": "=", "val": "{modelo}"}},' \
                        f'{{"field": "year", "op": "=", "val": {anio}}}]'
        url_modelos = f"{BASE_URL}/models/v2?page=1&limit=1&json={filtro_modelo}"
        r = requests.get(url_modelos)
        data_modelo = r.json()
        if not data_modelo.get("data"):
            return None
        modelo_info = data_modelo["data"][0]

        # 2️⃣ Buscar motor del vehículo
        motor_id = modelo_info.get("engine_id")
        if not motor_id:
            return None

        url_motor = f"{BASE_URL}/engines/v2?page=1&limit=1&json=[{{\"field\":\"id\",\"op\":\"=\",\"val\":{motor_id}}}]"
        r_motor = requests.get(url_motor)
        data_motor = r_motor.json()
        if not data_motor.get("data"):
            return None
        motor_info = data_motor["data"][0]

        potencia = motor_info.get("horsepower", None)

        # 3️⃣ Buscar consumo
        url_mileage = f"{BASE_URL}/mileages/v2?page=1&limit=1&json=[{{\"field\":\"engine_id\",\"op\":\"=\",\"val\":{motor_id}}}]"
        r_mileage = requests.get(url_mileage)
        data_mileage = r_mileage.json()
        if not data_mileage.get("data"):
            consumo = None
        else:
            consumo = data_mileage["data"][0].get("combination_l100km")  # l/100km

        return {
            "marca": marca,
            "modelo": modelo,
            "anio": anio,
            "consumo": consumo,
            "potencia": potencia
        }
    except Exception as e:
        print(f"Error obteniendo specs de {marca} {modelo} {anio}: {e}")
        return None