# detector_conversaciones_v2.py
# Módulo autónomo para detectar bloques de conversación (versión refinada)
# Veronica's Code 2.0 - Respeto de saltos de tiempo, pensamientos, sistema.

import os
import csv

def agrupar_bloques_conversacion(registros):
    """
    Agrupa líneas de diálogo, pensamiento y sistema en bloques de conversación.
    Rompe bloque al encontrar líneas de tipo 'otro' o tipos no contemplados.
    """
    bloques = []
    bloque_actual = []
    personajes_en_bloque = set()

    for registro in registros:
        id_linea, texto, personaje, tipo, nota = registro

        if tipo in {"dialogo", "pensamiento", "sistema"}:
            if personaje:
                personajes_en_bloque.add(personaje)
            bloque_actual.append((personaje, tipo, texto))
        else:
            # Tipo 'otro' o inesperado: rompe el bloque
            if bloque_actual:
                bloques.append((list(personajes_en_bloque), list(bloque_actual)))
                bloque_actual = []
                personajes_en_bloque = set()

    # Finalizar si queda algo
    if bloque_actual:
        bloques.append((list(personajes_en_bloque), list(bloque_actual)))

    return bloques

def cargar_registros(nombre_archivo):
    """
    Carga registros de un archivo CSV generado por la extracción.
    Espera la ruta en 'backup_base/{nombre_archivo}_traducir.csv'
    """
    ruta_csv = f"backup_base/{nombre_archivo}_traducir.csv"

    if not os.path.exists(ruta_csv):
        print(f"🛑 No encontrado: {ruta_csv}")
        return []

    registros = []
    with open(ruta_csv, "r", encoding="utf-8-sig") as csvfile:
        lector = csv.reader(csvfile)
        next(lector)  # Saltar encabezado
        for fila in lector:
            registros.append(fila)

    return registros

def mostrar_bloques(bloques):
    """
    Muestra por consola los bloques detectados
    """
    for idx, (personajes, lineas) in enumerate(bloques, 1):
        print("\n" + "=" * 40)
        print(f"===== BLOQUE {idx} =====")
        print(f"Participantes: {', '.join(personajes)}")
        print("-" * 40)
        for personaje, tipo, texto in lineas:
            if tipo == "pensamiento":
                print(f"({personaje} piensa) {texto}")
            elif tipo == "sistema":
                print(f"(SISTEMA) {texto}")
            else:
                print(f"[{personaje}] {texto}")

def main():
    print("\n🚀 Detector de Conversaciones v2 - Veronica's Code 🚀\n")
    archivo = input("🔹 Ingresa el nombre base del archivo (sin _traducir.csv): ")

    registros = cargar_registros(archivo)
    if not registros:
        print("⚠️ No hay registros para procesar.")
        return

    bloques = agrupar_bloques_conversacion(registros)
    mostrar_bloques(bloques)

if __name__ == "__main__":
    main()
