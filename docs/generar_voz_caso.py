"""Narración del caso STOM con voz masculina chilena (la misma de los videos de los caniles).

    C:\\Python314\\python.exe docs\\generar_voz_caso.py

Lee los guiones de docs/voces-caso-stom.json (uno por bloque de la página, en orden) y deja
casos/stom/audio/caso-NN.mp3. Voz es-CL-LorenzoNeural con edge-tts, -8 % de velocidad y -4 Hz
de tono; después ffmpeg los pasa a mono 32 kbps: es voz, no música, y así pesan poco.
Si cambia el número de bloques de la página, actualizar PISTAS en casos/stom/index.html.
"""
import asyncio
import json
import os
import shutil
import subprocess

import edge_tts

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUIONES = os.path.join(RAIZ, "docs", "voces-caso-stom.json")
SALIDA = os.path.join(RAIZ, "casos", "stom", "audio")
VOZ, VELOCIDAD, TONO = "es-CL-LorenzoNeural", "-8%", "-4Hz"


async def generar():
    textos = json.load(open(GUIONES, encoding="utf-8"))
    ffmpeg = shutil.which("ffmpeg")
    total = 0
    for i, texto in enumerate(textos):
        crudo = os.path.join(SALIDA, f"_crudo-{i:02d}.mp3")
        final = os.path.join(SALIDA, f"caso-{i:02d}.mp3")
        await edge_tts.Communicate(texto, VOZ, rate=VELOCIDAD, pitch=TONO).save(crudo)
        subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-i", crudo, "-ac", "1", "-ar", "22050",
                        "-b:a", "32k", final], check=True)
        os.remove(crudo)
        total += os.path.getsize(final)
        print(f"  caso-{i:02d}.mp3  {os.path.getsize(final) / 1024:.1f} KB")
    print(f"total: {total / 1024 / 1024:.2f} MB en {len(textos)} pistas")


asyncio.run(generar())
