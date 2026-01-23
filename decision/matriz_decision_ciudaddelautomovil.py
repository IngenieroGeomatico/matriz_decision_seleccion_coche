import pandas as pd

from .matriz_general import (
    normalizar,
    normalizar_objetivo,
    normalizar_edad,
    calcular_km_anio_media,
    calcular_edad,
    mapear_categorico,
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
