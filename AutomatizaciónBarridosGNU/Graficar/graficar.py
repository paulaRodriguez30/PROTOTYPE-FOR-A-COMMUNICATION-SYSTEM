'''import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

# ============================================================
# === FUNCIÓN PARA CARGAR Y PROCESAR UN BARRIDO ==============
# ============================================================
def procesar_barrido(archivo_txt):
    with open(archivo_txt, 'r', encoding='utf-8', errors='ignore') as f:
        lineas = [l.strip() for l in f if l.strip()]

    # Leer parámetros
    freq_central = sample_rate = vector_len = None
    for linea in lineas:
        if "Frequency" in linea:
            freq_central = float(linea.split(":")[1])
        elif "Sample Rate" in linea:
            sample_rate = float(linea.split(":")[1])
        elif "Vector Length" in linea:
            vector_len = int(linea.split(":")[1])

    # Extraer los vectores numéricos
    datos_txt = []
    for linea in lineas:
        if re.match(r"^[-\d\.\s,]+$", linea):
            valores = re.split(r"[\s,]+", linea.strip())
            numeros = []
            for v in valores:
                try:
                    if v.strip() not in ["", "-", "--"]:
                        numeros.append(float(v))
                except ValueError:
                    continue
            if len(numeros) > 1:
                datos_txt.append(numeros)

    # Tomar los 3 primeros vectores válidos
    primeros_vectores = [np.array(v) for v in datos_txt[:3] if len(v) == vector_len]

    # Eje de frecuencias
    freqs = np.linspace(freq_central - sample_rate / 2,
                        freq_central + sample_rate / 2,
                        vector_len)

    return freqs, primeros_vectores, freq_central


# ============================================================
# === LISTA DE LOS 19 BARRIDOS ===============================
# ============================================================
barridos = [
    {"txt": "/Users/USUARIO/Downloads/476M.csv"},
    {"txt": "/Users/USUARIO/Downloads/488_5M.csv"},
    {"txt": "/Users/USUARIO/Downloads/501M.csv"},
    {"txt": "/Users/USUARIO/Downloads/513_5M.csv"},
    {"txt": "/Users/USUARIO/Downloads/526M.csv"},
    {"txt": "/Users/USUARIO/Downloads/538_5M.csv"},
    {"txt": "/Users/USUARIO/Downloads/551M.csv"},
    {"txt": "/Users/USUARIO/Downloads/563_5M.csv"},
    {"txt": "/Users/USUARIO/Downloads/576M.csv"},
    {"txt": "/Users/USUARIO/Downloads/588_5M.csv"},
    {"txt": "/Users/USUARIO/Downloads/601M.csv"},
    {"txt": "/Users/USUARIO/Downloads/613_5M.csv"},
    {"txt": "/Users/USUARIO/Downloads/626M.csv"},
    {"txt": "/Users/USUARIO/Downloads/638_5M.csv"},
    {"txt": "/Users/USUARIO/Downloads/651M.csv"},
    {"txt": "/Users/USUARIO/Downloads/663_5M.csv"},
    {"txt": "/Users/USUARIO/Downloads/676M.csv"},
    {"txt": "/Users/USUARIO/Downloads/688_5M.csv"},
    {"txt": "/Users/USUARIO/Downloads/701M.csv"}
]

# ============================================================
# === ACUMULAR LOS TRES GRUPOS DE VECTORES ===================
# ============================================================
freqs_total = []
vectores_1 = []
vectores_2 = []
vectores_3 = []

for b in barridos:
    freqs, primeros_vectores, fc = procesar_barrido(b["txt"])

    if len(primeros_vectores) >= 1:
        vectores_1.append(primeros_vectores[0])
    if len(primeros_vectores) >= 2:
        vectores_2.append(primeros_vectores[1])
    if len(primeros_vectores) >= 3:
        vectores_3.append(primeros_vectores[2])

    freqs_total.append(freqs)

# Concatenar los 19 barridos
freqs_concat = np.concatenate(freqs_total)
vec1_concat = np.concatenate(vectores_1)
vec2_concat = np.concatenate(vectores_2)
vec3_concat = np.concatenate(vectores_3)

# ============================================================
# === FUNCIÓN PARA GRAFICAR CON REESCALADO ===================
# ============================================================
def graficar_vector(freqs, vector, titulo, color):
    plt.figure(figsize=(16, 7))
    plt.plot(freqs / 1e6, vector, color=color, linewidth=1.5)
    plt.title(titulo, fontsize=15, weight='bold')
    plt.xlabel("Frecuencia [MHz]", fontsize=12)
    plt.ylabel("Magnitud [dBm]", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)

    # Reescalado simétrico en Y
    ymin, ymax = np.min(vector), np.max(vector)
    rango = ymax - ymin
    plt.ylim(ymin - rango * 0.5, ymax + rango * 0.5)  # 0.5 = expande 50% hacia arriba y abajo

    plt.tight_layout()
    plt.show()

# ============================================================
# === GRAFICAR CADA VECTOR CONCATENADO POR SEPARADO ==========
# ============================================================
graficar_vector(freqs_concat, vec1_concat, "Vector 1 - Unión total de barridos (GNU Radio)", "orange")
graficar_vector(freqs_concat, vec2_concat, "Vector 2 - Unión total de barridos (GNU Radio)", "green")
graficar_vector(freqs_concat, vec3_concat, "Vector 3 - Unión total de barridos (GNU Radio)", "purple")'''
'''import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import os

# ============================================================
# === FUNCIÓN PARA CARGAR Y PROCESAR UN BARRIDO ==============
# ============================================================
def procesar_barrido(archivo_txt):
    with open(archivo_txt, 'r', encoding='utf-8', errors='ignore') as f:
        lineas = [l.strip() for l in f if l.strip()]

    freq_central = sample_rate = vector_len = None
    for linea in lineas:
        if "Frequency" in linea:
            freq_central = float(linea.split(":")[1])
        elif "Sample Rate" in linea:
            sample_rate = float(linea.split(":")[1])
        elif "Vector Length" in linea:
            vector_len = int(linea.split(":")[1])

    datos_txt = []
    for linea in lineas:
        if re.match(r"^[-\d\.\s,]+$", linea):
            valores = re.split(r"[\s,]+", linea.strip())
            numeros = []
            for v in valores:
                try:
                    if v.strip() not in ["", "-", "--"]:
                        numeros.append(float(v))
                except ValueError:
                    continue
            if len(numeros) > 1:
                datos_txt.append(numeros)

    primeros_vectores = [np.array(v) for v in datos_txt[:3] if len(v) == vector_len]

    freqs = np.linspace(freq_central - sample_rate / 2,
                        freq_central + sample_rate / 2,
                        vector_len)

    return freqs, primeros_vectores, freq_central


# ============================================================
# === LISTA DE LOS 19 BARRIDOS ===============================
# ============================================================
barridos = [
    {"txt": "/Users/USUARIO/Downloads/476M.csv"},
    {"txt": "/Users/USUARIO/Downloads/488_5M.csv"},
    {"txt": "/Users/USUARIO/Downloads/501M.csv"},
    {"txt": "/Users/USUARIO/Downloads/513_5M.csv"},
    {"txt": "/Users/USUARIO/Downloads/526M.csv"},
    {"txt": "/Users/USUARIO/Downloads/538_5M.csv"},
    {"txt": "/Users/USUARIO/Downloads/551M.csv"},
    {"txt": "/Users/USUARIO/Downloads/563_5M.csv"},
    {"txt": "/Users/USUARIO/Downloads/576M.csv"},
    {"txt": "/Users/USUARIO/Downloads/588_5M.csv"},
    {"txt": "/Users/USUARIO/Downloads/601M.csv"},
    {"txt": "/Users/USUARIO/Downloads/613_5M.csv"},
    {"txt": "/Users/USUARIO/Downloads/626M.csv"},
    {"txt": "/Users/USUARIO/Downloads/638_5M.csv"},
    {"txt": "/Users/USUARIO/Downloads/651M.csv"},
    {"txt": "/Users/USUARIO/Downloads/663_5M.csv"},
    {"txt": "/Users/USUARIO/Downloads/676M.csv"},
    {"txt": "/Users/USUARIO/Downloads/688_5M.csv"},
    {"txt": "/Users/USUARIO/Downloads/701M.csv"}
]

# ============================================================
# === ACUMULAR LOS TRES GRUPOS DE VECTORES ===================
# ============================================================
freqs_total = []
vectores_1 = []
vectores_2 = []
vectores_3 = []

for b in barridos:
    freqs, primeros_vectores, fc = procesar_barrido(b["txt"])

    if len(primeros_vectores) >= 1:
        vectores_1.append(primeros_vectores[0])
    if len(primeros_vectores) >= 2:
        vectores_2.append(primeros_vectores[1])
    if len(primeros_vectores) >= 3:
        vectores_3.append(primeros_vectores[2])

    freqs_total.append(freqs)

freqs_concat = np.concatenate(freqs_total)
vec1_concat = np.concatenate(vectores_1)
vec2_concat = np.concatenate(vectores_2)
vec3_concat = np.concatenate(vectores_3)

# ============================================================
# === FUNCIÓN PARA GRAFICAR Y GUARDAR =========================
# ============================================================
def graficar_vector(freqs, vector, titulo, color, nombre_archivo):
    fig, ax = plt.subplots(figsize=(16, 7))
    ax.plot(freqs / 1e6, vector, color=color, linewidth=1.5)
    ax.set_title(titulo, fontsize=15, weight='bold')
    ax.set_xlabel("Frecuencia [MHz]", fontsize=12)
    ax.set_ylabel("Magnitud [dBm]", fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.6)

    ymin, ymax = np.min(vector), np.max(vector)
    rango = ymax - ymin
    ax.set_ylim(ymin - rango * 0.5, ymax + rango * 0.5)

    fig.tight_layout()

    # Guardar antes de mostrar
    ruta_guardado = os.path.expanduser(f"~/Downloads/{nombre_archivo}")
    fig.savefig(ruta_guardado, dpi=300, bbox_inches='tight')
    print(f"✅ Imagen guardada en: {ruta_guardado}")

    plt.show()
    plt.close(fig)


# ============================================================
# === GRAFICAR Y GUARDAR CADA VECTOR =========================
# ============================================================
graficar_vector(freqs_concat, vec1_concat, "Vector 1 - Unión total de barridos (GNU Radio)", "orange", "vector1_total.png")
graficar_vector(freqs_concat, vec2_concat, "Vector 2 - Unión total de barridos (GNU Radio)", "green", "vector2_total.png")
graficar_vector(freqs_concat, vec3_concat, "Vector 3 - Unión total de barridos (GNU Radio)", "purple", "vector3_total.png")'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import os

# ============================================================
# === FUNCIÓN PARA CARGAR Y PROCESAR UN BARRIDO ==============
# ============================================================
def procesar_barrido(archivo_txt):
    with open(archivo_txt, 'r', encoding='utf-8', errors='ignore') as f:
        lineas = [l.strip() for l in f if l.strip()]

    freq_central = sample_rate = vector_len = None
    for linea in lineas:
        if "Frequency" in linea:
            freq_central = float(linea.split(":")[1])
        elif "Sample Rate" in linea:
            sample_rate = float(linea.split(":")[1])
        elif "Vector Length" in linea:
            vector_len = int(linea.split(":")[1])

    datos_txt = []
    for linea in lineas:
        if re.match(r"^[-\d\.\s,]+$", linea):
            valores = re.split(r"[\s,]+", linea.strip())
            numeros = []
            for v in valores:
                try:
                    if v.strip() not in ["", "-", "--"]:
                        numeros.append(float(v))
                except ValueError:
                    continue
            if len(numeros) > 1:
                datos_txt.append(numeros)

    primeros_vectores = [np.array(v) for v in datos_txt[:3] if len(v) == vector_len]

    freqs = np.linspace(freq_central - sample_rate / 2,
                        freq_central + sample_rate / 2,
                        vector_len)

    return freqs, primeros_vectores, freq_central


# ============================================================
# === LISTA DE LOS 19 BARRIDOS ===============================
# ============================================================
barridos = [
    {"txt": "/Users/USUARIO/Downloads/476M.csv"},
    {"txt": "/Users/USUARIO/Downloads/488_5M.csv"},
    {"txt": "/Users/USUARIO/Downloads/501M.csv"},
    {"txt": "/Users/USUARIO/Downloads/513_5M.csv"},
    {"txt": "/Users/USUARIO/Downloads/526M.csv"},
    {"txt": "/Users/USUARIO/Downloads/538_5M.csv"},
    {"txt": "/Users/USUARIO/Downloads/551M.csv"},
    {"txt": "/Users/USUARIO/Downloads/563_5M.csv"},
    {"txt": "/Users/USUARIO/Downloads/576M.csv"},
    {"txt": "/Users/USUARIO/Downloads/588_5M.csv"},
    {"txt": "/Users/USUARIO/Downloads/601M.csv"},
    {"txt": "/Users/USUARIO/Downloads/613_5M.csv"},
    {"txt": "/Users/USUARIO/Downloads/626M.csv"},
    {"txt": "/Users/USUARIO/Downloads/638_5M.csv"},
    {"txt": "/Users/USUARIO/Downloads/651M.csv"},
    {"txt": "/Users/USUARIO/Downloads/663_5M.csv"},
    {"txt": "/Users/USUARIO/Downloads/676M.csv"},
    {"txt": "/Users/USUARIO/Downloads/688_5M.csv"},
    {"txt": "/Users/USUARIO/Downloads/701M.csv"}
]

# ============================================================
# === CALCULAR EL PESO TOTAL DE LOS ARCHIVOS =================
# ============================================================
peso_total_bytes = 0
for b in barridos:
    if os.path.exists(b["txt"]):
        peso_total_bytes += os.path.getsize(b["txt"])

peso_total_MB = peso_total_bytes / (1024 * 1024)  # bytes → MB
peso_texto = f"Peso total del barrido: {peso_total_MB:.2f} MB"

# ============================================================
# === ACUMULAR LOS TRES GRUPOS DE VECTORES ===================
# ============================================================
freqs_total = []
vectores_1 = []
vectores_2 = []
vectores_3 = []

for b in barridos:
    freqs, primeros_vectores, fc = procesar_barrido(b["txt"])
    if len(primeros_vectores) >= 1:
        vectores_1.append(primeros_vectores[0])
    if len(primeros_vectores) >= 2:
        vectores_2.append(primeros_vectores[1])
    if len(primeros_vectores) >= 3:
        vectores_3.append(primeros_vectores[2])
    freqs_total.append(freqs)

freqs_concat = np.concatenate(freqs_total)
vec1_concat = np.concatenate(vectores_1)
vec2_concat = np.concatenate(vectores_2)
vec3_concat = np.concatenate(vectores_3)


# ============================================================
# === DETECCIÓN DE CANALES Y GRAFICADO =======================
# ============================================================
def detectar_y_graficar(freqs, magnitud, titulo, color, nombre_archivo, peso_texto):
    # --- Parámetros ---
    ventana_suavizado = 5
    k_sigma = 2.5
    min_ancho_MHz = 5
    tolerancia_puntos = 6
    porcentaje_ruido = 20
    gap_permitido = 6
    ancho_libre_MHz = 6

    # --- Suavizado ---
    magnitud_ext = np.pad(magnitud, (ventana_suavizado//2,), mode='reflect')
    magnitud_suav = np.convolve(magnitud_ext, np.ones(ventana_suavizado)/ventana_suavizado, mode='valid')

    margen = 3
    magnitud_suav[:margen] = magnitud_suav[margen]
    magnitud_suav[-margen:] = magnitud_suav[-margen-1]

    # --- Piso de ruido ---
    n_ruido = int(len(magnitud_suav) * porcentaje_ruido / 100)
    indices_ruido = np.argsort(magnitud_suav)[:n_ruido]
    piso_ruido = np.mean(magnitud_suav[indices_ruido])
    sigma_ruido = np.std(magnitud_suav[indices_ruido])
    umbral = piso_ruido + k_sigma * sigma_ruido

    # --- Detección de canales ocupados ---
    mask_ocupado = magnitud_suav > umbral
    canales_ocupados = []
    inicio = None
    gap_count = 0

    for i in range(len(mask_ocupado)):
        if mask_ocupado[i]:
            if inicio is None:
                inicio = i
            gap_count = 0
        else:
            if inicio is not None:
                gap_count += 1
                if gap_count > gap_permitido:
                    fin = i - gap_count + 1
                    if fin - inicio >= tolerancia_puntos:
                        f_inicio = freqs[inicio]
                        f_fin = freqs[fin - 1]
                        ancho = abs(f_fin - f_inicio)
                        if ancho >= min_ancho_MHz * 1e6:
                            canales_ocupados.append((f_inicio, f_fin))
                    inicio = None
                    gap_count = 0

    if inicio is not None:
        f_inicio = freqs[inicio]
        f_fin = freqs[-1]
        ancho = abs(f_fin - f_inicio)
        if ancho >= min_ancho_MHz * 1e6:
            canales_ocupados.append((f_inicio, f_fin))

    # --- Buscar canal libre más silencioso ---
    canales_libres = []
    f_min, f_max = freqs[0], freqs[-1]
    for (f1, f2) in canales_ocupados:
        canales_libres.append((f_min, f1))
        f_min = f2
    canales_libres.append((f_min, f_max))

    candidatos = []
    for (f1, f2) in canales_libres:
        ancho = (f2 - f1) / 1e6
        if ancho >= ancho_libre_MHz:
            idx = np.where((freqs >= f1) & (freqs <= f2))[0]
            if len(idx) > 0:
                potencia_prom = np.mean(magnitud_suav[idx])
                candidatos.append((f1, f2, potencia_prom))

    canal_libre = None
    f_c_recomendada = None
    if candidatos:
        canal_libre = min(candidatos, key=lambda x: x[2])[:2]
        f1, f2 = canal_libre
        f_c_recomendada = (f1 + f2) / 2

    # --- Gráfica ---
    fig, ax = plt.subplots(figsize=(16, 7))
    ax.plot(freqs / 1e6, magnitud_suav, color=color, linewidth=1.5, label='Magnitud suavizada')
    ax.axhline(piso_ruido, color='gray', linestyle='--', alpha=0.7, label=f'Piso de ruido ({piso_ruido:.1f} dBm)')
    ax.axhline(umbral, color='red', linestyle='--', alpha=0.7, label=f'Umbral ({umbral:.1f} dBm)')
    ax.text(0.98, 0.02, peso_texto, transform=ax.transAxes, fontsize=11,
            verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(facecolor='white', alpha=0.6, edgecolor='gray'))

    for (f_ini, f_fin) in canales_ocupados:
        ax.axvspan(f_ini / 1e6, f_fin / 1e6, color='red', alpha=0.25)

    if canal_libre:
        f1, f2 = canal_libre
        ax.axvspan(f1 / 1e6, f2 / 1e6, color='green', alpha=0.3,
                   label=f"Canal libre recomendado ({f1/1e6:.1f}–{f2/1e6:.1f} MHz)")
        ax.axvline(f_c_recomendada / 1e6, color='blue', linestyle='--',
                   label=f"f_c recomendada = {f_c_recomendada/1e6:.2f} MHz")

    ymin, ymax = np.min(magnitud_suav), np.max(magnitud_suav)
    rango = ymax - ymin
    ax.set_ylim(ymin - rango * 1.2, ymax + rango * 1.2)

    ax.set_title(titulo, fontsize=15, weight='bold')
    ax.set_xlabel("Frecuencia [MHz]", fontsize=12)
    ax.set_ylabel("Magnitud [dBm]", fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()

    fig.tight_layout()
    ruta_guardado = os.path.expanduser(f"~/Downloads/{nombre_archivo}")
    fig.savefig(ruta_guardado, dpi=300, bbox_inches='tight')
    print(f"✅ Imagen guardada en: {ruta_guardado}")

    plt.show()
    plt.close(fig)


# ============================================================
# === GRAFICAR LOS TRES VECTORES =============================
# ============================================================
detectar_y_graficar(freqs_concat, vec1_concat, "Vector 1 - Unión total de barridos (GNU Radio)", "orange", "vector1_total.png", peso_texto)
detectar_y_graficar(freqs_concat, vec2_concat, "Vector 2 - Unión total de barridos (GNU Radio)", "green", "vector2_total.png", peso_texto)
detectar_y_graficar(freqs_concat, vec3_concat, "Vector 3 - Unión total de barridos (GNU Radio)", "purple", "vector3_total.png", peso_texto)
