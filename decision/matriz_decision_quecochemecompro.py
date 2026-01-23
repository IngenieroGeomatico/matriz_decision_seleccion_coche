import pandas as pd

def mapear_etiqueta(df, ETIQUETAS):
    # Normaliza las claves de ETIQUETAS a mayúsculas para que coincidan
    etiquetas_up = {str(k).upper(): v for k, v in ETIQUETAS.items()}
    df["etiqueta_score"] = (
        df["etiqueta_medioambiental"].astype(str)
        .str.upper()
        .map(etiquetas_up)
        .fillna(0)
    ).astype(float)
    return df

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
    
def normalizar_precio(col, precio_objetivo):
    """
    1.0 si precio <= objetivo
    Penaliza progresivamente si lo supera
    """
    col = col.astype(float)

    score = 1 - (col - precio_objetivo) / precio_objetivo
    score[col <= precio_objetivo] = 1.0

    return score.clip(lower=0)

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
