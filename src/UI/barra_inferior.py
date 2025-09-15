
import flet as ft
from .tokens import Tokens
from .componentes import Rellenar
from typing import List, Dict, Optional, Callable
from estado import ROUTES
# 
class Barra_inferior(ft.Container):
    """Barra inferior fija, pegada abajo.

    OJO: No es un overlay; está en un Column raíz después del contenido, con
    border-top para separarla. De este modo se evita el efecto de *saltos* y la
    pantalla jamás queda en blanco.
    """

    def __init__(self, app):
        self.app = app
        self._buttons: List[ft.Container] = []
        super().__init__(
            content=self._build(),
            bgcolor=Tokens.SURFACE,
            padding=Rellenar .hv(14, 10),
            border=ft.border.only(top=ft.border.BorderSide(1, Tokens.BORDER)),
        )

    def _btn(self, *, icon: str, label: str, route: str) -> ft.Container:
        sel = self.app.state.active_route == route
        color = Tokens.PRIMARY if sel else Tokens.MUTED
        btn = ft.Container(
            content=ft.Column([ft.Icon(icon, size=22, color=color), ft.Text(label, size=10, color=color)], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            expand=True,
            on_click=lambda e, r=route: self.app.go(r),
        )
        self._buttons.append(btn)
        return btn

    def _build(self) -> ft.Control:
        self._buttons.clear()
        row = ft.Row([
            self._btn(icon=ft.Icons.HOME_ROUNDED, label="Inicio", route="/"),
            self._btn(icon=ft.Icons.SHOW_CHART_ROUNDED, label="Gráficos", route="/gráficos"),
            self._btn(icon=ft.Icons.CHAT_ROUNDED, label="Consultas", route="/consultas"),
            self._btn(icon=ft.Icons.HISTORY_ROUNDED, label="Historial", route="/historia"),
            self._btn(icon=ft.Icons.TRENDING_UP_ROUNDED, label="Predicción", route="/predicción"),
            self._btn(icon=ft.Icons.SMART_TOY_ROUNDED, label="Chatbot", route="/chat"),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=8)
        return row

    def refresh(self):
        for i, route in enumerate(ROUTES):
            sel = self.app.state.active_route == route
            color = Tokens.PRIMARY if sel else Tokens.MUTED
            col: ft.Column = self._buttons[i].content  # type: ignore
            icon: ft.Icon = col.controls[0]  # type: ignore
            text: ft.Text = col.controls[1]  # type: ignore
            icon.color = color
            text.color = color
        self.app.page.update()