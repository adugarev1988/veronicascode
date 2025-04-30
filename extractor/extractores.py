# extractor/extractores.py
# Motor final de extracción Veronica's Code Beta 1.1
# Adaptado a (ruta_entrada, ruta_salida) correctamente

import re

def generar_id_func():
    contador = [1]
    def siguiente():
        id_ = f"L{contador[0]:04d}"
        contador[0] += 1
        return id_
    return siguiente

def extractor_lineas_historia(ruta_entrada, ruta_salida):
    registros = []
    lineas_marcadas = []
    total_lineas = 0

    OMITIR_COMPLETAMENTE = [
        ".webp", ".ogg", ".png", ".jpg", ".mp3", ".mp4", ".rpy"
    ]

    with open(ruta_entrada, "r", encoding="utf-8-sig") as f_in, open(ruta_salida, "w", encoding="utf-8-sig") as f_out:
        lineas = f_in.readlines()
        generar_id = generar_id_func()

        for linea in lineas:
            total_lineas += 1
            linea_limpia = linea.strip().lower()

            if any(p in linea_limpia for p in OMITIR_COMPLETAMENTE):
                lineas_marcadas.append(linea)
                continue

            # INPUT RENPY
            if "$" in linea and "renpy.input" in linea and '"' in linea:
                match_input = re.search(r'"([^"]+)"', linea)
                if match_input:
                    texto = match_input.group(1).strip()
                    tipo = "input"
                    id_ = generar_id()
                    registros.append([id_, texto, "", tipo, ""])
                    linea_mod = linea.replace(f'"{texto}"', f'(# {id_})')
                    lineas_marcadas.append(linea_mod)
                    continue

            # NOTIFY SCREEN
            if "show screen notify" in linea_limpia and '"' in linea:
                match_notify = re.search(r'"([^"]+)"', linea)
                if match_notify:
                    texto = match_notify.group(1).strip()
                    tipo = "sistema"
                    id_ = generar_id()
                    registros.append([id_, texto, "", tipo, ""])
                    linea_mod = linea.replace(f'"{texto}"', f'(# {id_})')
                    lineas_marcadas.append(linea_mod)
                    continue

            if linea.strip() in {"...", "…", "ok", "no", "*", "*...", ". . ."}:
                lineas_marcadas.append(linea)
                continue

            # MENU CONDICIONAL
            if re.match(r'^\s*"[^"]+"\s+if\s+', linea):
                match_menu = re.search(r'"([^"]+)"', linea)
                if match_menu:
                    texto = match_menu.group(1)
                    tipo = "menu_condicional"
                    id_ = generar_id()
                    registros.append([id_, texto, "", tipo, ""])
                    linea_mod = linea.replace(f'"{texto}"', f'(# {id_})')
                    lineas_marcadas.append(linea_mod)
                    continue

            # MENU SIMPLE
            if re.match(r'^\s*"[^"]+":\s*$', linea):
                match_menu_simple = re.search(r'"([^"]+)"', linea)
                if match_menu_simple:
                    texto = match_menu_simple.group(1)
                    tipo = "menu_opcion"
                    id_ = generar_id()
                    registros.append([id_, texto, "", tipo, ""])
                    linea_mod = linea.replace(f'"{texto}"', f'(# {id_})')
                    lineas_marcadas.append(linea_mod)
                    continue

            # DIALOGO CON PERSONAJE
            if '"' in linea:
                match = re.match(r'^\s*(\w+)\s+"([^"]+)"', linea)
                if match:
                    personaje, texto = match.group(1), match.group(2)
                    post = linea.split(f'"{texto}"')[-1].strip()
                    if post:
                        lineas_marcadas.append(linea)
                        continue
                    tipo = "pensamiento" if personaje.endswith("t") else "dialogo"
                    id_ = generar_id()
                    registros.append([id_, texto, personaje, tipo, ""])
                    linea_mod = linea.replace(f'"{texto}"', f'(# {id_})')
                    lineas_marcadas.append(linea_mod)
                    continue

            # TEXTO SUELTO ENTRE COMILLAS
                match_cita = re.search(r'"([^"]+)"', linea)
                if match_cita:
                    texto = match_cita.group(1)
                    post = linea.split(f'"{texto}"')[-1].strip()
                    if post or texto.strip() in {"...", "…", "ok", "no", "*", "*...", ". . ."}:
                        lineas_marcadas.append(linea)
                        continue
                    tipo = "otro"
                    id_ = generar_id()
                    registros.append([id_, texto, "", tipo, ""])
                    linea_mod = linea.replace(f'"{texto}"', f'(# {id_})')
                    lineas_marcadas.append(linea_mod)
                    continue

            lineas_marcadas.append(linea)

        for linea_mod in lineas_marcadas:
            f_out.write(linea_mod)

    return registros, total_lineas

def extractor_lineas_chat(ruta_entrada, ruta_salida):
    registros = []
    lineas_marcadas = []
    total_lineas = 0

    with open(ruta_entrada, "r", encoding="utf-8-sig") as f_in, open(ruta_salida, "w", encoding="utf-8-sig") as f_out:
        lineas = f_in.readlines()
        generar_id = generar_id_func()

        for linea in lineas:
            total_lineas += 1

            # Textbutton con contenido
            if "textbutton" in linea.lower():
                match = re.search(r'"([^"]+)"', linea)
                if match:
                    texto = match.group(1).strip()
                    if texto.startswith("@") and len(texto.split()) == 1:
                        lineas_marcadas.append(linea)
                        continue
                    if texto.startswith("[") and texto.endswith("]"):
                        lineas_marcadas.append(linea)
                        continue
                    tipo = "interfaz"
                    id_ = generar_id()
                    registros.append([id_, texto, "", tipo, ""])
                    linea_mod = linea.replace(f'"{texto}"', f'(# {id_})')
                    lineas_marcadas.append(linea_mod)
                    continue

            # Show('notify', message='...') dentro de una acción
            if "show(" in linea.lower() and "notify" in linea.lower() and "message=" in linea.lower():
                match_notify = re.search(r'message\s*=\s*[\'"]([^\'"]+)[\'"]', linea)
                if match_notify:
                    texto = match_notify.group(1).strip()
                    tipo = "sistema"
                    id_ = generar_id()
                    registros.append([id_, texto, "", tipo, ""])
                    linea_mod = linea.replace(match_notify.group(0), f'message=(# {id_})')
                    lineas_marcadas.append(linea_mod)
                    continue

            lineas_marcadas.append(linea)

        for linea_mod in lineas_marcadas:
            f_out.write(linea_mod)

    return registros, total_lineas
