import flet as ft
from ..tokens import Tokens
from ..componentes import EspaciadorBarra, Rellenar, Seccion, Chip
from estado import ROUTES

class PredicciónVer:
    def __init__(self, app):
        self.app = app

    def _risk_row(self, name: str, level: str, color: str, bg: str) -> ft.Row:
        return ft.Row([ft.Text(name, size=12), Chip(level, color=color, bg=bg)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    def _recs(self) -> ft.Column:
        return ft.Column([
            ft.Container(ft.Text("💪 Ejercicio", weight=ft.FontWeight.W_600, size=12, color=ft.Colors.INDIGO_900), bgcolor=ft.Colors.INDIGO_50, padding=Rellenar .all(12), border_radius=10),
            ft.Container(ft.Text("🥗 Dieta", weight=ft.FontWeight.W_600, size=12, color=ft.Colors.GREEN_900), bgcolor=ft.Colors.GREEN_50, padding=Rellenar .all(12), border_radius=10),
            ft.Container(ft.Text("📊 Monitoreo", weight=ft.FontWeight.W_600, size=12, color=ft.Colors.AMBER_900), bgcolor=ft.Colors.AMBER_50, padding=Rellenar .all(12), border_radius=10),
            ft.Container(ft.Text("💊 Medicamentos", weight=ft.FontWeight.W_600, size=12, color=ft.Colors.PURPLE_900), bgcolor=ft.Colors.PURPLE_50, padding=Rellenar .all(12), border_radius=10),
        ], spacing=10)

    def build(self) -> ft.Control:
        risks = Seccion("Análisis de Riesgo", self._risk_row("Riesgo Cardiovascular", "Medio", Tokens.WARN, Tokens.WARN_50), self._risk_row("Riesgo Diabetes", "Bajo", Tokens.OK, Tokens.OK_50), self._risk_row("Riesgo Hipertensión", "Alto", Tokens.DANGER, Tokens.DANGER_50), icon=ft.Icons.TRENDING_UP)
        recs = Seccion("Recomendaciones Personalizadas", self._recs())
        lv = ft.ListView([
            ft.Container(ft.Text("Predicciones IA", **Tokens.H2), margin=ft.margin.only(left=16, right=16, top=16, bottom=8)),
            ft.Container(risks, margin=ft.margin.symmetric(horizontal=16, vertical=8)),
            ft.Container(recs, margin=ft.margin.symmetric(horizontal=16, vertical=8)),
            EspaciadorBarra(),
        ], expand=True)
        return lv

class PredicciónVerMiskito:
    def __init__(self, app):
        self.app = app

    def _risk_row(self, name: str, level: str, color: str, bg: str) -> ft.Row:
        return ft.Row(
            [ft.Text(name, size=12), Chip(level, color=color, bg=bg)],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

    def _recs(self) -> ft.Column:
        return ft.Column([
            ft.Container(
                ft.Text("💪 Winaia", weight=ft.FontWeight.W_600, size=12, color=ft.Colors.INDIGO_900),  # Ejercicio
                bgcolor=ft.Colors.INDIGO_50,
                padding=Rellenar.all(12),
                border_radius=10
            ),
            ft.Container(
                ft.Text("🥗 Wisna", weight=ft.FontWeight.W_600, size=12, color=ft.Colors.GREEN_900),  # Dieta
                bgcolor=ft.Colors.GREEN_50,
                padding=Rellenar.all(12),
                border_radius=10
            ),
            ft.Container(
                ft.Text("📊 Monituri", weight=ft.FontWeight.W_600, size=12, color=ft.Colors.AMBER_900),  # Monitoreo
                bgcolor=ft.Colors.AMBER_50,
                padding=Rellenar.all(12),
                border_radius=10
            ),
            ft.Container(
                ft.Text("💊 Pain nani", weight=ft.FontWeight.W_600, size=12, color=ft.Colors.PURPLE_900),  # Medicamentos
                bgcolor=ft.Colors.PURPLE_50,
                padding=Rellenar.all(12),
                border_radius=10
            ),
        ], spacing=10)

    def build(self) -> ft.Control:
        risks = Seccion(
            "Aisanka Risku",  # Análisis de Riesgo
            self._risk_row("Risku Kardiyolôjia", "Witin", Tokens.WARN, Tokens.WARN_50),   # Riesgo Cardiovascular, Medio
            self._risk_row("Risku Diabetis", "Yawan", Tokens.OK, Tokens.OK_50),          # Riesgo Diabetes, Bajo
            self._risk_row("Risku Hipertinsiun", "Yamni", Tokens.DANGER, Tokens.DANGER_50), # Riesgo Hipertensión, Alto
            icon=ft.Icons.TRENDING_UP
        )
        recs = Seccion("Dakra Aisanka", self._recs())  # Recomendaciones Personalizadas
        lv = ft.ListView([
            ft.Container(ft.Text("IA Prediksun", **Tokens.H2),  # Predicciones IA
                         margin=ft.margin.only(left=16, right=16, top=16, bottom=8)),
            ft.Container(risks, margin=ft.margin.symmetric(horizontal=16, vertical=8)),
            ft.Container(recs, margin=ft.margin.symmetric(horizontal=16, vertical=8)),
            EspaciadorBarra(),
        ], expand=True)
        return lv
