import os
import platform
import threading
import customtkinter as ctk
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Configuración estética global del Antivirus
ctk.set_appearance_mode("Dark") # Forzamos el modo oscuro Cyberpunk por defecto
ctk.set_default_color_theme("blue")

class AntivirusIAApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurar la ventana principal (Más estilizada y moderna)
        self.title("🛡️ CyberShield IA - NextGen Security")
        self.geometry("920x550")
        self.resizable(False, False)

        # Estado del hilo
        self.escaneo_activo = False

        # Contadores globales para alimentar el gráfico de la IA
        self.archivos_seguros = 0
        self.archivos_malware = 0

        # Detectar la carpeta de cuarentena según el sistema operativo
        self.sistema = platform.system()
        if self.sistema == "Windows":
            self.dir_cuarentena = Path(r"C:\AntivirusIA_Cuarentena")
        else:
            self.dir_cuarentena = Path.home() / "AntivirusIA_Cuarentena"

        # --- DISEÑO DE LA INTERFAZ MATRIX (GRID 2x2) ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 1. Panel Lateral Estilizado (Menú de Navegación Premium)
        self.menu_lateral = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="#111116")
        self.menu_lateral.grid(row=0, column=0, sticky="nsew")
        self.menu_lateral.grid_rowconfigure(5, weight=1)
        
        # Logo del Antivirus con tipografía imponente
        self.logo_label = ctk.CTkLabel(self.menu_lateral, text="🛡️ CYBERSHIELD AI", font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 40))

        # Botones de navegación con curvas y colores personalizados
        self.btn_nav_escaneo = ctk.CTkButton(self.menu_lateral, text="🔍  ESCÁNER", font=ctk.CTkFont(size=13, weight="bold"), height=40, corner_radius=10, fg_color="#1E1E24", hover_color="#2D2F36", command=self.mostrar_panel_escaneo)
        self.btn_nav_escaneo.grid(row=1, column=0, padx=15, pady=10, sticky="ew")

        self.btn_nav_cuarentena = ctk.CTkButton(self.menu_lateral, text="🔒  CUARENTENA", font=ctk.CTkFont(size=13, weight="bold"), height=40, corner_radius=10, fg_color="#1E1E24", hover_color="#2D2F36", command=self.mostrar_panel_cuarentena)
        self.btn_nav_cuarentena.grid(row=2, column=0, padx=15, pady=10, sticky="ew")

        self.btn_nav_stats = ctk.CTkButton(self.menu_lateral, text="📊  ESTADÍSTICAS", font=ctk.CTkFont(size=13, weight="bold"), height=40, corner_radius=10, fg_color="#1E1E24", hover_color="#2D2F36", command=self.mostrar_panel_estadisticas)
        self.btn_nav_stats.grid(row=3, column=0, padx=15, pady=10, sticky="ew")

        # Telemetría de OS en la parte inferior del menú
        self.info_os = ctk.CTkLabel(self.menu_lateral, text=f"PROTECCIÓN ACTIVA: {self.sistema.upper()}", text_color="#A3A3A3", font=ctk.CTkFont(size=11, weight="bold"))
        self.info_os.grid(row=5, column=0, padx=20, pady=20, sticky="s")

        # 2. Contenedor Principal Dinámico (Derecha)
        self.contenedor_principal = ctk.CTkFrame(self, corner_radius=15, fg_color="transparent")
        self.contenedor_principal.grid(row=0, column=1, padx=25, pady=25, sticky="nsew")
        self.contenedor_principal.grid_columnconfigure(0, weight=1)
        self.contenedor_principal.grid_rowconfigure(0, weight=1)

        self.mostrar_panel_escaneo()

    def limpiar_contenedor(self):
        if self.escaneo_activo:
            return False
        for widget in self.contenedor_principal.winfo_children():
            widget.destroy()
        return True

    # --- PANEL 1: ESCANER EMBELLECIDO ---
    def mostrar_panel_escaneo(self):
        if self.escaneo_activo and len(self.contenedor_principal.winfo_children()) > 0:
            return
            
        self.limpiar_contenedor()
        frame = ctk.CTkFrame(self.contenedor_principal, fg_color="transparent")
        frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        frame.grid_rowconfigure(2, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        titulo = ctk.CTkLabel(frame, text="Análisis Heurístico Avanzado por IA", font=ctk.CTkFont(family="Helvetica", size=22, weight="bold"))
        titulo.grid(row=0, column=0, pady=(0, 5), sticky="w")

        # Botón de Escaneo con degradado/color Turquesa Ciberseguridad
        self.btn_iniciar_scan = ctk.CTkButton(frame, text="Comenzar Escaneo Autónomo del Sistema", font=ctk.CTkFont(size=14, weight="bold"), height=45, corner_radius=12, fg_color="#00B4D8", hover_color="#0077B6", command=self.ejecutar_escaneo_hilo)
        self.btn_iniciar_scan.grid(row=1, column=0, pady=15, sticky="ew")

        # Consola de telemetría pulida con tipografía estilo código y bordes limpios
        self.consola_scan = ctk.CTkTextbox(frame, font=ctk.CTkFont(family="Consolas", size=12), corner_radius=12, border_width=1, border_color="#2D2F36", fg_color="#0F0F12")
        self.consola_scan.grid(row=2, column=0, pady=5, sticky="nsew")
        
        if self.escaneo_activo:
            self.btn_iniciar_scan.configure(state="disabled", text="ESCANEANDO AMENAZAS...", fg_color="#FFB703")
            self.consola_scan.insert("0.0", "[⚠️] El análisis heurístico sigue ejecutándose en segundo plano...\n")
        else:
            self.consola_scan.insert("0.0", "[🛡️] Núcleo de Inteligencia Artificial listo.\n[⚡] Presiona el botón superior para mapear tus discos locales y externos automáticamente...\n")

    def ejecutar_escaneo_hilo(self):
        if self.escaneo_activo:
            return
        self.escaneo_activo = True
        self.btn_iniciar_scan.configure(state="disabled", text="ESCANEANDO AMENAZAS...", fg_color="#FFB703")
        
        self.btn_nav_cuarentena.configure(state="disabled")
        self.btn_nav_stats.configure(state="disabled")
        
        threading.Thread(target=self.hilo_escaneo, daemon=True).start()

    def hilo_escaneo(self):
        import antivirus_v2
        
        class ConsolaSegura:
            def __init__(self, app_instancia):
                self.app = app_instancia
            def insert(self, index, text):
                try:
                    if hasattr(self.app, 'consola_scan') and self.app.consola_scan.winfo_exists():
                        self.app.consola_scan.insert(index, text)
                except:
                    pass
            def see(self, index):
                try:
                    if hasattr(self.app, 'consola_scan') and self.app.consola_scan.winfo_exists():
                        self.app.consola_scan.see(index)
                except:
                    pass

        consola_protegida = ConsolaSegura(self)
        consola_protegida.insert("end", "[🤖] Mapeando unidades físicas y lógicas...\n")

        try:
            antivirus_v2.escanear_sistema_completo(consola_gui=consola_protegida)
            self.archivos_seguros = getattr(antivirus_v2, 'conteo_analizados', 0)
            self.archivos_malware = getattr(antivirus_v2, 'conteo_amenazas', 0)
        except Exception as e:
            consola_protegida.insert("end", f"\n[❌] Error crítico en el motor: {e}\n")

        self.escaneo_activo = False
        try:
            if self.btn_iniciar_scan.winfo_exists():
                self.btn_iniciar_scan.configure(state="normal", text="Comenzar Escaneo Autónomo del Sistema", fg_color="#00B4D8")
            self.btn_nav_cuarentena.configure(state="normal")
            self.btn_nav_stats.configure(state="normal")
        except:
            pass

    # --- PANEL 2: CUARENTENA PREMIUM ---
    def mostrar_panel_cuarentena(self):
        if not self.limpiar_contenedor(): return
        
        frame = ctk.CTkFrame(self.contenedor_principal, fg_color="transparent")
        frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        titulo = ctk.CTkLabel(frame, text="Bóveda de Cuarentena Segura", font=ctk.CTkFont(family="Helvetica", size=22, weight="bold"))
        titulo.grid(row=0, column=0, pady=(0, 10), sticky="w")

        self.lista_cuarentena = ctk.CTkTextbox(frame, font=ctk.CTkFont(family="Consolas", size=12), corner_radius=12, border_width=1, border_color="#2D2F36", fg_color="#0F0F12")
        self.lista_cuarentena.grid(row=1, column=0, pady=5, sticky="nsew")
        
        bitacora = self.dir_cuarentena / "registro_cuarentena.txt"
        if bitacora.exists():
            with open(bitacora, "r", encoding="utf-8") as f:
                contenido = f.read()
            self.lista_cuarentena.insert("0.0", contenido if contenido.strip() else "🔒 La bóveda está vacía. Sistema protegido.")
        else:
            self.lista_cuarentena.insert("0.0", "🔒 La bóveda está vacía. Sistema protegido.")

        panel_botones = ctk.CTkFrame(frame, fg_color="transparent")
        panel_botones.grid(row=2, column=0, pady=(15, 0), sticky="w")

        btn_restaurar = ctk.CTkButton(panel_botones, text="🔓 Restaurar Todo", font=ctk.CTkFont(size=12, weight="bold"), width=150, height=38, corner_radius=8, fg_color="#E9C46A", text_color="black", hover_color="#F4A261", command=self.ejecutar_restauracion)
        btn_restaurar.grid(row=0, column=0, padx=5)

        btn_vaciar = ctk.CTkButton(panel_botones, text="🗑️ Vaciar Bóveda Permanente", font=ctk.CTkFont(size=12, weight="bold"), width=200, height=38, corner_radius=8, fg_color="#E76F51", hover_color="#D62828", command=self.vaciar_cuarentena_físico)
        btn_vaciar.grid(row=0, column=1, padx=5)

    def ejecutar_restauracion(self):
        import QuarantRestore as restaurar_cuarentena
        restaurar_cuarentena.restaurar_todo()
        self.mostrar_panel_cuarentena()

    def vaciar_cuarentena_físico(self):
        try:
            for archivo in self.dir_cuarentena.glob("*.peligro"):
                archivo.unlink()
                bitacora = self.dir_cuarentena / "registro_cuarentena.txt"
                if bitacora.exists():
                    bitacora.unlink()
                    self.archivos_malware = 0
                    self.mostrar_panel_cuarentena()
        except Exception as e:
            print(f"Error al vaciar boveda: {e}")
    # --- PANEL 3: ESTADÍSTICAS COMPACTAS ---
    def mostrar_panel_estadisticas(self):
        if not self.limpiar_contenedor(): return
        
        frame = ctk.CTkFrame(self.contenedor_principal, fg_color="transparent")
        frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        frame.grid_columnconfigure(0, weight=1)

        titulo = ctk.CTkLabel(frame, text="Métricas de Mitigación de Riesgo", font=ctk.CTkFont(family="Helvetica", size=22, weight="bold"))
        titulo.grid(row=0, column=0, pady=(0, 15), sticky="w")

        # --- SECCIÓN DEL GRÁFICO (DONUT) ---
        if self.archivos_seguros > 0 or self.archivos_malware > 0:
            fig, ax = plt.subplots(figsize=(5.5, 2.5), facecolor='none')
            fig.patch.set_facecolor('#141419')
            labels = ['Seguros', 'Malware']
            valores = [self.archivos_seguros, self.archivos_malware]
            colores = ['#2A9D8F', '#E76F51']
            if self.archivos_malware == 0:
                labels, valores, colores = ['Seguros'], [self.archivos_seguros], ['#2A9D8F']
            ax.pie(valores, labels=labels, colors=colores, autopct='%1.1f%%', startangle=90, textprops={'color': 'white', 'weight': 'bold', 'size': 10})
            ax.axis('equal')
            centro_circulo = plt.Circle((0,0), 0.70, fc='#141419')
            fig.gca().add_artist(centro_circulo)
            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.draw()
            canvas.get_tk_widget().grid(row=1, column=0, pady=2)
            plt.close(fig)
        else:
            lbl_vacio = ctk.CTkLabel(frame, text="📊 Telemetría en espera. Ejecuta un análisis para ver gráficos.", font=ctk.CTkFont(size=13), text_color="#A3A3A3")
            lbl_vacio.grid(row=1, column=0, pady=30)

        # --- NUEVA SECCIÓN DE AUTOMATIZACIÓN DINÁMICA ---
        subframe = ctk.CTkFrame(frame, corner_radius=12, border_width=1, border_color="#2D2F36", fg_color="#111116")
        subframe.grid(row=2, column=0, pady=10, padx=10, sticky="ew")
        
        lbl_autom = ctk.CTkLabel(subframe, text="⚙️ Planificador de Análisis en Tiempo Real", font=ctk.CTkFont(size=14, weight="bold"))
        lbl_autom.grid(row=0, column=0, columnspan=3, padx=15, pady=(12, 5), sticky="w")

        # Dropdown 1: Elegir Frecuencia (Semanal o Mensual)
        lbl_frec = ctk.CTkLabel(subframe, text="Frecuencia:", font=ctk.CTkFont(size=12))
        lbl_frec.grid(row=1, column=0, padx=(15, 5), pady=10, sticky="w")
        
        self.menu_frecuencia = ctk.CTkOptionMenu(subframe, values=["Semanal", "Mensual"], width=120, command=self.actualizar_visibilidad_dias)
        self.menu_frecuencia.grid(row=1, column=1, padx=5, pady=10, sticky="w")

        # Dropdown 2: Elegir Día (Solo aparece si la frecuencia es Semanal)
        self.lbl_dia = ctk.CTkLabel(subframe, text="Cada día:", font=ctk.CTkFont(size=12))
        self.lbl_dia.grid(row=1, column=2, padx=(15, 5), pady=10, sticky="w")
        
        self.menu_dias = ctk.CTkOptionMenu(subframe, values=["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"], width=120)
        self.menu_dias.grid(row=1, column=3, padx=5, pady=10, sticky="w")

        # Botón de disparo unificado
        self.btn_programar = ctk.CTkButton(subframe, text="📅 Registrar Plan de Escaneo", font=ctk.CTkFont(size=12, weight="bold"), height=35, fg_color="#457B9D", hover_color="#1D3557", command=self.ajustar_programacion_gui)
        self.btn_programar.grid(row=2, column=0, columnspan=4, padx=15, pady=(5, 15), sticky="ew")

    def actualizar_visibilidad_dias(self, eleccion):
        """Muestra u oculta el selector de días de la semana de manera dinámica."""
        if eleccion == "Mensual":
            self.lbl_dia.grid_remove()
            self.menu_dias.grid_remove()
        else:
            self.lbl_dia.grid()
            self.menu_dias.grid()

    def ajustar_programacion_gui(self):
        """Envía los parámetros del formulario gráfico al módulo del sistema operativo."""
        import ScheduleManager
        
        frecuencia = self.menu_frecuencia.get()
        dia = self.menu_dias.get()
        
        # Resetear estado del botón para permitir múltiples cambios de opinión del usuario
        self.btn_programar.configure(state="disabled", text="Registrando cambios...")
        
        # Llamar a la lógica enviándole los parámetros elegidos por el usuario
        resultado_txt = ScheduleManager.programar_escaneo(frecuencia, dia)
        
        # Mostrar el feedback visual de éxito o error
        self.btn_programar.configure(state="normal", text=resultado_txt, fg_color="#2A9D8F" if "✅" in resultado_txt else "#E76F51")


if __name__ == "__main__":
    app = AntivirusIAApp()
    app.mainloop()

