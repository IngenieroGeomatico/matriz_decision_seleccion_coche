# Matriz de decisión para selección de coche

Proyecto para ayudar a elegir un coche mediante una matriz de decisión basada en datos (especificaciones, valor de mercado y fiabilidad).

**Características:**
- **Objetivo:**: Facilitar la comparación y puntuación de coches según múltiples criterios.
- **Datos:**: Utiliza ficheros CSV con especificaciones, fiabilidad y precios.
- **Modular:**: Componentes separados en `api/` y `decision/` para facilitar extensión.

**Requisitos:**
- **Python:**: 3.8+
- **Dependencias:**: Instalar con `pip install -r requirements.txt`.
- **Recomendaciones:**: Instalar en entorno virtual `python3 -m venv .venv & source .venv/bin/activate`.

**Instalación rápida:**
```bash
git clone <repo>
cd matriz_decision_seleccion_coche
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**Archivos clave:**
- **`main.py`**: Punto de entrada para ejecutar el flujo completo de generación de la matriz de decisión.
- **api/**: Módulos para obtener y procesar datos de coches:
	- `coches_nuevos.py` — carga/normaliza catálogo de coches.
	- `especificaciones.py` — funciones para leer y procesar especificaciones técnicas.
	- `valor_mercado.py` — calcula o normaliza el valor de mercado/precio.
- **decision/matriz_decision.py**: Lógica para construir la matriz de decisión y calcular puntuaciones.
- **data/**: CSVs de ejemplo usados como entrada:
	- `coches_quecochemecompro.csv`
	- `fiabilidad_marcas.csv`

**Uso básico:**
1. Asegúrate de tener los CSVs actualizados en la carpeta `data/`.
2. Personaliza los valores de peso segú tu gusto, en el archivo main.py
3. Ejecuta:
```bash
python3 main.py
```
4. El script genera la matriz de decisión y muestra (o guarda) las puntuaciones finales. Revisa `decision/matriz_decision.py` para personalizar criterios o pesos.

**Contribución:**
- Abre issues y PRs. Sigue el estilo de código existente y añade tests cuando implementes funcionalidades nuevas.


**Licencia:**
- Revisa el fichero `LICENSE` en la raíz del repositorio.
