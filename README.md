# Matriz de decisión para selección de coche

Proyecto para ayudar a elegir un coche mediante una matriz de decisión basada en datos (especificaciones, valor de mercado y fiabilidad).

**Características**
- Objetivo: facilitar la comparación y puntuación de coches según múltiples criterios.
- Datos: usa CSVs en `data/` con especificaciones, precios y fiabilidad.
- Estructura modular: lógica de acceso a datos en `api/` y lógica de puntuación en `decision/`.

**Requisitos**
- Python 3.8+
- Dependencias: `pip install -r requirements.txt` (incluye `pandas`, `requests`, `numpy`, `bs4`).
- Recomendada instalación en entorno virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

**Estructura importante**
- `main.py`: punto de entrada que orquesta la carga de datos y el cálculo de scores.
- `api/`: módulos para obtener y preparar datos (por ejemplo `api_request.py`, `valor_ciudaddelautomovil.py`, `valor_cochesnet.py`, `valor_flexicar.py`, `valor_quecochemecompro.py`,`...`).
- `decision/`:
  - `matriz_general.py`: funciones genéricas reutilizables (normalizaciones, mapeos, utilidades).
  - `matriz_decision_ciudaddelautomovil.py`: lógica y pesos para el ranking según Ciudad del Automóvil.
  - `matriz_decision_quecochemecompro.py`: lógica y pesos para el ranking según QuéCocheMeCompro.
  - `...`
- `data/`: CSVs de ejemplo utilizados como entrada (por ejemplo `coches_quecochemecompro.csv`, `fiabilidad_marcas.csv`, `coches_segunda_mano.csv`,`...`).

**Uso básico**
1. Coloca los CSVs actualizados en `data/`.
2. Ajusta pesos y parámetros en `main.py` o en los módulos bajo `decision/`.
3. Ejecuta:

```bash
python3 main.py
```

El script genera y muestra (o guarda) las puntuaciones ordenadas por `score`.

**Pruebas rápidas / desarrollo**
- Para probar solo la lógica de decisión puedes importar los módulos desde un REPL:

```bash
python3 -c "import sys; sys.path.append('.'); from decision import matriz_general; print('ok')"
```

**Contribución**
- Abre issues o PRs. Mantén estilo y añade tests cuando añadas funcionalidad.

**Licencia**
- Revisa `LICENSE` en la raíz del repositorio.
