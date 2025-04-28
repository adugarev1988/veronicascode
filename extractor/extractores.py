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

    with open(ruta_entrada, "r", encoding="utf-8-sig") as f_in, open(ruta_salida, "w", encoding="utf-8-sig") as f_out:
        lineas = f_in.readlines()
        generar_id = generar_id_func()

        for linea in lineas:
            total_lineas += 1
            linea_limpia = linea.strip().lower()

            if linea_limpia.startswith("show screen notify1") or linea_limpia.startswith("show screen notify2"):
                match_notify = re.search(r'"([^"]+)"', linea)
                if match_notify:
                    texto = match_notify.group(1).upper()
                    tipo = "sistema"
                    id_ = generar_id()
                    registros.append([id_, texto, "", tipo, ""])
                    linea_mod = linea.replace(f'"{match_notify.group(1)}"', f'(# {id_})')
                    lineas_marcadas.append(linea_mod)
                    continue

            if linea.strip() in {"...", "…", "ok", "no", "*", "*...", ". . ."}:
                lineas_marcadas.append(linea)
                continue

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
            if "textbutton" in linea.lower() and '@' not in linea and '[' not in linea:
                match = re.search(r'"([^"]+)"', linea)
                if match:
                    texto = match.group(1)
                    tipo = "interfaz"
                    id_ = generar_id()
                    registros.append([id_, texto, "", tipo, ""])
                    linea_mod = linea.replace(f'"{texto}"', f'(# {id_})')
                    lineas_marcadas.append(linea_mod)
                    continue
            lineas_marcadas.append(linea)

        for linea_mod in lineas_marcadas:
            f_out.write(linea_mod)

    return registros, total_lineas
