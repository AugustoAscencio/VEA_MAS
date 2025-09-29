import flet as ft
from ..tokens import Tokens
from ..componentes import EspaciadorBarra, Rellenar

class ConsultasVer:
    def __init__(self, app):
        self.app = app

    def _appointment(self) -> ft.Container:
        chip = ft.Container(
            ft.Text("En progreso", size=10, color=Tokens.MUTED),
            bgcolor=ft.Colors.BLUE_GREY_50,
            padding=Rellenar.hv(10, 4),
            border_radius=12
        )
        row1 = ft.Row(
            [
                ft.Column([
                    ft.Text("Dra. María López", weight=ft.FontWeight.W_600, size=14),
                    ft.Text("Cardiología", size=11, color=Tokens.MUTED)
                ], spacing=4),
                chip
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
        row2 = ft.Row(
            [
                ft.Icon(ft.Icons.SCHEDULE, size=16, color=Tokens.MUTED),
                ft.Text("Inicio 14:30 · 30 min", size=11, color=Tokens.MUTED)
            ], spacing=8
        )
        btn = ft.FilledButton("Unirse a la consulta")
        return ft.Container(
            ft.Column([row1, row2, btn], spacing=12),
            bgcolor=Tokens.SURFACE,
            border_radius=Tokens.RADIUS,
            border=ft.border.all(0.5, Tokens.BORDER),
            padding=Rellenar.all(16)
        )

    def build(self) -> ft.Control:
        header = ft.Row(
            [
                ft.Text("Consultas", **Tokens.H2),
                ft.FilledButton(
                    ft.Row([ft.Icon(ft.Icons.ADD, size=16), ft.Text("Nueva", size=12)], spacing=8)
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
        items = ft.Column([self._appointment() for _ in range(2)], spacing=12)
        lv = ft.ListView([
            ft.Container(header, margin=ft.margin.only(left=16, right=16, top=16, bottom=8)),
            ft.Container(items, margin=ft.margin.symmetric(horizontal=16)),
            # Espacio inferior más grande (por ejemplo 80px de alto)
            ft.Container(height=80),
        ], expand=True)
        return lv
    
class ConsultasVerMiskito:
    def __init__(self, app):
        self.app = app

    def _appointment(self) -> ft.Container:
        chip = ft.Container(
            ft.Text("Yawan lila", size=10, color=Tokens.MUTED),  # En progreso
            bgcolor=ft.Colors.BLUE_GREY_50,
            padding=Rellenar.hv(10, 4),
            border_radius=12
        )
        row1 = ft.Row([
            ft.Column([
                ft.Text("Dra. María López", weight=ft.FontWeight.W_600, size=14),
                ft.Text("Kardiyolôjia", size=11, color=Tokens.MUTED)  # Cardiología
            ], spacing=4),
            chip
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        row2 = ft.Row([
            ft.Icon(ft.Icons.SCHEDULE, size=16, color=Tokens.MUTED),
            ft.Text("Tuktan 14:30 · 30 min", size=11, color=Tokens.MUTED)  # Inicio
        ], spacing=8)

        btn = ft.FilledButton("Aisanka unta")  # Unirse a la consulta

        return ft.Container(
            ft.Column([row1, row2, btn], spacing=12),
            bgcolor=Tokens.SURFACE,
            border_radius=Tokens.RADIUS,
            border=ft.border.all(0.5, Tokens.BORDER),
            padding=Rellenar.all(16)
        )

    def build(self) -> ft.Control:
        header = ft.Row([
            ft.Text("Aisanka", **Tokens.H2),  # Consultas
            ft.FilledButton(
                ft.Row([ft.Icon(ft.Icons.ADD, size=16), ft.Text("Nani", size=12)], spacing=8)  # Nueva
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        items = ft.Column([self._appointment() for _ in range(2)], spacing=12)

        lv = ft.ListView([
            ft.Container(header, margin=ft.margin.only(left=16, right=16, top=16, bottom=8)),
            ft.Container(items, margin=ft.margin.symmetric(horizontal=16)),
            EspaciadorBarra(),
        ], expand=True)
        return lv
