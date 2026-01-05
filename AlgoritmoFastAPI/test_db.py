# test_db.py
import sqlite3
from pathlib import Path

print("🔍 Buscando runs.sqlite3...")

# Busca en todas las ubicaciones posibles
locations = [
    Path.cwd(),
    Path.cwd() / "backend",
    Path.home() / "Downloads" / "gmsk_web_interface",
    Path.home() / "Downloads" / "gmsk_web_interface" / "backend",
]

for loc in locations:
    db_file = loc / "runs.sqlite3"
    if db_file.exists():
        print(f"✅ ENCONTRADO en: {db_file}")
        
        # Conectar y mostrar datos
        conn = sqlite3.connect(str(db_file))
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        # Mostrar tablas
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cur.fetchall()
        print(f"  Tablas: {[t[0] for t in tables]}")
        
        # Mostrar datos de runs
        if 'runs' in [t[0] for t in tables]:
            cur.execute("SELECT id, filename, status FROM runs LIMIT 5")
            rows = cur.fetchall()
            print(f"  Datos en 'runs' ({len(rows)} registros):")
            for row in rows:
                print(f"    - {row['id'][:8]}...: {row['filename']} [{row['status']}]")
        
        conn.close()
        break
else:
    print("❌ NO ENCONTRADO en ninguna ubicación")
    print("📁 Directorio actual:", Path.cwd())
    print("📁 Contenido:", list(Path.cwd().iterdir()))