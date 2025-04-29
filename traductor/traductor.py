import openai
import os
import csv
import time
from config import OPENAI_API_KEY, MODELOS, MODO, IDIOMA_DESTINO, TEMPERATURA, MAX_TOKENS, DELAY, PERSONAJES, TRADUCCION_CON_GENERO, FRASES_OMITIBLES
from detector.detector_conversaciones_v2 import agrupar_bloques_conversacion

def limpiar_comillas(texto):
    return texto.strip().strip('"')

def traducir_texto_api(texto_original, genero_hablante=None, genero_receptor=None):
    try:
        modelo = MODELOS.get(MODO, "gpt-3.5-turbo")
        if modelo == "auto":
            modelo = "gpt-3.5-turbo"

        texto_limpio = limpiar_comillas(texto_original)

        contexto = (f"Eres un traductor profesional especializado en narrativa literaria y diálogos emocionales.\n"
                    f"Traduce de forma natural y fluida al {IDIOMA_DESTINO}.\n")

        if TRADUCCION_CON_GENERO and genero_hablante and genero_receptor:
            contexto += (f"El hablante es {genero_hablante}, y se dirige a un {genero_receptor}.\n")

        contexto += f"Texto: {texto_limpio}"

        respuesta = openai.ChatCompletion.create(
            model=modelo,
            messages=[
                {"role": "system", "content": "Eres un traductor experto, creativo y sensible al contexto emocional."},
                {"role": "user", "content": contexto}
            ],
            temperature=TEMPERATURA,
            max_tokens=MAX_TOKENS
        )

        return respuesta['choices'][0]['message']['content'].strip()

    except Exception as e:
        print(f"\U0001f6d1 Error traduciendo: {e}")
        return f"[Error de traducción] {texto_original}"

def traducir_textos(nombre_sin_extension):
    try:
        openai.api_key = OPENAI_API_KEY
        ruta_csv_entrada = f"backup_base/{nombre_sin_extension}_traducir.csv"
        ruta_csv_salida = f"traducciones/{nombre_sin_extension}_traducido.csv"

        if not os.path.exists("traducciones"):
            os.makedirs("traducciones")

        registros = []
        with open(ruta_csv_entrada, "r", encoding="utf-8-sig") as csvfile:
            lector = csv.reader(csvfile)
            next(lector)
            for fila in lector:
                registros.append(fila)

        registros_traducidos = []
        bloques = agrupar_bloques_conversacion(registros)

        if not bloques:
            print("\u26a0\ufe0f No se detectaron bloques. Modo fallback activado (traducción línea por línea).")
            for fila in registros:
                id_linea, texto, personaje, tipo, nota = fila
                if texto.lower().strip() in FRASES_OMITIBLES:
                    texto_traducido = texto
                else:
                    sexo_hablante = PERSONAJES.get(personaje, {}).get("sexo", None)
                    texto_traducido = traducir_texto_api(texto, sexo_hablante, None)

                texto_traducido = f'"{texto_traducido}"'
                registros_traducidos.append([id_linea, texto_traducido, personaje, tipo, nota])
                time.sleep(DELAY)
        else:
            registros_originales = registros.copy()
            indice_global = 0
            for personajes, lineas in bloques:
                for idx, (personaje, tipo, texto) in enumerate(lineas):
                    if texto.lower().strip() in FRASES_OMITIBLES:
                        texto_traducido = texto
                    else:
                        hablante = personaje
                        receptor = lineas[idx + 1][0] if idx + 1 < len(lineas) else None

                        sexo_hablante = PERSONAJES.get(hablante, {}).get("sexo", None)
                        sexo_receptor = PERSONAJES.get(receptor, {}).get("sexo", None) if receptor else None

                        texto_traducido = traducir_texto_api(texto, sexo_hablante, sexo_receptor)

                    texto_traducido = f'"{texto_traducido}"'
                    id_linea = registros_originales[indice_global][0]
                    personaje_original = registros_originales[indice_global][2]
                    tipo_original = registros_originales[indice_global][3]
                    registros_traducidos.append([id_linea, texto_traducido, personaje_original, tipo_original, ""])
                    indice_global += 1
                    time.sleep(DELAY)

        with open(ruta_csv_salida, "w", newline='', encoding="utf-8-sig") as csvfile:
            escritor = csv.writer(csvfile)
            escritor.writerow(["ID", "Texto", "Personaje", "Tipo", "Nota"])
            for registro in registros_traducidos:
                escritor.writerow(registro)

        return nombre_sin_extension, len(registros_traducidos)

    except Exception as e:
        print(f"\U0001f6d1 Error en traducción global: {e}")
        return None, 0
