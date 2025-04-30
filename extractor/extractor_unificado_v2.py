# extractor/extractor_unificado_v2.py
# Módulo de extracción inteligente para Veronica's Code v1.1

import os
import csv
from extractor import extractores
from extractor.perfiles import PERFILES

def extraer_textos(nombre_archivo):
    try:
        nombre_sin_extension = nombre_archivo.replace(".rpy", "")
        ruta_entrada = os.path.join(nombre_archivo)
        ruta_backup = os.path.join("backup_base", f"{nombre_sin_extension}_base_con_marcas.rpy")
        ruta_csv = os.path.join("backup_base", f"{nombre_sin_extension}_traducir.csv")

        if not os.path.exists("backup_base"):
            os.makedirs("backup_base")

        perfil_detectado = None
        for perfil, datos in PERFILES.items():
            if nombre_archivo in datos["archivos"]:
                perfil_detectado = datos
                break

        if perfil_detectado:
            nombre_extractor = perfil_detectado["extractor"]
            descripcion = perfil_detectado["descripcion"]
            extractor_func = getattr(extractores, nombre_extractor)
            print(f"🔹 Perfil detectado: {descripcion}")
            print(f"🔹 Usando extractor: {nombre_extractor}")
        else:
            print("⚠️ No se encontró perfil específico. Se usará extractor_lineas_historia por defecto.")
            extractor_func = extractores.extractor_lineas_historia

        lineas_extraidas, total_lineas = extractor_func(ruta_entrada, ruta_backup)

        # Guardar CSV
        with open(ruta_csv, "w", newline='', encoding="utf-8-sig") as csvfile:
            escritor = csv.writer(csvfile)
            escritor.writerow(["ID", "Texto", "Personaje", "Tipo", "Nota"])
            for registro in lineas_extraidas:
                escritor.writerow(registro)

        print("\n📊 Reporte de extracción:")
        print(f"🔹 Total líneas leídas: {total_lineas}")
        print(f"🔹 Dialogos extraídos: {len(lineas_extraidas)}")
        eficiencia = (len(lineas_extraidas) / total_lineas) * 100 if total_lineas > 0 else 0
        print(f"🔹 Porcentaje de dialogos: {eficiencia:.2f}%")

        return nombre_sin_extension, len(lineas_extraidas)

    except Exception as e:
        print(f"🛑 Error en extractor_unificado_v2: {e}")
        return None, 0
