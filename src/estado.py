import datetime
from dataclasses import dataclass, field
from typing import List, Dict

ROUTES = ["/", "/gráficos", "/consultas", "/historia", "/predicción", "/chat", "/psicologico"]

@dataclass
class Mensaje:
    Amable : str
    Texto: str
    Tiempo: str
    
@dataclass
class MensajeMiskito:
    Amable : str
    Texto: str
    Tiempo: str


@dataclass
class Estado_de_la_aplicación:
    idioma: str = "es"   # 👈 por defecto español
    active_route: str = "/"
    chat: List[Mensaje] = field(
        default_factory=lambda: [
            Mensaje("bot", "¡Hola! Soy tu asistente. ¿En qué puedo ayudarte?", datetime.datetime.now().strftime("%H:%M"))
        ]
    )
    chat: List[MensajeMiskito] = field(
        default_factory=lambda: [
            MensajeMiskito("bot", "Ai! Yang asistente bila. Ba aiwan yamni taim sa?", datetime.datetime.now().strftime("%H:%M"))
        ]
    )
    
    bp_series: List[Dict] = field(
        default_factory=lambda: [
            {"date": "1 Mar", "sys": 120, "dia": 80},
            {"date": "5 Mar", "sys": 125, "dia": 85},
            {"date": "10 Mar", "sys": 118, "dia": 78},
            {"date": "15 Mar", "sys": 122, "dia": 82},
            {"date": "20 Mar", "sys": 115, "dia": 75},
            {"date": "25 Mar", "sys": 119, "dia": 79},
            {"date": "Hoy", "sys": 121, "dia": 81},
        ]
    )
    hr_series: List[Dict] = field(
        default_factory=lambda: [
            {"date": "1 Mar", "bpm": 72},
            {"date": "5 Mar", "bpm": 78},
            {"date": "10 Mar", "bpm": 70},
            {"date": "15 Mar", "bpm": 75},
            {"date": "20 Mar", "bpm": 68},
            {"date": "25 Mar", "bpm": 73},
            {"date": "Hoy", "bpm": 74},
        ]
    )
