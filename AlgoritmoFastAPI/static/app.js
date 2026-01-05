const $ = (id) => document.getElementById(id);

// 🔹 Cambia esta IP por la de tu servidor FastAPI
const SERVER_URL = "https://subturriculated-vinously-hazel.ngrok-free.dev";

let selectedFile = null;
let currentRunId = null;
let pollTimer = null;

function prettyBytes(n) {
  if (!n && n !== 0) return "";
  const u = ["B","KB","MB","GB"];
  let i = 0; let x = n;
  while (x >= 1024 && i < u.length-1) { x /= 1024; i++; }
  return `${x.toFixed(i===0?0:1)} ${u[i]}`;
}

function setFile(file) {
  selectedFile = file;
  if (!file) {
    $("fileName").textContent = "Ningún archivo seleccionado";
    $("fileSize").textContent = "";
    $("preview").style.display = "none";
    $("btnUpload").disabled = true;
    $("msg").textContent = "Selecciona una imagen para empezar.";
    $("msg").className = "msg";
    return;
  }
  $("fileName").textContent = file.name;
  $("fileSize").textContent = prettyBytes(file.size);
  $("btnUpload").disabled = false;
  const url = URL.createObjectURL(file);
  const img = $("preview");
  img.src = url;
  img.style.display = "block";
  $("msg").textContent = "Listo, ahora puedes iniciar la simulación.";
  $("msg").className = "msg";
}

function setDots(status) {
  const queued = $("dot-queued");
  const running = $("dot-running");
  const done = $("dot-done");
  queued.classList.remove("active");
  running.classList.remove("active");
  done.classList.remove("active");

  if (!status) return;

  if (status.startsWith("QUEUED")) queued.classList.add("active");
  if (status.startsWith("RUNNING")) {
    queued.classList.add("active");
    running.classList.add("active");
  }
  if (status.startsWith("DONE")) {
    queued.classList.add("active");
    running.classList.add("active");
    done.classList.add("active");
  }
  if (status.startsWith("FAILED")) {
    queued.classList.add("active");
    running.classList.add("active");
  }
}

async function upload() {
  const file = selectedFile;
  if (!file) return;

  $("btnUpload").disabled = true;
  $("msg").textContent = "Subiendo imagen y lanzando flowgraph...";
  $("msg").className = "msg";

  const form = new FormData();
  form.append("file", file);

  try {
    const res = await fetch(`${SERVER_URL}/api/upload`, {
      method: "POST",
      body: form,
    });
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail || "Error subiendo archivo");
    }
    currentRunId = data.run_id;
    $("runId").textContent = currentRunId;
    $("runStatus").textContent = data.status;
    $("runInfo").style.display = "flex";
    $("msg").textContent = "✅ Imagen enviada al backend. El flowgraph se está preparando (QUEUED).";
    $("msg").className = "msg ok";
    setDots(data.status);

    if (pollTimer) clearInterval(pollTimer);
    pollTimer = setInterval(pollStatus, 1500);
  } catch (err) {
    $("msg").textContent = "❌ " + err.message;
    $("msg").className = "msg err";
    $("btnUpload").disabled = false;
  }
}

async function pollStatus() {
  if (!currentRunId) return;
  try {
    const res = await fetch(`${SERVER_URL}/api/runs/${currentRunId}`);
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Error consultando estado");

    $("runStatus").textContent = data.status;
    setDots(data.status);

    const box = $("logBox");
    if (data.log_tail) {
      box.textContent = data.log_tail;
    } else {
      box.innerHTML = '<div class="placeholder">Esperando salida del script de GNU Radio...</div>';
    }

    if (data.status.startsWith("DONE") || data.status.startsWith("FAILED")) {
      clearInterval(pollTimer);
      pollTimer = null;
      if (data.status.startsWith("DONE")) {
        $("msg").textContent = "✅ Ejecución completada. Revisa la imagen recibida / resultados en tu flowgraph.";
        $("msg").className = "msg ok";
      } else {
        $("msg").textContent = "⚠️ El script terminó con error: " + data.status;
        $("msg").className = "msg err";
      }
      $("btnUpload").disabled = false;
    }
  } catch (err) {
    console.error(err);
  }
}

function init() {
  const dz = $("dropzone");
  const fileInput = $("fileInput");

  fileInput.addEventListener("change", (e) => {
    const file = e.target.files && e.target.files[0];
    if (file) setFile(file);
  });

  dz.addEventListener("dragover", (e) => {
    e.preventDefault();
    dz.classList.add("drag");
  });
  dz.addEventListener("dragleave", (e) => {
    e.preventDefault();
    dz.classList.remove("drag");
  });
  dz.addEventListener("drop", (e) => {
    e.preventDefault();
    dz.classList.remove("drag");
    const file = e.dataTransfer.files && e.dataTransfer.files[0];
    if (file) {
      setFile(file);
    }
  });

  $("btnUpload").addEventListener("click", upload);
   // Eventos para selector de modo (tu código existente)
  document.querySelectorAll('.mode-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const mode = e.currentTarget.dataset.mode;
      switchMode(mode);
    });
  });

  // Inicializar contador de caracteres (tu código existente)
  $("charCount").textContent = "0 caracteres";

  // 🆕 INICIALIZAR CHAT (NUEVO)
  initChat();
  
  // Opcional: Agregar mensajes de ejemplo (puedes quitar esto después)
  setTimeout(addSampleMessages, 500);
}

document.addEventListener("DOMContentLoaded", init);