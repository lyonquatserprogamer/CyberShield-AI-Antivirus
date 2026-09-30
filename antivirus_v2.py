import os
import platform
import datetime
import math
import shutil
import joblib
import pandas as pd
from pathlib import Path

SISTEMA = platform.system()

if SISTEMA == "Windows":
    DIR_CUARENTENA = Path(r"C:\AntivirusIA_Cuarentena")
else:
    DIR_CUARENTENA = Path.home() / "AntivirusIA_Cuarentena"

DIR_CUARENTENA.mkdir(parents=True, exist_ok=True)

# 📋 LISTA BLANCA DE PALABRAS CLAVE EN RUTAS (Filtro por aproximación de texto)
LISTA_BLANCA_RUTAS = [
    "amd", "intel", "nvidia", "radeon", "geforce", "realtek", "logitech", "corsair", "razer", "asus", "msi", "gigabyte",
    "chrome", "chromium", "firefox", "opera", "brave", "edge", "safari", "webkit", "electron", "vulkan", "directx",
    "ubisoft", "steam", "epic games", "origin", "riot games", "blizzard", "gog", "unity", "unreal engine", "godot", 
    "blender", "xboxgames", "xbox game pass", "xbox app", "xbox console companion", "playstation app", "epic games launcher", 
    "gog galaxy", "battle.net", "origin client", "ubisoft connect", "riot client", "discord", "discord app", "slack", 
    "zoom", "teams", "skype", "telegram", "whatsapp", "signal", "line", "wechat", "viber", "kakaotalk", "microsoft", 
    "office", "onedrive", "dropbox", "google drive", "twitch", "youtube", "netflix", "spotify", "apple music", "amazon music", 
    "soundcloud", "bandcamp", "deezer", "tidal", "pandora", "shazam", "audible", "kindle", "calibre", "goodreads", 
    "overdrive", "libby", "scribd", "hoopla", "kanopy", "plex", "jellyfin", "emby", "subsonic", "navidrome", "ampache", 
    "madsonic", "airsonic", "moode audio", "volumio", "pi musicbox", "raspberry pi os", "ubuntu studio", "kubuntu studio", 
    "linux mint", "elementary os", "pop os", "zorin os", "manjaro", "arch linux", "fedora", "centos", "debian", 
    "opensuse", "gentoo", "slackware", "void linux", "alpine linux", "kali linux", "parrot os", "tails", "whonix", 
    "qubes os", "tailscale", "zerotier", "openvpn", "wireguard", "protonvpn", "nordvpn", "expressvpn", "surfshark", 
    "cyberghost", "private internet access", "ipvanish", "hotspot shield", "hide my ass", "purevpn", "vpn unlimited", 
    "windscribe", "tunnelbear", "betternet", "speedify", "vpnhub", "vpn master", "vpn proxy master", "vpn shield", 
    "vpn secure", "vpn express", "vpn super unlimited proxy", "vpn free unlimited proxy", "vpn unlimited free proxy", 
    "vpn master free proxy", "vpn proxy master free proxy", "vpn shield free proxy", "vpn secure free proxy", 
    "vpn express free proxy", "vpn super unlimited proxy free proxy", "vpn free unlimited proxy free proxy",
    # Bloqueo total para el entorno de desarrollo y evitar colapsos
    ".vscode", "extensions", "roslyn", "debugger", "assembly", "metadata"
]

# 🚫 CARPETAS QUE SE SALTAN DIRECTAMENTE EN EL OS DE FORMA OPERATIVA
CARPETAS_EXCLUIDAS = [
    "system32", "syswow64", "winsxs", "boot", "recovery", "servicing", 
    "microsoft shared", "softwaredistribution", "$recycle.bin", "system volume information", "assembly"
]

PALABRAS_CLAVE_INSTALADORES = ["setup", "install", "installer", "stable", "update", "patch", "upgrade"]

MODELO_PATH = "antivirus_ia_modelo.pkl"
modelo_ia = joblib.load(MODELO_PATH) if os.path.exists(MODELO_PATH) else None

def calcular_entropia(ruta_archivo):
    try:
        if not ruta_archivo.is_file() or ruta_archivo.stat().st_size == 0:
            return 0
        with open(ruta_archivo, 'rb') as f:
            datos = f.read(1024 * 1024)
        if not datos:
            return 0
        frecuencias = [0] * 256
        for byte in datos:
            frecuencias[byte] += 1
        entropia = 0
        for f in frecuencias:
            if f > 0:
                p = f / len(datos)
                entropia -= p * math.log2(p)
        return round(entropia, 2)
    except:
        return 0

def enviar_a_cuarentena(ruta_archivo, probabilidad):
    try:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_seguro = f"SUSPECT_{timestamp}_{ruta_archivo.name}.peligro"
        ruta_destino = DIR_CUARENTENA / nombre_seguro
        shutil.move(str(ruta_archivo), str(ruta_destino))
        with open(DIR_CUARENTENA / "registro_cuarentena.txt", "a", encoding="utf-8") as log:
            log.write(f"[{datetime.datetime.now()}] AISLADO: {ruta_archivo.name} | Ruta original: {ruta_archivo} | Probabilidad: {probabilidad:.2f}%\n")
    except:
        pass

def obtener_unidades_sistema():
    unidades = []
    if SISTEMA == "Windows":
        for letra in range(65, 91):
            ruta_unidad = f"{chr(letra)}:\\"
            if os.path.exists(ruta_unidad):
                unidades.append(Path(ruta_unidad))
    else:
        unidades.append(Path("/"))
    return unidades

def escanear_sistema_completo(consola_gui=None):
    if modelo_ia is None:
        if consola_gui: consola_gui.insert("end", "❌ Error: No se encontró el archivo .pkl del modelo.\n")
        return

    unidades = obtener_unidades_sistema()
    msg_unidades = f"💾 Discos detectados para escaneo automático: {[str(u) for u in unidades]}\n"
    
    if consola_gui:
        consola_gui.insert("end", msg_unidades)
        consola_gui.see("end")

    hoy = datetime.datetime.now()
    global conteo_amenazas, conteo_analizados
    conteo_amenazas = 0
    conteo_analizados = 0
    extensiones_criticas = ('.exe', '.dll', '.bat', '.vbs', '.sh', '.py', '.bin', '.elf', '.scr')

    for unidad in unidades:
        msg_inicio = f"\n🔍 Analizando la unidad: {unidad}\n" + "="*70 + "\n"
        if consola_gui: consola_gui.insert("end", msg_inicio); consola_gui.see("end")
        
        for raiz, carpetas, archivos in os.walk(unidad):
            # Filtrado de carpetas básicas
            carpetas[:] = [c for c in carpetas if c.lower() not in CARPETAS_EXCLUIDAS and "antivirusia_cuarentena" not in c.lower()]
            
            for archivo in archivos:
                if not archivo.lower().endswith(extensiones_criticas):
                    continue
                
                ruta_completa = Path(raiz) / archivo
                nombre_lower = archivo.lower()
                ruta_str_lower = str(ruta_completa).lower()
                
                # 🔥 COMPROBACIÓN ROBUSTA DE LISTA BLANCA MULTI-CAPA:
                # Si cualquier palabra clave de la lista (incluyendo .vscode, roslyn, etc.) 
                # está contenida dentro de la ruta del archivo, la IA lo ignora instantáneamente.
                if any(marca in ruta_str_lower for marca in LISTA_BLANCA_RUTAS):
                    continue  

                if any(keyword in nombre_lower for keyword in PALABRAS_CLAVE_INSTALADORES):
                    if "temp" in ruta_str_lower or "downloads" in ruta_str_lower or "appdata" in ruta_str_lower:
                        continue 

                conteo_analizados += 1
                if consola_gui and conteo_analizados % 100 == 0:
                    consola_gui.insert("end", f"⏳ Analizados {conteo_analizados} archivos...\n")
                    consola_gui.see("end")

                try:
                    estadisticas = ruta_completa.stat()
                    tamano = estadisticas.st_size
                    fecha_mod = datetime.datetime.fromtimestamp(estadisticas.st_mtime)
                    antiguedad = (hoy - fecha_mod).days
                    longitud_nombre = len(archivo)
                    entropia = calcular_entropia(ruta_completa)

                    datos_archivo = pd.DataFrame([[longitud_nombre, tamano, antiguedad, entropia]], 
                                                 columns=["longitud_nombre", "tamano_bytes", "antiguedad_dias", "entropia"])
                    
                    prediccion = modelo_ia.predict(datos_archivo)
                    probabilidades = modelo_ia.predict_proba(datos_archivo)
                    probabilidad_malware = probabilidades[0][1] * 100

                    if prediccion == 1 and probabilidad_malware >= 80:
                        conteo_amenazas += 1
                        txt_alerta = f"❌ AMENAZA: {archivo} ({probabilidad_malware:.1f}% Malware)\n   ↳ Ubicación: {ruta_completa.parent}\n"
                        if consola_gui:
                            consola_gui.insert("end", txt_alerta)
                            consola_gui.see("end")
                        enviar_a_cuarentena(ruta_completa, probabilidad_malware)

                except:
                    continue

    mensaje_fin = "\n" + "="*70 + f"\n🏁 ESCANEO COMPLETADO.\n📊 Ejecutables revisados: {conteo_analizados}\n🔒 Amenazas enviadas a cuarentena: {conteo_amenazas}\n"
    if consola_gui:
        consola_gui.insert("end", mensaje_fin)
        consola_gui.see("end")
