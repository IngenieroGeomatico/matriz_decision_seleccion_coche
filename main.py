from lib.main_tipo import run_tipo

TIPO = "ciudaddelautomovil"  # 'ciudaddelautomovil' o 'quecochemecompro'

USAR_CSV_QUECOCHEMECOMPRO = True
CSV_QUECOCHEMECOMPRO_PATH = "data/coches_quecochemecompro.csv"
USAR_CSV_CIUDADDELAUTOMOVIL = True
CSV_CIUDADDELAUTOMOVIL_PATH = "data/coches_ciudaddelautomovil.csv"
fiabilidad_path="data/fiabilidad_marcas.csv"

pesos_QUECOCHEMECOMPRO = {
    "precio": 0.10,
    "consumo": 0.20,
    "potencia": 0.20,
    "etiqueta": 0.10,
    "fiabilidad": 0.40,
}

pesos_CIUDADDELAUTOMOVIL = {
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

precio_objetivo = 20000
porc_mas_precio_objetivo = 1.5

km_objetivo = 100000
porc_km_objetivo = 1.5

resultado = run_tipo(
    tipo=TIPO,
    USAR_CSV_QUECOCHEMECOMPRO=USAR_CSV_QUECOCHEMECOMPRO,
    CSV_QUECOCHEMECOMPRO_PATH=CSV_QUECOCHEMECOMPRO_PATH,
    USAR_CSV_CIUDADDELAUTOMOVIL=USAR_CSV_CIUDADDELAUTOMOVIL,
    CSV_CIUDADDELAUTOMOVIL_PATH=CSV_CIUDADDELAUTOMOVIL_PATH,
    fiabilidad_path=fiabilidad_path,
    pesos_QUECOCHEMECOMPRO=pesos_QUECOCHEMECOMPRO,
    pesos_CIUDADDELAUTOMOVIL=pesos_CIUDADDELAUTOMOVIL,
    ETIQUETAS=ETIQUETAS,
    COMBUSTIBLE_SCORE=COMBUSTIBLE_SCORE,
    CAMBIO_SCORE=CAMBIO_SCORE,
    GARANTIA=GARANTIA,
    precio_objetivo=precio_objetivo,
    porc_mas_precio_objetivo=porc_mas_precio_objetivo,
    km_objetivo=km_objetivo,
    porc_km_objetivo = porc_km_objetivo,
)
