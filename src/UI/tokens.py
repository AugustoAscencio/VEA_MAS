import flet as ft

class Tokens:
    # Colores base
    PRIMARY = '#bcdafe'
    PRIMARY_DARK = '#52a5d9'
    PRIMARY_50 = '#59f1d9'
    SUBTLE = ft.Colors.BLUE_GREY_600
    SURFACE = ft.Colors.WHITE
    TEXT = ft.Colors.BLACK
    MUTED = '#a7e4f2'
    BG = ft.Colors.BLUE_GREY_50
    OK = ft.Colors.GREEN_600
    OK_50 = ft.Colors.GREEN_50
    WARN = '#9860ab'
    WARN_50 = '#966682'
    DANGER = ft.Colors.RED_600
    DANGER_50 = ft.Colors.RED_50
    BORDER = '#615ac2'
    # Medidas
    GUTTER = 16
    RADIUS = 14
    DOCK_H = 76  # altura de la barra inferior

    # Tipos
    H1 = {"size": 20, "weight": ft.FontWeight.BOLD}
    H2 = {"size": 18, "weight": ft.FontWeight.W_600}
    SUB = {"size": 11, "color": SUBTLE}
