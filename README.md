# Carreta Romería - Gestor de Asistentes

Aplicación Django para gestionar personas que asisten a la Carreta Romería, con seguimiento de bebidas y pagos.

## Base de Datos
✅ **SQLite** - 100% gratuito, sin expiración, funcionamiento óptimo

## Características

- ✅ Gestión de asistentes con información personal
- ✅ Registro de bebidas principales, refrescos y alcohólicas
- ✅ Control de asistencia (Sábado, Domingo o ambos)
- ✅ Seguimiento de pagos
- ✅ Panel de análisis con estadísticas
- ✅ Lista de compra automática
- ✅ Búsqueda y filtros avanzados
- ✅ Sistema de autenticación seguro
- ✅ Diseño responsive para mobile

## Requisitos

- Python 3.8+
- Django 4.2.7
- PostgreSQL (para producción)

## Instalación Local

1. **Clonar el repositorio:**
```bash
git clone <URL_REPO>
cd Carreta
```

2. **Crear entorno virtual:**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno:**
```bash
cp .env.example .env
```

5. **Migrar base de datos:**
```bash
python manage.py migrate
```

6. **Crear superusuario:**
```bash
python manage.py createsuperuser
```

7. **Ejecutar servidor:**
```bash
python manage.py runserver
```

Acceder en: http://127.0.0.1:8000/

## Despliegue en Render

### Pasos:

1. **Crear repositorio en GitHub** y hacer push del código

2. **En Render.com:**
   - Crear nuevo "Web Service"
   - Conectar repositorio GitHub
   - Configurar variables de entorno:
     ```
     ALLOWED_HOSTS=tu-dominio.onrender.com
     DEBUG=False
     SECRET_KEY=tu-secret-key-aqui
     DATABASE_URL=postgresql://...
     ```

3. **Build & Start Commands:**
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn carretaRomeria.wsgi --log-file -`

4. **PostgreSQL:**
   - Crear una instancia PostgreSQL en Render
   - Copiar DATABASE_URL a variables de entorno

5. **Archivos necesarios:**
   - `Procfile` ✓
   - `requirements.txt` ✓
   - `.gitignore` ✓

## Uso

### Login
- Acceder con credenciales de superusuario

### Añadir Persona
1. Click en "Añadir Persona"
2. Completar formulario
3. Seleccionar días (Sábado, Domingo o ambos)
4. Guardar

### Gestión de Pagos
- Ver estado en tabla de personas
- Marcar como pagado en detalle de persona

### Análisis
- Ver estadísticas globales
- Distribución de bebidas
- Personas pagadas vs pendientes

### Lista de Compra
- Generada automáticamente según preferencias
- Personas que asisten 2 días → x2 bebidas alcohólicas y refrescos
- Bebidas principales se cuentan 1 en 1

## Estructura del Proyecto

```
Carreta/
├── carretaRomeria/          # Configuración principal
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── personas/                # App principal
│   ├── models.py           # Modelo Persona
│   ├── views.py            # Vistas y lógica
│   ├── forms.py            # Formularios
│   ├── urls.py             # URLs
│   └── templates/          # Templates HTML
├── static/                 # Archivos estáticos (CSS, JS, imágenes)
├── requirements.txt        # Dependencias Python
├── Procfile               # Configuración Render
├── manage.py              # Utilidad Django
└── db.sqlite3             # Base de datos (desarrollo)
```

## Tecnologías

- **Backend:** Django 4.2.7
- **Frontend:** Bootstrap 5.1.3, Font Awesome 6.0.0
- **Base de datos:** SQLite (dev) / PostgreSQL (prod)
- **Servidor:** Gunicorn + Render
- **Imágenes:** Pillow

## Licencia

MIT License
