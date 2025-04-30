# config.py
# Configuración general para Veronica's Code v1.1

# 🔑 Clave API de OpenAI
OPENAI_API_KEY = "OPEN-AI-API"

# 🌎 Idioma destino de la traducción
IDIOMA_DESTINO = "español latino"  
# Ejemplos de variaciones posibles:
# - "español latino"
# - "español de Argentina"
# - "español de España"
# - "inglés americano"
# - "inglés británico"
# - "francés"
# - "alemán"
# - "japonés"
# - "italiano"

# 💤 Retraso entre llamadas a la API (en segundos)
DELAY = 1.2

# 🎯 Modo de traducción (elige uno):
# - "Token Saver"       (gpt-3.5-turbo, barato y rápido)
# - "Precision Blade"   (gpt-4-turbo, más costoso pero más preciso)
# - "Instinto Veronica" (modo automático, el sistema elige)
MODO = "Token Saver"

# 🧠 Asociación de modo con modelo
MODELOS = {
    "Token Saver": "gpt-3.5-turbo",
    "Precision Blade": "gpt-4-turbo",
    "Instinto Veronica": "auto"
}

# 🎛️ Configuraciones avanzadas

# 🧠 Traducción consciente del sexo del personaje que habla y al que responde
TRADUCCION_CON_GENERO = True
# Si True: el prompt aclarará el sexo de hablante y receptor para mejorar precisión emocional.
# Si False: prompt normal sin información de género adicional (ahorra tokens).

# 🔥 Temperatura (creatividad de la traducción)
TEMPERATURA = 0.3
#  - 0.0 = Traducción ultra literal, casi sin creatividad
#  - 0.3 = Traducción precisa, pero permitiendo ligeros ajustes para sonar natural
#  - 0.7 = Traducción más creativa, capaz de parafrasear o ajustar el tono
#  - 1.0 = Traducción muy creativa, puede cambiar notablemente la redacción
#
# Ejemplo para frase en inglés "I have no idea what you're talking about":
#  - Temperatura 0.0 ➔ "No tengo idea de qué estás hablando."
#  - Temperatura 0.3 ➔ "No sé de qué hablas exactamente."
#  - Temperatura 0.7 ➔ "No tengo ni la menor pista de lo que dices."
#  - Temperatura 1.0 ➔ "¿De qué diablos estás hablando? No tengo ni idea."

# 🧮 Máximo de tokens en la respuesta
MAX_TOKENS = 1500
# (Esto limita la longitud máxima de cada respuesta que da el modelo. No suele ser necesario tocarlo.)

# 🎭 Estilos de personajes
PERSONAJES = {
    "ro": {
        "sexo": "femenino",
        "modo": "Malhablada, lujuriosa, pervertida"
    },
    "rot": { 
        "sexo": "femenino", 
        "modo": "" 
    },
    "mc": {
        "sexo": "masculino",
        "modo": "Juvenil, directo, curioso"
    },
    "mct": {
        "sexo": "masculino",
        "modo": "Introspectivo, inseguro, reflexivo"
    },
    "r": {
        "sexo": "femenino",
        "modo": "Tímida pero intensa"
    },
    "rt": { 
        "sexo": "femenino", 
        "modo": "" 
    },
    "nm": {
        "sexo": "femenino",
        "modo": "Formal, maternal, estricta"
    },
    "guy": {
        "sexo": "masculino",
        "modo" :""
    },
    "cm": { 
        "sexo": "masculino", 
        "modo": "" 
    },
    "crowd": { 
        "sexo": "indistinto",
        "modo": "" 
    },
    "un": { 
        "sexo": "indistinto", 
        "modo": "" 
    },
    "un2": { 
        "sexo": "indistinto", 
        "modo": "" 
    },
    "un3": { 
        "sexo": "indistinto", 
        "modo": "" 
    },
    "un4": { 
        "sexo": "indistinto", 
        "modo": "" 
    },
    "girls": { 
        "sexo": "femenino", 
        "modo": "" 
    },
    "girl": { 
        "sexo": "femenino", 
        "modo": "" 
    },
    "tv": { 
        "sexo": "indistinto", 
        "modo": "" 
    },
    "tel": { 
        "sexo": "indistinto", 
        "modo": "" 
    },
    "cinema": { 
        "sexo": "indistinto", 
        "modo": "" 
    },
    "erin": { 
        "sexo": "femenino", 
        "modo": "" 
    },
    "ingrid": { 
        "sexo": "femenino", 
        "modo": "" 
    },
    "travis": { 
        "sexo": "masculino", 
        "modo": "" 
    },
    "taylor": { 
        "sexo": "masculino", 
        "modo": "" 
    },
    "kiely": { 
        "sexo": "femenino", 
        "modo": "" 
    },
    "waitress": { 
        "sexo": "femenino", 
        "modo": "" 
    },
    "commentator1": { 
        "sexo": "indistinto", 
        "modo": "" 
    },
    "commentator2": { 
        "sexo": "indistinto", 
        "modo": "" 
    },
    "c": { 
        "sexo": "femenino", 
        "modo": ""
    },
    "ct": { 
        "sexo": "femenino", 
        "modo": "" 
    },
    "s": { 
        "sexo": "femenino", 
        "modo": "" 
    },
    "st": { 
        "sexo": "femenino", 
        "modo": "" 
    },
    "a": { 
        "sexo": "femenino", 
        "modo": "" 
    },
    "asht": { 
        "sexo": "femenino", 
        "modo": "" 
    },
    "nm": { 
        "sexo": "femenino", 
        "modo": "" 
    },
    "n": { 
        "sexo": "femenino", 
        "modo": "" 
    },
    "nt": { 
        "sexo": "femenino", 
        "modo": "" 
    },
    "mr": { 
        "sexo": "femenino", 
        "modo": "" 
    },
    "y": { 
        "sexo": "femenino", 
        "modo": "" 
    },
    "yt": { 
        "sexo": "femenino", 
        "modo": "" 
    },
    "e": { 
        "sexo": "masculino", 
        "modo": "" 
    },
    "ab": { 
        "sexo": "femenino", 
        "modo": "" 
    },
    "d": { 
        "sexo": "masculino", 
        "modo": "" 
    },
    "w": { 
        "sexo": "masculino", 
        "modo": "" 
    },
    "j": { 
        "sexo": "masculino", 
        "modo": "" 
    },
    "mom": { 
        "sexo": "femenino", 
        "modo": "" 
    },
    "landeck": { 
        "sexo": "masculino", 
        "modo": "" 
    },
    "msmerritt": { 
        "sexo": "femenino", 
        "modo": "" 
    },
    "niko": { 
        "sexo": "masculino", 
        "modo": "" 
    },
    "gwen": { 
        "sexo": "femenino", 
        "modo": "" 
    },
    "alyssa": { 
        "sexo": "femenino", 
        "modo": "" 
    },
    "m": { 
        "sexo": "masculino", 
        "modo": "" 
    },
    "ma": { 
        "sexo": "masculino", 
        "modo": "" 
    },
    "v": { 
        "sexo": "masculino", 
        "modo": "" 
    },
    "ja": { 
        "sexo": "masculino", 
        "modo": "" 
    },
    "f": { 
        "sexo": "masculino", 
        "modo": "" 
    },
    "maxi": { 
        "sexo": "masculino", 
        "modo": "" 
    },
    "nik": { 
        "sexo": "femenino", 
        "modo": "" 
    },
    "nikt": { 
        "sexo": "femenino", 
        "modo": ""
    },
    "mic": { 
        "sexo": "masculino", 
        "modo": "" 
    },
    "lexi": { 
        "sexo": "femenino", 
        "modo": "" 
    },
    "zac": { 
        "sexo": "masculino", 
        "modo": "" 
    },
    "sa": { 
        "sexo": "femenino", 
        "modo": "" 
    },
    "k": { 
        "sexo": "femenino", 
        "modo": "" 
    },
    "emma": { 
        "sexo": "femenino", 
        "modo": "" 
    },
    "med": { 
        "sexo": "femenino", 
        "modo": "" 
    },
    "solberg": { 
        "sexo": "femenino", 
        "modo": "" 
    },
    "cou": { 
        "sexo": "femenino", 
        "modo": "Hermana mayor, responsable, despreocupada" 
    },
    "mary": { 
        "sexo": "femenino", 
        "modo": "" 
    },
    "mall": { 
        "sexo": "femenino", 
        "modo": "" 
    },
    "ivy": { 
        "sexo": "femenino", 
        "modo": "" 
    },
    "lau": { 
        "sexo": "femenino", 
        "modo": "" 
    },
    "peggy": { 
        "sexo": "femenino", 
        "modo": "" 
    },
    "jackie": { 
        "sexo": "femenino", 
        "modo": "" 
    },
    "cleo": { 
        "sexo": "femenino", 
        "modo": "" 
    }
}

# ❌ Frases que deben omitirse de la traducción
FRASES_OMITIBLES = {"ok", "no", "mmm", "pfff", "humm", "hmm", "...", "…", "*", "*...", ". . ."}
