import pandas as pd
from datetime import datetime


# --------------------------------------------------
# Normalizaciones
# --------------------------------------------------

def normalizar(col, minimizar=True):
    col = col.astype(float)
    denom = col.max() - col.min()
    if denom == 0 or pd.isna(denom):
        # Si todos los valores son iguales, devolver una serie neutra (1.0)
        return pd.Series(1.0, index=col.index)

    if minimizar:
        return (col.max() - col) / denom
    else:
        return (col - col.min()) / denom

def normalizar_objetivo(col, objetivo):
    """
    Score 1.0 si col <= objetivo
    Penalización progresiva si lo supera
    """
    col = col.astype(float)

    score = 1 - (col - objetivo) / objetivo
    score[col <= objetivo] = 1.0

    return score.clip(lower=0)


def normalizar_edad(col_anio, edad_objetivo):
    """
    Convierte año -> edad y aplica normalización por objetivo
    """
    anio_actual = datetime.now().year
    edad = (anio_actual - col_anio.astype(int)).clip(lower=1)

    score = 1 - (edad - edad_objetivo) / edad_objetivo
    score[edad <= edad_objetivo] = 1.0

    return score.clip(lower=0)


# --------------------------------------------------
# Variables derivadas
# --------------------------------------------------

def calcular_km_anio_media(df):
    edad = df["edad"] 
    return df["Kilómetros"] / edad

def calcular_edad(df):
    """
    Convierte año -> edad y aplica normalización por objetivo
    """
    anio_actual = datetime.now().year
    return (anio_actual - df["Año"]).clip(lower=1)


# --------------------------------------------------
# Categóricos
# --------------------------------------------------

def mapear_categorico(df, columna, mapping, default=0.5):
    return (
        df[columna]
        .astype(str)
        .str.upper()
        .map(mapping)
        .fillna(default)
        .astype(float)
    )


# --------------------------------------------------
# Score principal
# --------------------------------------------------

def calcular_score_ciudaddelautomovil(
    df,
    pesos,
    COMBUSTIBLE_SCORE,
    CAMBIO_SCORE,   
    GARANTIA,
    precio_objetivo=18000,
    km_objetivo=70000,
    porc_mas_precio_objetivo = 1.5,
    porc_km_objetivo = 1.5,
):
    df = df.copy()

    # ----------------------------
    # Filtros duros
    # ----------------------------
    df = df[df["precio"] <= precio_objetivo * porc_mas_precio_objetivo]
    df = df[df["Kilómetros"] <= km_objetivo * porc_km_objetivo]

    # ----------------------------
    # Variables derivadas
    # ----------------------------
    df["edad"] = calcular_edad(df)
    df["km_anio_media"] = calcular_km_anio_media(df)

    # ----------------------------
    # Normalización
    # ----------------------------
    df_norm = pd.DataFrame(index=df.index)

    df_norm["precio"] = normalizar_objetivo(df["precio"], precio_objetivo)
    df_norm["kilometros"] = normalizar_objetivo(df["Kilómetros"], km_objetivo)

    df_norm["edad"] = normalizar(df["edad"], minimizar=True)
    
    df_norm["km_anio"] = normalizar(df["km_anio_media"], minimizar=True)

    df_norm["fiabilidad"] = normalizar(df["fiabilidad"], minimizar=False)

    df_norm["potencia"] = normalizar(df["potencia"], minimizar=False)

    df_norm["garantia"] = mapear_categorico(
        df, "Garantía", GARANTIA
    )
    df_norm["garantia"] = normalizar(df_norm["garantia"].astype(float), minimizar=False)


    df_norm["combustible"] = mapear_categorico(
        df, "Combustible", COMBUSTIBLE_SCORE
    )
    df_norm["combustible"] = normalizar(df_norm["combustible"].astype(float), minimizar=False)

    df_norm["cambio"] = mapear_categorico(
        df, "Cambio", CAMBIO_SCORE
    )
    df_norm["cambio"] = normalizar(df_norm["cambio"].astype(float), minimizar=False)

    # ----------------------------
    # Score final
    # ----------------------------
    pesos_series = pd.Series(pesos)
    df["score"] = df_norm.multiply(pesos_series, axis=1).sum(axis=1)

    return df.sort_values("score", ascending=False)
