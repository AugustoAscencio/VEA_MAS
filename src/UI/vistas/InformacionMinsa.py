import flet as ft

class MINSAInfoVerEspañol:
    def __init__(self, app):
        self.app = app

    def _get_styles(self):
        return {
            "primary_color": ft.Colors.BLUE_900,
            "surface_color": ft.Colors.WHITE,
            "text_color": ft.Colors.BLACK,
            "muted_text": ft.Colors.BLUE_GREY_600,
            "border_color": ft.Colors.BLUE_GREY_100,
            "background_color": ft.Colors.BLUE_GREY_50,
            "radius": 12,
            "gutter": 18,
        }

    def _create_section(self, title: str, content: ft.Control, icon: str = None):
        styles = self._get_styles()
        header = ft.Row(
            [
                ft.Row(
                    [
                        ft.Icon(icon, size=16, color=styles["primary_color"]),
                        ft.Text(title, size=18, weight="bold", color=styles["primary_color"]),
                    ],
                    spacing=8,
                ) if icon else ft.Row([ft.Text(title, size=18, weight="bold", color=styles["primary_color"])]),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        return ft.Container(
            content=ft.Column([header, content], spacing=12),
            bgcolor=styles["surface_color"],
            border_radius=styles["radius"],
            border=ft.border.all(0.5, styles["border_color"]),
            padding=ft.padding.all(16),
        )

    def _create_card(self, content: ft.Control):
        styles = self._get_styles()
        return ft.Container(
            content=content,
            bgcolor=styles["surface_color"],
            border_radius=styles["radius"],
            border=ft.border.all(0.5, styles["border_color"]),
            padding=ft.padding.all(14),
            expand=True
        )

    def _cabecera(self) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Ministerio de Salud de Nicaragua",
                        size=28,
                        weight="bold",
                        color=self._get_styles()["primary_color"],
                        text_align="center"
                    ),
                    ft.Text(
                        "Trabajando por el bienestar y el derecho a la salud de todas las familias.",
                        size=14,
                        color=self._get_styles()["muted_text"],
                        text_align="center",
                        italic=True
                    )
                ],
                alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=ft.padding.only(top=30, bottom=20),
            alignment=ft.alignment.center
        )

    def _mision_vision_objetivo(self) -> ft.Container:
        styles = self._get_styles()

        mision_card = self._create_card(
            ft.Column([
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.MAP, color=styles["primary_color"]),
                    title=ft.Text("Misión", size=16, weight="bold"),
                    subtitle=ft.Text(
                        "Restituir el derecho a la salud de la población nicaragüense mediante el MOSAFC, garantizando atención de calidad, calidez, equidad y gratuidad.",
                        size=12,
                        color=styles["muted_text"]
                    )
                ),
                ft.TextButton("Leer más", url="https://www.minsa.gob.ni/la-institucion/mision-y-vision")
            ], spacing=6)
        )

        vision_card = self._create_card(
            ft.Column([
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.VISIBILITY, color=styles["primary_color"]),
                    title=ft.Text("Visión", size=16, weight="bold"),
                    subtitle=ft.Text(
                        "Garantizar la salud como derecho constitucional fundamental y factor esencial del desarrollo social y económico, con cobertura universal.",
                        size=12,
                        color=styles["muted_text"]
                    )
                ),
                ft.TextButton("Leer más", url="https://www.minsa.gob.ni/la-institucion/mision-y-vision")
            ], spacing=6)
        )

        objetivo_card = self._create_card(
            ft.Column([
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.ADS_CLICK, color=styles["primary_color"]),
                    title=ft.Text("Objetivo Institucional", size=16, weight="bold"),
                    subtitle=ft.Text(
                        "Desarrollar un sistema de salud que haga efectivo el derecho ciudadano a la salud, impulsando promoción, prevención y rehabilitación.",
                        size=12,
                        color=styles["muted_text"]
                    )
                ),
                ft.TextButton("Leer más", url="https://www.minsa.gob.ni/la-institucion/mision-y-vision")
            ], spacing=6)
        )

        return self._create_section(
            "Misión, Visión y Objetivo",
            ft.Column([mision_card, vision_card, objetivo_card], spacing=15),
            icon=ft.Icons.INFO_OUTLINE
        )

    def _servicios_red(self) -> ft.Container:
        styles = self._get_styles()

        return self._create_section(
            "Servicios y Red de Salud",
            ft.Column([
                ft.Text(
                    "El MINSA opera a través de una red nacional de hospitales, centros, puestos de salud y casas maternas:", 
                    weight="bold", size=12, color=styles["text_color"]
                ),
                ft.Divider(height=1, color=styles["border_color"]),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.LOCAL_HOSPITAL, color=ft.Colors.RED_ACCENT_700),
                    title=ft.Text("Hospitales", size=14, weight="w600"),
                    subtitle=ft.Text("Atención de especialidades médicas y cirugías complejas.", color=styles["muted_text"])
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.MEDICAL_SERVICES, color=ft.Colors.BLUE_ACCENT_700),
                    title=ft.Text("Centros de Salud", size=14, weight="w600"),
                    subtitle=ft.Text("Consulta externa, vacunación y programas de salud.", color=styles["muted_text"])
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.HEALTH_AND_SAFETY, color=ft.Colors.GREEN_ACCENT_700),
                    title=ft.Text("Puestos de Salud", size=14, weight="w600"),
                    subtitle=ft.Text("Atención primaria en comunidades rurales.", color=styles["muted_text"])
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.PREGNANT_WOMAN, color=ft.Colors.PURPLE_ACCENT_700),
                    title=ft.Text("Casas Maternas", size=14, weight="w600"),
                    subtitle=ft.Text("Alojamiento y cuidado para embarazadas de zonas alejadas.", color=styles["muted_text"])
                ),
                ft.Divider(height=1, color=styles["border_color"]),
                ft.TextButton("Ver detalle de la red de servicios", url="https://www.minsa.gob.ni/entidades/servicios-salud")
            ], spacing=6),
            icon=ft.Icons.LOCAL_PHARMACY
        )

    def _campañas(self) -> ft.Container:
        campañas_data = [
            {"titulo": "Jornada de Vacunación", "desc": "Contra la Influenza, COVID-19 y otras enfermedades.", "icono": ft.Icons.VACCINES},
            {"titulo": "Escuelas Saludables", "desc": "Atención integral para estudiantes y docentes.", "icono": ft.Icons.SCHOOL},
            {"titulo": "Lucha Antiepidémica", "desc": "Fumigación y abatización contra zancudos.", "icono": ft.Icons.PEST_CONTROL},
            {"titulo": "Prevención del Cáncer", "desc": "Chequeos preventivos como mamografías y papanicolau.", "icono": ft.Icons.COLORIZE},
            {"titulo": "Juventud Saludable", "desc": "Promoción de nutrición y salud sexual.", "icono": ft.Icons.EMOJI_PEOPLE},
            {"titulo": "Operación Milagro", "desc": "Cirugías oftalmológicas gratuitas.", "icono": ft.Icons.VISIBILITY},
        ]

        campañas_cards = ft.Column([
            ft.Card(
                content=ft.ListTile(
                    leading=ft.Icon(data["icono"], color=ft.Colors.DEEP_ORANGE_ACCENT_400),
                    title=ft.Text(data["titulo"], size=14, weight="bold"),
                    subtitle=ft.Text(data["desc"], size=11),
                    on_click=lambda e: self.app.page.launch_url("https://www.minsa.gob.ni/campanas")
                ), elevation=1
            ) for data in campañas_data
        ], spacing=12)

        return self._create_section(
            "Campañas Nacionales de Salud",
            ft.Column([
                ft.Text("Conoce las principales campañas de salud en Nicaragua.", size=12, color=ft.Colors.BLUE_GREY_700),
                campañas_cards,
                ft.TextButton("Ver todas las campañas", url="https://www.minsa.gob.ni/campanas")
            ], spacing=12),
            icon=ft.Icons.CAMPAIGN
        )

    def _normativas(self) -> ft.Container:
        styles = self._get_styles()

        normas_list = ft.Column([
            ft.ListTile(leading=ft.Icon(ft.Icons.BOOK, color=styles["primary_color"]), title=ft.Text("Prevención y control de la rabia humana", color=styles["text_color"])),
            ft.ListTile(leading=ft.Icon(ft.Icons.BOOK, color=styles["primary_color"]), title=ft.Text("Atención integral al recién nacido", color=styles["text_color"])),
            ft.ListTile(leading=ft.Icon(ft.Icons.BOOK, color=styles["primary_color"]), title=ft.Text("Protocolos de atención prenatal y puerperio", color=styles["text_color"])),
            ft.ListTile(leading=ft.Icon(ft.Icons.BOOK, color=styles["primary_color"]), title=ft.Text("Manual de vigilancia epidemiológica", color=styles["text_color"])),
            ft.ListTile(leading=ft.Icon(ft.Icons.BOOK, color=styles["primary_color"]), title=ft.Text("Reglamento de la Ley General de Salud", color=styles["text_color"])),
            ft.ListTile(leading=ft.Icon(ft.Icons.BOOK, color=styles["primary_color"]), title=ft.Text("Manual de seguridad del paciente", color=styles["text_color"])),
        ])

        return self._create_section(
            "Normativas y Regulaciones",
            ft.Column([
                ft.Text("El MINSA rige sus acciones con un marco legal y normativo.", size=12, color=styles["muted_text"]),
                normas_list,
                ft.TextButton("Acceder a normativas", url="https://www.minsa.gob.ni/index.php/taxonomy/term/118"),
                ft.TextButton("Ley General de Salud", url="https://legislacion.asamblea.gob.ni/Normaweb.nsf/(All)/FF82EA58EC7C712E062570A1005810E1")
            ], spacing=12),
            icon=ft.Icons.GAVEL
        )



    def _estadisticas(self) -> ft.Container:
        styles = self._get_styles()

        def crear_tarjeta(icon, titulo, valor, descripcion, color):
            return ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Icon(icon, color=color, size=22),
                                ft.Text(titulo, size=12, color=styles["muted_text"]),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=6,
                        ),
                        ft.Text(
                            valor,
                            size=22,
                            weight="bold",
                            color=color,
                            text_align="center",
                        ),
                        ft.Text(
                            descripcion,
                            size=11,
                            color=styles["muted_text"],
                            text_align="center",
                        ),
                    ],
                    spacing=6,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                bgcolor=styles["surface_color"],
                border_radius=styles["radius"],
                border=ft.border.all(0.5, styles["border_color"]),
                padding=ft.padding.all(12),
            )

        estadisticas_cards = ft.Row(
            [
                crear_tarjeta(ft.Icons.PEOPLE_ALT, "Cobertura de salud", "95%", "Población con acceso a servicios.", ft.Colors.LIGHT_BLUE_700),
                crear_tarjeta(ft.Icons.LOCAL_PHARMACY, "Medicamentos", "98%", "Disponibilidad de esenciales.", ft.Colors.ORANGE_ACCENT_700),
                crear_tarjeta(ft.Icons.CHILD_CARE, "Vacunación infantil", "92%", "Cobertura nacional en menores de 5 años.", ft.Colors.GREEN_600),
                crear_tarjeta(ft.Icons.FAVORITE, "Mortalidad materna", "33 x100mil", "Reducción significativa en 2024.", ft.Colors.RED_ACCENT_400),
                crear_tarjeta(ft.Icons.HEALTH_AND_SAFETY, "Partos institucionales", "94%", "Atendidos en hospitales y casas maternas.", ft.Colors.PURPLE_600),
            ],
            spacing=12,
            run_spacing=12,
            alignment=ft.MainAxisAlignment.START,
            wrap=True  # 👈 en Row funciona
        )

        return self._create_section(
            "Estadísticas y Logros Clave",
            ft.Column(
                [
                    ft.Text("Indicadores destacados de la gestión de salud en el país.", size=12, color=ft.Colors.BLUE_GREY_700),
                    estadisticas_cards,
                ],
                spacing=15,
            ),
            icon=ft.Icons.INSIGHTS,
        )



    def _contacto(self) -> ft.Container:
        styles = self._get_styles()

        return self._create_section(
            "Contacto",
            ft.Column(
                [
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.LOCATION_ON, color=styles["primary_color"]),
                        title=ft.Text("Dirección", size=14, weight="w600"),
                        subtitle=ft.Text(
                            "Costado Oeste Colonia Primero de Mayo, Managua",
                            color=styles["muted_text"]
                        ),
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.PHONE, color=styles["primary_color"]),
                        title=ft.Text("Teléfonos", size=14, weight="w600"),
                        subtitle=ft.Text(
                            "PBX: (505) 2264-7630 / 2264-7730 / 7517-0700",
                            color=styles["muted_text"]
                        ),
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.MAIL, color=styles["primary_color"]),
                        title=ft.Text("Correo Electrónico", size=14, weight="w600"),
                        subtitle=ft.Text(
                            "info@minsa.gob.ni",
                            color=styles["muted_text"]
                        ),
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.LANGUAGE, color=styles["primary_color"]),
                        title=ft.Text("Sitio web oficial", size=14, weight="w600"),
                        subtitle=ft.Text(
                            "https://www.minsa.gob.ni",
                            color=styles["muted_text"]
                        ),
                        on_click=lambda e: self.app.page.launch_url("https://www.minsa.gob.ni"),
                    ),
                ],
                spacing=8
            ),
            icon=ft.Icons.CONTACT_MAIL
        )

    def build(self) -> ft.ListView:
        return ft.ListView(
            controls=[
                self._cabecera(),
                self._mision_vision_objetivo(),
                self._servicios_red(),
                self._campañas(),
                self._normativas(),
                self._estadisticas(),
                self._contacto(),
            ],
            spacing=20,
            padding=20,
            expand=True,
        )


def get_minsa_view(page: ft.Page):
        """Devuelve la vista del MINSA lista para integrarse al main"""
        class MockApp:
            def __init__(self, page):
                self.page = page

        vista = MINSAInfoVerEspañol(app=MockApp(page))
        return vista.build()



class MINSAInfoVerMiskito:
    def __init__(self, app):
        self.app = app

    def _get_styles(self):
        return {
            "primary_color": ft.Colors.BLUE_900,
            "surface_color": ft.Colors.WHITE,
            "text_color": ft.Colors.BLACK,
            "muted_text": ft.Colors.BLUE_GREY_600,
            "border_color": ft.Colors.BLUE_GREY_100,
            "background_color": ft.Colors.BLUE_GREY_50,
            "radius": 12,
            "gutter": 18,
        }

    def _create_section(self, title: str, content: ft.Control, icon: str = None):
        styles = self._get_styles()
        header = ft.Row(
            [
                ft.Row(
                    [
                        ft.Icon(icon, size=16, color=styles["primary_color"]),
                        ft.Text(title, size=18, weight="bold", color=styles["primary_color"]),
                    ],
                    spacing=8,
                ) if icon else ft.Row([ft.Text(title, size=18, weight="bold", color=styles["primary_color"])]),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        return ft.Container(
            content=ft.Column([header, content], spacing=12),
            bgcolor=styles["surface_color"],
            border_radius=styles["radius"],
            border=ft.border.all(0.5, styles["border_color"]),
            padding=ft.padding.all(16),
        )

    def _create_card(self, content: ft.Control):
        styles = self._get_styles()
        return ft.Container(
            content=content,
            bgcolor=styles["surface_color"],
            border_radius=styles["radius"],
            border=ft.border.all(0.5, styles["border_color"]),
            padding=ft.padding.all(14),
            expand=True
        )

    def _cabecera(self) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Nicaragua Siki Lakaia Minsitri-ka",
                        size=28,
                        weight="bold",
                        color=self._get_styles()["primary_color"],
                        text_align="center"
                    ),
                    ft.Text(
                        "Apia swin lakaia ka siknis sika lakaia ra bui kaikanka lakaia tuktan nani ra.",
                        size=14,
                        color=self._get_styles()["muted_text"],
                        text_align="center",
                        italic=True
                    )
                ],
                alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=ft.padding.only(top=30, bottom=20),
            alignment=ft.alignment.center
        )

    def _mision_vision_objetivo(self) -> ft.Container:
        styles = self._get_styles()

        mision_card = self._create_card(
            ft.Column([
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.MAP, color=styles["primary_color"]),
                    title=ft.Text("Wihka laka", size=16, weight="bold"),
                    subtitle=ft.Text(
                        "Nicaragua-kaia uplikaia siknis sika lakaia ra bui kaikanka lakaia wihka laka ra, MOSAFC laka ra, bui kaikanka lakaia tara, apia, ka apia dubaia ka wihkaia bui kaikanka lakaia.",
                        size=12,
                        color=styles["muted_text"]
                    )
                ),
                ft.TextButton("Kaia laka", url="https://www.minsa.gob.ni/la-institucion/mision-y-vision")
            ], spacing=6)
        )

        vision_card = self._create_card(
            ft.Column([
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.VISIBILITY, color=styles["primary_color"]),
                    title=ft.Text("Apia laka", size=16, weight="bold"),
                    subtitle=ft.Text(
                        "Siki lakaia kaia wihka dubaia ra, kaia wihka laka ra, kaia wihka laka ra, kaia wihka laka ra, kaia wihka laka ra, kaia wihka laka ra, kaia wihka laka ra, kaia wihka laka ra.",
                        size=12,
                        color=styles["muted_text"]
                    )
                ),
                ft.TextButton("Kaia laka", url="https://www.minsa.gob.ni/la-institucion/mision-y-vision")
            ], spacing=6)
        )

        objetivo_card = self._create_card(
            ft.Column([
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.ADS_CLICK, color=styles["primary_color"]),
                    title=ft.Text("Instiutishn lakaia turka laka", size=16, weight="bold"),
                    subtitle=ft.Text(
                        "Siki lakaia sistim-ka pakan uplikaia siki lakaia tura laka ra, promotion, prevention, ka rehabilitation ra.",
                        size=12,
                        color=styles["muted_text"]
                    )
                ),
                ft.TextButton("Kaia laka", url="https://www.minsa.gob.ni/la-institucion/mision-y-vision")
            ], spacing=6)
        )

        return self._create_section(
            "Wihka laka, apia laka, ka naha lakaia tura laka",
            ft.Column([mision_card, vision_card, objetivo_card], spacing=15),
            icon=ft.Icons.INFO_OUTLINE
        )

    def _servicios_red(self) -> ft.Container:
        styles = self._get_styles()

        return self._create_section(
            "Dawan lakaia ka siki lakaia netwurk-ka",
            ft.Column([
                ft.Text(
                    "MINSA-ka wihkaia hospital nani, senter nani, siki lakaia puestos nani, ka madar nani ra:",
                    weight="bold", size=12, color=styles["text_color"]
                ),
                ft.Divider(height=1, color=styles["border_color"]),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.LOCAL_HOSPITAL, color=ft.Colors.RED_ACCENT_700),
                    title=ft.Text("Hospitl nani", size=14, weight="w600"),
                    subtitle=ft.Text("Speshlti siknis bui kaikanka ka layaia kris nani.", color=styles["muted_text"])
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.MEDICAL_SERVICES, color=ft.Colors.BLUE_ACCENT_700),
                    title=ft.Text("Siki lakaia senter nani", size=14, weight="w600"),
                    subtitle=ft.Text("Outsaiyd konsulta, baksinishn ka siki lakaia programa nani.", color=styles["muted_text"])
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.HEALTH_AND_SAFETY, color=ft.Colors.GREEN_ACCENT_700),
                    title=ft.Text("Siki lakaia puestos nani", size=14, weight="w600"),
                    subtitle=ft.Text("Aysaia bui kaikankaia siki lakaia komyuniti nani ra.", color=styles["muted_text"])
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.PREGNANT_WOMAN, color=ft.Colors.PURPLE_ACCENT_700),
                    title=ft.Text("Madar nani", size=14, weight="w600"),
                    subtitle=ft.Text("Saki ka bui kaikankaia naha naha pregnant madar nani ra.", color=styles["muted_text"])
                ),
                ft.Divider(height=1, color=styles["border_color"]),
                ft.TextButton("Wihkaia dawan lakaia netwurk-ka", url="https://www.minsa.gob.ni/entidades/servicios-salud")
            ], spacing=6),
            icon=ft.Icons.LOCAL_PHARMACY
        )

    def _campañas(self) -> ft.Container:
        campañas_data = [
            {"titulo": "Baksinishn lakaia jarni", "desc": "Influenza, COVID-19 ka wihka siknis nani ra.", "icono": ft.Icons.VACCINES},
            {"titulo": "Siki lakaia skul nani", "desc": "Studiant nani ka ticha nani ra.", "icono": ft.Icons.SCHOOL},
            {"titulo": "Epidemik nani ra", "desc": "Fumigishn ka abatishn lakaia ra.", "icono": ft.Icons.PEST_CONTROL},
            {"titulo": "Kansar lakaia prevenshn", "desc": "Prevntiv chek nani ra.", "icono": ft.Icons.COLORIZE},
            {"titulo": "Siki lakaia yut", "desc": "Nutrishn ka sexwal siki lakaia promotion.", "icono": ft.Icons.EMOJI_PEOPLE},
            {"titulo": "Opresishn Milagro", "desc": "Oftalmolgical kirjri nani.", "icono": ft.Icons.VISIBILITY},
        ]

        campañas_cards = ft.Column([
            ft.Card(
                content=ft.ListTile(
                    leading=ft.Icon(data["icono"], color=ft.Colors.DEEP_ORANGE_ACCENT_400),
                    title=ft.Text(data["titulo"], size=14, weight="bold"),
                    subtitle=ft.Text(data["desc"], size=11),
                    on_click=lambda e: self.app.page.launch_url("https://www.minsa.gob.ni/campanas")
                ), elevation=1
            ) for data in campañas_data
        ], spacing=12)

        return self._create_section(
            "Nishnal siki lakaia kampen nani",
            ft.Column([
                ft.Text("Naha Nicaragua lakaia siki lakaia kampen nani ra.", size=12, color=ft.Colors.BLUE_GREY_700),
                campañas_cards,
                ft.TextButton("Wihkaia kampen nani", url="https://www.minsa.gob.ni/campanas")
            ], spacing=12),
            icon=ft.Icons.CAMPAIGN
        )

    def _normativas(self) -> ft.Container:
        styles = self._get_styles()

        normas_list = ft.Column([
            ft.ListTile(leading=ft.Icon(ft.Icons.BOOK, color=styles["primary_color"]), title=ft.Text("Prevension ka kontrol lakaia ra.", color=styles["text_color"])),
            ft.ListTile(leading=ft.Icon(ft.Icons.BOOK, color=styles["primary_color"]), title=ft.Text("Komprhnsiv bui kaikankaia nyu-baba nani ra.", color=styles["text_color"])),
            ft.ListTile(leading=ft.Icon(ft.Icons.BOOK, color=styles["primary_color"]), title=ft.Text("Prenatl bui kaikankaia protokol nani.", color=styles["text_color"])),
            ft.ListTile(leading=ft.Icon(ft.Icons.BOOK, color=styles["primary_color"]), title=ft.Text("Epideml-jikl vigilns lakaia manwl.", color=styles["text_color"])),
            ft.ListTile(leading=ft.Icon(ft.Icons.BOOK, color=styles["primary_color"]), title=ft.Text("Jeneral Siki Lakaia Ley lakaia reglament.", color=styles["text_color"])),
            ft.ListTile(leading=ft.Icon(ft.Icons.BOOK, color=styles["primary_color"]), title=ft.Text("Peshent sekurity lakaia manwl.", color=styles["text_color"])),
        ])

        return self._create_section(
            "Normativ nani ka regulishn nani",
            ft.Column([
                ft.Text("MINSA-ka wihkaia lakaia tura laka ra.", size=12, color=styles["muted_text"]),
                normas_list,
                ft.TextButton("Akses normativ nani ra", url="https://www.minsa.gob.ni/index.php/taxonomy/term/118"),
                ft.TextButton("Jeneral Siki Lakaia Ley", url="https://legislacion.asamblea.gob.ni/Normaweb.nsf/(All)/FF82EA58EC7C712E062570A1005810E1")
            ], spacing=12),
            icon=ft.Icons.GAVEL
        )



    def _estadisticas(self) -> ft.Container:
        styles = self._get_styles()

        def crear_tarjeta(icon, titulo, valor, descripcion, color):
            return ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Icon(icon, color=color, size=22),
                                ft.Text(titulo, size=12, color=styles["muted_text"]),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=6,
                        ),
                        ft.Text(
                            valor,
                            size=22,
                            weight="bold",
                            color=color,
                            text_align="center",
                        ),
                        ft.Text(
                            descripcion,
                            size=11,
                            color=styles["muted_text"],
                            text_align="center",
                        ),
                    ],
                    spacing=6,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                bgcolor=styles["surface_color"],
                border_radius=styles["radius"],
                border=ft.border.all(0.5, styles["border_color"]),
                padding=ft.padding.all(12),
            )

        estadisticas_cards = ft.Row(
            [
                crear_tarjeta(ft.Icons.PEOPLE_ALT, "Siki lakaia kobrtur", "95%", "Servis nani ra.", ft.Colors.LIGHT_BLUE_700),
                crear_tarjeta(ft.Icons.LOCAL_PHARMACY, "Medisen nani", "98%", "Esensial nani ra.", ft.Colors.ORANGE_ACCENT_700),
                crear_tarjeta(ft.Icons.CHILD_CARE, "Nit nani baksinishn", "92%", "Nashnal kobrtur lakaia ra.", ft.Colors.GREEN_600),
                crear_tarjeta(ft.Icons.FAVORITE, "Madar morthliti", "33 x100mil", "2024 lakaia redukshn.", ft.Colors.RED_ACCENT_400),
                crear_tarjeta(ft.Icons.HEALTH_AND_SAFETY, "Instiutishn partos", "94%", "Hospitl nani ka madar nani ra.", ft.Colors.PURPLE_600),
            ],
            spacing=12,
            run_spacing=12,
            alignment=ft.MainAxisAlignment.START,
            wrap=True
        )

        return self._create_section(
            "Stdistik nani ka turka lakaia lgos nani",
            ft.Column(
                [
                    ft.Text("Siki lakaia jestin lakaia indikeitor nani.", size=12, color=ft.Colors.BLUE_GREY_700),
                    estadisticas_cards,
                ],
                spacing=15,
            ),
            icon=ft.Icons.INSIGHTS,
        )



    def _contacto(self) -> ft.Container:
        styles = self._get_styles()

        return self._create_section(
            "Kontak",
            ft.Column(
                [
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.LOCATION_ON, color=styles["primary_color"]),
                        title=ft.Text("Direkshn", size=14, weight="w600"),
                        subtitle=ft.Text(
                            "Kostado Oest Koloni Primero de Mayo, Managua",
                            color=styles["muted_text"]
                        ),
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.PHONE, color=styles["primary_color"]),
                        title=ft.Text("Tilfun nani", size=14, weight="w600"),
                        subtitle=ft.Text(
                            "PBX: (505) 2264-7630 / 2264-7730 / 7517-0700",
                            color=styles["muted_text"]
                        ),
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.MAIL, color=styles["primary_color"]),
                        title=ft.Text("Koro Elektronik", size=14, weight="w600"),
                        subtitle=ft.Text(
                            "info@minsa.gob.ni",
                            color=styles["muted_text"]
                        ),
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.LANGUAGE, color=styles["primary_color"]),
                        title=ft.Text("Ofisial sait-web", size=14, weight="w600"),
                        subtitle=ft.Text(
                            "https://www.minsa.gob.ni",
                            color=styles["muted_text"]
                        ),
                        on_click=lambda e: self.app.page.launch_url("https://www.minsa.gob.ni"),
                    ),
                ],
                spacing=8
            ),
            icon=ft.Icons.CONTACT_MAIL
        )

    def build(self) -> ft.ListView:
        return ft.ListView(
            controls=[
                self._cabecera(),
                self._mision_vision_objetivo(),
                self._servicios_red(),
                self._campañas(),
                self._normativas(),
                self._estadisticas(),
                self._contacto(),
            ],
            spacing=20,
            padding=20,
            expand=True,
        )


def get_minsa_view(page: ft.Page):
        """Dvlve naha MINSA lakaia main ra"""
        class MockApp:
            def __init__(self, page):
                self.page = page

        vista = MINSAInfoVerMiskito(app=MockApp(page))
        return vista.build()

# # =======================
# #     PRUEBA UNITARIA
# # =======================
# if __name__ == "__main__":
#     def main(page: ft.Page):
#         page.title = "Prueba standalone MINSA"
#         page.scroll = ft.ScrollMode.AUTO
#         page.padding = 20
#         page.bgcolor = ft.Colors.BLUE_GREY_50

#         contenido = get_minsa_view(page)
#         page.add(contenido)

#     ft.app(target=main)