import csv
import os
import time
from config import OPENAI_API_KEY, MODELOS, MODO, IDIOMA_DESTINO, TEMPERATURA, MAX_TOKENS, DELAY, PERSONAJES, TRADUCCION_CON_GENERO, FRASES_OMITIBLES
import openai

openai.api_key = OPENAI_API_KEY

modo_actual = MODELOS.get(MODO) or list(MODELOS.values())[0]

from colorama import Fore, Style
from datetime import timedelta
import sys
import re

NOMBRE_CAMUFLAJE = "Zarphotron"

def mostrar_progreso(i, total, inicio):
    progreso = min((i + 1) / total, 1.0)
    if progreso == 0:
        return
    if i % max(1, total // 100) != 0 and i + 1 != total:
        return
    tiempo_transcurrido = time.time() - inicio
    tiempo_estimado_total = tiempo_transcurrido / progreso if progreso > 0 else 0
    tiempo_restante = tiempo_estimado_total - tiempo_transcurrido
    eta_str = str(timedelta(seconds=int(max(0, tiempo_restante))))
    barra = int(progreso * 30) * "█" + int((1 - progreso) * 30) * "─"
    sys.stdout.write(f"\r⏳ {Fore.MAGENTA}[{barra}]{Style.RESET_ALL} {progreso*100:.2f}% ({min(i + 1, total)}/{total}) | ETA: {eta_str}   ")
    sys.stdout.flush()
    if i + 1 == total:
        print()

def obtener_datos_personaje(nombre):
    info = PERSONAJES.get(nombre.lower(), {})
    sexo = info.get("sexo", "indistinto")
    modo = info.get("modo", "").strip()
    return sexo, modo

def restaurar_variables(texto):
    return texto.replace(NOMBRE_CAMUFLAJE, "[name]")

### AQUI SE CONSTRUYE EL PROMPT DE TRADUCCION, SIENTASE LIBRE DE MODIFICARLO PARA OBTENER MEJORES RESULTADOS ###

def construir_prompt(texto, personaje, tipo, interlocutor=""):
    texto = texto.replace("[name]", NOMBRE_CAMUFLAJE).replace("[nombre]", NOMBRE_CAMUFLAJE)
    texto_instruccion = "cuando sea una sola palabra devuelve la traduccion exacta sin mas adornos, cuando se hable de Zarphotron siempre sera masculino y nunca modifiques etiquetas de estilo como {color=#...}."

    sexo, modo = obtener_datos_personaje(personaje)
    sexo_receptor, _ = obtener_datos_personaje(interlocutor)

    if personaje in {"mc", "mct"}:
        texto_instruccion += " Este personaje es el protagonista masculino."

    if tipo == "pensamiento":
        if modo:
            return f"Realiza una traducción natural y literal al {IDIOMA_DESTINO} ajustandote siempre al genero y respetando frases coloquiales el pensamiento de un personaje de género {sexo} con estilo {modo} {texto_instruccion}: '{texto}'"
        else:
            return f"Realiza una traducción natural y literal al {IDIOMA_DESTINO} ajustandote siempre al genero y respetando frases coloquiales el pensamiento de un personaje de género {sexo} {texto_instruccion}: '{texto}'"
    else:
        if modo:
            return f"Realiza una traducción natural y literal al {IDIOMA_DESTINO} ajustandote siempre al genero y respetando frases coloquiales de este frase dicha por un personaje de género {sexo} con estilo {modo} a un personaje de género {sexo_receptor} {texto_instruccion}: '{texto}'"
        else:
            return f"Realiza una traducción natural y literal al {IDIOMA_DESTINO} ajustandote siempre al genero y respetando frases coloquiales de esta frase dicha por un personaje de género {sexo} a un personaje de género {sexo_receptor} {texto_instruccion}: '{texto}'"

def limpiar_traduccion(texto):
    texto = texto.strip()
    if (texto.startswith("'") and texto.endswith("'")) or (texto.startswith('"') and texto.endswith('"')):
        texto = texto[1:-1].strip()
    texto = restaurar_variables(texto)
    return texto

def traducir_bloques(bloques):
    resultados = []
    total_lineas = sum(len(b) for b in bloques)
    progreso_idx = 0
    inicio = time.time()

    for bloque in bloques:
        personajes = [linea[2] for linea in bloque if linea[2]]
        interlocutor = personajes[1] if len(set(personajes)) > 1 else ""

        for id_linea, texto, personaje, tipo, nota in bloque:
            if texto.strip().lower() in FRASES_OMITIBLES:
                resultados.append([id_linea, texto, personaje, tipo, nota])
                progreso_idx += 1
                mostrar_progreso(progreso_idx, total_lineas, inicio)
                continue

            if not OPENAI_API_KEY:
                traduccion = f"[{IDIOMA_DESTINO[:2].upper()}] {texto}"
            else:
                prompt = construir_prompt(texto, personaje, tipo, interlocutor)
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
                    print(f"\n🛑 Error traduciendo línea {id_linea}: {e}")
                    traduccion = texto

            traduccion = limpiar_traduccion(traduccion)
            resultados.append([id_linea, traduccion, personaje, tipo, nota])
            progreso_idx += 1
            mostrar_progreso(progreso_idx, total_lineas, inicio)

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
            prompt = construir_prompt(texto, personaje, tipo)
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
                print(f"\n🛑 Error traduciendo línea {id_linea}: {e}")
                traduccion = texto

        traduccion = limpiar_traduccion(traduccion)
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

    traducidos = []
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

        ids_traducidos = set(t[0] for t in traducidos)
        restantes = [r for r in registros if r[0] not in ids_traducidos]
        if restantes:
            print(f"⚠️ {len(restantes)} líneas quedaron fuera de bloques. Se traducirán individualmente.")
            traducidos_restantes = traducir_individual(restantes)
            traducidos.extend(traducidos_restantes)
    else:
        traducidos = traducir_individual(registros)

    diccionario_traducciones = {fila[0]: fila for fila in traducidos}
    resultado_final = [diccionario_traducciones.get(f[0], f) for f in registros]

    ruta_salida = f"traducciones/{nombre_archivo}_traducido.csv"
    with open(ruta_salida, "w", encoding="utf-8-sig", newline='') as f:
        escritor = csv.writer(f)
        escritor.writerow(["ID", "Texto", "Personaje", "Tipo", "Nota"])
        escritor.writerows(resultado_final)

    return ruta_salida, len(resultado_final)
