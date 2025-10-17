import flet as ft
from .tokens import Tokens
from typing import List, Dict, Optional, Callable


class Rellenar :
    @staticmethod
    def all(v: int) -> ft.padding.Padding:
        return ft.padding.all(v)

    @staticmethod
    def hv(h: int, v: int) -> ft.padding.Padding:
        return ft.padding.symmetric(horizontal=h, vertical=v)


class Espaciador(ft.Container):
    """Espaciador vertical que puedes insertar al final de un ListView."""

    def __init__(self, h: int = Tokens.GUTTER):
        super().__init__(height=h)


class EspaciadorBarra(ft.Container):
    """Espaciador del alto del dock (para que nada quede tapado)."""

    def __init__(self):
        super().__init__(height=Tokens.DOCK_H + 8)


class Chip(ft.Container):
    def __init__(self, text: str, *, color: str, bg: Optional[str] = None):
        super().__init__(
            content=ft.Text(text, size=10, color=color),
            bgcolor=bg or ft.Colors.with_opacity(0.10, color),
            padding=Rellenar .hv(10, 4),
            border=ft.border.all(0.5, color),
            border_radius=12,
        )


class Seccion(ft.Container):
    def __init__(self, title: str, *children: ft.Control, icon: Optional[str] = None):
        header = ft.Row(
            [
                ft.Row(
                    [ft.Icon(icon, size=16, color=Tokens.PRIMARY), ft.Text(title, **Tokens.H2)],
                    spacing=8,
                )
                if icon
                else ft.Row([ft.Text(title, **Tokens.H2)]),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        body = ft.Column(list(children), spacing=12)
        super().__init__(
            content=ft.Column([header, body], spacing=12),
            bgcolor=Tokens.SURFACE,
            border_radius=Tokens.RADIUS,
            border=ft.border.all(0.5, Tokens.BORDER),
            padding=Rellenar .all(16),
        )


class Tarjeta_estadistica(ft.Container):
    def __init__(self, *, icon: str, color: str, title: str, chip: str, value: str):
        body = ft.Column(
            [
                ft.Row(
                    [ft.Icon(icon, color=color, size=22), Chip(chip, color=color)],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Text(title, size=11, color=Tokens.WARN_50),
                ft.Text(value, size=16, weight=ft.FontWeight.W_600),
            ],
            spacing=8,
        )
        super().__init__(
            content=body,
            bgcolor=Tokens.SURFACE,
            border_radius=Tokens.RADIUS,
            border=ft.border.all(0.5, Tokens.BORDER),
            padding=Rellenar .all(14),
            expand=True,
        )


class Tarjeta_de_accion(ft.Container):
    def __init__(self, *, icon: str, color: str, title: str, subtitle: str, on_click: Optional[Callable] = None):
        body = ft.Column(
            [
                ft.Icon(icon, color=color, size=28),
                ft.Text(title, size=12, weight=ft.FontWeight.W_600, text_align=ft.TextAlign.CENTER),
                ft.Text(subtitle, size=10, color=Tokens.WARN_50, text_align=ft.TextAlign.CENTER),
            ],
            spacing=6,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        super().__init__(
            content=body,
            bgcolor=Tokens.SURFACE,
            border_radius=Tokens.RADIUS,
            border=ft.border.all(0.5, Tokens.BORDER),
            padding=Rellenar .all(14),
            expand=True,
            on_click=on_click,
        )


class Tarjeta_de_lista(ft.Container):
    def __init__(self, *, icon: str, color: str, title: str, subtitle: str):
        lead = ft.Container(
            ft.Icon(icon, color=color, size=16),
            bgcolor=ft.Colors.with_opacity(0.1, color),
            width=32,
            height=32,
            border_radius=16,
            alignment=ft.alignment.center,
        )
        txt = ft.Column(
            [ft.Text(title, size=12, weight=ft.FontWeight.W_500), ft.Text(subtitle, size=10, color=Tokens.WARN_50)],
            spacing=4,
        )
        super().__init__(
            content=ft.Row([ft.Row([lead, txt], spacing=12), ft.Icon(ft.Icons.CHEVRON_RIGHT, size=16, color=Tokens.MUTED)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            bgcolor=Tokens.SURFACE,
            border_radius=Tokens.RADIUS,
            border=ft.border.all(0.5, Tokens.BORDER),
            padding=Rellenar .all(14),
        )

