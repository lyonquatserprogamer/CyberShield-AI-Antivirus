import os
import platform
import shutil
import re
from pathlib import Path

SISTEMA = platform.system()
if SISTEMA == "Windows":
    DIR_CUARENTENA = Path(r"C:\AntivirusIA_Cuarentena")
else:
    DIR_CUARENTENA = Path.home() / "AntivirusIA_Cuarentena"

BITACORA_PATH = DIR_CUARENTENA / "registro_cuarentena.txt"

def restaurar_todo():
    print("🔓 INICIANDO PROCESO DE RESTAURACIÓN ROBUSTO...")
    print("=" * 90)

    if not BITACORA_PATH.exists():
        print("ℹ️ El archivo de registro no existe o la cuarentena está vacía.")
        return

    with open(BITACORA_PATH, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    if not lineas:
        print("ℹ️ No hay registros de archivos para restaurar en la bitácora.")
        return

    lineas_no_restauradas = []

    for linea in lineas:
        if not linea.strip():
            continue
            
        try:
            # Nueva Expresión Regular: Captura absolutamente todo entre "Ruta original: " y " | Probabilidad:"
            match_nombre = re.search(r"AISLADO:\s*([^|]+?)\s*\|", linea)
            match_ruta = re.search(r"Ruta original:\s*(.+?)\s*\|", linea)

            if not match_nombre or not match_ruta:
                lineas_no_restauradas.append(linea)
                continue

            nombre_original_limpio = match_nombre.group(1).strip()
            ruta_original_completa = Path(match_ruta.group(1).strip())

            # Buscar el archivo modificado adentro de la carpeta de cuarentena
            archivo_encontrado_en_cuarentena = None
            for archivo_bloqueado in DIR_CUARENTENA.glob("*.peligro"):
                if nombre_original_limpio in archivo_bloqueado.name:
                    archivo_encontrado_en_cuarentena = archivo_bloqueado
                    break

            if archivo_encontrado_en_cuarentena and archivo_encontrado_en_cuarentena.exists():
                # Crear la carpeta de origen con soporte completo para espacios
                ruta_original_completa.parent.mkdir(parents=True, exist_ok=True)

                # Mover de vuelta el archivo físico
                shutil.move(str(archivo_encontrado_en_cuarentena), str(ruta_original_completa))
                print(f"✅ RESTAURADO CON ÉXITO: {nombre_original_limpio}")
            else:
                print(f"⚠️ No se encontró el archivo físico en cuarentena para: {nombre_original_limpio}")
                lineas_no_restauradas.append(linea)

        except Exception as e:
            print(f"❌ Error al intentar restaurar una línea: {e}")
            lineas_no_restauradas.append(linea)

    # Reescritura limpia de la bitácora
    with open(BITACORA_PATH, "w", encoding="utf-8") as f:
        f.writelines(lineas_no_restauradas)

    print("=" * 90)
    print("🏁 Proceso de restauración finalizado.")

if __name__ == "__main__":
    restaurar_todo()