import subprocess
import sys
from pathlib import Path

from ..core.config import GNU_SCRIPT_TEXT_PATH

def run_gnuradio_text_flowgraph(run_id: str, log_path: Path) -> int:
    """Ejecuta el script de GNU Radio para texto en un proceso hijo."""
    log_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [sys.executable, str(GNU_SCRIPT_TEXT_PATH)]

    with open(log_path, "w", encoding="utf-8", errors="ignore") as f:
        f.write(f"=== Run {run_id} (MODO TEXTO) ===\n")
        f.write(f"Command: {' '.join(cmd)}\n")
        f.write(f"Script: {GNU_SCRIPT_TEXT_PATH}\n\n")
        f.flush()
        
        try:
            proc = subprocess.run(
                cmd, 
                stdout=f, 
                stderr=subprocess.STDOUT,
                timeout=30  # 30 segundos timeout
            )
            return int(proc.returncode)
        except subprocess.TimeoutExpired:
            f.write("\n[ERROR] Timeout - El script tardó demasiado\n")
            return 1
        except Exception as e:
            f.write(f"\n[ERROR] Exception: {e}\n")
            return 1