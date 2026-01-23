from lib.main_tipo import run_tipo

TIPO = "usados"  # 'nuevos' o 'usados'

USAR_CSV_NUEVOS = True
CSV_NUEVOS_PATH = "data/coches_quecochemecompro.csv"
USAR_CSV_USADOS = True
CSV_USADOS_PATH = "data/coches_segunda_mano.csv"
fiabilidad_path="data/fiabilidad_marcas.csv"

pesos_nuevos = {
    "precio": 0.10,
    "consumo": 0.20,
    "potencia": 0.20,
    "etiqueta": 0.10,
    "fiabilidad": 0.40,
}

pesos_usados = {
    "precio": 0.20,
    "kilometros": 0.10,
    "anio": 0.10,
    "km_anio": 0.10,
    "potencia": 0.10,
    "garantia": 0.10,
    "combustible": 0.10,
    "cambio": 0.10,
    "fiabilidad": 0.10,
}

ETIQUETAS = {
    "B": 0.1, 
    "C": 0.2, 
    "ECO": 0.50, 
    "zero": 1.00, 
    "0": 1.00, 
    "0 emisiones": 1.00
}

COMBUSTIBLE_SCORE = {
    "ELÉCTRICO": 1.0,
    "HÍBRIDO": 0.9,
    "HÍBRIDO ENCHUFABLE": 0.85,
    "GASOLINA": 0.7,
    "DIÉSEL": 0.6,
    "GLP": 0.65,
}

CAMBIO_SCORE = {
    "AUTOMÁTICO": 1.0, 
    "MANUAL": 0.7
}

GARANTIA = {
    "Sí": 1.0, 
    "No": 0.7
}

precio_objetivo = 10000
porc_mas_precio_objetivo = 1.5

km_objetivo = 20000 * 3
porc_km_objetivo = 1.5

resultado = run_tipo(
    tipo=TIPO,
    usar_csv_precios=USAR_CSV_NUEVOS,
    csv_precios_path=CSV_NUEVOS_PATH,
    usar_csv_usados=USAR_CSV_USADOS,
    csv_usados_path=CSV_USADOS_PATH,
    fiabilidad_path=fiabilidad_path,
    pesos_nuevos=pesos_nuevos,
    pesos_usados=pesos_usados,
    ETIQUETAS=ETIQUETAS,
    COMBUSTIBLE_SCORE=COMBUSTIBLE_SCORE,
    CAMBIO_SCORE=CAMBIO_SCORE,
    GARANTIA=GARANTIA,
    precio_objetivo=precio_objetivo,
    porc_mas_precio_objetivo=porc_mas_precio_objetivo,
    km_objetivo=km_objetivo,
    porc_km_objetivo = porc_km_objetivo,
)
