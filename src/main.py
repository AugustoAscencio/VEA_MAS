from __future__ import annotations

import flet as ft
from estado import Estado_de_la_aplicación, ROUTES
from typing import Optional
from dataclasses import dataclass, field
from UI.componentes import Tokens
from UI.vistas.inicio import Vista_del_panel
from UI.vistas.graficos import Vista_de_gráficos
from UI.vistas.consultas import ConsultasVer
from UI.vistas.historial import HistoriaVer
from UI.vistas.prediccion import PredicciónVer
from UI.vistas.chatbot import ChatVer
from UI.barra_inferior import Barra_inferior



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

        # layout raíz: Column [Expanded(content), BottomBar]
        self.content_container = ft.Container(ref=self.content_ref, expand=True)
        self.nav = Barra_inferior(self)
        root = ft.Column([self._route_to_view(self.state.active_route), self.nav], spacing=0, expand=True)
        # importante: reemplazaremos el índice 0 del Column (contenido) en _set_content
        self.root = root

        # una sola view
        page.views.clear()
        page.views.append(ft.View(route="/", controls=[root], padding=0, bgcolor=Tokens.BG))
        page.update()

    # -------- navegación interna (sin page.go) --------
    def go(self, route: str):
        if route not in ROUTES:
            route = "/"
        self.state.active_route = route
        self._set_content(self._route_to_view(route))
        if self.nav:
            self.nav.refresh()

    def _set_content(self, control: ft.Control):
        # Reemplaza el slot 0 del Column root
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

def main(page: ft.Page):
    App(page)


if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.FLET_APP)
