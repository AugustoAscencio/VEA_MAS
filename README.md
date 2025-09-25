# 📱 VEA+ – Aplicación Móvil de Salud para Nicaragua

VEA+ es una aplicación móvil en **Python + Flet**, que busca transformar el seguimiento de la salud en Nicaragua.  
Está orientada a usuarios jóvenes, adultos y adultos mayores, con soporte inicial en **español y miskito**, y se conecta a fuentes oficiales como el **MINSA**.

---

## 📖 Propósito del Proyecto
Brindar a los nicaragüenses una herramienta accesible y confiable para:
- Registrar parámetros médicos y hábitos de vida.  
- Recibir recordatorios y alertas de salud.  
- Visualizar estadísticas personales y nacionales.  
- Ubicar centros de salud cercanos.  
- Contar con apoyo psicológico básico mediante ejercicios de respiración guiada, registro de emociones y un chatbot empático.
- Acceder a notificaciones oficiales del **Ministerio de Salud (MINSA)**.  

Este proyecto nace como respuesta a la necesidad de **prevención y seguimiento constante**, frente a la falta de soluciones accesibles para el monitoreo de enfermedades crónicas como diabetes e hipertensión.

---

## ✨ Características Principales
- 🔐 **Login / Registro interactivo** mediante chatbot.  
- 🌐 **Idiomas soportados**: Español y Miskito.  
- 🤖 **Chatbot inteligente** (simulación de LLaMA) para cuestionarios de salud.  
- 📊 **Estadísticas locales y personales** con gráficos interactivos.  
- 🏥 **Directorio de clínicas y hospitales** con integración a Google Maps.  
- 📢 **Alertas oficiales del MINSA**.  
- 📤 **Exportación de reportes médicos** (Word/PDF).  
- 🧠 **Asistencia Psicológica** ejercicios de respiración guiada, registro de emociones y chatbot empático.
- 📱 **Compatibilidad multiplataforma**: Web, Android, iOS y Escritorio.  

---

## 📂 Estructura del Proyecto
El proyecto está organizado en módulos dentro de `src/`:

```
src/
 ├── assets/                     # Recursos gráficos e íconos
 │   ├── icon.png
 │   └── splash_android.png
 │
 ├── UI/                         # Interfaz de usuario (UI)
 │   ├── __init__.py
 │   ├── tokens.py                # Paleta de colores, estilos y tamaños
 │   ├── componentes.py           # Widgets reutilizables (tarjetas, botones, etc.)
 │   ├── barra_inferior.py        # Barra de navegación inferior
 │   ├── Login.py                 # Pantallas de login y registro (Español / Miskito)
 │   │
 │   └── vistas/                  # Vistas principales
 │       ├── __init__.py
 │       ├── inicio.py            # Pantalla principal (Acciones rápidas, etc.)
 │       ├── graficos.py          # Visualización de datos y gráficas
 │       ├── consultas.py         # Módulo de consultas médicas virtuales
 │       ├── historial.py         # Historial de consultas, registros, signos vitales
 │       ├── prediccion.py        # Vista de predicción (IA aplicada a salud)
 │       ├── chatbot.py           # Interacción con chatbot médico
 │       ├── psicologo.py         # Asistente psicológico / All-in-One
 │       └── InformacionMinsa.py  # Información oficial del Ministerio de Salud (MINSA)
 │
 ├── main.py                      # Punto de entrada principal de la aplicación
 ├── estado.py                    # Estado global de la aplicación y rutas
 ├── requirements.txt             # Dependencias del proyecto
 └── pyproject.toml               # Configuración del entorno y dependencias
---

## ⚙️ Instalación y Ejecución

### 1. Clonar el repositorio
```bash
git clone https://github.com/AugustoAscencio/VEA_MAS.git
cd VEA_MAS
```

### 2. Crear entorno virtual e instalar dependencias
```bash
python -m venv .venv
source .venv/bin/activate   # Linux / Mac
.venv\Scripts\activate      # Windows

pip install -r requirements.txt
```

### 3. Ejecutar la aplicación
```bash
flet run src/main.py -d
```

### 4. Construir versión instalable
```bash
flet pack src/main.py
```

---

## 📊 Requerimientos 

### Funcionalidad 
- **MUST**: chatbot bilingüe, cuestionarios, seguimiento de 15 padecimientos, estadísticas, mapas, alertas MINSA.  
- **SHOULD**: exportación de reportes, FAQ integrada, interfaz accesible con íconos grandes.  
- **CAN**: conexión con médicos particulares, integración con wearables.  

### Usabilidad
- Interfaz accesible a adultos mayores.  
- Idiomas: español y miskito.  

### Rendimiento
- Compatibilidad mínima: **Android 8 / 4 GB RAM**.  
- Procesamiento de gráficos local.  

### Confiabilidad
- Base de datos ligera basada en archivos tabulares
- Tolerancia máxima a pérdida de datos: minutos.  

---

## 🌎 Impacto en Nicaragua
- Más de **718,000 nicaragüenses** viven con enfermedades crónicas.  
- VEA+ busca **prevenir, acompañar y dar seguimiento constante** para mejorar la calidad de vida de pacientes y familias.  

---

## 📜 Licencia
Proyecto desarrollado en el marco de **Ideathon Nicaragua** por el equipo **Burritos Binarios**.  
Todos los derechos reservados © 2025.  
No se permite la copia, distribución, modificación o uso del código sin autorización expresa por escrito del autor.