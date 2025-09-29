import re
from datetime import datetime
import flet as ft
from ..tokens import Tokens
from ..componentes import EspaciadorBarra, Chip
from estado import ROUTES

class Vista_de_gráficos:
    def __init__(self, app):
        self.app = app

        # --- asegurar listas de estado ---
        if not hasattr(self.app.state, "bp_series") or self.app.state.bp_series is None:
            self.app.state.bp_series = []
        if not hasattr(self.app.state, "hr_series") or self.app.state.hr_series is None:
            self.app.state.hr_series = []

        # --- campos de entrada ---
        self.sys_field = ft.TextField(label="Sistólica", width=110, keyboard_type=ft.KeyboardType.NUMBER)
        self.dia_field = ft.TextField(label="Diastólica", width=110, keyboard_type=ft.KeyboardType.NUMBER)
        self.bpm_field = ft.TextField(label="BPM", width=110, keyboard_type=ft.KeyboardType.NUMBER)

        self.date_field = ft.TextField(
            label="Fecha",
            hint_text="dd/mm/aaaa",
            width=160,
            on_change=self._on_date_text_change,
        )
        self.time_field = ft.TextField(
            label="Hora",
            hint_text="HH:MM",
            width=120,
            on_change=self._on_time_text_change,
        )

        self.btn_now = ft.IconButton(icon=ft.Icons.ACCESS_TIME, tooltip="Usar ahora", on_click=self._fill_now)
        self.btn_clear = ft.IconButton(icon=ft.Icons.CLEAR, tooltip="Limpiar", on_click=self._clear_fields)

        self.add_button = ft.ElevatedButton("Agregar", icon=ft.Icons.ADD, on_click=self._add_record, expand=True)

        self.note_text = ft.Text(
            "Ingrese Sistólica+Diastólica y/o BPM. Fecha en formato dd/mm/aaaa.",
            size=11,
            color=ft.Colors.GREY,
        )

        self.records_list = ft.ListView(spacing=8, expand=True, auto_scroll=True)

        # referencias a gráficos
        self._bp_chart_control = None
        self._hr_chart_control = None

    # ----------------- autocompletar fecha/hora -----------------
    def _on_date_text_change(self, e):
        txt = (self.date_field.value or "").strip()
        if not txt:
            return
        clean = re.sub(r"[^0-9]", "", txt)
        try:
            if len(clean) == 6:
                dd, mm, yy = int(clean[:2]), int(clean[2:4]), int(clean[4:6])
                year = 2000 + yy if yy < 50 else 1900 + yy
                dt = datetime(year, mm, dd)
                self.date_field.value = dt.strftime("%d/%m/%Y")
                self.date_field.update()
            elif len(clean) == 8:
                dd, mm, yyyy = int(clean[:2]), int(clean[2:4]), int(clean[4:8])
                dt = datetime(yyyy, mm, dd)
                self.date_field.value = dt.strftime("%d/%m/%Y")
                self.date_field.update()
        except Exception:
            pass

    def _on_time_text_change(self, e):
        txt = (self.time_field.value or "").strip()
        clean = re.sub(r"[^0-9]", "", txt)
        try:
            if len(clean) == 3:  # HMM
                hh, mm = int(clean[0]), int(clean[1:])
                if 0 <= hh < 24 and 0 <= mm < 60:
                    self.time_field.value = f"{hh:02d}:{mm:02d}"
                    self.time_field.update()
            elif len(clean) == 4:  # HHMM
                hh, mm = int(clean[:2]), int(clean[2:])
                if 0 <= hh < 24 and 0 <= mm < 60:
                    self.time_field.value = f"{hh:02d}:{mm:02d}"
                    self.time_field.update()
        except Exception:
            pass

    def _fill_now(self, e):
        now = datetime.now()
        self.date_field.value = now.strftime("%d/%m/%Y")
        self.time_field.value = now.strftime("%H:%M")
        self.date_field.update(); self.time_field.update()

    def _clear_fields(self, e):
        for f in [self.sys_field, self.dia_field, self.bpm_field, self.date_field, self.time_field]:
            f.value = ""
            f.update()

    # ----------------- utilidades -----------------
    def _bp_series(self):
        return self.app.state.bp_series

    def _hr_series(self):
        return self.app.state.hr_series

    # ----------------- agregar registro -----------------
    def _add_record(self, e):
        date_text = (self.date_field.value or "").strip() or datetime.now().strftime("%d/%m/%Y")
        time_text = (self.time_field.value or "").strip() or datetime.now().strftime("%H:%M")
        timestamp = f"{date_text} {time_text}"

        sys_v = self.sys_field.value.strip() if self.sys_field.value else None
        dia_v = self.dia_field.value.strip() if self.dia_field.value else None
        bpm_v = self.bpm_field.value.strip() if self.bpm_field.value else None

        added = False

        if sys_v and dia_v:
            try:
                sys_v, dia_v = int(sys_v), int(dia_v)
                self.app.state.bp_series.append({"date": timestamp, "sys": sys_v, "dia": dia_v})
                added = True
                self.records_list.controls.insert(
                    0,
                    ft.ListTile(
                        title=ft.Text(f"{sys_v}/{dia_v} mmHg", weight=ft.FontWeight.BOLD),
                        subtitle=ft.Text(timestamp, size=11, color=ft.Colors.GREY),
                        leading=ft.Icon(ft.Icons.FAVORITE, color=ft.Colors.RED_400),
                    ),
                )
            except:
                pass

        if bpm_v:
            try:
                bpm_v = int(bpm_v)
                self.app.state.hr_series.append({"date": timestamp, "bpm": bpm_v})
                added = True
                self.records_list.controls.insert(
                    0,
                    ft.ListTile(
                        title=ft.Text(f"{bpm_v} bpm", weight=ft.FontWeight.BOLD),
                        subtitle=ft.Text(timestamp, size=11, color=ft.Colors.GREY),
                        leading=ft.Icon(ft.Icons.MONITOR_HEART, color=ft.Colors.DEEP_PURPLE_300),
                    ),
                )
            except:
                pass

        if not added:
            self.app.snack_bar = ft.SnackBar(ft.Text("Ingrese valores válidos."))
            self.app.snack_bar.open = True
            self.app.update()
            return

        # limpiar numéricos
        for f in [self.sys_field, self.dia_field, self.bpm_field]:
            f.value = ""
            f.update()

        self._refresh_charts()
        self.records_list.update()

    def _refresh_charts(self):
        if self._bp_chart_control:
            self._bp_chart_control.content = self._build_bp_chart().content
            self._bp_chart_control.update()
        if self._hr_chart_control:
            self._hr_chart_control.content = self._build_hr_chart().content
            self._hr_chart_control.update()

    # ----------------- construir gráficos -----------------
    def _build_bp_chart(self):
        series = self.app.state.bp_series
        if not series:
            return ft.Container()

        pts_sys = [ft.LineChartDataPoint(i, d["sys"]) for i, d in enumerate(series)]
        pts_dia = [ft.LineChartDataPoint(i, d["dia"]) for i, d in enumerate(series)]
        labels = [ft.ChartAxisLabel(value=i, label=ft.Text(d["date"].split()[0], size=11)) for i, d in enumerate(series)]

        chart = ft.LineChart(
            data_series=[
                ft.LineChartData(data_points=pts_sys, color=ft.Colors.RED, stroke_width=3, curved=True),
                ft.LineChartData(data_points=pts_dia, color=ft.Colors.BLUE, stroke_width=3, curved=True),
            ],
            left_axis=ft.ChartAxis(labels_size=34),
            bottom_axis=ft.ChartAxis(labels_size=14, labels=labels),
            horizontal_grid_lines=ft.ChartGridLines(color=ft.Colors.BLUE_GREY_100, width=0.6),
            vertical_grid_lines=ft.ChartGridLines(color=ft.Colors.BLUE_GREY_100, width=0.6),
            min_y=min(min(d["dia"], d["sys"]) for d in series) - 10,
            max_y=max(max(d["dia"], d["sys"]) for d in series) + 10,
            expand=True,
        )

        legend = ft.Row([
            ft.Row([ft.Container(width=12, height=12, border_radius=6, bgcolor=ft.Colors.RED), ft.Text("Sistólica")], spacing=8),
            ft.Row([ft.Container(width=12, height=12, border_radius=6, bgcolor=ft.Colors.BLUE), ft.Text("Diastólica")], spacing=8),
        ], alignment=ft.MainAxisAlignment.CENTER)

        return ft.Container(
            ft.Column([
                ft.Row([ft.Icon(ft.Icons.FAVORITE, color=ft.Colors.RED), ft.Text("Presión Arterial", weight=ft.FontWeight.W_600, size=16)]),
                ft.Container(chart, height=240),
                legend,
            ], spacing=10),
            bgcolor=Tokens.SURFACE,
            border_radius=Tokens.RADIUS,
            padding=12,
            shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.BLUE_GREY_50),
        )

    def _build_hr_chart(self):
        series = self.app.state.hr_series
        if not series:
            return ft.Container()

        pts = [ft.LineChartDataPoint(i, d["bpm"]) for i, d in enumerate(series)]
        labels = [ft.ChartAxisLabel(value=i, label=ft.Text(d["date"].split()[0], size=11)) for i, d in enumerate(series)]

        chart = ft.LineChart(
            data_series=[ft.LineChartData(data_points=pts, color=ft.Colors.DEEP_PURPLE_400, stroke_width=3, curved=True)],
            left_axis=ft.ChartAxis(labels_size=34),
            bottom_axis=ft.ChartAxis(labels_size=14, labels=labels),
            horizontal_grid_lines=ft.ChartGridLines(color=ft.Colors.BLUE_GREY_100, width=0.6),
            vertical_grid_lines=ft.ChartGridLines(color=ft.Colors.BLUE_GREY_100, width=0.6),
            min_y=min(d["bpm"] for d in series) - 10,
            max_y=max(d["bpm"] for d in series) + 10,
            expand=True,
        )

        status = Chip("Normal", color=Tokens.OK, bg=Tokens.OK_50)

        return ft.Container(
            ft.Column([
                ft.Row([ft.Icon(ft.Icons.MONITOR_HEART, color=ft.Colors.DEEP_PURPLE_400), ft.Text("Frecuencia Cardíaca", weight=ft.FontWeight.W_600, size=16), status], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(chart, height=200),
            ], spacing=10),
            bgcolor=Tokens.SURFACE,
            border_radius=Tokens.RADIUS,
            padding=12,
            shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.BLUE_GREY_50),
        )

    # ----------------- formulario -----------------
    def _form_section(self):
        inputs_row = ft.ResponsiveRow(
            [self.sys_field, self.dia_field, self.bpm_field, self.date_field, self.time_field, self.btn_now, self.btn_clear],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            run_spacing=8,
        )
        return ft.Container(
            ft.Column([inputs_row, self.note_text, self.add_button], spacing=10),
            bgcolor=Tokens.SURFACE,
            border_radius=Tokens.RADIUS,
            padding=12,
            shadow=ft.BoxShadow(blur_radius=6, color=ft.Colors.BLUE_GREY_50),
        )

    # ----------------- layout -----------------
    def build(self) -> ft.Control:
        header = ft.Text("Gráficos", **Tokens.H2)

        self._bp_chart_control = ft.Container(self._build_bp_chart())
        self._hr_chart_control = ft.Container(self._build_hr_chart())

        content = [
            ft.Container(header, margin=ft.margin.all(16)),
            ft.Container(self._bp_chart_control, margin=ft.margin.symmetric(horizontal=16, vertical=8)),
            ft.Container(self._hr_chart_control, margin=ft.margin.symmetric(horizontal=16, vertical=8)),
            ft.Container(self._form_section(), margin=ft.margin.symmetric(horizontal=16, vertical=8)),
            ft.Container(self.records_list, margin=ft.margin.symmetric(horizontal=16, vertical=8)),
            EspaciadorBarra(),
        ]

        return ft.ListView(content, expand=True)
