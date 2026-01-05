'''from fastapi import FastAPI, UploadFile, File, HTTPException, Request, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pathlib import Path
import uuid
import shutil

from .core.config import (
    UPLOAD_DIR,
    IMAGE_INPUT_PATH,
    ALLOWED_MIME,
    MAX_UPLOAD_BYTES,
)
from .db import init_db, create_run, update_status, get_run
from .services.runner import run_gnuradio_flowgraph

BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

def create_app() -> FastAPI:
    app = FastAPI(title="GMSK Image Web Interface")

    # Static files
    app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

    @app.on_event("startup")
    def _startup():
        init_db()

    @app.get("/", response_class=HTMLResponse)
    def index(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})

    @app.post("/api/upload")
    async def upload_image(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
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
            filename=file.filename,
            stored_path=str(stored_path),
            status="QUEUED",
            log_path=str(log_path),
        )

        # Lanzar el flowgraph en segundo plano
        background_tasks.add_task(_run_flow_in_background, run_id, log_path)

        return {
            "run_id": run_id,
            "status": "QUEUED",
            "filename": file.filename,
        }

    @app.get("/api/runs/{run_id}")
    def get_run_status(run_id: str):
        run = get_run(run_id)
        if not run:
            raise HTTPException(status_code=404, detail="Run no encontrado")
        # Leer últimas líneas del log (si existe)
        log_tail = ""
        log_path = run.get("log_path")
        if log_path and Path(log_path).exists():
            try:
                with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()[-0:]
                log_tail = "".join(lines)
            except Exception:
                log_tail = ""
        run["log_tail"] = log_tail
        return run

    return app


def _run_flow_in_background(run_id: str, log_path: Path):
    update_status(run_id, status="RUNNING", finished=False)
    rc = run_gnuradio_flowgraph(run_id, log_path)
    if rc == 0:
        update_status(run_id, status="DONE", finished=True)
    else:
        update_status(run_id, status=f"FAILED (rc={rc})", finished=True)


app = create_app()'''

from fastapi import FastAPI, UploadFile, File, HTTPException, Request, BackgroundTasks, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pathlib import Path
import uuid
import shutil

from .core.config import (
    UPLOAD_DIR,
    IMAGE_INPUT_PATH,
    TEXT_INPUT_PATH,      # <-- AÑADIR
    ALLOWED_MIME,
    MAX_UPLOAD_BYTES,
    MAX_TEXT_CHARS,       # <-- AÑADIR
)
from .db import init_db, create_run, update_status, get_run
from .services.runner import run_gnuradio_flowgraph

BASE_DIR = Path(__file__).resolve().parent


templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

def create_app() -> FastAPI:
    app = FastAPI(title="GMSK Image Web Interface")

    # Static files
    app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

    @app.on_event("startup")
    def _startup():
        init_db()

    @app.get("/", response_class=HTMLResponse)
    def index(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})

    # ========== ENDPOINT ORIGINAL (IMÁGENES) - NO CAMBIAR ==========
    @app.post("/api/upload")
    async def upload_image(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
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
            filename=file.filename,
            stored_path=str(stored_path),
            status="QUEUED",
            log_path=str(log_path),
        )

        # Lanzar el flowgraph en segundo plano (modo imagen)
        background_tasks.add_task(_run_flow_in_background, run_id, log_path, "image")

        return {
            "run_id": run_id,
            "status": "QUEUED",
            "filename": file.filename,
            "mode": "image"
        }

    # ========== NUEVO ENDPOINT PARA TEXTO ==========
    @app.post("/api/upload_text")
    async def upload_text(background_tasks: BackgroundTasks, text: str = Form(...)):
        # Validar texto
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
            filename="text_input.txt",
            stored_path=str(stored_path),
            status="QUEUED",
            log_path=str(log_path),
        )

        # Lanzar el flowgraph en segundo plano (modo texto)
        background_tasks.add_task(_run_flow_in_background, run_id, log_path, "text")

        return {
            "run_id": run_id,
            "status": "QUEUED",
            "filename": "text_input.txt",
            "mode": "text",
            "text_preview": text[:100] + ("..." if len(text) > 100 else "")
        }

    @app.get("/api/runs/{run_id}")
    def get_run_status(run_id: str):
        run = get_run(run_id)
        if not run:
            raise HTTPException(status_code=404, detail="Run no encontrado")
        # Leer últimas líneas del log (si existe)
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
    rc = run_gnuradio_flowgraph(run_id, log_path, mode)  # Pasar el modo
    if rc == 0:
        update_status(run_id, status="DONE", finished=True)
    else:
        update_status(run_id, status=f"FAILED (rc={rc})", finished=True)


app = create_app()