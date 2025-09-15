import flet as ft

class Tokens:
    # Colores base
    PRIMARY = ft.Colors.INDIGO_600
    PRIMARY_DARK = ft.Colors.INDIGO_700
    PRIMARY_50 = ft.Colors.INDIGO_50
    BG = ft.Colors.BLUE_GREY_50
    SURFACE = ft.Colors.WHITE
    TEXT = ft.Colors.BLACK
    MUTED = ft.Colors.BLUE_GREY_400
    OK = ft.Colors.GREEN_600
    OK_50 = ft.Colors.GREEN_50
    WARN = ft.Colors.AMBER_700
    WARN_50 = ft.Colors.AMBER_50
    DANGER = ft.Colors.RED_600
    DANGER_50 = ft.Colors.RED_50
    BORDER = ft.Colors.BLUE_GREY_50

    # Medidas
    GUTTER = 16
    RADIUS = 14
    DOCK_H = 76  # altura de la barra inferior

    # Tipos
    H1 = {"size": 20, "weight": ft.FontWeight.BOLD}
    H2 = {"size": 18, "weight": ft.FontWeight.W_600}
    SUB = {"size": 11, "color": MUTED}
