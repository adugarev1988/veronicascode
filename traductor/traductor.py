import csv
import os
import time
from config import OPENAI_API_KEY, MODELOS, MODO, IDIOMA_DESTINO, TEMPERATURA, MAX_TOKENS, DELAY, PERSONAJES, TRADUCCION_CON_GENERO, FRASES_OMITIBLES
import openai

openai.api_key = OPENAI_API_KEY

modo_actual = MODELOS.get(MODO) or list(MODELOS.values())[0]

from colorama import Fore, Style
from datetime import timedelta

def mostrar_progreso(i, total, inicio):
    progreso = (i + 1) / total
    tiempo_transcurrido = time.time() - inicio
    tiempo_estimado_total = tiempo_transcurrido / progreso
    tiempo_restante = tiempo_estimado_total - tiempo_transcurrido
    eta_str = str(timedelta(seconds=int(tiempo_restante)))
    print(f"⏳ Traduciendo: {Fore.MAGENTA}{progreso*100:.2f}%{Style.RESET_ALL} ({i + 1}/{total}) | ETA: {eta_str}")

def traducir_bloques(bloques):
    resultados = []
    inicio = time.time()
    for idx, bloque in enumerate(bloques):
        id_bloque = bloque[0][0] if bloque else ""
        mensajes = []
        for id_linea, texto, personaje, tipo, nota in bloque:
            if personaje:
                genero = PERSONAJES.get(personaje.lower(), "indistinto")
                if tipo == "pensamiento":
                    prompt = f"Traduce al {IDIOMA_DESTINO} el pensamiento de un personaje de género {genero}: '{texto}'"
                else:
                    prompt = f"Traduce al {IDIOMA_DESTINO} esta frase hablada por un personaje de género {genero}: '{texto}'"
            else:
                prompt = f"Traduce al {IDIOMA_DESTINO}: '{texto}'"
            mensajes.append({"role": "user", "content": prompt})

        if not OPENAI_API_KEY:
            traducciones = [f"[{IDIOMA_DESTINO[:2].upper()}] {linea[1]}" for linea in bloque]
        else:
            try:
                respuesta = openai.ChatCompletion.create(
                    model=modo_actual,
                    messages=mensajes,
                    temperature=TEMPERATURA,
                    max_tokens=MAX_TOKENS,
                )
                traducciones = [r["message"]["content"].strip() for r in respuesta["choices"]]
                time.sleep(DELAY)
            except Exception as e:
                print(f"🛑 Error traduciendo bloque {id_bloque}: {e}")
                traducciones = [linea[1] for linea in bloque]

        for i, linea in enumerate(bloque):
            if len(linea) == 5:
                resultados.append([linea[0], traducciones[i], linea[2], linea[3], linea[4]])
            else:
                print(f"⚠️ Línea con formato inválido: {linea}")

        mostrar_progreso(idx, len(bloques), inicio)

    return resultados

def traducir_individual(registros):
    resultados = []
    inicio = time.time()
    for idx, (id_linea, texto, personaje, tipo, nota) in enumerate(registros):
        if texto.strip().lower() in FRASES_OMITIBLES:
            resultados.append([id_linea, texto, personaje, tipo, nota])
            continue

        if not OPENAI_API_KEY:
            traduccion = f"[{IDIOMA_DESTINO[:2].upper()}] {texto}"
        else:
            if personaje:
                genero = PERSONAJES.get(personaje.lower(), "indistinto")
                if tipo == "pensamiento":
                    prompt = f"Traduce al {IDIOMA_DESTINO} el pensamiento de un personaje de género {genero}: '{texto}'"
                else:
                    prompt = f"Traduce al {IDIOMA_DESTINO} esta frase hablada por un personaje de género {genero}: '{texto}'"
            else:
                prompt = f"Traduce al {IDIOMA_DESTINO}: '{texto}'"

            try:
                respuesta = openai.ChatCompletion.create(
                    model=modo_actual,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=TEMPERATURA,
                    max_tokens=MAX_TOKENS,
                )
                traduccion = respuesta["choices"][0]["message"]["content"].strip()
                time.sleep(DELAY)
            except Exception as e:
                print(f"🛑 Error traduciendo línea {id_linea}: {e}")
                traduccion = texto

        resultados.append([id_linea, traduccion, personaje, tipo, nota])
        mostrar_progreso(idx, len(registros), inicio)

    return resultados

def traducir_textos(nombre_archivo):
    ruta_csv = f"backup_base/{nombre_archivo}_traducir.csv"
    registros = []
    with open(ruta_csv, "r", encoding="utf-8-sig") as f:
        lector = csv.reader(f)
        next(lector)
        for fila in lector:
            if len(fila) == 5:
                registros.append(fila)
            else:
                print(f"⚠️ Fila ignorada (formato inválido): {fila}")

    if TRADUCCION_CON_GENERO:
        bloques = []
        bloque_actual = []
        for reg in registros:
            if reg[1].strip().lower() in FRASES_OMITIBLES:
                continue
            if bloque_actual and reg[2] != bloque_actual[-1][2]:
                bloques.append(bloque_actual)
                bloque_actual = []
            bloque_actual.append(reg)
        if bloque_actual:
            bloques.append(bloque_actual)
        traducidos = traducir_bloques(bloques)
    else:
        traducidos = traducir_individual(registros)

    ruta_salida = f"traducciones/{nombre_archivo}_traducido.csv"
    with open(ruta_salida, "w", encoding="utf-8-sig", newline='') as f:
        escritor = csv.writer(f)
        escritor.writerow(["ID", "Texto", "Personaje", "Tipo", "Nota"])
        escritor.writerows(traducidos)

    return ruta_salida, len(traducidos)
