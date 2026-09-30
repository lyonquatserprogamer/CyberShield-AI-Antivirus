import os
import platform
import subprocess
import sys
from pathlib import Path

SISTEMA = platform.system()

def programar_escaneo(frecuencia, dia_seleccionado=None):
    """
    Configura el escaneo según la opción seleccionada.
    frecuencia: "Semanal" o "Mensual"
    dia_seleccionado: Solo se usa si es Semanal (ej: "Lunes", "Martes", etc.)
    """
    ruta_base = Path(__file__).parent.absolute()
    nombre_tarea = "CyberShieldIA_AutoScan"
    
    # Diccionario para mapear los días de la interfaz al formato schtasks de Windows
    dias_win = {
        "Lunes": "MON", "Martes": "TUE", "Miércoles": "WED", 
        "Jueves": "THU", "Viernes": "FRI", "Sábado": "SAT", "Domingo": "SUN"
    }
    
    # Diccionario para mapear los días al formato cron de Linux (1=Lunes, 7=Domingo)
    dias_linux = {
        "Lunes": "1", "Martes": "2", "Miércoles": "3", 
        "Jueves": "4", "Viernes": "5", "Sábado": "6", "Domingo": "7"
    }

    if SISTEMA == "Windows":
        ruta_lanzador = ruta_base / "CyberShield.bat"
        
        if frecuencia == "Semanal":
            dia_win = dias_win.get(dia_seleccionado, "FRI")
            comando = f'schtasks /create /tn "{nombre_tarea}" /tr "{ruta_lanzador}" /sc WEEKLY /d {dia_win} /st 18:00 /f'
            msg_exito = f"📅 Escaneo programado: Cada semana los días {dia_seleccionado} a las 18:00."
        else: # Mensual (Se ejecuta el día 1 de cada mes)
            comando = f'schtasks /create /tn "{nombre_tarea}" /tr "{ruta_lanzador}" /sc MONTHLY /d 1 /st 18:00 /f'
            msg_exito = "📅 Escaneo programado: El día 1 de cada mes a las 18:00."
            
        try:
            resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
            if resultado.returncode == 0:
                return f"✅ {msg_exito}"
            else:
                return f"❌ Error de permisos o argumentos de Windows. ({resultado.stderr.strip()})"
        except Exception as e:
            return f"❌ Error al crear la tarea: {e}"
            
    else: # Linux / macOS (Cron)
        ruta_script = ruta_base / "AntivirusGUI.py"
        
        if frecuencia == "Semanal":
            dia_cron = dias_linux.get(dia_seleccionado, "5")
            comando_cron = f"0 18 * * {dia_cron} export DISPLAY=:0 && {sys.executable} {ruta_script}\n"
            msg_exito = f"📅 Escaneo programado en Linux: Todos los {dia_seleccionado} a las 18:00."
        else: # Mensual (Minuto 0, Hora 18, Día 1 del mes)
            comando_cron = f"0 18 1 * * export DISPLAY=:0 && {sys.executable} {ruta_script}\n"
            msg_exito = "📅 Escaneo programado en Linux: El día 1 de cada mes a las 18:00."
        
        try:
            actual = subprocess.run("crontab -l", shell=True, capture_output=True, text=True)
            lineas_actuales = actual.stdout if actual.returncode == 0 else ""
            
            # Limpiar entradas anteriores de CyberShield para no acumular basura
            lineas_filtradas = ""
            for linea in lineas_actuales.splitlines():
                if str(ruta_script) not in linea:
                    lineas_filtradas += linea + "\n"
                    
            nuevas_lineas = lineas_filtradas + comando_cron
            
            proceso = subprocess.Popen("crontab -", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = proceso.communicate(input=nuevas_lineas)
            
            if proceso.returncode == 0:
                return f"✅ {msg_exito}"
            else:
                return f"❌ Error al guardar en Cron: {stderr.strip()}"
        except Exception as e:
            return f"❌ Error al interactuar con Cron: {e}"
