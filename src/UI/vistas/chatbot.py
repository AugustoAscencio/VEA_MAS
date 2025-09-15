from __future__ import annotations

import asyncio, datetime, threading, aiohttp
import flet as ft
from asyncio import run_coroutine_threadsafe

from ..tokens import Tokens
from ..componentes import EspaciadorBarra, Rellenar
from estado import Mensaje

N8N_WEBHOOK_URL = "https://augustocraft02.app.n8n.cloud/webhook/875be057-eabd-4d46-99e6-0448922119a6"

# ===== Bucle asincrónico en segundo plano =====
loop = asyncio.new_event_loop()
def start_loop(lp: asyncio.AbstractEventLoop):
    asyncio.set_event_loop(lp)
    lp.run_forever()
threading.Thread(target=start_loop, args=(loop,), daemon=True).start()


class ChatVer:
    """Vista principal del chat con el bot."""

    def __init__(self, app):
        self.app = app
        self.list_ref: ft.Ref[ft.ListView] = ft.Ref[ft.ListView]()
        self.input_ref: ft.Ref[ft.TextField] = ft.Ref[ft.TextField]()
        self.typing_ref: ft.Ref[ft.Container] = ft.Ref[ft.Container]()

    # ---------------- Burbuja ------------------
    def _bubble(self, msg: Mensaje) -> ft.Row:
        is_user = msg.Amable == "user"

        # Usuario: azul vivo, Bot: celeste muy claro (casi blanco)
        bg_color = "#4FC3F7" if is_user else "#E6F7FF"   # celeste muy claro
        fg_color = ft.Colors.WHITE if is_user else Tokens.TEXT
        ts_color = ft.Colors.with_opacity(0.7, fg_color)

        # En Flet 0.28.3 limitamos ancho con width en Container
        cont = ft.Container(
            width=400,                         # ancho máximo deseado
            content=ft.Column(
                [
                    ft.Text(
                        msg.Texto,
                        size=14,
                        color=fg_color,
                        selectable=True,
                        no_wrap=False,
                    ),
                    ft.Text(msg.Tiempo, size=10, color=ts_color),
                ],
                spacing=4,
                tight=True,
            ),
            bgcolor=bg_color,
            padding=Rellenar.all(12),
            border_radius=ft.border_radius.all(18),
            margin=ft.margin.only(
                left=60 if is_user else 8,
                right=8 if is_user else 60,
                top=2,
                bottom=2,
            ),
            shadow=ft.BoxShadow(
                blur_radius=6,
                spread_radius=1,
                color=ft.Colors.with_opacity(0.15, "black"),
            ),
        )

        return ft.Row(
            [cont],
            alignment=ft.MainAxisAlignment.END if is_user else ft.MainAxisAlignment.START,
        )

    # ---------------- Añadir mensaje ------------
    def append(self, msg: Mensaje) -> None:
        self.app.state.chat.append(msg)
        if self.list_ref.current:
            self.list_ref.current.controls.append(self._bubble(msg))
            self.list_ref.current.scroll_to(offset=99999, duration=200)
        self.app.page.update()

    # ---------------- Indicador "Escribiendo" ---
    def show_typing(self, show: bool) -> None:
        if not self.list_ref.current:
            return
        if show:
            bubble = ft.Container(
                ref=self.typing_ref,
                content=ft.Row(
                    [
                        ft.ProgressRing(width=16, height=16, stroke_width=2, color=Tokens.PRIMARY),
                        ft.Text("Escribiendo...", size=12, color=Tokens.MUTED),
                    ],
                    spacing=8,
                ),
                padding=Rellenar.all(10),
                border_radius=16,
                bgcolor=ft.Colors.BLUE_GREY_800,
                margin=ft.margin.only(right=120, left=8),
            )
            self.list_ref.current.controls.append(bubble)
        else:
            if self.typing_ref.current and self.typing_ref.current in self.list_ref.current.controls:
                self.list_ref.current.controls.remove(self.typing_ref.current)

        self.list_ref.current.scroll_to(offset=99999, duration=200)
        self.app.page.update()

    # ---------------- Llamada webhook ----------
    async def handle_user_message(self, text: str) -> None:
        self.show_typing(True)
        reply_text = ""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    N8N_WEBHOOK_URL,
                    json={"usuario": "augusto", "chatInput": text},
                    timeout=20,
                ) as resp:
                    raw = await resp.text()
                    if resp.status == 200:
                        try:
                            data = await resp.json()
                            reply_text = data.get("respuesta", raw) if isinstance(data, dict) else raw
                        except Exception:
                            reply_text = raw
                    else:
                        reply_text = f"Error {resp.status}: {raw}"
        except Exception as e:
            reply_text = f"Error de conexión: {e}"

        self.show_typing(False)
        self.append(Mensaje("bot", reply_text, datetime.datetime.now().strftime("%H:%M")))

    # ---------------- Envío mensaje -------------
    def _send(self, e: ft.ControlEvent) -> None:
        if not self.input_ref.current:
            return
        text = (self.input_ref.current.value or "").strip()
        if not text:
            return

        self.input_ref.current.value = ""
        self.append(Mensaje("user", text, datetime.datetime.now().strftime("%H:%M")))
        run_coroutine_threadsafe(self.handle_user_message(text), loop)

    # ---------------- UI principal --------------
    def build(self) -> ft.Control:
        items = [self._bubble(m) for m in self.app.state.chat]

        lv = ft.ListView(
            ref=self.list_ref,
            controls=items,
            spacing=12,
            expand=True,
            auto_scroll=True,
            padding=ft.padding.symmetric(horizontal=6, vertical=10),
        )

        input_box = ft.Row(
            [
                ft.TextField(
                    ref=self.input_ref,
                    hint_text="Escribe un mensaje…",
                    expand=True,
                    border_radius=24,
                    filled=True,
                    bgcolor="#263238",
                    color=ft.Colors.WHITE,
                    cursor_color=Tokens.PRIMARY,
                    content_padding=12,
                    on_submit=self._send,
                ),
                ft.IconButton(
                    ft.Icons.SEND_ROUNDED,
                    tooltip="Enviar",
                    icon_color=ft.Colors.WHITE,
                    bgcolor=Tokens.PRIMARY,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
                    on_click=self._send,
                ),
            ],
            spacing=8,
        )

        body = ft.Column([lv, input_box], spacing=10, expand=True)
        wrap = ft.Container(body, margin=ft.margin.all(12), padding=ft.padding.only(bottom=16), expand=True)

        return ft.Column([wrap, EspaciadorBarra()], spacing=0, expand=True)
