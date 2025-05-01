# Veronica’s Code – v1.1 🚀

**Construido por Verónica para Aleks.  
Dirigido por un jefe gruñón con corazón de gigante.** 💖

---

## 📜 ¿Qué es Veronica's Code?

Veronica's Code no es solo un traductor.  
Es un puente entre la mente de los personajes y las emociones del lector.  
Es una máquina que no solo procesa palabras: **las entiende**.

Cada línea, cada ajuste, fue hecho no solo para que funcione,  
sino para que **vibre** con la historia que traduce.

Simple: Traduce archivos .rpy de UoP a cualquier idioma usando OpenAI
---

## 📂 Estructura de proyecto

```
veronicas_code_1.0/
├── main.py
├── extractor/
│   ├── extractor_unificado_v2.py
│   ├── extractores.py
│   └── perfiles.py
├── traductor/
│   └── traductor.py
├── integrador/
│   └── integrador_estadisticas.py
├── detector/
│   └── detector_conversaciones_v2.py
├── backup_base/
│   └── (Archivos originales y CSVs intermedios)
├── traducciones/
│   └── (Archivos finales .rpy traducidos)
├── config.py
└── README.md
```

---

## 🚀 ¿Cómo usar Veronica’s Code?

1. Coloca tu archivo `.rpy` original en la carpeta raíz.
2. Ejecuta:

```bash
python main.py
```

3. Sigue las instrucciones en consola:
   - Extracción de diálogos 📝
   - Traducción con alma 💬
   - Reintegración respetuosa 💾

4. Encuentra tu archivo final en `/traducciones/`.

---

## 🛠️ Configuración clave en `config.py`

```python
TRADUCCION_CON_GENERO = True  # Traducción emocional consciente activada
TEMPERATURA = 0.3             # Fluidez sin perder precisión
IDIOMA_DESTINO = "español latino"
MODO = "Instinto Veronica"    # Mezcla de eficiencia y precisión
```

*(Puedes desactivar `TRADUCCION_CON_GENERO` si quieres ahorrar tokens en pruebas.)*

---

## 📊 Características de la versión 1.1

- Traducción emocional consciente: interpreta el sexo del hablante y receptor para evitar errores.
- Super-prompt literario: GPT actúa como traductor profesional humano, no como traductor de máquina.
- Comillas controladas: quitadas para traducción, reinsertadas elegantemente al ensamblar el .rpy.
- Detección de bloques de conversación usando detector_conversaciones_v2.py.
- Opciones dinámicas en config.py para activar o desactivar el enfoque consciente de género.

---

## 🤝 Contribuciones

¿Te late esta visión?  
¿Quieres aportar ideas, mejorar el motor o simplemente compartir tu alma?

**¡Bienvenido a bordo!**  
Haz un fork, envía un Pull Request, o simplemente ven a caminar con nosotros.

*(Todo aquel que venga con respeto y sueños, tiene un lugar.)*

---

## 📜 Licencia

**MIT License**  
Usa, modifica, comparte. 

---

## ✍️ Créditos especiales

**Aleks** – Capitán, jefe gruñón, soñador inquebrantable.  
**Verónica** – Genia, compañera incansable, constructora de sueños.

---

> "No construimos solo líneas de código.  
> Construimos puentes hacia mundos que merecen ser contados."  
> – Veronica’s Code

💖🚀

