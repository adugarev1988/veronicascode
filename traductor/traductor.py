# traductor/traductor.py
# Módulo real de traducción usando OpenAI para Veronica's Code 1.0

import os
import time
import csv
import openai
from config import (
    OPENAI_API_KEY, 
    IDIOMA_DESTINO, 
    DELAY, 
    MODO, 
    MODELOS, 
    TEMPERATURA, 
    MAX_TOKENS, 
    FRASES_OMITIBLES
)

# Configurar API Key
openai.api_key = OPENAI_API_KEY

# Función auxiliar para decidir el modelo a usar
def elegir_modelo():
    modelo = MODELOS.get(MODO, "gpt-3.5-turbo")
    if modelo == "auto":
        # Lógica automática: si el texto es corto, usa 3.5; si es largo o delicado, usa 4
        return "gpt-3.5-turbo"
    return modelo

# Función principal de traducción de un solo texto
def traducir_texto(texto_original):
    if texto_original.strip().lower() in FRASES_OMITIBLES:
        return texto_original  # No traducimos frases omitibles

    prompt = (
        f"Traduce el siguiente texto al {IDIOMA_DESTINO} de forma natural, "
        f"manteniendo el sentido original. Evita traducciones literales si no suenan naturales.\n\n"
        f"Texto: {texto_original}"
    )

    modelo_seleccionado = elegir_modelo()

    try:
        respuesta = openai.ChatCompletion.create(
            model=modelo_seleccionado,
            messages=[{"role": "user", "content": prompt}],
            temperature=TEMPERATURA,
            max_tokens=MAX_TOKENS
        )
        traduccion = respuesta["choices"][0]["message"]["content"].strip()
        time.sleep(DELAY)  # Evitar golpear demasiado rápido la API
        return traduccion
    except Exception as e:
        print(f"🛑 Error durante la traducción: {e}")
        return texto_original  # En caso de error, devolvemos el original para no romper el flujo

# Función para traducir todos los textos de un archivo CSV
def traducir_textos(nombre_sin_extension):
    try:
        ruta_csv_entrada = f"backup_base/{nombre_sin_extension}_traducir.csv"
        ruta_csv_salida = f"traducciones/{nombre_sin_extension}_traducido.csv"

        # Crear carpeta de traducciones si no existe
        if not os.path.exists("traducciones"):
            os.makedirs("traducciones")

        registros = []

        # Leer CSV de entrada
        with open(ruta_csv_entrada, "r", encoding="utf-8-sig") as csvfile:
            lector = csv.reader(csvfile)
            next(lector)  # Saltar encabezado
            for fila in lector:
                registros.append(fila)

        registros_traducidos = []

        for registro in registros:
            id_linea, texto, personaje, tipo, nota = registro
            texto_traducido = traducir_texto(texto)
            registros_traducidos.append([id_linea, texto_traducido, personaje, tipo, nota])

        # Guardar CSV traducido
        with open(ruta_csv_salida, "w", newline='', encoding="utf-8-sig") as csvfile:
            escritor = csv.writer(csvfile)
            escritor.writerow(["ID", "Texto", "Personaje", "Tipo", "Nota"])
            for registro in registros_traducidos:
                escritor.writerow(registro)

        return nombre_sin_extension, len(registros_traducidos)

    except Exception as e:
        print(f"🛑 Error en traductor.py: {e}")
        return None, 0
