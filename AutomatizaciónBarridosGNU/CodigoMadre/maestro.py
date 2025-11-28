'''import subprocess
import time
import os

# Lista de tus 19 scripts originales
scripts = [
    "prueba_barrido_476M.py",
    "prueba_barrido_488_5M.py",
    "prueba_barrido_501M.py",
    "prueba_barrido_513_5M.py",
    "prueba_barrido_526M.py",
    "prueba_barrido_538_5M.py",
    "prueba_barrido_551M.py",
    "prueba_barrido_563_5M.py",
    "prueba_barrido_576M.py",
    "prueba_barrido_588_5M.py",
    "prueba_barrido_601M.py",
    "prueba_barrido_613_5M.py",
    "prueba_barrido_626M.py",
    "prueba_barrido_638_5M.py",
    "prueba_barrido_651M.py",
    "prueba_barrido_663_5M.py",
    "prueba_barrido_676M.py",
    "prueba_barrido_688_5M.py",
    "prueba_barrido_701M.py"
]

duracion = 100  # segundos = 1 min 40 s

for s in scripts:
    print(f"Lanzando {s}")
    
    # Ejecuta el script como proceso
    proc = subprocess.Popen(["python", s])

    # Espera la duración del barrido
    time.sleep(duracion)

    # Termina el script
    proc.terminate()
    proc.wait()
    print(f"{s} finalizado, pasando al siguiente\n")

print("Todos los barridos completos!")'''
'''import subprocess
import time
import os

# Lista de tus 19 scripts originales
scripts = [
    "prueba_barrido_476M.py",
    "prueba_barrido_488_5M.py",
    "prueba_barrido_501M.py",
    "prueba_barrido_513_5M.py",
    "prueba_barrido_526M.py",
    "prueba_barrido_538_5M.py",
    "prueba_barrido_551M.py",
    "prueba_barrido_563_5M.py",
    "prueba_barrido_576M.py",
    "prueba_barrido_588_5M.py",
    "prueba_barrido_601M.py",
    "prueba_barrido_613_5M.py",
    "prueba_barrido_626M.py",
    "prueba_barrido_638_5M.py",
    "prueba_barrido_651M.py",
    "prueba_barrido_663_5M.py",
    "prueba_barrido_676M.py",
    "prueba_barrido_688_5M.py",
    "prueba_barrido_701M.py"
]

# Cada barrido necesita 3 vectores de 1024
min_lines = 1024 * 3

# Timeout máximo por barrido en segundos
max_duracion = 200

def contar_lineas_numericas(csv_file):
    """
    Cuenta solo las filas numéricas (ignora encabezados)
    """
    count = 0
    if not os.path.exists(csv_file):
        return 0

    with open(csv_file, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            # Chequear si todos los valores son números
            if all(p.replace(".","",1).replace("e","").replace("-","").isdigit() for p in parts if p):
                count += 1
    return count

# Carpeta donde están los scripts y donde se guardan los CSV
working_dir = os.getcwd()

for s in scripts:
    print(f"Lanzando {s}")
    
    # Ejecuta el script como proceso
    proc = subprocess.Popen(["python", s], cwd=working_dir)

    # Construir el nombre del CSV según la convención que usas en cada script
    csv_file = os.path.join(working_dir, s.split("_")[2].replace("M.py", "M.csv"))

    start_time = time.time()
    while True:
        if os.path.exists(csv_file):
            num_lines = contar_lineas_numericas(csv_file)
            if num_lines >= min_lines:
                print(f"{s}: Se han generado {num_lines} líneas numéricas. Listo para pasar al siguiente.")
                break

        # Timeout
        if time.time() - start_time > max_duracion:
            print(f"{s}: Timeout alcanzado ({max_duracion}s). Pasando al siguiente...")
            break
        
        time.sleep(1)

    # Terminar el script y esperar que cierre
    proc.terminate()
    proc.wait()
    print(f"{s} finalizado, pasando al siguiente\n")

print("Todos los barridos completos!")'''
import subprocess
import time
import os

# Lista de tus 19 scripts originales
scripts = [
    "prueba_barrido_476M.py",
    "prueba_barrido_488_5M.py",
    "prueba_barrido_501M.py",
    "prueba_barrido_513_5M.py",
    "prueba_barrido_526M.py",
    "prueba_barrido_538_5M.py",
    "prueba_barrido_551M.py",
    "prueba_barrido_563_5M.py",
    "prueba_barrido_576M.py",
    "prueba_barrido_588_5M.py",
    "prueba_barrido_601M.py",
    "prueba_barrido_613_5M.py",
    "prueba_barrido_626M.py",
    "prueba_barrido_638_5M.py",
    "prueba_barrido_651M.py",
    "prueba_barrido_663_5M.py",
    "prueba_barrido_676M.py",
    "prueba_barrido_688_5M.py",
    "prueba_barrido_701M.py"
]

# Cada barrido necesita 3 vectores de 1024
min_lines = 1024 * 3

# Timeout máximo por barrido en segundos
max_duracion = 200

def contar_lineas_numericas(csv_file):
    """
    Cuenta solo las filas numéricas (ignora encabezados)
    """
    count = 0
    if not os.path.exists(csv_file):
        return 0

    with open(csv_file, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            # Chequear si todos los valores son números
            if all(p.replace(".", "", 1).replace("e", "").replace("-", "").isdigit() for p in parts if p):
                count += 1
    return count

# Carpeta donde están los scripts y donde se guardan los CSV
working_dir = os.getcwd()

for s in scripts:
    print(f"Lanzando {s}")
    
    # Ejecuta el script como proceso
    proc = subprocess.Popen(["python", s], cwd=working_dir)

    # Construir el nombre del CSV según la convención que usas en cada script
    csv_file = os.path.join(working_dir, s.split("_")[2].replace("M.py", "M.csv"))

    start_time = time.time()
    while True:
        if os.path.exists(csv_file):
            num_lines = contar_lineas_numericas(csv_file)
            if num_lines >= min_lines:
                print(f"{s}: Se han generado {num_lines} líneas numéricas. Listo para pasar al siguiente.")
                break

        # Timeout
        if time.time() - start_time > max_duracion:
            print(f"{s}: Timeout alcanzado ({max_duracion}s). Pasando al siguiente...")
            break
        
        time.sleep(1)

    # Terminar el script y esperar que cierre
    proc.terminate()
    proc.wait()
    print(f"{s} finalizado, pasando al siguiente\n")

print("✅ Todos los barridos completos!")

# ==========================================================
# === EJECUTAR EL SCRIPT DE GRAFICADO AL FINAL AUTOMÁTICAMENTE ===
# ==========================================================
graficar_script = os.path.join(working_dir, "graficar.py")

if os.path.exists(graficar_script):
    print("\n📊 Ejecutando graficar.py...")
    subprocess.run(["python", graficar_script], cwd=working_dir)
    print("✅ graficar.py ejecutado correctamente.")
else:
    print("\n⚠️ No se encontró graficar.py en la carpeta actual.")
