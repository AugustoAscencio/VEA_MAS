# from __future__ import annotations
# import flet as ft
# from estado import Estado_de_la_aplicación, ROUTES
# from UI.componentes import Tokens
# from UI.vistas.inicio import Vista_del_panel, Vista_del_panel_Miskito
# from UI.vistas.graficos import Vista_de_gráficos
# from UI.vistas.consultas import ConsultasVer, ConsultasVerMiskito
# from UI.vistas.historial import HistoriaVer, HistoriaVerMiskito
# from UI.vistas.prediccion import PredicciónVer, PredicciónVerMiskito
# from UI.vistas.chatbot import ChatVer, ChatVerMiskito
# from UI.barra_inferior import Barra_inferior
# from UI.Login import LoginChatbot, LoginChatbotMiskito
# from UI.vistas.psicologo import VeaAllInOne, VeaAllInOneMiskito
# from UI.vistas.InformacionMinsa import MINSAInfoVerEspañol, MINSAInfoVerMiskito
# # =============================================================================
# class App:
#     def __init__(self, page: ft.Page, lang: str = "es"):
#         self.page = page
#         #self.state = Estado_de_la_aplicación()
#         self.state = Estado_de_la_aplicación(idioma=lang)

#         self.content_ref: ft.Ref[ft.Container] = ft.Ref[ft.Container]()
#         self.nav = Barra_inferior(self)

#         page.title = "VEA+"
#         page.theme_mode = ft.ThemeMode.LIGHT
#         page.padding = 0
#         page.bgcolor = Tokens.BG
#         page.window_bgcolor = Tokens.BG
#         page.scroll = ft.ScrollMode.AUTO

#         self.content_container = ft.Container(ref=self.content_ref, expand=True)
#         root = ft.Column([self._route_to_view(self.state.active_route), self.nav],
#                          spacing=0, expand=True)
#         self.root = root

#         page.views.clear()
#         page.views.append(ft.View(route="/", controls=[root], padding=0, bgcolor=Tokens.BG))
#         page.update()

#     def go(self, route: str):
#         if route not in ROUTES:
#             route = "/"
#         self.state.active_route = route
#         self._set_content(self._route_to_view(route))
#         self.nav.refresh()

#     def _set_content(self, control: ft.Control):
#         self.root.controls[0] = control
#         self.page.update()

#     def _route_to_view(self, route: str) -> ft.Control:
#         es = self.state.idioma == "es"

#         if route == "/":
#             return (Vista_del_panel if es else Vista_del_panel_Miskito)(self).build()
#         if route == "/gráficos":
#             return Vista_de_gráficos(self).build()  # 👈 solo tienes versión ES
#         if route == "/consultas":
#             return (ConsultasVer if es else ConsultasVerMiskito)(self).build()
#         if route == "/historia":
#             return (HistoriaVer if es else HistoriaVerMiskito)(self).build()
#         if route == "/predicción":
#             return (PredicciónVer if es else PredicciónVerMiskito)(self).build()
#         if route == "/chat":
#             return (ChatVer if es else ChatVerMiskito)(self).build()
#         if route == "/psicologico":
#             if not hasattr(self, "psicologo_view"):
#                 self.psicologo_view = (VeaAllInOne if es else VeaAllInOneMiskito)(self.page)
#             return self.psicologo_view.build()
#         if route == "/InfoMinsa":
#             return (MINSAInfoVerEspañol if es else MINSAInfoVerMiskito)(self).build()
#         return ft.Container(ft.Text("Ruta no encontrada"), expand=True)



# # =============================================================================
# #                         PANTALLA SELECCIÓN DE IDIOMA ESTÉTICA
# # =============================================================================
# def language_selector(page: ft.Page):
    
#     def select_language(lang: str):
#         page.controls.clear()
#         if lang == "es":
#             login = LoginChatbot(page, on_finish=lambda: launch_app(lang))
#         else:
#             login = LoginChatbotMiskito(page, on_finish=lambda: launch_app(lang))
#         page.add(login.build())
#         page.update()

#     def launch_app(lang: str):
#         page.controls.clear()
#         app = App(page, lang=lang)
#         page.update()


#     # Fondo degradado
#     page.bgcolor = ft.Colors.BLUE_GREY_900

#     # Título centralizado y bilingüe
#     titulo = ft.Container(
#     content=ft.Column(
#         [
#             ft.Text(
#                 "Seleccione su idioma / Lasi la gune",
#                 size=32,
#                 weight=ft.FontWeight.BOLD,
#                 color=ft.Colors.WHITE,
#                 text_align=ft.TextAlign.CENTER,   # Centra el texto horizontalmente
#             ),
#             ft.Text(
#                 "Español / Miskito",
#                 size=22,
#                 color=ft.Colors.WHITE70,
#                 text_align=ft.TextAlign.CENTER
#             )
#         ],
#         spacing=10,
#         horizontal_alignment=ft.CrossAxisAlignment.CENTER
#     ),
#     padding=ft.padding.symmetric(vertical=60, horizontal=20),  # más padding arriba/abajo
#     alignment=ft.alignment.center,  # lo centra dinámicamente en su contenedor
#     expand=True
# )

#     # Botones con estilo moderno
#     botones = ft.Row(
#         [
#             ft.Container(
#                 content=ft.ElevatedButton(
#                     "Español",
#                     on_click=lambda e: select_language("es"),
#                     expand=True,
#                     height=60
#                 ),
#                 padding=10,
#                 border_radius=12,
#                 bgcolor=ft.Colors.BLUE_700,
#                 shadow=ft.BoxShadow(blur_radius=10, spread_radius=2, color=ft.Colors.BLACK26)
#             ),
#             ft.Container(
#                 content=ft.ElevatedButton(
#                     "Miskito",
#                     on_click=lambda e: select_language("mi"),
#                     expand=True,
#                     height=60
#                 ),
#                 padding=10,
#                 border_radius=12,
#                 bgcolor=ft.Colors.GREEN_700,
#                 shadow=ft.BoxShadow(blur_radius=10, spread_radius=2, color=ft.Colors.BLACK26)
#             )
#         ],
#         alignment=ft.MainAxisAlignment.CENTER,
#         spacing=30,
#         expand=True
#     )

#     container = ft.Column(
#         [titulo, botones],
#         alignment=ft.MainAxisAlignment.CENTER,
#         horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#         expand=True,
#         spacing=50
#     )

#     page.controls.clear()
#     page.add(container)
#     page.update()

# # =============================================================================
# def main(page: ft.Page):
#     language_selector(page)


# if __name__ == "__main__":
#     ft.app(target=main, view=ft.AppView.FLET_APP)

from __future__ import annotations
import flet as ft
from estado import Estado_de_la_aplicación, ROUTES
from UI.componentes import Tokens
from UI.vistas.inicio import Vista_del_panel, Vista_del_panel_Miskito
from UI.vistas.graficos import Vista_de_gráficos
from UI.vistas.consultas import ConsultasVer, ConsultasVerMiskito
from UI.vistas.historial import HistoriaVer, HistoriaVerMiskito
from UI.vistas.prediccion import PredicciónVer, PredicciónVerMiskito
from UI.vistas.chatbot import ChatVer, ChatVerMiskito
from UI.barra_inferior import Barra_inferior
from UI.Login import LoginChatbot, LoginChatbotMiskito
from UI.vistas.psicologo import VeaAllInOne, VeaAllInOneMiskito
from UI.vistas.InformacionMinsa import MINSAInfoVerEspañol, MINSAInfoVerMiskito

# =============================================================================
class App:
    def __init__(self, page: ft.Page, lang: str = "es"):
        self.page = page
        self.state = Estado_de_la_aplicación(idioma=lang)

        self.content_ref: ft.Ref[ft.Container] = ft.Ref[ft.Container]()
        self.nav = Barra_inferior(self)

        page.title = "VEA+"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0
        page.bgcolor = Tokens.BG
        page.window_bgcolor = Tokens.BG
        page.scroll = ft.ScrollMode.AUTO

        self.content_container = ft.Container(ref=self.content_ref, expand=True)
        root = ft.Column([self._route_to_view(self.state.active_route), self.nav],
                         spacing=0, expand=True)
        self.root = root

        page.views.clear()
        page.views.append(ft.View(route="/", controls=[root], padding=0, bgcolor=Tokens.BG))
        page.update()

    def go(self, route: str):
        if route not in ROUTES:
            route = "/"
        self.state.active_route = route
        self._set_content(self._route_to_view(route))
        self.nav.refresh()

    def _set_content(self, control: ft.Control):
        self.root.controls[0] = control
        self.page.update()

    def _route_to_view(self, route: str) -> ft.Control:
        es = self.state.idioma == "es"

        if route == "/":
            return (Vista_del_panel if es else Vista_del_panel_Miskito)(self).build()
        if route == "/gráficos":
            return Vista_de_gráficos(self).build()  # 👈 solo tienes versión ES
        if route == "/consultas":
            return (ConsultasVer if es else ConsultasVerMiskito)(self).build()
        if route == "/historia":
            return (HistoriaVer if es else HistoriaVerMiskito)(self).build()
        if route == "/predicción":
            return (PredicciónVer if es else PredicciónVerMiskito)(self).build()
        if route == "/chat":
            return (ChatVer if es else ChatVerMiskito)(self).build()
        if route == "/psicologico":
            if not hasattr(self, "psicologo_view"):
                self.psicologo_view = (VeaAllInOne if es else VeaAllInOneMiskito)(self.page)
            return self.psicologo_view.build()
        if route == "/InfoMinsa":
            return (MINSAInfoVerEspañol if es else MINSAInfoVerMiskito)(self).build()
        return ft.Container(ft.Text("Ruta no encontrada"), expand=True)


# =============================================================================
#                  PANTALLA SELECCIÓN DE IDIOMA (MODERNA)
# =============================================================================
def language_selector(page: ft.Page):
    
    def select_language(lang: str):
        page.controls.clear()
        if lang == "es":
            login = LoginChatbot(page, on_finish=lambda: launch_app(lang))
        else:
            login = LoginChatbotMiskito(page, on_finish=lambda: launch_app(lang))
        page.add(login.build())
        page.update()

    def launch_app(lang: str):
        page.controls.clear()
        app = App(page, lang=lang)
        page.update()

    # Fondo blanco mate
    page.bgcolor = ft.Colors.WHITE

    # Título centralizado
    titulo = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "Seleccione su idioma / Lasi la gune",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_900,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "Español / Miskito",
                    size=18,
                    color=ft.Colors.BLUE_GREY_600,
                    text_align=ft.TextAlign.CENTER
                )
            ],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=ft.padding.symmetric(vertical=60, horizontal=20),
        alignment=ft.alignment.center,
        expand=True
    )

    # Botones modernos con colores suaves
    botones = ft.Row(
        [
            ft.ElevatedButton(
                "Español",
                on_click=lambda e: select_language("es"),
                height=55,
                width=150,
                bgcolor=ft.Colors.LIGHT_BLUE_100,
                color=ft.Colors.BLUE_900,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=12),
                    elevation={"": 2, "hovered": 6, "pressed": 2},
                )
            ),
            ft.ElevatedButton(
                "Miskito",
                on_click=lambda e: select_language("mi"),
                height=55,
                width=150,
                bgcolor=ft.Colors.LIGHT_GREEN_100,
                color=ft.Colors.GREEN_900,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=12),
                    elevation={"": 2, "hovered": 6, "pressed": 2},
                )
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=30,
        expand=True
    )

    container = ft.Column(
        [titulo, botones],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
        spacing=50
    )

    page.controls.clear()
    page.add(container)
    page.update()

# =============================================================================
def main(page: ft.Page):
    language_selector(page)


if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.FLET_APP)

