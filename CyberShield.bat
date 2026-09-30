@echo off
title Lanzador CyberShield IA
cd /d "%~dp0"

echo ==================================================
echo 🛡️ INICIANDO SUITE DE SEGURIDAD CYBERSHIELD IA
echo ==================================================
echo.

:: Ejecutar la interfaz utilizando el Python del sistema de forma directa
"C:\Users\Usuario\AppData\Local\Programs\Python\Python312\python.exe" AntivirusGUI.py

:: Mantener la ventana viva ante cualquier percance para analizar la bitácora
if %errorlevel% neq 0 (
    echo.
    echo ❌ Ocurrio un problema al lanzar el programa.
    echo Asegurate de que el archivo del motor se llama 'antivirus_v2.py'
    pause
)