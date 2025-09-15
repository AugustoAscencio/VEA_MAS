import flet as ft
from ..tokens import Tokens
from ..componentes import EspaciadorBarra, Rellenar, Seccion
from estado import ROUTES
class HistoriaVer:
    def __init__(self, app):
        self.app = app

    def _personal(self) -> ft.Container:
        g1 = ft.Row([ft.Column([ft.Text("Edad", size=10, color=Tokens.MUTED), ft.Text("32 años", size=12)], spacing=4), ft.Column([ft.Text("Grupo", size=10, color=Tokens.MUTED), ft.Text("O+", size=12)], spacing=4)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        g2 = ft.Row([ft.Column([ft.Text("Peso", size=10, color=Tokens.MUTED), ft.Text("71.3 kg", size=12)], spacing=4), ft.Column([ft.Text("Altura", size=10, color=Tokens.MUTED), ft.Text("1.75 m", size=12)], spacing=4)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        return Seccion("Información Personal", g1, g2, icon=ft.Icons.BADGE_OUTLINED)

    def _allergies(self) -> ft.Container:
        chips = ft.Row([ft.Container(ft.Text("Penicilina", size=10, color=ft.Colors.WHITE), bgcolor=Tokens.DANGER, border_radius=12, padding=Rellenar .hv(10,4)), ft.Container(ft.Text("Mariscos", size=10, color=ft.Colors.WHITE), bgcolor=Tokens.DANGER, border_radius=12, padding=Rellenar .hv(10,4))], spacing=8)
        return Seccion("Alergias", chips, icon=ft.Icons.WARNING_AMBER)

    def build(self) -> ft.Control:
        lv = ft.ListView([
            ft.Container(ft.Text("Historial", **Tokens.H2), margin=ft.margin.only(left=16, right=16, top=16, bottom=8)),
            ft.Container(self._personal(), margin=ft.margin.symmetric(horizontal=16, vertical=8)),
            ft.Container(self._allergies(), margin=ft.margin.symmetric(horizontal=16, vertical=8)),
            EspaciadorBarra(),
        ], expand=True)
        return lv
