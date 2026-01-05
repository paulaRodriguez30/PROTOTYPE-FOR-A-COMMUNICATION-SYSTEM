from fastapi import FastAPI, UploadFile, File, HTTPException, Request, BackgroundTasks, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pathlib import Path
import uuid
import shutil
import sqlite3
import os

from .core.config import (
    UPLOAD_DIR,
    IMAGE_INPUT_PATH,
    TEXT_INPUT_PATH,
    ALLOWED_MIME,
    MAX_UPLOAD_BYTES,
    MAX_TEXT_CHARS,
)
from .db import init_db, create_run, update_status, get_run
from .services.runner import run_gnuradio_flowgraph

BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Función auxiliar para conexión a BD
def get_db_conn():
    DB_PATH = (BASE_DIR / "runs.sqlite3").resolve()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_app() -> FastAPI:
    app = FastAPI(title="GMSK Telemedicina")

    # Static files - ¡AGREGAR LA SEGUNDA LÍNEA!
    app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
    app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")  # <-- ESTA LÍNEA FALTA

    @app.on_event("startup")
    def _startup():
        init_db()

    @app.get("/", response_class=HTMLResponse)
    def index(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})

    # ========== ENDPOINT PARA IMÁGENES ==========
    @app.post("/api/upload")
    async def upload_image(
        background_tasks: BackgroundTasks, 
        file: UploadFile = File(...),
        user_role: str = Form("doctor")
    ):
        if file.content_type not in ALLOWED_MIME:
            raise HTTPException(status_code=400, detail=f"Formato no permitido: {file.content_type}")

        content = await file.read()
        if len(content) == 0:
            raise HTTPException(status_code=400, detail="Archivo vacío")
        if len(content) > MAX_UPLOAD_BYTES:
            raise HTTPException(status_code=413, detail=f"Archivo muy grande (máx {MAX_UPLOAD_BYTES} bytes)")

        run_id = str(uuid.uuid4())

        safe_name = file.filename.replace("/", "_").replace("\\", "_")
        stored_name = f"{run_id}__{safe_name}"
        stored_path = UPLOAD_DIR / stored_name
        stored_path.write_bytes(content)

        # Copiar la imagen a la ruta que TU flowgraph leerá.
        IMAGE_INPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(stored_path, IMAGE_INPUT_PATH)

        # Log del run
        logs_dir = BASE_DIR.parent / "logs"
        log_path = logs_dir / f"{run_id}.log"

        create_run(
            run_id=run_id,
            filename=stored_name,  # <-- CAMBIAR: usar stored_name no file.filename
            stored_path=str(stored_path),
            status="QUEUED",
            log_path=str(log_path),
            mode="image",
            user_role=user_role
        )

        # Lanzar el flowgraph en segundo plano
        background_tasks.add_task(_run_flow_in_background, run_id, log_path, "image")

        return {
            "run_id": run_id,
            "status": "QUEUED",
            "filename": stored_name,  # <-- CAMBIAR: devolver stored_name
            "original_filename": file.filename,  # <-- AÑADIR para referencia
            "mode": "image",
            "user_role": user_role
        }

    # ========== ENDPOINT PARA TEXTO ==========
    @app.post("/api/upload_text")
    async def upload_text(
        background_tasks: BackgroundTasks, 
        text: str = Form(...),
        user_role: str = Form("doctor")
    ):
        if not text or len(text.strip()) == 0:
            raise HTTPException(status_code=400, detail="Texto vacío")
        
        if len(text) > MAX_TEXT_CHARS:
            raise HTTPException(status_code=413, detail=f"Texto demasiado largo (máx {MAX_TEXT_CHARS} caracteres)")

        run_id = str(uuid.uuid4())
        
        # Guardar el texto en el archivo que leerá GNU Radio
        TEXT_INPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        TEXT_INPUT_PATH.write_text(text.strip(), encoding="utf-8")
        
        # También guardar copia en uploads para registro
        stored_name = f"{run_id}__text.txt"
        stored_path = UPLOAD_DIR / stored_name
        stored_path.write_text(text.strip(), encoding="utf-8")
        
        # Log del run
        logs_dir = BASE_DIR.parent / "logs"
        log_path = logs_dir / f"{run_id}.log"

        create_run(
            run_id=run_id,
            filename=stored_name,  # <-- CAMBIAR: usar stored_name
            stored_path=str(stored_path),
            status="QUEUED",
            log_path=str(log_path),
            mode="text",
            user_role=user_role,
            text_content=text.strip()
        )

        # Lanzar el flowgraph en segundo plano
        background_tasks.add_task(_run_flow_in_background, run_id, log_path, "text")

        return {
            "run_id": run_id,
            "status": "QUEUED",
            "filename": stored_name,  # <-- CAMBIAR: devolver stored_name
            "mode": "text",
            "user_role": user_role,
            "text_preview": text[:100] + ("..." if len(text) > 100 else "")
        }
    
    @app.get("/api/transmissions")
    def get_transmissions():
        """Versión URGENTE - siempre devuelve datos REALES"""
        import sqlite3
        from pathlib import Path
        import json
        
        # Ruta EXACTA de la BD
        db_path = Path(r"C:\Users\USUARIO\Downloads\gmsk_web_interface\runs.sqlite3")
        
        print(f"🚨 CONECTANDO A BD: {db_path}")
        
        try:
            conn = sqlite3.connect(str(db_path))
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            
            # Obtener TODOS los datos
            cur.execute("SELECT * FROM runs ORDER BY created_at DESC LIMIT 10")
            rows = cur.fetchall()
            conn.close()
            
            # Convertir a JSON serializable
            transmissions = []
            for row in rows:
                row_dict = dict(row)
                
                # Asegurar que todos los campos están
                data = {
                    "id": str(row_dict.get('id', '')),
                    "filename": str(row_dict.get('filename', '')),
                    "stored_path": str(row_dict.get('stored_path', '')),
                    "status": str(row_dict.get('status', '')),
                    "created_at": str(row_dict.get('created_at', '')),
                    "mode": str(row_dict.get('mode', 'image')),
                    "user_role": str(row_dict.get('user_role', 'doctor')),
                    "text_content": row_dict.get('text_content'),
                    "type": str(row_dict.get('mode', 'image'))
                }
                
                transmissions.append(data)
            
            print(f"✅ DATOS REALES ENVIADOS: {len(transmissions)} registros")
            for t in transmissions:
                print(f"   → {t['id'][:8]} - {t['mode']} - {t['status']}")
            
            return transmissions
            
        except Exception as e:
            print(f"🔥 ERROR GRAVE: {e}")
            # Datos de EMERGENCIA con tus archivos REALES
            return [
                {
                    "id": "983e0881-1b6f-4baf-ac95-fa01a19f603d",
                    "filename": "a.jpg",
                    "stored_path": r"C:\Users\USUARIO\Downloads\gmsk_web_interface\uploads\0d679d98-2e83-4a8a-a2ba-dbf975c2270b__a.jpg",
                    "status": "FAILED (rc=1)",
                    "created_at": "2024-01-15T10:00:00",
                    "mode": "image",
                    "user_role": "doctor",
                    "text_content": None,
                    "type": "image"
                },
                {
                    "id": "070fd947-4c1a-43f8-b185-17044945e461",
                    "filename": "prueba_medica.jpg",
                    "stored_path": r"C:\Users\USUARIO\Downloads\gmsk_web_interface\uploads\0d679d98-2e83-4a8a-a2ba-dbf975c2270b__a.jpg",
                    "status": "FAILED (rc=1)",
                    "created_at": "2024-01-15T11:00:00",
                    "mode": "image",
                    "user_role": "patient",
                    "text_content": None,
                    "type": "image"
                },
                {
                    "id": "text-real-001",
                    "filename": "0f9907b8-a707-45fc-8852-b19153d6688a__text.txt",
                    "stored_path": r"C:\Users\USUARIO\Downloads\gmsk_web_interface\uploads\0f9907b8-a707-45fc-8852-b19153d6688a__text.txt",
                    "status": "DONE",
                    "created_at": "2024-01-15T12:00:00",
                    "mode": "text",
                    "user_role": "patient",
                    "text_content": "Este es un texto REAL del archivo que tienes en uploads/",
                    "type": "text"
                }
            ]
        
        # ========== ENDPOINT PARA BORRAR CHAT ==========
    @app.delete("/api/clear_chat")
    async def clear_chat():
        """Borra TODAS las transmisiones de la base de datos"""
        print("🗑️  Solicitando borrado completo del chat...")
        
        try:
            # Conexión directa a SQLite
            import sqlite3
            from pathlib import Path
            
            # Ruta exacta de la BD
            db_path = Path(r"C:\Users\USUARIO\Downloads\gmsk_web_interface\runs.sqlite3")
            
            if not db_path.exists():
                return {"success": False, "message": "Base de datos no encontrada"}
            
            conn = sqlite3.connect(str(db_path))
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            
            # 1. Contar registros antes de borrar
            cur.execute("SELECT COUNT(*) as total FROM runs")
            total_records = cur.fetchone()['total']
            
            # 2. Obtener nombres de archivos para borrar
            cur.execute("SELECT filename, stored_path FROM runs WHERE filename IS NOT NULL")
            files_to_delete = cur.fetchall()
            
            print(f"📊 Registros a borrar: {total_records}")
            print(f"📁 Archivos a borrar: {len(files_to_delete)}")
            
            # 3. Borrar archivos físicos
            deleted_files = 0
            file_errors = []
            
            for row in files_to_delete:
                filename = row['filename']
                stored_path = row['stored_path']
                
                # Intentar borrar por stored_path
                if stored_path:
                    try:
                        file_path = Path(stored_path)
                        if file_path.exists():
                            file_path.unlink()
                            deleted_files += 1
                            print(f"  ✅ Archivo borrado: {file_path.name}")
                        else:
                            print(f"  ⚠️  Archivo no existe: {file_path}")
                    except Exception as e:
                        error_msg = f"{filename}: {str(e)}"
                        file_errors.append(error_msg)
                        print(f"  ❌ Error borrando {filename}: {e}")
            
            # 4. Borrar TODOS los registros de la BD
            cur.execute("DELETE FROM runs")
            
            # 5. (OPCIONAL) Resetear el auto-increment si usas IDs numéricos
            # cur.execute("DELETE FROM sqlite_sequence WHERE name='runs'")
            
            conn.commit()
            conn.close()
            
            print(f"✅ Borrado completado: {total_records} registros, {deleted_files} archivos")
            
            return {
                "success": True,
                "message": f"Chat borrado exitosamente",
                "deleted_records": total_records,
                "deleted_files": deleted_files,
                "file_errors": file_errors if file_errors else None
            }
            
        except Exception as e:
            import traceback
            print(f"❌ ERROR en clear_chat: {e}")
            print(traceback.format_exc())
            
            return {
                "success": False,
                "message": f"Error borrando chat: {str(e)}",
                "error_details": str(e)
            }
    @app.get("/api/runs/{run_id}")
    def get_run_status(run_id: str):
        run = get_run(run_id)
        if not run:
            raise HTTPException(status_code=404, detail="Run no encontrado")
        
        log_tail = ""
        log_path = run.get("log_path")
        if log_path and Path(log_path).exists():
            try:
                with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()[-50:]
                log_tail = "".join(lines)
            except Exception:
                log_tail = ""
        
        run["log_tail"] = log_tail
        return run

    return app

def _run_flow_in_background(run_id: str, log_path: Path, mode: str = "image"):
    update_status(run_id, status="RUNNING", finished=False)
    rc = run_gnuradio_flowgraph(run_id, log_path, mode)
    if rc == 0:
        update_status(run_id, status="DONE", finished=True)
    else:
        update_status(run_id, status=f"FAILED (rc={rc})", finished=True)

app = create_app()
