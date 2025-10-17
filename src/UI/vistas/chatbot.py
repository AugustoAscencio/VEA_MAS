from __future__ import annotations

import asyncio, datetime, threading, httpx
import flet as ft
from asyncio import run_coroutine_threadsafe

from ..tokens import Tokens
from ..componentes import EspaciadorBarra, Rellenar
from estado import Mensaje, MensajeMiskito

N8N_WEBHOOK_URL = "https://augustosecundario.app.n8n.cloud/webhook/d689c13c-e591-45e1-886c-8fd2325991af"

#La de abajo es para testear
N8N_WEBHOOK_URL_MISKITO = "https://augustosecundario.app.n8n.cloud/webhook/bacdd82a-9b9a-4543-a27c-c5783b683163"
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
        bg_color = "#4FC3F7" if is_user else "#E6F7FF"
        fg_color = ft.Colors.WHITE if is_user else Tokens.TEXT
        ts_color = ft.Colors.with_opacity(0.7, fg_color)

        # Burbuja adaptativa (sin width fijo)
        cont = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        msg.Texto,
                        size=14,
                        color=fg_color,
                        selectable=True,
                        no_wrap=False,  # permite saltos de línea
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

        # Lo metemos en un contenedor expandible dentro del Row
        return ft.Row(
            [
                ft.Container(
                    content=cont,
                    expand=True,   # se adapta al ancho disponible
                )
            ],
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
            async with httpx.AsyncClient(timeout=20) as client:
                resp = await client.post(
                    N8N_WEBHOOK_URL,
                    json={"usuario": "augusto", "chatInput": text},
                )
                raw = resp.text
                if resp.status_code == 200:
                    try:
                        data = resp.json()
                        reply_text = data.get("respuesta", raw) if isinstance(data, dict) else raw
                    except Exception:
                        reply_text = raw
                else:
                    reply_text = f"Error {resp.status_code}: {raw}"
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
            padding=ft.padding.symmetric(horizontal=6, vertical=50),
        )

        input_box = ft.Row(
            [
                ft.TextField(
                    ref=self.input_ref,
                    hint_text="Escribe un mensaje…",
                    expand=True,
                    border_radius=24,
                    filled=True,
                    bgcolor=Tokens.PRIMARY,
                    color=Tokens.SUBTLE,
                    cursor_color=Tokens.WARN,
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

        wrap = ft.Container(
            body,
            padding=ft.padding.only(left=8, right=8, bottom=10),  # 👈 aire lateral + 5px abajo
            expand=True,
        )

        return ft.Column([wrap], spacing=0, expand=True)


class ChatVerMiskito:
    """Vista principal del chat con el bot en miskito"""

    def __init__(self, app):
        self.app = app
        self.list_ref: ft.Ref[ft.ListView] = ft.Ref[ft.ListView]()
        self.input_ref: ft.Ref[ft.TextField] = ft.Ref[ft.TextField]()
        self.typing_ref: ft.Ref[ft.Container] = ft.Ref[ft.Container]()

    # ---------------- Burbuja ------------------
    def _bubble(self, msg: MensajeMiskito) -> ft.Row:
        is_user = msg.Amable == "user"

        # Usuario: azul vivo, Bot: celeste muy claro (casi blanco)
        bg_color = "#4FC3F7" if is_user else "#E6F7FF"
        fg_color = ft.Colors.WHITE if is_user else Tokens.TEXT
        ts_color = ft.Colors.with_opacity(0.7, fg_color)

        # Burbuja adaptativa (sin width fijo)
        cont = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        msg.Texto,
                        size=14,
                        color=fg_color,
                        selectable=True,
                        no_wrap=False,  # permite saltos de línea
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

        # Lo metemos en un contenedor expandible dentro del Row
        return ft.Row(
            [
                ft.Container(
                    content=cont,
                    expand=True,   # se adapta al ancho disponible
                )
            ],
            alignment=ft.MainAxisAlignment.END if is_user else ft.MainAxisAlignment.START,
        )

    # ---------------- Añadir mensaje ------------
    def append(self, msg: MensajeMiskito) -> None:
        self.app.state.chat2.append(msg)
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
                        ft.Text("Warkisa...", size=12, color=Tokens.MUTED),
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
            async with httpx.AsyncClient(timeout=20) as client:
                resp = await client.post(
                    N8N_WEBHOOK_URL_MISKITO,
                    json={"usuario": "augusto", "chatInput": text},
                )
                raw = resp.text
                if resp.status_code == 200:
                    try:
                        data = resp.json()
                        reply_text = data.get("respuesta", raw) if isinstance(data, dict) else raw
                    except Exception:
                        reply_text = raw
                else:
                    reply_text = f"Error {resp.status_code}: {raw}"
        except Exception as e:
            reply_text = f"Konneksion sa warkisa: {e}"

        self.show_typing(False)
        self.append(MensajeMiskito("bot", reply_text, datetime.datetime.now().strftime("%H:%M")))


    # ---------------- Envío mensaje -------------
    def _send(self, e: ft.ControlEvent) -> None:
        if not self.input_ref.current:
            return
        text = (self.input_ref.current.value or "").strip()
        if not text:
            return

        self.input_ref.current.value = ""
        self.append(MensajeMiskito("user", text, datetime.datetime.now().strftime("%H:%M")))
        run_coroutine_threadsafe(self.handle_user_message(text), loop)

    # ---------------- UI principal --------------
    def build(self) -> ft.Control:
        items = [self._bubble(m) for m in self.app.state.chat2]

        lv = ft.ListView(
            ref=self.list_ref,
            controls=items,
            spacing=12,
            expand=True,
            auto_scroll=True,
            padding=ft.padding.symmetric(horizontal=6, vertical=50),
        )

        input_box = ft.Row(
            [
                ft.TextField(
                    ref=self.input_ref,
                    hint_text="Warkisa wan pas…",
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
                    tooltip="Taya",
                    icon_color=ft.Colors.WHITE,
                    bgcolor=Tokens.PRIMARY,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
                    on_click=self._send,
                ),
            ],
            spacing=8,
        )

        body = ft.Column([lv, input_box], spacing=10, expand=True)

        wrap = ft.Container(
            body,
            padding=ft.padding.only(left=8, right=8, bottom=10),  # 👈 aire lateral + 5px abajo
            expand=True,
        )

        return ft.Column([wrap], spacing=0, expand=True)
