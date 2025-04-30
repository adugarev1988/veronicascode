import os
import csv
import re

CARPETA_BASE = "backup_base"
CARPETA_TRADUCIDA = "traducciones"

def reintegrar_traducciones(nombre_archivo):
    base_path = os.path.join(CARPETA_BASE, f"{nombre_archivo}_base_con_marcas.rpy")
    traducido_path = os.path.join(CARPETA_TRADUCIDA, f"{nombre_archivo}_traducido.csv")
    traducir_path = os.path.join(CARPETA_BASE, f"{nombre_archivo}_traducir.csv")
    salida_path = os.path.join(CARPETA_TRADUCIDA, f"{nombre_archivo}_traducido_es.rpy")

    if not os.path.exists(base_path):
        print(f"🛑 Archivo base no encontrado: {base_path}")
        return False
    if not os.path.exists(traducido_path):
        print(f"🛑 Archivo traducido no encontrado: {traducido_path}")
        return False
    if not os.path.exists(traducir_path):
        print(f"🛑 Archivo original de traducción no encontrado: {traducir_path}")
        return False

    with open(traducido_path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        traducciones = {row["ID"]: row["Texto"] for row in reader}

    with open(traducir_path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        originales = {row["ID"]: row["Texto"] for row in reader}

    faltantes = set(originales.keys()) - set(traducciones.keys())
    if faltantes:
        print(f"⚠️ {len(faltantes)} líneas no fueron traducidas, se usará el texto original.")

    with open(base_path, encoding="utf-8-sig") as f:
        lineas = f.readlines()

    salida = []
    for linea in lineas:
        match = re.search(r'\(#\s*(L\d{4})\)', linea)
        if match:
            id_ = match.group(1)
            texto = traducciones.get(id_, originales.get(id_, ""))
            if texto.strip():
                linea_nueva = re.sub(r'\(#\s*' + re.escape(id_) + r'\)', f'"{texto}"', linea)
            else:
                print(f"⚠️ Línea {id_} tiene texto vacío. Se usará texto original.")
                texto_original = originales.get(id_, f"[{id_}]")
                linea_nueva = re.sub(r'\(#\s*' + re.escape(id_) + r'\)', f'"{texto_original}"', linea)
            salida.append(linea_nueva)
        else:
            salida.append(linea)

    os.makedirs(CARPETA_TRADUCIDA, exist_ok=True)
    with open(salida_path, "w", encoding="utf-8-sig") as f:
        for linea in salida:
            f.write(linea)

    print(f"✅ Archivo final generado: {salida_path}")
    return True
