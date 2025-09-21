import flet as ft
from ..tokens import Tokens
from UI.vistas.psicologo import VeaAllInOne
#from vistas
from ..componentes import EspaciadorBarra, Rellenar, Tarjeta_estadistica, Tarjeta_de_accion, Tarjeta_de_lista
from estado import ROUTES
class Vista_del_panel:
    def __init__(self, app):
        self.app = app

    def build(self) -> ft.Control:
        welcome = ft.Container(
            content=ft.Column(
                [ft.Text("¡Buen día!", **Tokens.H2), ft.Text("Tu próxima cita es hoy a las 15:00", **Tokens.SUB)],
                spacing=4,
            ),
            bgcolor=Tokens.PRIMARY_50,
            border_radius=Tokens.RADIUS,
            padding=Rellenar .all(16),
        )

        row1 = ft.Row(
            [
                 Tarjeta_estadistica(icon=ft.Icons.FAVORITE, color=Tokens.OK, title="Estado General", chip="Sin riesgos", value="Bueno"),
                 Tarjeta_estadistica(icon=ft.Icons.MONITOR_HEART, color=ft.Colors.BLUE_600, title="Frecuencia", chip="74 BPM", value="Normal"),
            ],
            spacing=12,
        )
        row2 = ft.Row(
            [
                 Tarjeta_estadistica(icon=ft.Icons.WARNING, color=Tokens.WARN, title="Riesgo PA", chip="Alta", value="Medio"),
                 Tarjeta_estadistica(icon=ft.Icons.CALENDAR_TODAY, color=ft.Colors.DEEP_PURPLE, title="Próx. Cita", chip="15:00", value="Hoy"),
            ],
            spacing=12,
        )

        quick_title = ft.Text("Acciones Rápidas", **Tokens.H2)
        quick1 = ft.Row(
            [
                Tarjeta_de_accion(icon=ft.Icons.PSYCHOLOGY, color=ft.Colors.DEEP_PURPLE, title="Análisis IA", subtitle="Síntomas", on_click=lambda _: self.app.go("/chat")),
                Tarjeta_de_accion(icon=ft.Icons.VIDEO_CALL, color=ft.Colors.BLUE_600, title="Consulta Virtual", subtitle="Especialistas"),
            ],
            spacing=12,
        )
        quick2 = ft.Row(
            [
                Tarjeta_de_accion(icon=ft.Icons.MONITOR_HEART, color=Tokens.OK, title="Monitoreo", subtitle="Signos vitales"),
                Tarjeta_de_accion(icon=ft.Icons.EMERGENCY, color=Tokens.DANGER, title="Emergencia", subtitle="SOS"),
            ],
            spacing=12,
        )
        quick3 = ft.Row(  
            [
                Tarjeta_de_accion(
                    icon=ft.Icons.SELF_IMPROVEMENT,
                    color=ft.Colors.PURPLE_400,
                    title="Asistente Psicológico",
                    subtitle="Apoyo emocional",
                    on_click=lambda _: self.app.go("/psicologico"), 
                    
                ),
            ],
            spacing=12,
        )
        recent_title = ft.Text("Actividad Reciente", **Tokens.H2)
        recent = ft.Column(
            [
                Tarjeta_de_lista(icon=ft.Icons.FAVORITE, color=Tokens.OK, title="Presión registrada", subtitle="121/81 · Hace 2 h"),
                Tarjeta_de_lista(icon=ft.Icons.CHAT, color=ft.Colors.BLUE_600, title="Consulta virtual", subtitle="Dra. López · Ayer"),
            ],
            spacing=12,
        )

        lv = ft.ListView(
            [
                ft.Container(welcome, margin=ft.margin.only(left=16, right=16, top=16, bottom=8)),
                ft.Container(row1, margin=ft.margin.symmetric(horizontal=16)),
                ft.Container(row2, margin=ft.margin.only(left=16, right=16, top=12, bottom=8)),
                ft.Container(quick_title, margin=ft.margin.only(left=16, right=16, top=8, bottom=8)),
                ft.Container(quick1, margin=ft.margin.symmetric(horizontal=16)),
                ft.Container(quick2, margin=ft.margin.only(left=16, right=16, top=12, bottom=8)),
                ft.Container(quick3, margin=ft.margin.only(left=16, right=16, top=12, bottom=8)),  
                ft.Container(recent_title, margin=ft.margin.only(left=16, right=16, top=8, bottom=8)),
                ft.Container(recent, margin=ft.margin.symmetric(horizontal=16)),
                EspaciadorBarra(),
            ],
            expand=True,
        )
        return lv

class Vista_del_panel_Miskito:
    def __init__(self, app):
        self.app = app

    def build(self) -> ft.Control:
        welcome = ft.Container(
            content=ft.Column(
                [ft.Text("Pain sa!", **Tokens.H2), ft.Text("Mairin baia cita nani aiwan nani 15:00 taim ra", **Tokens.SUB)],
                spacing=4,
            ),
            bgcolor=Tokens.PRIMARY_50,
            border_radius=Tokens.RADIUS,
            padding=Rellenar .all(16),
        )

        row1 = ft.Row(
            [
                 Tarjeta_estadistica(icon=ft.Icons.FAVORITE, color=Tokens.OK, title="General baia", chip="Risk sa", value="Pain"),
                 Tarjeta_estadistica(icon=ft.Icons.MONITOR_HEART, color=ft.Colors.BLUE_600, title="Frekuensia", chip="74 BPM", value="Normal"),
            ],
            spacing=12,
        )
        row2 = ft.Row(
            [
                 Tarjeta_estadistica(icon=ft.Icons.WARNING, color=Tokens.WARN, title="Risk PA", chip="Yamni", value="Tuktan"),
                 Tarjeta_estadistica(icon=ft.Icons.CALENDAR_TODAY, color=ft.Colors.DEEP_PURPLE, title="Baia cita", chip="15:00", value="Nani"),
            ],
            spacing=12,
        )

        quick_title = ft.Text("Rápido baia wina", **Tokens.H2)
        quick1 = ft.Row(
            [
                Tarjeta_de_accion(icon=ft.Icons.PSYCHOLOGY, color=ft.Colors.DEEP_PURPLE, title="IA baia análisis", subtitle="Sintomas", on_click=lambda _: self.app.go("/chat")),
                Tarjeta_de_accion(icon=ft.Icons.VIDEO_CALL, color=ft.Colors.BLUE_600, title="Virtual baia consulta", subtitle="Especialista nani"),
            ],
            spacing=12,
        )
        quick2 = ft.Row(
            [
                Tarjeta_de_accion(icon=ft.Icons.MONITOR_HEART, color=Tokens.OK, title="Monitoreo", subtitle="Vital baia sinia"),
                Tarjeta_de_accion(icon=ft.Icons.EMERGENCY, color=Tokens.DANGER, title="Emergencia", subtitle="SOS"),
            ],
            spacing=12,
        )
        quick3 = ft.Row(  
            [
                Tarjeta_de_accion(
                    icon=ft.Icons.SELF_IMPROVEMENT,
                    color=ft.Colors.PURPLE_400,
                    title="Psicológico asistente",
                    subtitle="Emosional baia asistensia",
                    on_click=lambda _: self.app.go("/psicologico"), 
                ),
            ],
            spacing=12,
        )
        recent_title = ft.Text("Nani baia actividad", **Tokens.H2)
        recent = ft.Column(
            [
                Tarjeta_de_lista(icon=ft.Icons.FAVORITE, color=Tokens.OK, title="Presion warkisa”", subtitle="121/81 · 2 taim ra"),
                Tarjeta_de_lista(icon=ft.Icons.CHAT, color=ft.Colors.BLUE_600, title="“Virtual baia consulta", subtitle="Dra. López · Yawan"),
            ],
            spacing=12,
        )
        
        lv = ft.ListView(
            [
                ft.Container(welcome, margin=ft.margin.only(left=16, right=16, top=16, bottom=8)),
                ft.Container(row1, margin=ft.margin.symmetric(horizontal=16)),
                ft.Container(row2, margin=ft.margin.only(left=16, right=16, top=12, bottom=8)),
                ft.Container(quick_title, margin=ft.margin.only(left=16, right=16, top=8, bottom=8)),
                ft.Container(quick1, margin=ft.margin.symmetric(horizontal=16)),
                ft.Container(quick2, margin=ft.margin.only(left=16, right=16, top=12, bottom=8)),
                ft.Container(quick3, margin=ft.margin.only(left=16, right=16, top=12, bottom=8)),  
                ft.Container(recent_title, margin=ft.margin.only(left=16, right=16, top=8, bottom=8)),
                ft.Container(recent, margin=ft.margin.symmetric(horizontal=16)),
                EspaciadorBarra(),
            ],
            expand=True,
        )
        return lv