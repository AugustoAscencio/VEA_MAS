import flet as ft
from ..tokens import Tokens
from ..componentes import EspaciadorBarra, Rellenar, Seccion, Chip
from estado import ROUTES
class Vista_de_gráficos:
    def __init__(self, app):
        self.app = app

    def _bp_chart(self) -> ft.Control:
        pts_sys = [ft.LineChartDataPoint(i, d["sys"]) for i, d in enumerate(self.app.state.bp_series)]
        pts_dia = [ft.LineChartDataPoint(i, d["dia"]) for i, d in enumerate(self.app.state.bp_series)]
        labels = [ft.ChartAxisLabel(value=i, label=ft.Text(d["date"], size=9)) for i, d in enumerate(self.app.state.bp_series)]
        chart = ft.LineChart(
            data_series=[
                ft.LineChartData(data_points=pts_sys, color=ft.Colors.RED_600, stroke_width=2, curved=True, stroke_cap_round=True),
                ft.LineChartData(data_points=pts_dia, color=ft.Colors.BLUE_600, stroke_width=2, curved=True, stroke_cap_round=True),
            ],
            left_axis=ft.ChartAxis(labels_size=12),
            bottom_axis=ft.ChartAxis(labels_size=12, labels=labels),
            horizontal_grid_lines=ft.ChartGridLines(color=ft.Colors.BLUE_GREY_50, width=0.5),
            vertical_grid_lines=ft.ChartGridLines(color=ft.Colors.BLUE_GREY_50, width=0.5),
            min_y=60,
            max_y=140,
            expand=True,
        )
        legend = ft.Row([ft.Row([ft.Container(width=8, height=8, border_radius=4, bgcolor=ft.Colors.RED_600), ft.Text("Sistólica", size=10)], spacing=6), ft.Row([ft.Container(width=8, height=8, border_radius=4, bgcolor=ft.Colors.BLUE_600), ft.Text("Diastólica", size=10)], spacing=6)], spacing=16, alignment=ft.MainAxisAlignment.CENTER)
        return Seccion("Presión Arterial", ft.Container(chart, height=220), legend, icon=ft.Icons.FAVORITE)

    def _hr_chart(self) -> ft.Control:
        pts = [ft.LineChartDataPoint(i, d["bpm"]) for i, d in enumerate(self.app.state.hr_series)]
        labels = [ft.ChartAxisLabel(value=i, label=ft.Text(d["date"], size=9)) for i, d in enumerate(self.app.state.hr_series)]
        chart = ft.LineChart(
            data_series=[ft.LineChartData(data_points=pts, color=ft.Colors.DEEP_PURPLE_400, stroke_width=2, curved=True, stroke_cap_round=True)],
            left_axis=ft.ChartAxis(labels_size=12),
            bottom_axis=ft.ChartAxis(labels_size=12, labels=labels),
            horizontal_grid_lines=ft.ChartGridLines(color=ft.Colors.BLUE_GREY_50, width=0.5),
            vertical_grid_lines=ft.ChartGridLines(color=ft.Colors.BLUE_GREY_50, width=0.5),
            min_y=60,
            max_y=90,
            expand=True,
        )
        status = Chip("Normal", color=Tokens.OK, bg=Tokens.OK_50)
        head = ft.Row([ft.Row([ft.Icon(ft.Icons.MONITOR_HEART, size=16, color=ft.Colors.DEEP_PURPLE_400), ft.Text("Frecuencia Cardíaca", weight=ft.FontWeight.W_600, size=14)], spacing=8), status], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        box = ft.Container(content=ft.Column([head, ft.Container(chart, height=180)], spacing=8), bgcolor=Tokens.SURFACE, border_radius=Tokens.RADIUS, border=ft.border.all(0.5, Tokens.BORDER), padding=Rellenar .all(16))
        return box

    def build(self) -> ft.Control:
        header = ft.Row([ft.Text("Gráficos", **Tokens.H2), ft.FilledTonalButton(ft.Row([ft.Icon(ft.Icons.CALENDAR_TODAY, size=16), ft.Text("Este mes", size=12)], spacing=8))], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        lv = ft.ListView([
            ft.Container(header, margin=ft.margin.only(left=16, right=16, top=16, bottom=8)),
            ft.Container(self._bp_chart(), margin=ft.margin.symmetric(horizontal=16, vertical=8)),
            ft.Container(self._hr_chart(), margin=ft.margin.symmetric(horizontal=16, vertical=8)),
            EspaciadorBarra(),
        ], expand=True)
        return lv
