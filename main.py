# main.py
# Lanzador principal de Veronica's Code -  v1.1
# Versión mejorada, lista para extracción con perfiles

from extractor.extractor_unificado_v2 import extraer_textos
from traductor.traductor import traducir_textos
from integrador.integrador_estadisticas import reintegrar_traducciones
import os

def main():
    print("\n🚀 Bienvenido a Veronica's Code - Beta 1.1 🚀")
    
    archivo = input("🔹 Ingresa el nombre del archivo .rpy para procesar: ")

    # Paso 1: Extracción
    print("\n🔍 Extrayendo diálogos...")
    archivo_extraido, lineas_extraidas = extraer_textos(archivo)
    if not archivo_extraido:
        print("🛑 No se pudo extraer. Revisa el archivo e intenta de nuevo.")
        return

    # Paso 2: Traducción
    print("\n🌎 Traduciendo líneas extraídas...")
    archivo_traducido, lineas_traducidas = traducir_textos(archivo_extraido)
    if not archivo_traducido:
        print("🛑 No se pudo traducir. Revisa errores posibles.")
        return
    
    # Paso 3: Reintegración
    print("\n💾 Reintegrando traducciones...")
    nombre_sin_extension = os.path.splitext(archivo)[0]
    exito = reintegrar_traducciones(nombre_sin_extension)
    if exito:
        print("\n✅ Proceso completado con éxito.")
    else:
        print("\n⚠️ Hubo problemas en la integración. Revisa los archivos generados.")

if __name__ == "__main__":
    main()
