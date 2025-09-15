from __future__ import annotations

import asyncio, datetime, threading, httpx, json, os, random
import flet as ft
from asyncio import run_coroutine_threadsafe
from pathlib import Path

# ===== Configuración =====
N8N_WEBHOOK_URL = "######https://augustocraft02.app.n8n.cloud/webhook/cfc33be7-9e23-4b29-93b4-d1f893213f7e"
#USER_DATA_FILE = os.path.join(str(Path.home()), "user_data.json")

# ===== Bucle asincrónico en segundo plano =====
loop = asyncio.new_event_loop()
def start_loop(lp: asyncio.AbstractEventLoop):
    asyncio.set_event_loop(lp)
    lp.run_forever()
threading.Thread(target=start_loop, args=(loop,), daemon=True).start()


class LoginChatbot:
    """Chatbot para registro/inicio de sesión con typing natural (sin audio)."""

    def __init__(self, page: ft.Page, on_finish=None):
        self.page = page
        self.on_finish = on_finish
        self.list_ref: ft.Ref[ft.ListView] = ft.Ref[ft.ListView]()
        self.input_ref: ft.Ref[ft.TextField] = ft.Ref[ft.TextField]()
        self.typing_ref: ft.Ref[ft.Container] = ft.Ref[ft.Container]()
        self.messages: list[dict] = []
        self.answers: dict = {}
        self.step = 0

        # Conversación más natural
        self.questions = [
            ("¡Hey! Bienvenido 😃, dime, ¿cómo te llamas?", "nombre"),
            ("Genial, {nombre}! 🙌 ¿Y qué edad tienes?", "edad"),
            ("Perfecto, gracias. Ahora dime, ¿cómo te identificas? (Masculino / Femenino / Otro)", "genero"),
            ("Interesante 👍. ¿En qué zona vives? (Urbano / Periurbano / Rural)", "zona"),
            ("Cuéntame, ¿tienes alguna condición de salud que debamos monitorear? (Sí crónica / Sí temporal / No)", "condicion"),
            ("Ok, entendido. ¿Cómo es tu acceso a Internet? (Siempre / Mayormente / Ocasional / Casi nunca)", "internet"),
            ("Y dime, ¿qué dispositivo usas más seguido? (Android / iPhone / Básico / Tableta / Otro)", "dispositivo"),
            ("Perfecto 👌. Solo falta que crees una contraseña para tu cuenta 🔑", "password"),
        ]

        # Iniciar con bienvenida natural
        run_coroutine_threadsafe(self.start_chat(), loop)

    # ---------------- Utilidades UI ------------------
    def _bubble(self, sender: str, text: str) -> ft.Row:
        is_user = sender == "user"
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
            margin=ft.margin.only(
                left=60 if is_user else 8,
                right=8 if is_user else 60,
                top=2,
                bottom=2,
            ),
            shadow=ft.BoxShadow(blur_radius=6, spread_radius=1, color=ft.Colors.with_opacity(0.15, "black")),
        )

        return ft.Row(
            [ft.Container(content=cont, expand=True)],
            alignment=ft.MainAxisAlignment.END if is_user else ft.MainAxisAlignment.START,
        )

    def append(self, sender: str, text: str):
        if self.list_ref.current:
            self.list_ref.current.controls.append(self._bubble(sender, text))
            self.list_ref.current.scroll_to(offset=99999, duration=200)
        self.page.update()

    # ---------------- Indicador escribiendo -------------------
    def show_typing(self, show: bool):
        if not self.list_ref.current:
            return
        if show:
            bubble = ft.Container(
                ref=self.typing_ref,
                content=ft.Row(
                    [ft.ProgressRing(width=16, height=16, stroke_width=2, color=ft.Colors.BLUE),
                     ft.Text("Escribiendo...", size=12, color=ft.Colors.GREY)],
                    spacing=8,
                ),
                padding=ft.padding.all(10),
                border_radius=16,
                bgcolor=ft.Colors.BLUE_GREY_800,
                margin=ft.margin.only(right=120, left=8),
            )
            self.list_ref.current.controls.append(bubble)
        else:
            if self.typing_ref.current and self.typing_ref.current in self.list_ref.current.controls:
                self.list_ref.current.controls.remove(self.typing_ref.current)
        self.list_ref.current.scroll_to(offset=99999, duration=200)
        self.page.update()

    async def bot_say(self, text: str, delay: float | None = None, first: bool = False):
        if delay is None:
            delay = random.uniform(1.3, 2.3)

        self.show_typing(True)
        await asyncio.sleep(delay)

        self.show_typing(False)
        await asyncio.sleep(0.25)

        if self.list_ref.current:
            bubble = self._bubble("bot", text)
            if first and isinstance(bubble, ft.Row):
                if isinstance(bubble.controls[0], ft.Container):
                    bubble.controls[0].margin = ft.margin.only(top=40, left=8, right=8, bottom=2)
            self.list_ref.current.controls.append(bubble)
            self.list_ref.current.scroll_to(offset=99999, duration=200)

        self.page.update()

    # ---------------- Flujo preguntas -----------    
    async def start_chat(self):
        await self.bot_say("👋 ¡Hola! Soy VE+.", first=True)
        await self.bot_say("Te ayudaré a crear tu cuenta en unos pasos sencillos 🙌.")
        await asyncio.sleep(0.8)
        self.ask_next()

    def ask_next(self):
        if self.step < len(self.questions):
            q, key = self.questions[self.step]
            text = q.format(**self.answers)

            async def ask():
                await self.bot_say(text)

            run_coroutine_threadsafe(ask(), loop)
        else:
            run_coroutine_threadsafe(self.finish_registration(), loop)

    def handle_answer(self, text: str):
        if self.step >= len(self.questions):
            return

        key = self.questions[self.step][1]
        self.answers[key] = text
        self.step += 1

        compliments = ["¡Genial 😃!", "Perfecto, gracias 🙏.", "👌 Muy bien.", "🚀 Súper, sigamos."]

        async def sequence():
            await self.bot_say(compliments[self.step % len(compliments)])
            await asyncio.sleep(0.6)
            self.ask_next()

        run_coroutine_threadsafe(sequence(), loop)

    # ---------------- Finalizar registro -------
    async def finish_registration(self):
        await self.bot_say("✅ Registro completado. ¡Bienvenido a VE+!")
       # with open(USER_DATA_FILE, "w", encoding="utf-8") as f:
            #json.dump(self.answers, f, ensure_ascii=False, indent=2)

        run_coroutine_threadsafe(self.send_to_n8n(), loop)

        if self.on_finish:
            self.on_finish()

    async def send_to_n8n(self):
        try:
            async with httpx.AsyncClient(timeout=20) as client:
                resp = await client.post(N8N_WEBHOOK_URL, json=self.answers)
                await asyncio.sleep(0)
                print("Enviado a n8n, status:", resp.status_code)
        except Exception as e:
            print("Error enviando a n8n:", e)

    # ---------------- Enviar mensaje -----------    
    def _send(self, e: ft.ControlEvent):
        if not self.input_ref.current:
            return
        text = (self.input_ref.current.value or "").strip()
        if not text:
            return

        self.input_ref.current.value = ""
        self.append("user", text)
        self.handle_answer(text)

    # ---------------- UI principal --------------    
    def build(self) -> ft.Control:
        lv = ft.ListView(
            ref=self.list_ref,
            controls=[],
            spacing=12,
            expand=True,
            auto_scroll=True,
            padding=ft.padding.symmetric(horizontal=10, vertical=10)
        )

        input_box = ft.Row(
            [
                ft.TextField(
                    ref=self.input_ref,
                    hint_text="Escribe tu respuesta...",
                    expand=True,
                    border_radius=24,
                    filled=True,
                    bgcolor="#263238",
                    color=ft.Colors.WHITE,
                    cursor_color=ft.Colors.BLUE,
                    content_padding=12,
                    on_submit=self._send,
                ),
                ft.IconButton(
                    ft.Icons.SEND_ROUNDED,
                    tooltip="Enviar",
                    icon_color=ft.Colors.WHITE,
                    bgcolor=ft.Colors.BLUE,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
                    on_click=self._send,
                ),
            ],
            spacing=8,
        )

        body = ft.Column([lv, input_box], spacing=10, expand=True)
        wrap = ft.Container(body, padding=ft.padding.only(left=8, right=8, bottom=10), expand=True)
        return ft.Column([wrap], spacing=0, expand=True)
