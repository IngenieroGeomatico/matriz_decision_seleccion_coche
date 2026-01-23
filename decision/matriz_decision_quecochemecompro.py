import pandas as pd

from .matriz_general import (
    mapear_etiqueta,
    normalizar,
    normalizar_precio,
)

def calcular_score_quecochemecompro(df, pesos, ETIQUETAS, precio_objetivo=20000, porc_mas_precio_objetivo=1.5):
    df = df.copy()

    # Etiqueta medioambiental → numérica
    df = mapear_etiqueta(df, ETIQUETAS)

    # ❌ DESCARTAR coches fuera de presupuesto o que su valor sea 0
    df = df[df["precio"] <= precio_objetivo * porc_mas_precio_objetivo]
    df = df[df["precio"] >= 10]

    df_norm = pd.DataFrame(index=df.index)

    df_norm["precio"] = normalizar_precio(df["precio"], precio_objetivo)
    df_norm["consumo"] = normalizar(df["consumo"], minimizar=True)
    df_norm["potencia"] = normalizar(df["potencia"], minimizar=False)
    df_norm["fiabilidad"] = normalizar(df["fiabilidad"], minimizar=False)
    df_norm["etiqueta"] = normalizar(df["etiqueta_score"].astype(float) , minimizar=False)

    # Score final ponderado (multiplica cada columna por su peso y suma por fila)
    pesos_series = pd.Series(pesos)
    df["score"] = df_norm.multiply(pesos_series, axis=1).sum(axis=1)

    return df.sort_values("score", ascending=False)
