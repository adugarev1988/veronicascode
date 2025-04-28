# integrador/integrador_estadisticas.py
# Módulo de integración para Veronica's Code Beta 1.1
# Ensambla backup base + traducciones en .rpy final

import os
import csv

def reintegrar_traducciones(nombre_sin_extension):
    try:
        ruta_backup = f"backup_base/{nombre_sin_extension}_base_con_marcas.rpy"
        ruta_csv_traduccion = f"traducciones/{nombre_sin_extension}_traducido.csv"
        ruta_salida = f"traducciones/{nombre_sin_extension}_final.rpy"

        # Confirmar existencia de archivos
        if not os.path.exists(ruta_backup):
            print(f"🛑 Archivo de backup no encontrado: {ruta_backup}")
            return False
        if not os.path.exists(ruta_csv_traduccion):
            print(f"🛑 Archivo de traducciones no encontrado: {ruta_csv_traduccion}")
            return False

        # Cargar traducciones en un diccionario
        traducciones = {}

        with open(ruta_csv_traduccion, "r", encoding="utf-8-sig") as csvfile:
            lector = csv.DictReader(csvfile)
            for fila in lector:
                id_linea = fila["ID"]
                texto_traducido = fila["Texto"]
                traducciones[id_linea] = texto_traducido

        # Leer backup y reemplazar
        lineas_finales = []
        with open(ruta_backup, "r", encoding="utf-8-sig") as f_in:
            for linea in f_in:
                if "(# L" in linea:
                    match = os.path.splitext(linea)[0].split("(# L")[-1].split(")")[0]
                    id_detectado = f"L{match}"
                    if id_detectado in traducciones:
                        linea_modificada = linea.replace(f"(# {id_detectado})", traducciones[id_detectado])
                        lineas_finales.append(linea_modificada)
                    else:
                        lineas_finales.append(linea)
                else:
                    lineas_finales.append(linea)

        # Guardar archivo final .rpy
        with open(ruta_salida, "w", encoding="utf-8-sig") as f_out:
            for linea in lineas_finales:
                f_out.write(linea)

        print(f"\n✅ Archivo final generado: {ruta_salida}")
        return True

    except Exception as e:
        print(f"🛑 Error en reintegrar_traducciones: {e}")
        return False
