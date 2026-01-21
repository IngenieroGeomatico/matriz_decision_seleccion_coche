import pandas as pd

def mapear_etiqueta(df, ETIQUETAS):
    df["etiqueta_score"] = (
        df["etiqueta_medioambiental"]
        .str.upper()
        .map(ETIQUETAS)
        .fillna(0)
    )
    return df

def normalizar(col, minimizar=True):
    col = col.astype(float)

    if minimizar:
        return (col.max() - col) / (col.max() - col.min())
    else:
        return (col - col.min()) / (col.max() - col.min())
    
def normalizar_precio(col, precio_objetivo):
    """
    1.0 si precio <= objetivo
    Penaliza progresivamente si lo supera
    """
    col = col.astype(float)

    score = 1 - (col - precio_objetivo) / precio_objetivo
    score[col <= precio_objetivo] = 1.0

    return score.clip(lower=0)

def calcular_score(df, pesos,ETIQUETAS, precio_objetivo:20000, porc_mas_precio_objetivo:1.5):
    df = df.copy()

    # Etiqueta medioambiental → numérica
    df = mapear_etiqueta(df, ETIQUETAS)

    # ❌ DESCARTAR coches fuera de presupuesto o que su valor sea 0
    df = df[df["precio"] <= precio_objetivo * porc_mas_precio_objetivo]
    df = df[df["precio"] >= 1000]

    df_norm = pd.DataFrame()

    df_norm["precio"] = normalizar_precio(df["precio"], precio_objetivo)
    df_norm["consumo"] = normalizar(df["consumo"], minimizar=True)
    df_norm["potencia"] = normalizar(df["potencia"], minimizar=False)
    df_norm["fiabilidad"] = normalizar(df["fiabilidad"], minimizar=False)
    df_norm["etiqueta"] = df["etiqueta_score"]  # ya está normalizada

    # Score final ponderado
    df["score"] = sum(df_norm[c] * pesos[c] for c in pesos)

    return df.sort_values("score", ascending=False)
