import os
import time
from datetime import datetime
from roboflow import Roboflow

# --- Configuración ---
API_KEY = ""
WORKSPACE = ""
PROJECT_NAME = ""  # 👈 nuevo proyecto con modelo ent>
FOLDER_PATH = ""
LOG_FILE = "/root/roboflow_resultados.log"
INTERVALO_SEGUNDOS = 30  # esperar entre escaneos

def cargar_log():
    if not os.path.exists(LOG_FILE):
        return set()
    with open(LOG_FILE, "r") as log:
        return set(line.split(" | ")[1].strip() for line in log if " | " in line)

def main():
    print("Conectando con Roboflow...")
    rf = Roboflow(api_key=API_KEY)

    print("Cargando workspace y proyecto...")
    project = rf.workspace(WORKSPACE).project(PROJECT_NAME)

    print("Usando versión 1 del proyecto...")
    model = project.version(1).model  # 👈 usa la versión 1 del proyecto entrenado

    archivos_analizados = cargar_log()

    print("Esperando nuevas imágenes...")

    while True:
        nuevos = False
        for root, _, files in os.walk(FOLDER_PATH):
            for name in files:
                if not name.lower().endswith(".jpg"):
                    continue
                path = os.path.join(root, name)
                if path in archivos_analizados:
                    continue

                print(f"📷 Analizando {path}...")
                try:
                    prediction = model.predict(path).json()
                    timestamp = datetime.now().isoformat()
                    with open(LOG_FILE, "a") as log:
                        log.write(f"{timestamp} | {path} | {prediction}\n")
                    print(f"✅ Resultado: {prediction}")
                    archivos_analizados.add(path)
                    nuevos = True
                except Exception as e:
                    print(f"❌ Error en {path}: {e}")

        if not nuevos:
            print(f"⏳ Nada nuevo, esperando {INTERVALO_SEGUNDOS} segundos...")
        time.sleep(INTERVALO_SEGUNDOS)

if __name__ == "__main__":
    main()
