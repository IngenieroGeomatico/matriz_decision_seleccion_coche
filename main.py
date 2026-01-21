import pandas as pd
from api.valor_mercado import obtener_valor_mercado_todos
from decision.matriz_decision import calcular_score

# -----------------------------
# 5️⃣ Definir pesos de la matriz de decisión
# -----------------------------
pesos = {
    "precio": 0.20,
    "consumo": 0.20,
    "potencia": 0.20,
    "etiqueta": 0.10,
    "fiabilidad": 0.30,
    
}

ETIQUETAS = {
    "B": 0.1,
    "C": 0.2,
    "ECO": 0.50,
    "0": 1.00,
    "0 emisiones": 1.00
}

precio_objetivo=20000
porc_mas_precio_objetivo = 1.5


# -----------------------------
# Configuración: origen de las especificaciones
# -----------------------------
USAR_CSV_PRECIOS = True
CSV_PRECIOS_PATH = "data/coches_quecochemecompro.csv"

# -----------------------------
# 2️⃣ Cargar CSV de fiabilidad
# -----------------------------
fiabilidad_csv = pd.read_csv("data/fiabilidad_marcas.csv")
# Diccionario con claves en minúsculas
fiabilidad_dict = dict(zip(fiabilidad_csv.marca.str.lower(), fiabilidad_csv.fiabilidad))

# -----------------------------
# 3️⃣ Preparar dataset
# -----------------------------
dataset = []

if not USAR_CSV_PRECIOS:
    precio = obtener_valor_mercado_todos()   

# Leer CSV con especificaciones
df_precios = pd.read_csv(CSV_PRECIOS_PATH)
# Crear diccionario {(marca, modelo, anio): specs}
precios_dict = {
    row.slug_version: row
    for _, row in df_precios.iterrows()
}



for coche in precios_dict:
    c = precios_dict[coche]

    slug_version_lower = c["slug_version"].lower()
    marca_lower = c["marca"].lower()
    modelo_lower = c["modelo"].lower()
    anio = c["anio"]
    
    precio_row = precios_dict.get(slug_version_lower)

    precio = {
        "nombre": precio_row.get("nombre"),
        "marca": precio_row.get("marca"),
        "modelo": precio_row.get("modelo"),
        "slug_version": precio_row.get("slug_version"),
        "precio": precio_row.get("precio"),
        "combustible": precio_row.get("combustible"),
        "potencia": precio_row.get("potencia"),
        "consumo": precio_row.get("consumo"),
        "anio": precio_row.get("anio"),
        "etiqueta_medioambiental": precio_row.get("etiqueta_medioambiental"),
        "url_version": precio_row.get("url_version")
    }


    dataset.append({
        **c,
        "consumo": precio.get("consumo"),
        "potencia": precio.get("potencia"),
        "nombre": precio.get("nombre"),
        "marca": precio.get("marca"),
        "modelo": precio.get("modelo"),
        "slug_version": precio.get("slug_version"),
        "precio": precio.get("precio"),
        "combustible": precio.get("combustible"),
        "potencia": precio.get("potencia"),
        "consumo": precio.get("consumo"),
        "anio": precio.get("anio"),
        "etiqueta": precio.get("etiqueta_medioambiental"),
        "fiabilidad": fiabilidad_dict.get(marca_lower, 0.6)
    })

# -----------------------------
# 4️⃣ Crear DataFrame
# -----------------------------
df = pd.DataFrame(dataset)
print(f"🚗 Coches listos para evaluación: {len(df)}")


# -----------------------------
# 6️⃣ Calcular score y ordenar
# -----------------------------
resultado = calcular_score(df, pesos,ETIQUETAS, precio_objetivo, porc_mas_precio_objetivo)
columnas_mostrar = [
    "nombre",
    # "marca",
    # "modelo",
    "precio",
    "etiqueta",
    "fiabilidad",
    "consumo",
    "score"
]

print("🏆 Ranking coches nuevos según tus criterios:")
print(resultado[columnas_mostrar].head(50))
