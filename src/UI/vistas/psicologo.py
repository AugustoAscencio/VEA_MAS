
from __future__ import annotations
"""
VEA+ — versión "todo en una sola clase" con chat asincrónico a n8n
Modificado: paleta de colores con ft.Colors y "Evaluación rápida" con diálogo de confirmación.
Guarda como: psicologo_unaclase_modificado.py
Requiere: pip install flet httpx
Ejecuta: python psicologo_unaclase_modificado.py
"""

import os
import time
import json
import math
import threading
import datetime
import traceback
from typing import Any, Callable, Dict, List, Optional, Tuple

# httpx + asyncio para llamadas asincrónicas al webhook
import asyncio
import httpx
from asyncio import run_coroutine_threadsafe

import flet as ft

# URL del webhook n8n (tu webhook)
N8N_WEBHOOK_URL = "https://augustocraft02.app.n8n.cloud/webhook/875be057-eabd-4d46-99e6-0448922119a6"

APP_NAME = "VEA+ Asistencia Psicológica (Una clase)"
# ---------- PALETA OSCURA (solo tonos azules, morados y claros para contraste) ----------
PRIMARY = ft.Colors.INDIGO_600
ACCENT  = ft.Colors.TEAL_600
BG      = ft.Colors.BLUE_GREY_50
SURFACE = ft.Colors.WHITE
TEXT    = ft.Colors.BLACK
MUTED   = ft.Colors.BLUE_GREY_500

OK            = ft.Colors.GREEN_400          # Verde visible pero no saturado
OK_50         = ft.Colors.GREEN_100          # Verde claro para fondos suaves

WARN          = ft.Colors.AMBER_400          # Amarillo vibrante para alertas
WARN_50       = ft.Colors.AMBER_100          # Amarillo claro para fondos

DANGER        = ft.Colors.RED_400            # Rojo visible pero no agresivo
DANGER_50     = ft.Colors.RED_100            # Rojo claro para fondos

BORDER        = ft.Colors.BLUE_GREY_700      # Bordes sutiles pero definidos
BG_LIGHT      = ft.Colors.BLUE_GREY_700      # Fondo alternativo más claro

# ---------- Aliases ----------
ACCENT        = ft.Colors.PURPLE_ACCENT_700  # Morado vibrante para acentos
BG_DARK       = ft.Colors.BLUE_GREY_900      # Fondo oscuro principal
CARD_DARK     = ft.Colors.BLUE_GREY_800      # Cards y paneles
MUTED_DARK    = ft.Colors.BLUE_GREY_600      # Texto secundario en modo oscuro
TEXT_LIGHT    = ft.Colors.GREY_100           # Texto claro
TEXT_DARK     = ft.Colors.GREY_300           # Texto menos contrastante en fondos oscuros


# # ---------- PALETA (usar constantes de ft.Colors para un aspecto consistente) ----------
# PRIMARY       = ft.Colors.INDIGO_900         # Más profundo y dominante
# PRIMARY_DARK  = ft.Colors.DEEP_PURPLE_900    # Contraste elegante y fuerte
# PRIMARY_50    = ft.Colors.INDIGO_100         # Más visible que el 50, pero aún suave

# BG            = ft.Colors.BLUE_GREY_100      # Más claro para mejor contraste
# SURFACE       = ft.Colors.GREY_50            # Ligero pero no blanco puro
# TEXT          = ft.Colors.GREY_900           # Negro más suave, menos duro
# MUTED         = ft.Colors.BLUE_GREY_600      # Más visible que el 400

# OK            = ft.Colors.GREEN_ACCENT_700   # Verde vibrante y moderno
# OK_50         = ft.Colors.GREEN_ACCENT_100   # Verde claro pero más saturado

# WARN          = ft.Colors.AMBER_900          # Amarillo intenso, más alerta
# WARN_50       = ft.Colors.AMBER_100          # Más saturado que el 50

# DANGER        = ft.Colors.RED_ACCENT_700     # Rojo fuerte y llamativo
# DANGER_50     = ft.Colors.RED_ACCENT_100     # Rojo claro pero más visible

# BORDER        = ft.Colors.BLUE_GREY_200      # Más definido que el 50
# BG_LIGHT      = ft.Colors.GREY_100           # Más cálido que blanco puro

# # Aliases
# ACCENT        = ft.Colors.TEAL_ACCENT_700    # Teal vibrante
# BG_DARK       = ft.Colors.BLUE_GREY_300      # Más contraste para modo oscuro
# CARD_DARK     = ft.Colors.GREY_200           # Fondo de tarjeta más definido
# MUTED_DARK    = ft.Colors.BLUE_GREY_700      # Más fuerte para modo oscuro
# TEXT_LIGHT    = ft.Colors.GREY_50            # Blanco suave para texto claro
# TEXT_DARK     = ft.Colors.GREY_900           # Consistente con texto principal

# # --------------------------------------------------------------------------------------

DATA_DIR = os.path.join(os.getcwd(), "vea_data")
os.makedirs(DATA_DIR, exist_ok=True)

# ====== Bucle asíncrono en background ======
loop = asyncio.new_event_loop()


def start_loop(lp: asyncio.AbstractEventLoop):
    asyncio.set_event_loop(lp)
    lp.run_forever()


threading.Thread(target=start_loop, args=(loop,), daemon=True).start()


class VeaAllInOne:
    """
    Clase única que contiene:
      - utilidades responsivas
      - animación de respiración (pulmón)
      - almacenamiento de estado de ánimo
      - burbujas de chat
      - bot empático simple (backup local)
      - síntoma/assessment
      - UI y lógica de interacción con Flet
      - chat mediante webhook n8n (asincrónico)
    """

    # ----------------------
    # Constantes de síntoma (se mantienen como clase)
    # ----------------------
    SYMPTOMS = [
        ("Pérdida de interés o placer", "anhedonia"),
        ("Bajo estado de ánimo la mayor parte del día", "depresivo"),
        ("Fatiga o pérdida de energía", "fatiga"),
        ("Insomnio o hipersomnia", "sueño"),
        ("Dificultad para concentrarse", "concentracion"),
        ("Sentimientos de inutilidad o culpa", "culpa"),
        ("Pensamientos de muerte o suicidio", "suicida"),
        ("Ansiedad excesiva o preocupaciones", "ansiedad"),
        ("Agitación o irritabilidad", "irritabilidad"),
    ]

    def __init__(self, page: ft.Page):
        # Página
        self.page = page
        self.page.title = APP_NAME
        self.page.window_width = 360
        self.page.window_height = 820

        # Tema
        self._dark = False
        self._apply_theme()

        # Parámetros y estado
        self._breathing = False
        self._breath_thread: Optional[threading.Thread] = None
        self._breath_lock = threading.Lock()
        self._breath_fps = 40
        self._breath_base_diameter = 260
        # fases (segundos)
        self._inhale = 4.0
        self._hold = 1.5
        self._exhale = 5.0

        # Posiciones relativas (centro visual)
        self._left_center_rel = (0.25, 0.50)
        self._right_center_rel = (0.75, 0.50)
        self._center_center_rel = (0.50, 0.50)

        # Bot simple (backup local si falla webhook)
        self.templates = {
            "greet": [
                "Hola — soy VEA+. Estoy aquí para acompañarte con calma. ¿Cómo te sientes hoy?",
                "Bienvenido/a a VEA+. Si quieres, podemos respirar juntos o puedes contarme qué te pasa."
            ],
            "validate": [
                "Gracias por contármelo — lo que sientes tiene sentido.",
                "Te escucho. ¿Quieres que registremos esto o prefieres un ejercicio corto?"
            ],
            "breathe": [
                "Vamos a respirar juntos: cuando estés listo, pulsa Iniciar."
            ],
            "positive": [
                "Me alegra leer eso 😊 ¿Te gustaría registrar este buen momento?"
            ],
            "default": [
                "Gracias por compartir. ¿Quieres que lo registremos o prefieres un ejercicio de respiración?"
            ],
        }
        self.rules = {
            "triste": "Siento que te sientes triste. Si quieres, podemos probar una respiración corta ahora.",
            "llor": "Siento que lo estás pasando mal. ¿Quieres que guardemos esto o contactar a alguien de confianza?",
            "ansio": "Parece ansiedad. Puedo guiarte en una respiración 4-2-6 para calmarte.",
            "angry": "La ira es una emoción válida. Respirar lento puede ayudar a bajar la tensión."
        }
        self.risk_words = ["suicid", "no quiero vivir", "quiero morir", "lastim"]

        # Storage (archivo)
        self.storage_file = os.path.join(DATA_DIR, "mood_history.json")
        self.mood_entries: List[Dict[str, Any]] = []
        self._load_mood_storage()

        # UI references
        self.page.on_resize = self._on_resize if hasattr(self.page, "on_resize") else None
        self.chat_list: Optional[ft.ListView] = None
        self.input_field: Optional[ft.TextField] = None
        self.breath_btn: Optional[ft.ElevatedButton] = None
        self.status_text: Optional[ft.Text] = None
        self.mood_dropdown: Optional[ft.Dropdown] = None
        self.intensity_slider: Optional[ft.Slider] = None
        self.notes_field: Optional[ft.TextField] = None
        self.tags_field: Optional[ft.TextField] = None
        self.symptom_checks: Dict[str, ft.Checkbox] = {}
        self.typing_indicator = None

    # ----------------------
    # Utilidades (métodos "estáticos" dentro de la clase)
    # ----------------------
    @staticmethod
    def clamp(v: float, a: float, b: float) -> float:
        return max(a, min(b, v))

    @staticmethod
    def now_ts() -> str:
        return datetime.datetime.now().isoformat()

    def adaptive_text_size(self, window_width: int, small=12, medium=14, large=16) -> int:
        try:
            if window_width < 480:
                return small
            elif window_width < 900:
                return medium
            else:
                return large
        except Exception:
            return medium

    def save_json(self, name: str, obj: Any) -> str:
        path = os.path.join(DATA_DIR, name)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
        return path

    # ----------------------
    # Storage mood
    # ----------------------
    def _load_mood_storage(self):
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, "r", encoding="utf-8") as f:
                    self.mood_entries = json.load(f)
            else:
                self.mood_entries = []
        except Exception:
            self.mood_entries = []

    def _save_mood_storage(self):
        try:
            with open(self.storage_file, "w", encoding="utf-8") as f:
                json.dump(self.mood_entries, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def mood_add(self, mood: str, intensity: int, notes: str, tags: List[str]) -> Dict[str, Any]:
        e = {"timestamp": self.now_ts(), "mood": mood, "intensity": int(intensity), "notes": notes, "tags": tags}
        self.mood_entries.insert(0, e)
        self._save_mood_storage()
        return e

    def mood_export_csv(self, filename: str) -> str:
        import csv
        path = os.path.join(DATA_DIR, filename)
        with open(path, "w", newline="", encoding="utf-8") as csvfile:
            w = csv.writer(csvfile)
            w.writerow(["timestamp", "mood", "intensity", "notes", "tags"])
            for e in self.mood_entries:
                w.writerow([e["timestamp"], e["mood"], e["intensity"], e["notes"], ",".join(e["tags"])])
        return path

    # ----------------------
    # Bot (muy simple) - backup local si n8n falla
    # ----------------------
    def _bot_choose(self, key):
        import random
        return random.choice(self.templates.get(key, self.templates["default"]))

    def bot_respond(self, text: str) -> Dict[str, Any]:
        t = (text or "").strip().lower()
        if not t:
            return {"text": self._bot_choose("greet"), "tags": [], "escalate": False}
        tags, escalate = [], False
        for w in self.risk_words:
            if w in t:
                escalate = True
                tags.append("riesgo-suicida")
        for k, v in self.rules.items():
            if k in t:
                tags.append(k)
                return {"text": v, "tags": tags, "escalate": escalate}
        if any(p in t for p in ["bien", "feliz", "contento", "alegre", "genial"]):
            return {"text": self._bot_choose("positive"), "tags": ["positivo"], "escalate": False}
        return {"text": self._bot_choose("validate"), "tags": [], "escalate": escalate}

    # ----------------------
    # Chat bubble (contenedor simple)
    # ----------------------
    def _make_bubble(self, text: str, sender: str = "bot", compact: bool = False, size: int = 14) -> ft.Container:
        user = sender == "user"
        #bgcolor = ft.Colors.with_opacity(0.16, ACCENT) if user else ft.Colors.with_opacity(0.06, PRIMARY)
        #color = TEXT_LIGHT if not user else TEXT_LIGHT
        if user:
            # Usuario → violeta más fuerte con texto blanco
            bgcolor = ft.Colors.with_opacity(0.15, PRIMARY)
            color = ft.Colors.WHITE
        else:
            # Bot → gris azulado muy claro con texto oscuro
            bgcolor = ft.Colors.with_opacity(0.25, ft.Colors.BLUE_GREY_100)
            color = ft.Colors.BLACK
        align = ft.alignment.center_right if user else ft.alignment.center_left
        margin = ft.margin.only(left=62, right=12, bottom=8) if not user else ft.margin.only(left=12, right=24, bottom=8)
        inner = ft.Column([
            ft.Text(text, size=size if not compact else max(12, size-1), color=color, selectable=True),
            ft.Text(datetime.datetime.now().strftime("%H:%M"), size=10, color=ft.Colors.with_opacity(0.6, MUTED_DARK))
        ], tight=True, spacing=6)
        return ft.Container(content=inner, padding=ft.padding.symmetric(vertical=10, horizontal=12), bgcolor=bgcolor, border_radius=14, margin=margin, alignment=align)

    # ----------------------
    # Evaluación rápida de síntomas
    # ----------------------
    def quick_assess(self, selected: List[str]) -> Dict[str, Any]:
        if "suicida" in selected:
            return {"level": "alto", "score": 10, "advice": "Contacta ayuda profesional o servicios de emergencia inmediatamente."}
        score = len(selected)
        if score >= 6:
            level = "alto"
        elif score >= 3:
            level = "moderado"
        else:
            level = "bajo"
        advice_map = {"bajo": "Observa y registra. Considera una actividad de autocuidado.",
                      "moderado": "Considera hablar con un profesional o con alguien de confianza.",
                      "alto": "Busca ayuda profesional cuanto antes."}
        return {"level": level, "score": score, "advice": advice_map[level]}

    # ----------------------
    # Breathing animation (todo dentro de la clase)
    # ----------------------
    def _build_breath_widget(self) -> ft.Control:
        d = self._breath_base_diameter
        stack = ft.Stack(controls=[
            ft.Container(
                width=d,
                height=d,
                border_radius=d,
                bgcolor=ft.Colors.with_opacity(0.04, PRIMARY),
                left=0, top=0,
            ),
            ft.Container(
                width=int(d * 0.55),
                height=int(d * 0.72),
                left=int(d * 0.5 - (d * 0.55) * 0.5 - d * 0.12),
                top=int(d * 0.14),
                border_radius=9999,
                rotate=math.radians(-12),
                bgcolor=ft.Colors.with_opacity(0.16, PRIMARY),
                key="left_lobe",
            ),
            ft.Container(
                width=int(d * 0.55),
                height=int(d * 0.72),
                left=int(d * 0.5 - (d * 0.55) * 0.5 + d * 0.12),
                top=int(d * 0.14),
                border_radius=9999,
                rotate=math.radians(12),
                bgcolor=ft.Colors.with_opacity(0.14, PRIMARY),
                key="right_lobe",
            ),
            ft.Container(
                width=int(d * 0.42),
                height=int(d * 0.42),
                left=int(d * 0.5 - (d * 0.42) * 0.5),
                top=int(d * 0.48 - (d * 0.42) * 0.5),
                border_radius=9999,
                bgcolor=ft.Colors.with_opacity(0.22, PRIMARY),
                key="center",
            ),
        ])
        outer = ft.Container(
            width=d + 36,
            height=d + 36,
            padding=ft.padding.all(8),
            alignment=ft.alignment.center,
            content=stack
        )
        return outer

    def _find_breath_controls(self, container: ft.Container) -> Tuple[Optional[ft.Container], Optional[ft.Container], Optional[ft.Container]]:
        try:
            stack = container.content
            controls = getattr(stack, "controls", [])
            left = right = center = None
            for c in controls:
                if getattr(c, "key", None) == "left_lobe":
                    left = c
                elif getattr(c, "key", None) == "right_lobe":
                    right = c
                elif getattr(c, "key", None) == "center":
                    center = c
            return left, right, center
        except Exception:
            return None, None, None

    def _center_for_size(self, size_w: int, size_h: int, rel: Tuple[float, float]) -> Tuple[int, int]:
        d = self._breath_base_diameter
        cx = int(d * rel[0])
        cy = int(d * rel[1])
        left = max(0, int(cx - size_w / 2))
        top = max(0, int(cy - size_h / 2))
        return left, top

    def _ease_in_out(self, t: float) -> float:
        return 0.5 - 0.5 * math.cos(math.pi * t)

    def _vibrate(self, target_controls: List[Optional[ft.Container]], magnitude_px=6, cycles=6, duration=0.36):
        steps = max(6, int(cycles * 2))
        interval = duration / steps
        for i in range(steps):
            with self._breath_lock:
                if not self._breathing:
                    return
            phase = math.sin(math.pi * (i / steps) * cycles)
            delta = int(magnitude_px * phase)
            for c in target_controls:
                try:
                    if c:
                        if getattr(c, "left", None) is not None:
                            c.left = (getattr(c, "left", 0) or 0) + (delta if i % 2 == 0 else -delta)
                        if getattr(c, "top", None) is not None:
                            c.top = (getattr(c, "top", 0) or 0) + (int(delta/2) if i % 2 == 0 else -int(delta/2))
                except Exception:
                    pass
            try:
                self.page.update()
            except Exception:
                pass

    def _run_breath_phase(self, duration: float, phase_name: str, container: ft.Container) -> bool:
        steps = max(4, int(self._breath_fps * duration))
        start = time.time()
        left_ctrl, right_ctrl, center_ctrl = self._find_breath_controls(container)

        for step in range(steps):
            with self._breath_lock:
                if not self._breathing:
                    return False
            elapsed = time.time() - start
            progress = min(1.0, elapsed / max(1e-6, duration))
            eased = self._ease_in_out(progress)

            if phase_name == "inhale":
                scale = 0.8 + 0.2 * eased
            elif phase_name == "hold":
                scale = 1.0
            else:
                scale = 1.0 - 0.2 * eased

            alpha_center = 0.18 + 0.06 * math.sin(math.pi * progress)
            alpha_lobe = 0.14 + 0.05 * math.sin(math.pi * progress + 0.3)

            try:
                if left_ctrl and right_ctrl and center_ctrl:
                    base_left_w = int(self._breath_base_diameter * 0.55)
                    base_left_h = int(self._breath_base_diameter * 0.72)
                    base_right_w = base_left_w
                    base_right_h = base_left_h
                    base_center = int(self._breath_base_diameter * 0.42)

                    new_left_w = max(12, int(base_left_w * (scale * (0.96 + 0.04 * math.sin(progress * 3.14)))))
                    new_left_h = max(12, int(base_left_h * (scale * (0.98 + 0.03 * math.cos(progress * 2.17)))))

                    new_right_w = max(12, int(base_right_w * (scale * (0.98 + 0.03 * math.sin(progress * 2.9)))))
                    new_right_h = max(12, int(base_right_h * (scale * (0.96 + 0.04 * math.cos(progress * 1.9)))))

                    new_center = max(12, int(base_center * (scale)))

                    left_ctrl.width = new_left_w
                    left_ctrl.height = new_left_h
                    right_ctrl.width = new_right_w
                    right_ctrl.height = new_right_h
                    center_ctrl.width = new_center
                    center_ctrl.height = new_center

                    left_l, left_t = self._center_for_size(new_left_w, new_left_h, self._left_center_rel)
                    right_l, right_t = self._center_for_size(new_right_w, new_right_h, self._right_center_rel)
                    center_l, center_t = self._center_for_size(new_center, new_center, self._center_center_rel)

                    left_ctrl.left = int(left_l - (self._breath_base_diameter * 0.02) * (1 - scale))
                    left_ctrl.top = int(left_t + (self._breath_base_diameter * 0.01) * (1 - scale))

                    right_ctrl.left = int(right_l + (self._breath_base_diameter * 0.02) * (1 - scale))
                    right_ctrl.top = int(right_t + (self._breath_base_diameter * 0.01) * (1 - scale))

                    center_ctrl.left = int(center_l)
                    center_ctrl.top = int(center_t)

                    center_ctrl.bgcolor = ft.Colors.with_opacity(alpha_center, PRIMARY)
                    left_ctrl.bgcolor = ft.Colors.with_opacity(alpha_lobe, PRIMARY)
                    right_ctrl.bgcolor = ft.Colors.with_opacity(alpha_lobe - 0.02, PRIMARY)

                    # actualizar texto de estado si existe
                    try:
                        if self.status_text:
                            if phase_name == "inhale":
                                self.status_text.value = f"Inhala... {int(progress*100)}%"
                            elif phase_name == "hold":
                                self.status_text.value = "Sostén..."
                            else:
                                self.status_text.value = f"Exhala... {int(progress*100)}%"
                    except Exception:
                        pass

                try:
                    self.page.update()
                except Exception:
                    pass
            except Exception:
                pass

            time.sleep(duration / steps if steps else (1.0 / self._breath_fps))

        if phase_name == "inhale":
            targets = [left_ctrl, right_ctrl, center_ctrl]
            self._vibrate(targets, magnitude_px=5, cycles=6, duration=0.28)
        return True

    def _breath_loop(self, container: ft.Container):
        try:
            while True:
                with self._breath_lock:
                    if not self._breathing:
                        break
                if not self._run_breath_phase(self._inhale, "inhale", container):
                    break
                if not self._run_breath_phase(self._hold, "hold", container):
                    break
                if not self._run_breath_phase(self._exhale, "exhale", container):
                    break
        except Exception:
            traceback.print_exc()

    def _start_breath(self, container: ft.Container):
        with self._breath_lock:
            if self._breathing:
                return
            self._breathing = True
        self._breath_thread = threading.Thread(target=self._breath_loop, args=(container,), daemon=True)
        self._breath_thread.start()

    def _stop_breath(self):
        with self._breath_lock:
            self._breathing = False

    # ----------------------
    # UI: build completo
    # ----------------------
    def build(self) -> ft.Control:
        # ancho adaptativo
        try:
            width = getattr(self.page, "window_width", None) or self.page.window_width or 380
        except Exception:
            width = 380

        font_small = self.adaptive_text_size(width, small=12, medium=13, large=14)
        font_medium = self.adaptive_text_size(width, small=13, medium=14, large=16)
        font_title = self.adaptive_text_size(width, small=18, medium=20, large=22)

        # Header
        title_col = ft.Column([
            ft.Text("VEA+", size=font_title, weight=ft.FontWeight.W_700, color=TEXT_LIGHT if self._dark else TEXT_DARK),
            ft.Text("Asistencia Psicológica — tu espacio seguro", size=12, color=ft.Colors.with_opacity(0.8, MUTED_DARK))
        ], spacing=6)
        #close_btn = ft.ElevatedButton("Cerrar", on_click=lambda e: self.page.window_close(), bgcolor=PRIMARY)
        theme_toggle = ft.IconButton(ft.Icons.DARK_MODE, on_click=self._toggle_theme, tooltip="Cambiar tema")
        header = ft.Row([title_col, ft.Row([theme_toggle,])], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        header = ft.Row([title_col,], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        # Breath card
        breath_title = ft.Text("Respiración guiada", size=18, weight=ft.FontWeight.W_600, color=TEXT_LIGHT if self._dark else TEXT_DARK)
        breath_instr = ft.Text("Pulsa Iniciar y sigue la forma en el centro. Respira con calma.", size=12, color=ft.Colors.with_opacity(0.8, MUTED_DARK))
        # widget dinámico (guardamos referencia del contenedor)
        self._breath_widget_container = self._build_breath_widget()
        self.breath_btn = ft.ElevatedButton("Iniciar Respiración", on_click=lambda e: self._on_breath_btn(e), bgcolor=PRIMARY, width=140)
        stop_btn = ft.ElevatedButton("Detener", on_click=lambda e: self._on_stop_breath(e), width=100)
        breath_controls = ft.Row([self.breath_btn, stop_btn], spacing=12, alignment=ft.MainAxisAlignment.CENTER)
        self.status_text = ft.Text(
            "",
            size=font_medium,
            color=ft.Colors.BLACK,   # siempre oscuro para que contraste bien en fondo claro
            weight=ft.FontWeight.W_600
        )
        breath_card = ft.Container(content=ft.Column([breath_title, breath_instr, ft.Row([self._breath_widget_container], alignment=ft.MainAxisAlignment.CENTER), breath_controls, ft.Container(self.status_text, padding=ft.padding.only(top=8))], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding=ft.padding.all(14), border_radius=14, bgcolor=ft.Colors.with_opacity(0.02, PRIMARY), margin=ft.margin.only(bottom=6))

        # Chat
        self.chat_list = ft.ListView(expand=True, spacing=8, padding=ft.padding.only(bottom=8))
        greet = self.bot_respond("")["text"]
        self.chat_list.controls.insert(0, self._make_bubble(greet, sender="bot", size=font_medium))
        self.input_field = ft.TextField(hint_text="Escribe aquí... (presiona Enter para enviar)", expand=True, on_submit=lambda e: self._user_send(e))
        send_btn = ft.IconButton(ft.Icons.SEND, on_click=lambda e: self._user_send(e))
        input_row = ft.Row([self.input_field, send_btn], spacing=8)
        chat_card = ft.Container(content=ft.Column([ft.Text("Conversación", size=16, weight=ft.FontWeight.W_600, color=TEXT_DARK if self._dark else TEXT_DARK), ft.Text("Habla cuando quieras — yo escucho.", size=12, color=ft.Colors.with_opacity(0.8, MUTED_DARK)), self.chat_list, input_row], spacing=10), padding=ft.padding.all(12), border_radius=14, bgcolor=ft.Colors.with_opacity(0.01, PRIMARY), margin=ft.margin.only(bottom=6))

        # Right: mood & checklist
        mood_opts = ["Feliz", "Triste", "Ansioso", "Enojado", "Cansado", "Neutral", "Aliviado", "Esperanzado"]
        self.mood_dropdown = ft.Dropdown(options=[ft.dropdown.Option(m) for m in mood_opts], hint_text="Selecciona tu estado", expand=True)
        self.intensity_slider = ft.Slider(min=1, max=10, divisions=9, label="Intensidad", value=5, expand=True)
        self.notes_field = ft.TextField(label="Notas / ¿Qué pasó hoy?", multiline=True, min_lines=3, max_lines=6, expand=True)
        self.tags_field = ft.TextField(label="Etiquetas (separadas por comas)", expand=True)
        register_row = ft.Row([ft.ElevatedButton("Registrar", on_click=lambda e: self._register_mood(e), bgcolor=ACCENT, width=140), ft.ElevatedButton("Exportar", on_click=lambda e: self._export_local(e), width=120)], spacing=12)

        # --- Info / aviso antes del checklist ---
        quick_info = ft.Container(
            ft.Row(
                [
                    ft.Icon(ft.Icons.INFO_OUTLINE, size=20, color=PRIMARY),
                    ft.Column(
                        [
                            ft.Text("Evaluación rápida", weight=ft.FontWeight.W_700, size=font_small),
                            ft.Text(
                                "Valoración breve para identificar señales. No sustituye una evaluación profesional.",
                                size=max(10, font_small-1),
                                color=ft.Colors.with_opacity(0.9, MUTED),
                            ),
                        ],
                        spacing=2,
                    ),
                ],
                spacing=8,
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.all(10),
            bgcolor=ft.Colors.with_opacity(0.04, PRIMARY),
            border_radius=8,
            margin=ft.margin.only(bottom=8),
        )

        # --- Checklist (ahora con el aviso visible encima) ---
        checks_col = ft.Column([quick_info, ft.Text("Checklist rápido", weight=ft.FontWeight.W_600, size=font_medium)])
        self.symptom_checks = {}
        cb_font = self.adaptive_text_size(width, small=12, medium=13, large=14)
        for label, key in self.SYMPTOMS:
            cb = ft.Checkbox(label, value=False, expand=True, label_style=ft.TextStyle(size=cb_font))
            self.symptom_checks[key] = cb
            checks_col.controls.append(cb)

        # el botón ahora pide confirmación antes de ejecutar la evaluación
        assess_btn = ft.ElevatedButton("Evaluar", on_click=lambda e: self._confirm_assessment(e), bgcolor=WARN, width=140)
        checks_col.controls.append(ft.Container(assess_btn, padding=ft.padding.only(top=8)))

        right_card = ft.Container(content=ft.Column([ft.Text("Registro de emociones", size=16, weight=ft.FontWeight.W_600, color=TEXT_LIGHT if self._dark else TEXT_DARK), ft.Text("Registrar ayuda a identificar patrones con el tiempo.", size=12, color=ft.Colors.with_opacity(0.8, MUTED_DARK)), self.mood_dropdown, self.intensity_slider, self.notes_field, self.tags_field, register_row], spacing=10), padding=ft.padding.all(12), border_radius=14, bgcolor=ft.Colors.with_opacity(0.01, PRIMARY), margin=ft.margin.only(bottom=6))

        # Layout
        top_spacing = ft.Container(height=14)

        if width < 800:
            content = ft.Column([
                top_spacing,
                header,
                ft.Divider(height=1),
                breath_card,
                ft.Divider(height=1),
                chat_card,
                ft.Divider(height=1),
                right_card,
                ft.Divider(height=1),
                checks_col
            ], spacing=14, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            root = ft.ListView(controls=[content], padding=ft.padding.symmetric(horizontal=14, vertical=8), expand=True)
            return root
        else:
            left_col = ft.Column([breath_card], width=360, spacing=12)
            mid_col = ft.Column([chat_card], expand=True, spacing=12)
            right_col = ft.Column([right_card, checks_col], width=380, spacing=12)
            layout_row = ft.Row([left_col, mid_col, right_col], spacing=18, alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            content = ft.Column([top_spacing, header, layout_row], spacing=14)
            root = ft.ListView(controls=[content], padding=ft.padding.symmetric(horizontal=16, vertical=10), expand=True)
            return root

    # ----------------------
    # Acciones y callbacks
    # ----------------------
    def _on_breath_btn(self, e=None):
        if not self._breath_widget_container:
            return
        if not self._breathing:
            self._start_breath(self._breath_widget_container)
            if self.breath_btn:
                self.breath_btn.text = "Pausar Respiración"
                self.breath_btn.bgcolor = "#FF6F61"
            self._append_chat("Comenzamos una respiración guiada. Sígueme con calma.", sender="bot")
        else:
            self._stop_breath()
            if self.breath_btn:
                self.breath_btn.text = "Iniciar Respiración"
                self.breath_btn.bgcolor = PRIMARY
            self._append_chat("Respiración pausada. Respira a tu ritmo.", sender="bot")

    def _on_stop_breath(self, e=None):
        self._stop_breath()
        if self.breath_btn:
            self.breath_btn.text = "Iniciar Respiración"
            self.breath_btn.bgcolor = PRIMARY
        self._append_chat("Respiración detenida.", sender="bot")

    def _append_chat(self, text: str, sender: str = "bot", compact: bool = False):
        if not self.chat_list:
            return
        size = self.adaptive_text_size(getattr(self.page, 'window_width', 380), small=13, medium=14, large=16)
        bub = self._make_bubble(text, sender=sender, compact=compact, size=size)
        self.chat_list.controls.append(bub)
        if len(self.chat_list.controls) > 2000:
            self.chat_list.controls = self.chat_list.controls[:2000]
        try:
            self.page.update()
        except Exception:
            pass

    def _show_typing(self):
        if not self.chat_list or self.typing_indicator:
            return
        c = ft.Container(ft.Row([ft.Text("VEA+ está escribiendo...", size=12, color=ft.Colors.with_opacity(0.7, MUTED_DARK)), ft.ProgressRing()]), padding=6, bgcolor=ft.Colors.with_opacity(0.02, PRIMARY), border_radius=8, margin=ft.margin.only(bottom=8))
        self.typing_indicator = c
        self.chat_list.controls.append(c)
        try:
            self.page.update()
        except Exception:
            pass

    def _hide_typing(self):
        if not self.chat_list or not self.typing_indicator:
            return
        try:
            self.chat_list.controls.remove(self.typing_indicator)
        except Exception:
            pass
        self.typing_indicator = None
        try:
            self.page.update()
        except Exception:
            pass

    # ----------------------
    # Nuevo: integración asincrónica con n8n (httpx + asyncio)
    # ----------------------
    async def _handle_user_message(self, text: str) -> None:
        """
        Envia el mensaje al webhook de n8n asincrónicamente y agrega la respuesta al chat.
        Espera JSON tipo: { "respuesta": "texto..." }
        """
        self._show_typing()
        reply = ""
        try:
            async with httpx.AsyncClient(timeout=20) as client:
                # Enviamos usuario + chatInput (puedes ajustar keys si lo requiere tu flujo n8n)
                resp = await client.post(N8N_WEBHOOK_URL, json={"usuario": "augusto", "chatInput": text})
                raw = resp.text
                if resp.status_code == 200:
                    try:
                        data = resp.json()
                        # extraemos 'respuesta' si existe, si no usamos raw
                        reply = data.get("respuesta", raw) if isinstance(data, dict) else raw
                    except Exception:
                        reply = raw
                else:
                    reply = f"Error {resp.status_code}: {raw}"
        except Exception as ex:
            # fallback a bot local si quieres — aquí mostramos el error y luego un backup
            reply = f"Error de conexión: {ex}\n\nUsando respuesta local."
            try:
                local = self.bot_respond(text)
                reply += f"\n\n{local.get('text','Lo siento, ocurrió un error.')}"
            except Exception:
                pass

        self._hide_typing()
        self._append_chat(reply, sender="bot")

    def _user_send(self, e=None):
        if not self.input_field:
            return
        text = (self.input_field.value or "").strip()
        if not text:
            return

        # Mostrar mensaje del usuario en el chat
        self._append_chat(text, sender="user")
        # vaciar campo
        self.input_field.value = ""
        try:
            # ejecutar la llamada asincrónica en el loop de background
            run_coroutine_threadsafe(self._handle_user_message(text), loop)
        except Exception:
            # fallback síncrono si algo falla (muy raro)
            def worker():
                time.sleep(0.35 + min(1.2, len(text) / 60.0))
                try:
                    resp = self.bot_respond(text)
                    self._append_chat(resp["text"], sender="bot")
                except Exception:
                    self._append_chat("Lo siento, ocurrió un error procesando tu pedido.", sender="bot")
            threading.Thread(target=worker, daemon=True).start()

        try:
            self.page.update()
        except Exception:
            pass

    def _register_mood(self, e=None):
        mood = (self.mood_dropdown.value or "Neutral").strip()
        intensity = int(self.intensity_slider.value or 5)
        notes = (self.notes_field.value or "").strip()
        tags_raw = (self.tags_field.value or "").strip()
        tags = [t.strip() for t in tags_raw.split(",") if t.strip()]
        entry = self.mood_add(mood, intensity, notes, tags)
        self._append_chat(f"He registrado: {mood} (Int: {intensity}). Gracias por compartir.", sender="bot")
        self.notes_field.value = ""
        self.tags_field.value = ""
        self.intensity_slider.value = 5
        self.mood_dropdown.value = None
        try:
            self.page.update()
        except Exception:
            pass

    def _assess_symptoms(self, e=None):
        selected = [k for k, cb in self.symptom_checks.items() if cb.value]
        res = self.quick_assess(selected)
        self._append_chat(f"Evaluación rápida: nivel {res['level'].upper()} (síntomas: {res['score']}). {res['advice']}", sender="bot")

    def _export_local(self, e=None):
        path = self.save_json(f"mood_export_{int(time.time())}.json", self.mood_entries)
        self._append_chat(f"Exportado localmente a: {path}", sender="bot")

    # ----------------------
    # DIALOGOS DE CONFIRMACIÓN / EVALUACIÓN
    # ----------------------
    def _confirm_assessment(self, e=None):
        """
        Muestra un diálogo de confirmación antes de realizar la evaluación rápida.
        """
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar evaluación rápida"),
            content=ft.Column(
                [
                    ft.Text("Vas a realizar una evaluación breve. Esta valoración es orientativa y no sustituye la atención profesional."),
                    ft.Text("¿Deseas continuar?", weight=ft.FontWeight.W_700),
                ],
                spacing=8,
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda ev: self._close_dialog(ev, dialog)),
                ft.ElevatedButton("Continuar", on_click=lambda ev: self._do_assessment(ev, dialog)),
            ],
        )
        self.page.dialog = dialog
        dialog.open = True
        try:
            self.page.update()
        except Exception:
            pass

    def _close_dialog(self, ev, dialog):
        try:
            dialog.open = False
            self.page.update()
        except Exception:
            pass

    def _do_assessment(self, ev, dialog):
        # cerrar diálogo
        try:
            dialog.open = False
            self.page.update()
        except Exception:
            pass

        # recoger selección y ejecutar la evaluación (existing helper quick_assess)
        selected = [k for k, cb in self.symptom_checks.items() if cb.value]
        res = self.quick_assess(selected)

        # mostrar resultado en un diálogo resumido
        result_dialog = ft.AlertDialog(
            title=ft.Text("Resultado - Evaluación rápida"),
            content=ft.Column(
                [
                    ft.Text(f"Nivel: {res['level'].upper()}  (síntomas: {res['score']})"),
                    ft.Text(res['advice']),
                ],
                spacing=8,
            ),
            actions=[ft.ElevatedButton("Cerrar", on_click=lambda ev: self._close_dialog(ev, result_dialog))],
        )
        self.page.dialog = result_dialog
        result_dialog.open = True
        try:
            self.page.update()
        except Exception:
            pass

        # además, registrar en chat (como antes)
        self._append_chat(f"Evaluación rápida: nivel {res['level'].upper()} (síntomas: {res['score']}). {res['advice']}", sender="bot")

    # ----------------------
    # Theming & resize
    # ----------------------
    def _apply_theme(self):
        if self._dark:
            self.page.theme = ft.Theme(color_scheme_seed=PRIMARY)
            self.page.theme_mode = ft.ThemeMode.DARK
            self.page.bgcolor = BG_DARK
        else:
            self.page.theme = ft.Theme(color_scheme_seed=PRIMARY)
            self.page.theme_mode = ft.ThemeMode.LIGHT
            self.page.bgcolor = BG_LIGHT

    def _toggle_theme(self, e=None):
        self._dark = not self._dark
        self._apply_theme()
        try:
            self.page.controls.clear()
            self.page.add(self.build())
            self.page.update()
        except Exception:
            pass

    def _on_resize(self, e):
        def ui():
            try:
                self.page.controls.clear()
                self.page.add(self.build())
                self.page.update()
            except Exception:
                pass
        try:
            self.page.callable_ui(ui)
        except Exception:
            ui()


# ----------------------
# Run
# ----------------------
def main(page: ft.Page):
    app = VeaAllInOne(page)
    page.add(app.build())


if __name__ == "__main__":
    ft.app(target=main)
