# GMSK Image Web Interface

Proyecto de ejemplo donde:

- Un usuario sube una imagen desde una interfaz web bonita (FastAPI + HTML/JS).
- El backend guarda la imagen en `/uploads` y la copia a `gnuradio/input_image.jpg`.
- Se ejecuta tu script de GNU Radio (por defecto `gnuradio/FULL_SIM_GMSK_v2.py`) en segundo plano.
- Puedes ver el estado (QUEUED, RUNNING, DONE, FAILED) y las últimas líneas del log.

## 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

> Recomendación: haz esto dentro de tu entorno de Radioconda, así usas el mismo Python
> que tiene GNU Radio instalado.

## 2. Colocar tus flowgraphs

Copia tus archivos generados por GRC dentro de la carpeta `gnuradio/`, por ejemplo:

- `gnuradio/FULL_SIM_GMSK_v2.py`
- `gnuradio/FULL_SIM_GMSK_v2_epy_block_1.py`
- `gnuradio/FULL_SIM_GMSK_v2_epy_block_3.py`
- `gnuradio/FULL_SIM_GMSK_v2_epy_block_4.py`

Ajusta tu bloque `image_sender` para leer la imagen desde `input_image.jpg` en esta carpeta.
Por ejemplo (Python):

```python
from pathlib import Path
img_path = Path(__file__).resolve().parent / "input_image.jpg"
with open(img_path, "rb") as f:
    self.image_data = f.read()
```

## 3. Ejecutar el servidor

Desde la raíz del proyecto:

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8080 --reload
```

o:

```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8080 --reload
```

Luego abre en tu navegador:

- http://127.0.0.1:8080

## 4. Flujo cuando subes una imagen

1. Guardar el archivo original en `uploads/<run_id>__nombre.ext`.
2. Copiar ese archivo a `gnuradio/input_image.jpg` (sobrescribe la anterior).
3. Registrar un `run` en SQLite (`runs.sqlite3`).
4. Lanzar un BackgroundTask que ejecuta `python gnuradio/FULL_SIM_GMSK_v2.py`
   usando el mismo Python con el que arrancaste uvicorn.
5. El output de tu script se guarda en `logs/<run_id>.log`.
6. El frontend consulta `/api/runs/{run_id}` para mostrar estado + log.

## 5. Cambiar el nombre del script

Si tu script no se llama `FULL_SIM_GMSK_v2.py`, puedes:

- Cambiar la variable de entorno `GNU_SCRIPT_NAME`, o
- Editar `backend/core/config.py` y poner tu nombre ahí.
