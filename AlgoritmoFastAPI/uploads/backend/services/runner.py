'''import subprocess
import sys
from pathlib import Path

from ..core.config import GNU_SCRIPT_PATH

def run_gnuradio_flowgraph(run_id: str, log_path: Path) -> int:
    """Ejecuta el script de GNU Radio en un proceso hijo.

    - Usa el mismo Python con el que corre FastAPI (sys.executable),
      por lo que si levantas uvicorn desde Radioconda, usará ese entorno.
    - Redirige stdout+stderr al archivo log_path.
    """
    log_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [sys.executable, str(GNU_SCRIPT_PATH)]


    with open(log_path, "w", encoding="utf-8", errors="ignore") as f:
        f.write(f"=== Run {run_id} ===\n")
        f.write(f"Command: {' '.join(cmd)}\n\n")
        f.flush()
        proc = subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT)
        return int(proc.returncode)'''
import subprocess
import sys
from pathlib import Path

from ..core.config import GNU_SCRIPT_IMAGE_PATH, GNU_SCRIPT_TEXT_PATH

def run_gnuradio_flowgraph(run_id: str, log_path: Path, mode: str = "image") -> int:
    """Ejecuta el script de GNU Radio en un proceso hijo."""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Elegir el script correcto según el modo
    if mode == "image":
        script_path = GNU_SCRIPT_IMAGE_PATH
    elif mode == "text":
        script_path = GNU_SCRIPT_TEXT_PATH
    else:
        script_path = GNU_SCRIPT_IMAGE_PATH
    
    cmd = [sys.executable, str(script_path)]

    with open(log_path, "w", encoding="utf-8", errors="ignore") as f:
        f.write(f"=== Run {run_id} (Modo: {mode}) ===\n")
        f.write(f"Command: {' '.join(cmd)}\n\n")
        f.flush()
        proc = subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT)
        return int(proc.returncode)