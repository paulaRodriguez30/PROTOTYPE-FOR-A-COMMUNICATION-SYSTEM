'''# backend/core/config.py
from pathlib import Path
import os

# Carpeta base del proyecto (donde está la carpeta backend/)
BASE_DIR = Path(__file__).resolve().parents[2]

# Carpeta donde se guardan las imágenes originales subidas
UPLOAD_DIR = (BASE_DIR / "uploads").resolve()
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Carpeta donde esperas tener tus scripts de GNU Radio
GNU_DIR = (BASE_DIR / "gnuradio").resolve()
GNU_DIR.mkdir(parents=True, exist_ok=True)

# Script de GNU Radio a ejecutar (puedes cambiarlo por variable de entorno)
GNU_SCRIPT_NAME = os.environ.get("GNU_SCRIPT_NAME", "FULL_SIM_GMSK_v2.py")
GNU_SCRIPT_PATH = GNU_DIR / GNU_SCRIPT_NAME

# Ruta donde TU flowgraph debe leer la imagen de entrada.
# Recomendación: en tu bloque image_sender, leer esta ruta.
IMAGE_INPUT_PATH = GNU_DIR / "input_image.jpg"

# Ruta donde TU flowgraph leerá el texto de entrada (¡AGREGA ESTA LÍNEA!)
TEXT_INPUT_PATH = GNU_DIR / "input_text.txt"  # ¡ESTO ES LO QUE FALTA!

# Tamaño máximo del archivo (15 MB)
MAX_UPLOAD_BYTES = 15 * 1024 * 1024

ALLOWED_MIME = {"image/png", "image/jpeg", "image/jpg", "image/bmp", "image/tiff"}'''
from pathlib import Path
import os

# Carpeta base del proyecto (donde está la carpeta backend/)
BASE_DIR = Path(__file__).resolve().parents[2]

# Carpeta donde se guardan las imágenes originales subidas
UPLOAD_DIR = (BASE_DIR / "uploads").resolve()
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Carpeta donde esperas tener tus scripts de GNU Radio
GNU_DIR = (BASE_DIR / "gnuradio").resolve()
GNU_DIR.mkdir(parents=True, exist_ok=True)

# Scripts de GNU Radio (IMPORTANTE: DOS SCRIPTS DIFERENTES)
GNU_SCRIPT_IMAGE = os.environ.get("GNU_SCRIPT_IMAGE", "FULL_SIM_GMSK_v2.py")
GNU_SCRIPT_TEXT = os.environ.get("GNU_SCRIPT_TEXT", "FULL_SIM_GMSK_v2_TEXTO.py")

GNU_SCRIPT_IMAGE_PATH = GNU_DIR / GNU_SCRIPT_IMAGE
GNU_SCRIPT_TEXT_PATH = GNU_DIR / GNU_SCRIPT_TEXT

# Ruta donde TU flowgraph debe leer la imagen de entrada.
IMAGE_INPUT_PATH = GNU_DIR / "input_image.jpg"

# Ruta donde TU flowgraph leerá el texto de entrada
TEXT_INPUT_PATH = GNU_DIR / "input_text.txt"

# Ruta donde se guardará el texto recibido
TEXT_OUTPUT_PATH = GNU_DIR / "output_received_text.txt"

# Tamaño máximo del archivo (15 MB)
MAX_UPLOAD_BYTES = 15 * 1024 * 1024

# Máximo caracteres para texto - ¡ESTO ES LO QUE FALTABA!
MAX_TEXT_CHARS = 5000

ALLOWED_MIME = {"image/png", "image/jpeg", "image/jpg", "image/bmp", "image/tiff"}

