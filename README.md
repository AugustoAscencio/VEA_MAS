# 📱 VEA+ – Aplicación Móvil de Salud para Nicaragua

VEA+ es una aplicación móvil y de escritorio desarrollada en **Python + Flet**, que busca transformar el seguimiento de la salud en Nicaragua.  
Está orientada a usuarios jóvenes, adultos y adultos mayores, con soporte inicial en **español y miskito**, y se conecta a fuentes oficiales como el **MINSA**.

---

## 📖 Propósito del Proyecto
Brindar a los nicaragüenses una herramienta accesible y confiable para:
- Registrar parámetros médicos y hábitos de vida.  
- Recibir recordatorios y alertas de salud.  
- Visualizar estadísticas personales y nacionales.  
- Ubicar centros de salud cercanos.  
- Acceder a notificaciones oficiales del **Ministerio de Salud (MINSA)**.  

Este proyecto nace como respuesta a la necesidad de **prevención y seguimiento constante**, frente a la falta de soluciones accesibles para el monitoreo de enfermedades crónicas como diabetes e hipertensión.

---

## ✨ Características Principales
- 🔐 **Login / Registro interactivo** mediante chatbot.  
- 🌐 **Idiomas soportados**: Español y Miskito.  
- 🤖 **Chatbot inteligente** (simulación de LLaMA) para cuestionarios de salud.  
- 📊 **Estadísticas locales y personales** con gráficos interactivos.  
- 🏥 **Mapa de clínicas y hospitales** con integración a Google Maps.  
- 📢 **Alertas oficiales del MINSA**.  
- 📤 **Exportación de reportes médicos** (Word/PDF).  
- 📱 **Compatibilidad multiplataforma**: Web, Android, iOS y Escritorio.  

---

## 📂 Estructura del Proyecto
El proyecto está organizado en módulos dentro de `src/`:

```
src/
 ├── UI/
 │   ├── Login.py            # Chatbot de login y registro (Español/Miskito)
 │   ├── InformacionMinsa.py # Estadísticas y logros clave del MINSA
 │   └── ...
 ├── assets/                 # Recursos gráficos e íconos
 ├── main.py                 # Punto de entrada principal de la aplicación
 └── ...
```

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

## 📊 Requerimientos (Resumen SRS)

### Funcionalidad (FURPS+)
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
- Base de datos centralizada en **MySQL**.  
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