from __future__ import annotations

import flet as ft
import os

from estado import Estado_de_la_aplicación, ROUTES
from typing import Optional
from UI.componentes import Tokens
from UI.vistas.inicio import Vista_del_panel
from UI.vistas.graficos import Vista_de_gráficos
from UI.vistas.consultas import ConsultasVer
from UI.vistas.historial import HistoriaVer
from UI.vistas.prediccion import PredicciónVer
from UI.vistas.chatbot import ChatVer
from UI.barra_inferior import Barra_inferior
from UI.Login import LoginChatbot

USER_DATA_FILE = "user_data.json"


# =============================================================================
class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.state = Estado_de_la_aplicación()

        # refs
        self.content_ref: ft.Ref[ft.Container] = ft.Ref[ft.Container]()
        self.nav: Optional[Barra_inferior] = None

        # config
        page.title = "MediAssist – Mobile"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0
        page.bgcolor = Tokens.BG
        page.window_bgcolor = Tokens.BG
        page.scroll = ft.ScrollMode.AUTO

        # layout raíz
        self.content_container = ft.Container(ref=self.content_ref, expand=True)
        self.nav = Barra_inferior(self)
        root = ft.Column(
            [self._route_to_view(self.state.active_route), self.nav],
            spacing=0,
            expand=True,
        )
        self.root = root

        # única view
        page.views.clear()
        page.views.append(
            ft.View(route="/", controls=[root], padding=0, bgcolor=Tokens.BG)
        )
        page.update()

    # -------- navegación interna --------
    def go(self, route: str):
        if route not in ROUTES:
            route = "/"
        self.state.active_route = route
        self._set_content(self._route_to_view(route))
        if self.nav:
            self.nav.refresh()

    def _set_content(self, control: ft.Control):
        self.root.controls[0] = control
        self.page.update()

    def _route_to_view(self, route: str) -> ft.Control:
        if route == "/":
            return Vista_del_panel(self).build()
        if route == "/gráficos":
            return Vista_de_gráficos(self).build()
        if route == "/consultas":
            return ConsultasVer(self).build()
        if route == "/historia":
            return HistoriaVer(self).build()
        if route == "/predicción":
            return PredicciónVer(self).build()
        if route == "/chat":
            return ChatVer(self).build()
        return ft.Container(ft.Text("Ruta no encontrada"), expand=True)


# =============================================================================
#                               ENTRADA
# =============================================================================
# =============================================================================
#                               ENTRADA
# =============================================================================
def main(page: ft.Page):
    def launch_app():
        # 👇 Limpiar controles previos y cargar la app principal
        page.controls.clear()
        App(page)  # la propia App ya hace page.update()

    # 👇 Verificar si ya existe registro de usuario
    if not os.path.exists(USER_DATA_FILE):
        # Mostrar el login tipo chatbot
        login = LoginChatbot(page, on_finish=launch_app)
        page.add(login.build())
    else:
        # Cargar la app normal directamente
        App(page)



if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.FLET_APP)
