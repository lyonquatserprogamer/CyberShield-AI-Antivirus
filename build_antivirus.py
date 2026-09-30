import os
import sys
import subprocess

print("==================================================")
print("🛡️ INICIANDO COMPILACIÓN INTERNA DE CYBERSHIELD IA")
print("==================================================")

# Configurar los argumentos del comando para inyectar el modelo .pkl
argumentos = [
    sys.executable, "-m", "PyInstaller",
    "--noconsole",
    "--onefile",
    "--add-data", "antivirus_ia_modelo.pkl;.",
    "AntivirusGUI.py"
]

print(f"🚀 Ejecutando comando de empaquetado nativo...")
# Ejecutar la compilación forzando el uso del intérprete local de Python
resultado = subprocess.run(argumentos, shell=True)

if resultado.returncode == 0:
    print("\n🎯 ¡COMPILACIÓN COMPLETADA CON ÉXITO PERFECTO!")
    print("Busca en tu directorio la nueva carpeta llamada 'dist'.")
    print("Ahí adentro encontrarás tu archivo independiente 'AntivirusGUI.exe'.")
else:
    print("\n❌ Error en el empaquetado. Verifica las dependencias de la consola.")
print("==================================================")
