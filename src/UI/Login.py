# UI/Login.py
from __future__ import annotations

"""
Login.py - Chatbot de login/registro para VE+

Características:
 - Flujo de login y registro completamente controlado por máquina de estados.
 - Validaciones estrictas: edad, género, zona, internet, dispositivo, condición de salud.
 - Password: el usuario VE+ ve la contraseña en claro mientras la escribe; en el chat aparece
   enmascarada (****) cuando se muestra como mensaje.
 - Evita el bug "Escribiendo..." atascado mediante lock y uso correcto de coroutines.
 - Construcción del username: PrimerNombre_PrimerApellido.
 - Llamadas a dos endpoints (LOGIN_N8N_URL y REGISTER_N8N_URL) como placeholders.
 - Lógica robusta de reintentos y mensajes empáticos.
 - Integración con `on_finish()` (callback desde main.py) para continuar a la app principal.
"""

import asyncio
import datetime
import threading
import random
import httpx
import json
import os
import traceback
from asyncio import run_coroutine_threadsafe
from pathlib import Path
import flet as ft
from typing import Callable, Any, Optional

# ====== CONFIG - Cambia estas URLs por tus endpoints n8n reales ======
#LOGIN_N8N_URL = "https://augustocraft02.app.n8n.cloud/webhook/b4966ffa-b9aa-49b8-b1a4-54cea285f83f"       # <- reemplaza por tu URL de validación
#REGISTER_N8N_URL = "https://augustocraft02.app.n8n.cloud/webhook/cbe10780-7e24-4118-8820-8c30cdc8c86e" # <- reemplaza por tu URL de registro
LOGIN_N8N_URL = "https://augustosecundario.app.n8n.cloud/webhook/b4966ffa-b9aa-49b8-b1a4-54cea285f83f"       # <- reemplaza por tu URL de validación
REGISTER_N8N_URL = "https://augustosecundario.app.n8n.cloud/webhook/9859b5b2-d480-42bd-a4e5-7aeb0efb7529" # <- reemplaza por tu URL de registro

# ======================================================================
# Simple logging helper (puedes redirigir a logger real si lo deseas)
# ======================================================================
def log_debug(msg: str):
    print(f"[DEBUG {datetime.datetime.now().isoformat()}] {msg}")

# ======================================================================
# Creamos un event loop dedicado en background para coroutines del bot
# ======================================================================
loop = asyncio.new_event_loop()


def _start_background_loop(lp: asyncio.AbstractEventLoop):
    asyncio.set_event_loop(lp)
    lp.run_forever()


_bg_thread = threading.Thread(target=_start_background_loop, args=(loop,), daemon=True)
_bg_thread.start()

# ======================================================================
# Utilities async / sync helpers
# ======================================================================
async def _sleep_and_call(delay: float, callable_obj: Callable[..., Any], *args, **kwargs):
    """
    Espera `delay` segundos (async) y luego ejecuta callable_obj.
    Si callable_obj es coroutine, lo await; si es función normal lo llama.
    Esto evita pasar `asyncio.sleep` a run_coroutine_threadsafe directamente.
    """
    await asyncio.sleep(delay)
    if asyncio.iscoroutinefunction(callable_obj):
        await callable_obj(*args, **kwargs)
    else:
        callable_obj(*args, **kwargs)


async def _maybe_await(fn: Callable[..., Any], *args, **kwargs):
    """Si fn es coroutine function, lo await; si es sync, lo llama."""
    if asyncio.iscoroutinefunction(fn):
        return await fn(*args, **kwargs)
    else:
        return fn(*args, **kwargs)


def safe_run_coroutine(coro):
    """
    Wrapper pequeño para enviar coroutines al loop de fondo y obtener el Future.
    Asegura que el argumento sea una coroutine object (no una función normal).
    """
    if asyncio.iscoroutine(coro):
        return run_coroutine_threadsafe(coro, loop)
    else:
        # intentar convertir si nos pasaron una coroutine function llamándola sin args
        raise TypeError("safe_run_coroutine espera un objeto coroutine (ej: mi_coroutine(...)).")


# ======================================================================
# LoginChatbot class
# ======================================================================
class LoginChatbot:
    """
    Chatbot para login/registro con Flet.

    Integración con Main:
      - main.py crea LoginChatbot(page, on_finish=launch_app)
      - on_finish se llamará cuando login/registro sean exitosos.
    """

    def __init__(self, page: ft.Page, on_finish: Optional[Callable[[], Any]] = None):
        self.page = page
        self.on_finish = on_finish

        # UI refs
        self.list_ref: ft.Ref[ft.ListView] = ft.Ref[ft.ListView]()
        self.input_ref: ft.Ref[ft.TextField] = ft.Ref[ft.TextField]()
        self.typing_ref: ft.Ref[ft.Container] = ft.Ref[ft.Container]()

        # estado
        self.state: str = "initial"
        self.answers: dict[str, Any] = {}
        self.pending_login: dict[str, str] = {}
        self._speak_lock = asyncio.Lock()
        self._last_bot_task = None

        # opciones válidas (normalizadas)
        self.valid_generos = {"femenino", "masculino", "otro", "prefiero no decir", "no binario", "mujer", "hombre"}
        self.valid_zonas = {"urbano", "periurbano", "rural"}
        self.valid_internet = {"siempre", "mayormente", "ocasionalmente", "casi nunca", "ocasional", "mayormente (con intermitencias)"}
        self.valid_dispositivos = {"android", "iphone", "basico", "tableta", "otro", "ios", "ipad"}

        # Inicia el chat en background
        run_coroutine_threadsafe(self.start_chat(), loop)

    # ---------------- UI helpers ----------------
    def _bubble(self, sender: str, text: str) -> ft.Row:
        """
        Construye un bubble simple para el ListView del chat.
        """
        is_user = (sender == "user")
        bg_color = "#4FC3F7" if is_user else "#E6F7FF"
        fg_color = ft.Colors.WHITE if is_user else ft.Colors.BLACK
        ts_color = ft.Colors.with_opacity(0.7, fg_color)
        cont = ft.Container(
            content=ft.Column(
                [
                    ft.Text(text, size=14, color=fg_color, selectable=True, no_wrap=False),
                    ft.Text(datetime.datetime.now().strftime("%H:%M"), size=10, color=ts_color),
                ],
                spacing=4,
                tight=True,
            ),
            bgcolor=bg_color,
            padding=ft.padding.all(12),
            border_radius=18,
            margin=ft.margin.only(left=60 if is_user else 8, right=8 if is_user else 60, top=2, bottom=2),
            shadow=ft.BoxShadow(blur_radius=6, spread_radius=1, color=ft.Colors.with_opacity(0.15, "black")),
        )
        return ft.Row([ft.Container(content=cont, expand=True)], alignment=ft.MainAxisAlignment.END if is_user else ft.MainAxisAlignment.START)

    def append(self, sender: str, text: str):
        """
        Añade un mensaje al ListView y fuerza update de la página.
        """
        if self.list_ref.current:
            self.list_ref.current.controls.append(self._bubble(sender, text))
            self.list_ref.current.scroll_to(offset=99999, duration=200)
        self.page.update()

    # ---------------- typing indicator ----------------
    def show_typing(self, show: bool):
        """
        Muestra o quita el indicador 'Escribiendo...'.
        Protegemos con comprobaciones para no añadir duplicados.
        """
        if not self.list_ref.current:
            return
        if show:
            if not (self.typing_ref.current and self.typing_ref.current in self.list_ref.current.controls):
                bubble = ft.Container(
                    ref=self.typing_ref,
                    content=ft.Row([ft.ProgressRing(width=16, height=16, stroke_width=2, color=ft.Colors.BLUE),
                                    ft.Text("Escribiendo...", size=12, color=ft.Colors.GREY)], spacing=8),
                    padding=ft.padding.all(10),
                    border_radius=16,
                    bgcolor=ft.Colors.BLUE_GREY_800,
                    margin=ft.margin.only(right=120, left=8),
                )
                self.list_ref.current.controls.append(bubble)
        else:
            if self.typing_ref.current and self.typing_ref.current in self.list_ref.current.controls:
                try:
                    self.list_ref.current.controls.remove(self.typing_ref.current)
                except Exception:
                    # fallback: eliminar todos los que parezcan typing_ref
                    self.list_ref.current.controls = [c for c in self.list_ref.current.controls if c is not self.typing_ref.current]
        self.list_ref.current.scroll_to(offset=99999, duration=200)
        self.page.update()

    async def bot_say(self, text: str, delay: float | None = None, first: bool = False):
        """
        Secuencia segura para que el bot "escriba" y luego muestre el mensaje.
        Usamos un lock para evitar solapamientos y para asegurarnos que 'Escribiendo...'
        siempre sea limpiado correctamente.
        """
        async with self._speak_lock:
            if delay is None:
                delay = random.uniform(1.1, 2.0)
            # mostrar typing
            self.show_typing(True)
            await asyncio.sleep(delay)
            # quitar typing
            self.show_typing(False)
            # breve pausa para lograr efecto natural
            await asyncio.sleep(0.18)
            # agregar mensaje
            if self.list_ref.current:
                bubble = self._bubble("bot", text)
                if first and isinstance(bubble, ft.Row):
                    if isinstance(bubble.controls[0], ft.Container):
                        bubble.controls[0].margin = ft.margin.only(top=36, left=8, right=8, bottom=2)
                self.list_ref.current.controls.append(bubble)
                self.list_ref.current.scroll_to(offset=99999, duration=200)
            self.page.update()

    # ---------------- flujo principal ----------------
    async def start_chat(self):
        """
        Arranca la conversación: saludo y primera pregunta.
        """
        await self.bot_say("👋 ¡Hola! Soy VE+, tu asistente de registro e inicio de sesión.", first=True)
        await self.bot_say("Antes de comenzar, por favor dime si ya tienes una cuenta con nosotros. Responde: Sí o No.")
        self.state = "have_account"

    # ----------------- ASK helpers (sincrónicos) -----------------
    # Cada helper cambia el estado y lanza un bot_say de forma segura (pasan coroutine a run_coroutine_threadsafe).
    def ask_login_username(self):
        self.state = "login_username"
        run_coroutine_threadsafe(self.bot_say("Perfecto — por favor ingresa tu nombre de usuario (ej: Augusto_Ascencio)."), loop)

    def ask_login_password(self):
        self.state = "login_password"
        # No activamos modo password en el TextField: el usuario ve lo que escribe.
        run_coroutine_threadsafe(self.bot_say("Ahora ingresa tu contraseña (se mostrará enmascarada en el chat)."), loop)

    def ask_registration_first_name(self):
        self.state = "reg_first_name"
        run_coroutine_threadsafe(self.bot_say("Genial. ¿Cuál es tu primer nombre?"), loop)

    def ask_registration_last_name(self):
        self.state = "reg_last_name"
        run_coroutine_threadsafe(self.bot_say("Perfecto. ¿Cuál es tu primer apellido?"), loop)

    def ask_registration_age(self):
        self.state = "reg_edad"
        run_coroutine_threadsafe(self.bot_say(f"Encantado, {self.answers.get('first_name','')}. ¿Cuántos años tienes? (ej: 30)"), loop)

    def ask_registration_genero(self):
        self.state = "reg_genero"
        run_coroutine_threadsafe(self.bot_say("¿Cuál es tu género? (Femenino / Masculino / Otro)"), loop)

    def ask_registration_zona(self):
        self.state = "reg_zona"
        run_coroutine_threadsafe(self.bot_say("¿En qué zona vives? (Urbano / Periurbano / Rural)"), loop)

    def ask_registration_condicion(self):
        self.state = "reg_condicion"
        run_coroutine_threadsafe(self.bot_say("¿Tienes alguna condición de salud que deba monitorearse? Responde: 'Sí crónica', 'Sí temporal' o 'No'."), loop)

    def ask_registration_condicion_detalle(self):
        self.state = "reg_condicion_detalle"
        run_coroutine_threadsafe(self.bot_say("Entiendo. ¿Podrías especificar cuál(es)? (ej: diabetes, hipertensión, asma)"), loop)

    def ask_registration_internet(self):
        self.state = "reg_internet"
        run_coroutine_threadsafe(self.bot_say("¿Cuál es tu nivel de acceso a Internet? (Siempre / Mayormente / Ocasionalmente / Casi nunca)"), loop)

    def ask_registration_dispositivo(self):
        self.state = "reg_dispositivo"
        run_coroutine_threadsafe(self.bot_say("¿Qué dispositivo usas más seguido? (Android / iPhone / Básico / Tableta / Otro)"), loop)

    def ask_registration_password(self):
        # No activar modo password del TextField (usuario lo ve al escribir).
        self.state = "reg_password"
        run_coroutine_threadsafe(self.bot_say("Por último, crea una contraseña para tu cuenta 🔑 (se mostrará enmascarada en el chat)."), loop)

    # ----------------- normalización y validación -----------------
    def _normalize(self, text: str) -> str:
        return text.strip().lower()

    # ----------------- procesamiento de la entrada del usuario -----------------
    def process_input(self, text: str):
        """
        Lógica que determina qué hacer con el texto del usuario en función del estado.
        Nota: esta función es síncrona (no coroutine) y lanza coroutines al loop de fondo cuando es necesario.
        """
        try:
            txt = self._normalize(text)
            # ------------- Estados -------------
            if self.state == "have_account":
                if txt in {"si", "sí", "s"}:
                    self.ask_login_username()
                elif txt in {"no", "n"}:
                    self.answers.clear()
                    self.ask_registration_first_name()
                else:
                    run_coroutine_threadsafe(self.bot_say("Por favor responde únicamente 'Sí' o 'No'."), loop)
                return

            # ---- LOGIN FLOW ----
            if self.state == "login_username":
                # almacenamos tal cual (puedes normalizar a lower si lo prefieres)
                self.pending_login["username"] = text.strip()
                self.ask_login_password()
                return

            if self.state == "login_password":
                self.pending_login["password"] = text
                # lanzamos validación en background; attempt_login es coroutine
                run_coroutine_threadsafe(self.attempt_login(self.pending_login["username"], self.pending_login["password"]), loop)
                self.state = "login_wait"
                return

            # ---- REGISTER FLOW ----
            if self.state == "reg_first_name":
                candidate = text.strip()
                if len(candidate) < 2:
                    run_coroutine_threadsafe(self.bot_say("Por favor escribe al menos 2 letras para tu nombre."), loop)
                    return
                self.answers["first_name"] = candidate.strip().capitalize()
                self.ask_registration_last_name()
                return

            if self.state == "reg_last_name":
                candidate = text.strip()
                if len(candidate) < 2:
                    run_coroutine_threadsafe(self.bot_say("Por favor escribe al menos 2 letras para tu apellido."), loop)
                    return
                self.answers["last_name"] = candidate.strip().capitalize()

                # Construir username: PrimerNombre_PrimerApellido
                first_clean = self.answers.get("first_name", "").replace(" ", "_")
                last_clean = self.answers.get("last_name", "").replace(" ", "_")
                username_combined = f"{first_clean}_{last_clean}"
                self.answers["username"] = username_combined

                run_coroutine_threadsafe(self.bot_say(f"Perfecto — tu nombre de usuario sugerido será: {username_combined}"), loop)
                # pausa breve y seguir con edad (usar coroutine para pausar + llamar)
                run_coroutine_threadsafe(_sleep_and_call(0.45, self.ask_registration_age), loop)
                return

            if self.state == "reg_edad":
                try:
                    edad_val = int(text.strip())
                    if not (5 <= edad_val <= 120):
                        raise ValueError()
                    self.answers["edad"] = edad_val
                    self.ask_registration_genero()
                except Exception:
                    run_coroutine_threadsafe(self.bot_say("Ingresa tu edad en números (ej: 30). Debe estar entre 5 y 120."), loop)
                return

            if self.state == "reg_genero":
                if txt in {"femenino", "mujer"}:
                    self.answers["genero"] = "Femenino"
                    self.ask_registration_zona()
                elif txt in {"masculino", "hombre"}:
                    self.answers["genero"] = "Masculino"
                    self.ask_registration_zona()
                elif txt in {"otro", "prefiero no decir", "no binario"}:
                    self.answers["genero"] = text.strip()
                    self.ask_registration_zona()
                else:
                    run_coroutine_threadsafe(self.bot_say("Respuesta no válida. Por favor escribe: Femenino, Masculino u Otro."), loop)
                return

            if self.state == "reg_zona":
                if txt in {"urbano", "periurbano", "rural"}:
                    self.answers["zona"] = text.strip().capitalize()
                    self.ask_registration_condicion()
                else:
                    run_coroutine_threadsafe(self.bot_say("Por favor elige: Urbano / Periurbano / Rural."), loop)
                return

            if self.state == "reg_condicion":
                if txt.startswith("si") or txt.startswith("sí"):
                    if "cron" in txt:
                        self.answers["condicion"] = "Sí - crónica"
                        self.ask_registration_condicion_detalle()
                    elif "temp" in txt or "temporal" in txt:
                        self.answers["condicion"] = "Sí - temporal"
                        self.ask_registration_condicion_detalle()
                    else:
                        run_coroutine_threadsafe(self.bot_say("¿Es crónica o temporal? Responde: 'Sí crónica' o 'Sí temporal'."), loop)
                elif txt in {"no", "n"}:
                    self.answers["condicion"] = "No"
                    self.ask_registration_internet()
                else:
                    run_coroutine_threadsafe(self.bot_say("Respuesta no válida. Escribe: 'Sí crónica', 'Sí temporal' o 'No'."), loop)
                return

            if self.state == "reg_condicion_detalle":
                detalle = text.strip()
                if len(detalle) < 2:
                    run_coroutine_threadsafe(self.bot_say("Por favor especifica brevemente tu condición (ej: diabetes, hipertensión)."), loop)
                else:
                    self.answers["condicion_detalle"] = detalle
                    # empatía
                    run_coroutine_threadsafe(self.bot_say(f"Entiendo — {detalle}. Gracias por compartir, lo tendré en cuenta en futuras recomendaciones."), loop)
                    # pequeña pausa y continuar a internet
                    run_coroutine_threadsafe(_sleep_and_call(0.35, self.ask_registration_internet), loop)
                return

            if self.state == "reg_internet":
                if txt in {"siempre", "si", "siempre (wifi o datos)"}:
                    self.answers["internet"] = "Siempre"
                    self.ask_registration_dispositivo()
                elif txt in {"mayormente", "mayormente (con intermitencias)"}:
                    self.answers["internet"] = "Mayormente"
                    self.ask_registration_dispositivo()
                elif txt in {"ocasionalmente", "ocasional", "ocasionalmente (con intermitencias)"}:
                    self.answers["internet"] = "Ocasionalmente"
                    self.ask_registration_dispositivo()
                elif txt in {"casi nunca"}:
                    self.answers["internet"] = "Casi nunca"
                    self.ask_registration_dispositivo()
                else:
                    run_coroutine_threadsafe(self.bot_say("Por favor elige: Siempre / Mayormente / Ocasionalmente / Casi nunca."), loop)
                return

            if self.state == "reg_dispositivo":
                if "android" in txt:
                    self.answers["dispositivo"] = "Android"
                    self.ask_registration_password()
                elif "iphone" in txt or "ios" in txt:
                    self.answers["dispositivo"] = "iPhone"
                    self.ask_registration_password()
                elif "bas" in txt or "basico" in txt:
                    self.answers["dispositivo"] = "Básico"
                    self.ask_registration_password()
                elif "table" in txt or "tablet" in txt:
                    self.answers["dispositivo"] = "Tableta"
                    self.ask_registration_password()
                elif "otro" in txt:
                    self.answers["dispositivo"] = text.strip()
                    self.ask_registration_password()
                else:
                    run_coroutine_threadsafe(self.bot_say("Respuesta no válida. Escribe Android / iPhone / Básico / Tableta / Otro."), loop)
                return

            if self.state == "reg_password":
                pw_val = text.strip()
                if len(pw_val) < 4:
                    run_coroutine_threadsafe(self.bot_say("La contraseña debe tener al menos 4 caracteres. Intenta otra."), loop)
                else:
                    # Guardamos contraseña en memory y enviamos a registro
                    self.answers["password"] = pw_val
                    run_coroutine_threadsafe(self.bot_say("Perfecto. Envío tus datos y te confirmo."), loop)
                    run_coroutine_threadsafe(self.complete_registration(), loop)
                return

            # si estamos esperando login response
            if self.state == "login_wait":
                run_coroutine_threadsafe(self.bot_say("Todavía estoy validando tus credenciales, por favor espera un momento."), loop)
                return

            # fallback: reiniciar
            run_coroutine_threadsafe(self.bot_say("No entendí eso. ¿Tienes cuenta? Responde Sí o No."), loop)
            self.state = "have_account"

        except Exception as exc:
            # capturamos excepciones para evitar que el hilo principal muera
            log_debug(f"Error en process_input: {exc}\n{traceback.format_exc()}")
            run_coroutine_threadsafe(self.bot_say("Ocurrió un error interno procesando tu mensaje. Intentemos de nuevo. ¿Tienes cuenta? Responde Sí o No."), loop)
            self.state = "have_account"

    # ---------------- acciones async con n8n ----------------
    async def attempt_login(self, username: str, password: str):
        """
        Envia credenciales a LOGIN_N8N_URL. Se espera JSON {'ok': True/False, 'message': ...}
        Si el endpoint devuelve otro formato, ajusta el parseo.
        """
        try:
            self.state = "login_wait"
            await self.bot_say("Validando credenciales, espera un momento...")
            async with httpx.AsyncClient(timeout=15) as client:
                payload = {"action": "login", "username": username, "password": password}
                try:
                    resp = await client.post(LOGIN_N8N_URL, json=payload)
                except Exception as e:
                    await self.bot_say(f"Error conectando al servidor de autenticación: {e}")
                    self.state = "have_account"
                    await asyncio.sleep(0.3)
                    await self.bot_say("¿Tienes una cuenta? Responde Sí o No.")
                    return

                try:
                    data = resp.json()
                except Exception:
                    # No JSON: asumimos ok por status 200/201 o falso
                    data = {"ok": resp.status_code in (200, 201), "message": resp.text}

            if data.get("ok"):
                await self.bot_say("✔️ Inicio de sesión correcto. ¡Bienvenido de nuevo!")
                self.state = "logged_in"
                await asyncio.sleep(0.45)
                # llamar on_finish - si es coroutine lo await, si no lo llama en sync
                if self.on_finish:
                    if asyncio.iscoroutinefunction(self.on_finish):
                        await self.on_finish()
                    else:
                        try:
                            self.on_finish()
                        except Exception as e:
                            log_debug(f"Error calling on_finish: {e}")
                return
            else:
                msg = data.get("message") or "Usuario o contraseña incorrectos."
                await self.bot_say(f"❌ {msg} Por favor intenta nuevamente.")
                self.state = "have_account"
                await asyncio.sleep(0.3)
                await self.bot_say("¿Tienes una cuenta? Responde Sí o No.")
                return
        except Exception as e:
            await self.bot_say(f"Error validando credenciales: {e}")
            self.state = "have_account"
            await asyncio.sleep(0.3)
            await self.bot_say("¿Tienes una cuenta? Responde Sí o No.")
            return

    async def complete_registration(self):
        """
        Envia los datos de self.answers a REGISTER_N8N_URL.
        payload: { action: "register", data: self.answers }
        """
        try:
            await self.bot_say("Enviando tus datos de registro... espera un momento.")
            async with httpx.AsyncClient(timeout=20) as client:
                payload = {"action": "register", "data": self.answers}
                try:
                    resp = await client.post(REGISTER_N8N_URL, json=payload)
                except Exception as e:
                    await self.bot_say(f"Error conectando con el servidor de registro: {e}")
                    self.state = "have_account"
                    await asyncio.sleep(0.3)
                    await self.bot_say("¿Tienes una cuenta? Responde Sí o No.")
                    return

                try:
                    data = resp.json()
                except Exception:
                    data = {"ok": resp.status_code in (200, 201), "message": resp.text}

            if data.get("ok", True):
                await self.bot_say("✅ Registro completado. Gracias por unirte a VE+.")
                # Mostrar al usuario brevemente su usuario sugerido y recordarle no compartir contraseña
                await self.bot_say(f"Tu nombre de usuario es: {self.answers.get('username', '(no disponible)')}")
                # No mostramos la contraseña real en el chat; mostramos asteriscos
                masked_pw = "*" * len(self.answers.get("password", ""))
                await self.bot_say(f"Contraseña: {masked_pw} (se ha enviado de forma segura).")
                await asyncio.sleep(0.6)
                # Llamar on_finish para que main.py muestre la app principal
                if self.on_finish:
                    if asyncio.iscoroutinefunction(self.on_finish):
                        await self.on_finish()
                    else:
                        try:
                            self.on_finish()
                        except Exception as e:
                            log_debug(f"Error calling on_finish after register: {e}")
                return
            else:
                msg = data.get("message", "Hubo un problema en el registro.")
                await self.bot_say(f"❌ {msg} - Intentemos de nuevo.")
                self.state = "have_account"
                await asyncio.sleep(0.3)
                await self.bot_say("¿Tienes una cuenta? Responde Sí o No.")
                return
        except Exception as e:
            await self.bot_say(f"Error al enviar registro: {e}")
            self.state = "have_account"
            await asyncio.sleep(0.3)
            await self.bot_say("¿Tienes una cuenta? Responde Sí o No.")
            return

    # ---------------- envío de mensaje del usuario (handler) ----------------
    def _send(self, e: ft.ControlEvent):
        """
        Evento asociado al botón envíar o al submit del TextField.
        - Muestra el mensaje del usuario (enmascara si estamos en password states)
        - Limpia el TextField
        - Llama a process_input con el valor real (no enmascarado)
        """
        if not self.input_ref.current:
            return
        text = (self.input_ref.current.value or "").strip()
        if not text:
            return

        # mostrar masked en la UI únicamente si estamos en estados de password
        display_text = text
        if self.state in {"reg_password", "login_password"}:
            display_text = "*" * len(text)

        # limpiar campo
        self.input_ref.current.value = ""
        # append del usuario
        self.append("user", display_text)
        # procesar valor real
        try:
            self.process_input(text)
        except Exception as e:
            log_debug(f"Error en process_input (desde _send): {e}\n{traceback.format_exc()}")
            run_coroutine_threadsafe(self.bot_say("Ocurrió un error procesando tu mensaje. Intenta nuevamente."), loop)

    # ---------------- construcción UI ----------------
    def build(self) -> ft.Control:
        """
        Construye y devuelve el control principal del Chatbot.
        - Ajusta padding vertical para que el primer mensaje no esté pegado.
        """
        lv = ft.ListView(ref=self.list_ref, controls=[], spacing=12, expand=True, auto_scroll=True,
                         padding=ft.padding.symmetric(horizontal=10, vertical=16))

        input_box = ft.Row(
            [
                ft.TextField(ref=self.input_ref, hint_text="Escribe tu respuesta...",
                             expand=True, border_radius=24, filled=True,
                             bgcolor="#263238", color=ft.Colors.WHITE,
                             cursor_color=ft.Colors.BLUE, content_padding=12,
                             on_submit=self._send,
                             password=False,  # ver en claro mientras escribe
                             autofocus=True,
                             ),
                ft.IconButton(ft.Icons.SEND_ROUNDED, tooltip="Enviar", icon_color=ft.Colors.WHITE,
                              bgcolor=ft.Colors.BLUE, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
                              on_click=self._send),
            ],
            spacing=8,
        )

        body = ft.Column([lv, input_box], spacing=10, expand=True)
        wrap = ft.Container(body, padding=ft.padding.only(left=8, right=8, bottom=10), expand=True)
        return ft.Column([wrap], spacing=0, expand=True)

# ======================================================================
# LoginChatbot Miskito
# ======================================================================
class LoginChatbotMiskito:
    """
    Chatbot para login/registro con Flet.

    Integración con Main:
      - main.py crea LoginChatbot(page, on_finish=launch_app)
      - on_finish se llamará cuando login/registro sean exitosos.
    """

    def __init__(self, page: ft.Page, on_finish: Optional[Callable[[], Any]] = None):
        self.page = page
        self.on_finish = on_finish

        # UI refs
        self.list_ref: ft.Ref[ft.ListView] = ft.Ref[ft.ListView]()
        self.input_ref: ft.Ref[ft.TextField] = ft.Ref[ft.TextField]()
        self.typing_ref: ft.Ref[ft.Container] = ft.Ref[ft.Container]()

        # estado
        self.state: str = "initial"
        self.answers: dict[str, Any] = {}
        self.pending_login: dict[str, str] = {}
        self._speak_lock = asyncio.Lock()
        self._last_bot_task = None

        # opciones válidas (normalizadas)
        self.valid_generos = {"lih", "lihna", "mismu", "mismu", "wala", "na yus"}
        self.valid_zonas = {"tawan", "periurbano", "tara"}
        self.valid_internet = {"taki", "lilan", "yutkaia", "kumi"}
        self.valid_dispositivos = {"android", "iphone", "basico", "tableta", "otro", "ios", "ipad"}

        # Inicia el chat en background
        run_coroutine_threadsafe(self.start_chat(), loop)

    # ---------------- UI helpers ----------------
    def _bubble(self, sender: str, text: str) -> ft.Row:
        """
        Construye un bubble simple para el ListView del chat.
        """
        is_user = (sender == "user")
        bg_color = "#4FC3F7" if is_user else "#E6F7FF"
        fg_color = ft.Colors.WHITE if is_user else ft.Colors.BLACK
        ts_color = ft.Colors.with_opacity(0.7, fg_color)
        cont = ft.Container(
            content=ft.Column(
                [
                    ft.Text(text, size=14, color=fg_color, selectable=True, no_wrap=False),
                    ft.Text(datetime.datetime.now().strftime("%H:%M"), size=10, color=ts_color),
                ],
                spacing=4,
                tight=True,
            ),
            bgcolor=bg_color,
            padding=ft.padding.all(12),
            border_radius=18,
            margin=ft.margin.only(left=60 if is_user else 8, right=8 if is_user else 60, top=2, bottom=2),
            shadow=ft.BoxShadow(blur_radius=6, spread_radius=1, color=ft.Colors.with_opacity(0.15, "black")),
        )
        return ft.Row([ft.Container(content=cont, expand=True)], alignment=ft.MainAxisAlignment.END if is_user else ft.MainAxisAlignment.START)

    def append(self, sender: str, text: str):
        """
        Añade un mensaje al ListView y fuerza update de la página.
        """
        if self.list_ref.current:
            self.list_ref.current.controls.append(self._bubble(sender, text))
            self.list_ref.current.scroll_to(offset=99999, duration=200)
        self.page.update()

    # ---------------- typing indicator ----------------
    def show_typing(self, show: bool):
        """
        Muestra o quita el indicador 'Escribiendo...'.
        Protegemos con comprobaciones para no añadir duplicados.
        """
        if not self.list_ref.current:
            return
        if show:
            if not (self.typing_ref.current and self.typing_ref.current in self.list_ref.current.controls):
                bubble = ft.Container(
                    ref=self.typing_ref,
                    content=ft.Row([ft.ProgressRing(width=16, height=16, stroke_width=2, color=ft.Colors.BLUE),
                                    ft.Text("Mairin...", size=12, color=ft.Colors.GREY)], spacing=8),
                    padding=ft.padding.all(10),
                    border_radius=16,
                    bgcolor=ft.Colors.BLUE_GREY_800,
                    margin=ft.margin.only(right=120, left=8),
                )
                self.list_ref.current.controls.append(bubble)
        else:
            if self.typing_ref.current and self.typing_ref.current in self.list_ref.current.controls:
                try:
                    self.list_ref.current.controls.remove(self.typing_ref.current)
                except Exception:
                    # fallback: eliminar todos los que parezcan typing_ref
                    self.list_ref.current.controls = [c for c in self.list_ref.current.controls if c is not self.typing_ref.current]
        self.list_ref.current.scroll_to(offset=99999, duration=200)
        self.page.update()

    async def bot_say(self, text: str, delay: float | None = None, first: bool = False):
        """
        Secuencia segura para que el bot "escriba" y luego muestre el mensaje.
        Usamos un lock para evitar solapamientos y para asegurarnos que 'Escribiendo...'
        siempre sea limpiado correctamente.
        """
        async with self._speak_lock:
            if delay is None:
                delay = random.uniform(1.1, 2.0)
            # mostrar typing
            self.show_typing(True)
            await asyncio.sleep(delay)
            # quitar typing
            self.show_typing(False)
            # breve pausa para lograr efecto natural
            await asyncio.sleep(0.18)
            # agregar mensaje
            if self.list_ref.current:
                bubble = self._bubble("bot", text)
                if first and isinstance(bubble, ft.Row):
                    if isinstance(bubble.controls[0], ft.Container):
                        bubble.controls[0].margin = ft.margin.only(top=36, left=8, right=8, bottom=2)
                self.list_ref.current.controls.append(bubble)
                self.list_ref.current.scroll_to(offset=99999, duration=200)
            self.page.update()

    # ---------------- flujo principal ----------------
    async def start_chat(self):
        """
        Arranca la conversación: saludo y primera pregunta.
        """
        await self.bot_say("👋 ¡Hola! VE+ ai taba, u login o register warkkaia dukia.", first=True)
        await self.bot_say("Mairin dukiara, aiwa account wina nan ba dakbi. 'Ayam' o 'Apia' diara yus.")
        self.state = "have_account"

    # ----------------- ASK helpers (sincrónicos) -----------------
    # Cada helper cambia el estado y lanza un bot_say de forma segura (pasan coroutine a run_coroutine_threadsafe).
    def ask_login_username(self):
        self.state = "login_username"
        run_coroutine_threadsafe(self.bot_say("Ayas — username diara yus (i.e., Augusto_Ascencio)."), loop)

    def ask_login_password(self):
        self.state = "login_password"
        # No activamos modo password en el TextField: el usuario ve lo que escribe.
        run_coroutine_threadsafe(self.bot_say("Naha bila password diara yus (chat wina ba masked)."), loop)

    def ask_registration_first_name(self):
        self.state = "reg_first_name"
        run_coroutine_threadsafe(self.bot_say("Ayas. Ba wan name diara?"), loop)

    def ask_registration_last_name(self):
        self.state = "reg_last_name"
        run_coroutine_threadsafe(self.bot_say("Perfecto. Ba wan last name diara?"), loop)

    def ask_registration_age(self):
        self.state = "reg_edad"
        run_coroutine_threadsafe(self.bot_say(f"Glad, {self.answers.get('first_name','')}. Wan sa age (i.e., 30)?"), loop)

    def ask_registration_genero(self):
        self.state = "reg_genero"
        run_coroutine_threadsafe(self.bot_say("Wan sa gender (Lihna / Mismu / Wala)?"), loop)

    def ask_registration_zona(self):
        self.state = "reg_zona"
        run_coroutine_threadsafe(self.bot_say("Tawan ba kumi nani (Tawan / Periurbano / Tara)?"), loop)

    def ask_registration_condicion(self):
        self.state = "reg_condicion"
        run_coroutine_threadsafe(self.bot_say("Health condition nani ba dukiara ('Ayam crónica', 'Ayam temporal', o 'Apia')."), loop)

    def ask_registration_condicion_detalle(self):
        self.state = "reg_condicion_detalle"
        run_coroutine_threadsafe(self.bot_say("Ayas. Wan sa condition (i.e., diabetes, hipertensión, asma)?"), loop)

    def ask_registration_internet(self):
        self.state = "reg_internet"
        run_coroutine_threadsafe(self.bot_say("Internet wina nan ba dukiara (Taki / Lilan / Yutkaia / Kumi)?"), loop)

    def ask_registration_dispositivo(self):
        self.state = "reg_dispositivo"
        run_coroutine_threadsafe(self.bot_say("Wan sa device wina nan ba dukiara (Android / iPhone / Básico / Tableta / Otro)?"), loop)

    def ask_registration_password(self):
        # No activar modo password del TextField (usuario lo ve al escribir).
        self.state = "reg_password"
        run_coroutine_threadsafe(self.bot_say("Naha bila password (se mostrará enmascarada en el chat)."), loop)

    # ----------------- normalización y validación -----------------
    def _normalize(self, text: str) -> str:
        return text.strip().lower()

    # ----------------- procesamiento de la entrada del usuario -----------------
    def process_input(self, text: str):
        """
        Lógica que determina qué hacer con el texto del usuario en función del estado.
        Nota: esta función es síncrona (no coroutine) y lanza coroutines al loop de fondo cuando es necesario.
        """
        try:
            txt = self._normalize(text)
            # ------------- Estados -------------
            if self.state == "have_account":
                if txt in {"ayam"}:
                    self.ask_login_username()
                elif txt in {"apia"}:
                    self.answers.clear()
                    self.ask_registration_first_name()
                else:
                    run_coroutine_threadsafe(self.bot_say("'Ayam' o 'Apia' diara yus."), loop)
                return

            # ---- LOGIN FLOW ----
            if self.state == "login_username":
                # almacenamos tal cual (puedes normalizar a lower si lo prefieres)
                self.pending_login["username"] = text.strip()
                self.ask_login_password()
                return

            if self.state == "login_password":
                self.pending_login["password"] = text
                # lanzamos validación en background; attempt_login es coroutine
                run_coroutine_threadsafe(self.attempt_login(self.pending_login["username"], self.pending_login["password"]), loop)
                self.state = "login_wait"
                return

            # ---- REGISTER FLOW ----
            if self.state == "reg_first_name":
                candidate = text.strip()
                if len(candidate) < 2:
                    run_coroutine_threadsafe(self.bot_say("Nani name ba 2 letters wina nan."), loop)
                    return
                self.answers["first_name"] = candidate.strip().capitalize()
                self.ask_registration_last_name()
                return

            if self.state == "reg_last_name":
                candidate = text.strip()
                if len(candidate) < 2:
                    run_coroutine_threadsafe(self.bot_say("Nani last name ba 2 letters wina nan."), loop)
                    return
                self.answers["last_name"] = candidate.strip().capitalize()

                # Construir username: PrimerNombre_PrimerApellido
                first_clean = self.answers.get("first_name", "").replace(" ", "_")
                last_clean = self.answers.get("last_name", "").replace(" ", "_")
                username_combined = f"{first_clean}_{last_clean}"
                self.answers["username"] = username_combined

                run_coroutine_threadsafe(self.bot_say(f"Perfecto — wan sa username ba {username_combined}."), loop)
                # pausa breve y seguir con edad (usar coroutine para pausar + llamar)
                run_coroutine_threadsafe(_sleep_and_call(0.45, self.ask_registration_age), loop)
                return

            if self.state == "reg_edad":
                try:
                    edad_val = int(text.strip())
                    if not (5 <= edad_val <= 120):
                        raise ValueError()
                    self.answers["edad"] = edad_val
                    self.ask_registration_genero()
                except Exception:
                    run_coroutine_threadsafe(self.bot_say("Age ba numbers wina (i.e., 30). 5 o 120 wina nan."), loop)
                return

            if self.state == "reg_genero":
                if txt in {"lih", "lihna"}:
                    self.answers["genero"] = "Femenino"
                    self.ask_registration_zona()
                elif txt in {"mismu"}:
                    self.answers["genero"] = "Masculino"
                    self.ask_registration_zona()
                elif txt in {"wala", "na yus"}:
                    self.answers["genero"] = "Otro"
                    self.ask_registration_zona()
                else:
                    run_coroutine_threadsafe(self.bot_say("Diara ba valid (Lihna, Mismu, o Wala)."), loop)
                return

            if self.state == "reg_zona":
                if txt in {"tawan", "periurbano", "tara"}:
                    self.answers["zona"] = text.strip().capitalize()
                    self.ask_registration_condicion()
                else:
                    run_coroutine_threadsafe(self.bot_say("Tawan / Periurbano / Tara diara yus."), loop)
                return

            if self.state == "reg_condicion":
                if "ayam" in txt:
                    if "cronica" in txt:
                        self.answers["condicion"] = "Sí - crónica"
                        self.ask_registration_condicion_detalle()
                    elif "temporal" in txt:
                        self.answers["condicion"] = "Sí - temporal"
                        self.ask_registration_condicion_detalle()
                    else:
                        run_coroutine_threadsafe(self.bot_say("¿Ba crónica o temporal? 'Ayam crónica' o 'Ayam temporal'."), loop)
                elif "apia" in txt:
                    self.answers["condicion"] = "No"
                    self.ask_registration_internet()
                else:
                    run_coroutine_threadsafe(self.bot_say("Diara ba valid. 'Ayam crónica', 'Ayam temporal' o 'Apia'."), loop)
                return

            if self.state == "reg_condicion_detalle":
                detalle = text.strip()
                if len(detalle) < 2:
                    run_coroutine_threadsafe(self.bot_say("Condition wina (i.e., diabetes, hipertensión)."), loop)
                else:
                    self.answers["condicion_detalle"] = detalle
                    # empatía
                    run_coroutine_threadsafe(self.bot_say(f"Ayas — {detalle}. Gracias."), loop)
                    # pequeña pausa y continuar a internet
                    run_coroutine_threadsafe(_sleep_and_call(0.35, self.ask_registration_internet), loop)
                return

            if self.state == "reg_internet":
                if txt in {"taki", "always"}:
                    self.answers["internet"] = "Siempre"
                    self.ask_registration_dispositivo()
                elif txt in {"lilan"}:
                    self.answers["internet"] = "Mayormente"
                    self.ask_registration_dispositivo()
                elif txt in {"yutkaia"}:
                    self.answers["internet"] = "Ocasionalmente"
                    self.ask_registration_dispositivo()
                elif txt in {"kumi"}:
                    self.answers["internet"] = "Casi nunca"
                    self.ask_registration_dispositivo()
                else:
                    run_coroutine_threadsafe(self.bot_say("Taki / Lilan / Yutkaia / Kumi diara yus."), loop)
                return

            if self.state == "reg_dispositivo":
                if "android" in txt:
                    self.answers["dispositivo"] = "Android"
                    self.ask_registration_password()
                elif "iphone" in txt or "ios" in txt:
                    self.answers["dispositivo"] = "iPhone"
                    self.ask_registration_password()
                elif "bas" in txt or "basico" in txt:
                    self.answers["dispositivo"] = "Básico"
                    self.ask_registration_password()
                elif "table" in txt or "tablet" in txt:
                    self.answers["dispositivo"] = "Tableta"
                    self.ask_registration_password()
                elif "otro" in txt:
                    self.answers["dispositivo"] = text.strip()
                    self.ask_registration_password()
                else:
                    run_coroutine_threadsafe(self.bot_say("Diara ba valid. Android / iPhone / Básico / Tableta / Otro."), loop)
                return

            if self.state == "reg_password":
                pw_val = text.strip()
                if len(pw_val) < 4:
                    run_coroutine_threadsafe(self.bot_say("Password ba 4 characters wina nan. Taki diara yus."), loop)
                else:
                    # Guardamos contraseña en memory y enviamos a registro
                    self.answers["password"] = pw_val
                    run_coroutine_threadsafe(self.bot_say("Perfecto. Warkkaia bila."), loop)
                    run_coroutine_threadsafe(self.complete_registration(), loop)
                return

            # si estamos esperando login response
            if self.state == "login_wait":
                run_coroutine_threadsafe(self.bot_say("Credenciales ba takan dukiara."), loop)
                return

            # fallback: reiniciar
            run_coroutine_threadsafe(self.bot_say("Naha bila. ¿Wan sa cuenta? 'Ayam' o 'Apia'."), loop)
            self.state = "have_account"

        except Exception as exc:
            # capturamos excepciones para evitar que el hilo principal muera
            log_debug(f"Error en process_input: {exc}\n{traceback.format_exc()}")
            run_coroutine_threadsafe(self.bot_say("Error. Taki diara yus. ¿Wan sa cuenta? 'Ayam' o 'Apia'."), loop)
            self.state = "have_account"

    # ---------------- acciones async con n8n ----------------
    async def attempt_login(self, username: str, password: str):
        """
        Envia credenciales a LOGIN_N8N_URL. Se espera JSON {'ok': True/False, 'message': ...}
        Si el endpoint devuelve otro formato, ajusta el parseo.
        """
        try:
            self.state = "login_wait"
            await self.bot_say("Credenciales ba takan dukiara...")
            async with httpx.AsyncClient(timeout=15) as client:
                payload = {"action": "login", "username": username, "password": password}
                try:
                    resp = await client.post(LOGIN_N8N_URL, json=payload)
                except Exception as e:
                    await self.bot_say(f"Error server wina: {e}")
                    self.state = "have_account"
                    await asyncio.sleep(0.3)
                    await self.bot_say("¿Wan sa cuenta? 'Ayam' o 'Apia'.")
                    return

                try:
                    data = resp.json()
                except Exception:
                    # No JSON: asumimos ok por status 200/201 o falso
                    data = {"ok": resp.status_code in (200, 201), "message": resp.text}

            if data.get("ok"):
                await self.bot_say("✔️ Login correcto. Welcome back!")
                self.state = "logged_in"
                await asyncio.sleep(0.45)
                # llamar on_finish - si es coroutine lo await, si no lo llama en sync
                if self.on_finish:
                    if asyncio.iscoroutinefunction(self.on_finish):
                        await self.on_finish()
                    else:
                        try:
                            self.on_finish()
                        except Exception as e:
                            log_debug(f"Error calling on_finish: {e}")
                return
            else:
                msg = data.get("message") or "Username o password warkkaia."
                await self.bot_say(f"❌ {msg} Taki diara yus.")
                self.state = "have_account"
                await asyncio.sleep(0.3)
                await self.bot_say("¿Wan sa cuenta? 'Ayam' o 'Apia'.")
                return
        except Exception as e:
            await self.bot_say(f"Error credentials: {e}")
            self.state = "have_account"
            await asyncio.sleep(0.3)
            await self.bot_say("¿Wan sa cuenta? 'Ayam' o 'Apia'.")
            return

    async def complete_registration(self):
        """
        Envia los datos de self.answers a REGISTER_N8N_URL.
        payload: { action: "register", data: self.answers }
        """
        try:
            await self.bot_say("Register data sending...")
            async with httpx.AsyncClient(timeout=20) as client:
                payload = {"action": "register", "data": self.answers}
                try:
                    resp = await client.post(REGISTER_N8N_URL, json=payload)
                except Exception as e:
                    await self.bot_say(f"Error register server wina: {e}")
                    self.state = "have_account"
                    await asyncio.sleep(0.3)
                    await self.bot_say("¿Wan sa cuenta? 'Ayam' o 'Apia'.")
                    return

                try:
                    data = resp.json()
                except Exception:
                    data = {"ok": resp.status_code in (200, 201), "message": resp.text}

            if data.get("ok", True):
                await self.bot_say("✅ Register complete. VE+ wina welcome.")
                # Mostrar al usuario brevemente su usuario sugerido y recordarle no compartir contraseña
                await self.bot_say(f"Username ba: {self.answers.get('username', '(no disponible)')}")
                # No mostramos la contraseña real en el chat; mostramos asteriscos
                masked_pw = "*" * len(self.answers.get("password", ""))
                await self.bot_say(f"Password: {masked_pw} (safe).")
                await asyncio.sleep(0.6)
                # Llamar on_finish para que main.py muestre la app principal
                if self.on_finish:
                    if asyncio.iscoroutinefunction(self.on_finish):
                        await self.on_finish()
                    else:
                        try:
                            self.on_finish()
                        except Exception as e:
                            log_debug(f"Error calling on_finish after register: {e}")
                return
            else:
                msg = data.get("message", "Register wina problem.")
                await self.bot_say(f"❌ {msg} - Taki diara yus.")
                self.state = "have_account"
                await asyncio.sleep(0.3)
                await self.bot_say("¿Wan sa cuenta? 'Ayam' o 'Apia'.")
                return
        except Exception as e:
            await self.bot_say(f"Error register wina: {e}")
            self.state = "have_account"
            await asyncio.sleep(0.3)
            await self.bot_say("¿Wan sa cuenta? 'Ayam' o 'Apia'.")
            return

    # ---------------- envío de mensaje del usuario (handler) ----------------
    def _send(self, e: ft.ControlEvent):
        """
        Evento asociado al botón envíar o al submit del TextField.
        - Muestra el mensaje del usuario (enmascara si estamos en password states)
        - Limpia el TextField
        - Llama a process_input con el valor real (no enmascarado)
        """
        if not self.input_ref.current:
            return
        text = (self.input_ref.current.value or "").strip()
        if not text:
            return

        # mostrar masked en la UI únicamente si estamos en estados de password
        display_text = text
        if self.state in {"reg_password", "login_password"}:
            display_text = "*" * len(text)

        # limpiar campo
        self.input_ref.current.value = ""
        # append del usuario
        self.append("user", display_text)
        # procesar valor real
        try:
            self.process_input(text)
        except Exception as e:
            log_debug(f"Error en process_input (desde _send): {e}\n{traceback.format_exc()}")
            run_coroutine_threadsafe(self.bot_say("Error. Taki diara yus."), loop)

    # ---------------- construcción UI ----------------
    def build(self) -> ft.Control:
        """
        Construye y devuelve el control principal del Chatbot.
        - Ajusta padding vertical para que el primer mensaje no esté pegado.
        """
        lv = ft.ListView(ref=self.list_ref, controls=[], spacing=12, expand=True, auto_scroll=True,
                         padding=ft.padding.symmetric(horizontal=10, vertical=16))

        input_box = ft.Row(
            [
                ft.TextField(ref=self.input_ref, hint_text="Wan sa response...",
                             expand=True, border_radius=24, filled=True,
                             bgcolor="#263238", color=ft.Colors.WHITE,
                             cursor_color=ft.Colors.BLUE, content_padding=12,
                             on_submit=self._send,
                             password=False,  # ver en claro mientras escribe
                             autofocus=True,
                             ),
                ft.IconButton(ft.Icons.SEND_ROUNDED, tooltip="Warkkaia", icon_color=ft.Colors.WHITE,
                              bgcolor=ft.Colors.BLUE, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
                              on_click=self._send),
            ],
            spacing=8,
        )

        body = ft.Column([lv, input_box], spacing=10, expand=True)
        wrap = ft.Container(body, padding=ft.padding.only(left=8, right=8, bottom=10), expand=True)
        return ft.Column([wrap], spacing=0, expand=True)