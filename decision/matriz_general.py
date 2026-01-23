import pandas as pd
from datetime import datetime
from typing import Mapping


# -----------------------------
# Normalizaciones genéricas
# -----------------------------

def normalizar(col, minimizar=True):
    col = col.astype(float)
    denom = col.max() - col.min()
    if denom == 0 or pd.isna(denom):
        return pd.Series(1.0, index=col.index)

    if minimizar:
        return (col.max() - col) / denom
    else:
        return (col - col.min()) / denom


def normalizar_objetivo(col, objetivo):
    col = col.astype(float)
    score = 1 - (col - objetivo) / objetivo
    score[col <= objetivo] = 1.0
    return score.clip(lower=0)


def normalizar_precio(col, precio_objetivo):
    return normalizar_objetivo(col, precio_objetivo)


def normalizar_edad(col_anio, edad_objetivo):
    anio_actual = datetime.now().year
    edad = (anio_actual - col_anio.astype(int)).clip(lower=1)
    score = 1 - (edad - edad_objetivo) / edad_objetivo
    score[edad <= edad_objetivo] = 1.0
    return score.clip(lower=0)


# -----------------------------
# Variables derivadas
# -----------------------------

def calcular_km_anio_media(df):
    edad = df["edad"]
    return df["Kilómetros"] / edad


def calcular_edad(df_or_series):
    anio_actual = datetime.now().year
    if isinstance(df_or_series, pd.Series):
        return (anio_actual - df_or_series.astype(int)).clip(lower=1)
    else:
        return (anio_actual - df_or_series["Año"]).clip(lower=1)


# -----------------------------
# Categóricos
# -----------------------------

def mapear_categorico(df, columna, mapping: Mapping, default=0.5):
    mapping_up = {str(k).upper(): v for k, v in mapping.items()}
    return (
        df[columna]
        .astype(str)
        .str.upper()
        .map(mapping_up)
        .fillna(default)
        .astype(float)
    )


def mapear_etiqueta(df, ETIQUETAS, output_col="etiqueta_score"):
    etiquetas_up = {str(k).upper(): v for k, v in ETIQUETAS.items()}
    df[output_col] = (
        df["etiqueta_medioambiental"].astype(str).str.upper().map(etiquetas_up).fillna(0)
    ).astype(float)
    return df
