# 📋 INSTRUCCIONES PARA DESPLIEGUE EN RENDER

## PASO 1: Preparar GitHub

```bash
# En la raíz del proyecto
git init
git add .
git commit -m "Initial commit: Carreta Romería app"
git branch -M main
git remote add origin https://github.com/tu-usuario/carreta.git
git push -u origin main
```

## PASO 2: Crear Proyecto en Render.com

1. Ir a https://render.com
2. Click en "New +" → "Web Service"
3. Conectar GitHub (autorizar si es necesario)
4. Seleccionar el repositorio "carreta"
5. Configurar:
   - **Name:** carreta-romeria
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn carretaRomeria.wsgi --log-file -`

## PASO 3: Crear Base de Datos PostgreSQL

1. En Render, click "New +" → "PostgreSQL"
2. Configurar:
   - **Name:** carreta-db
   - **Database:** carreta
   - **User:** carreta_user
3. Copiar la **Internal Database URL**

## PASO 4: Variables de Entorno en Render

En el Web Service, ir a "Environment":

```
DEBUG=False
SECRET_KEY=genera-uno-con: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
ALLOWED_HOSTS=carreta-romeria.onrender.com
DATABASE_URL=postgresql://carreta_user:PASSWORD@carreta-db:5432/carreta
```

## PASO 5: Conectar BD al Servicio Web

En el Web Service:
- Ir a "Dependencies"
- Buscar el PostgreSQL service "carreta-db"
- Hacer clic para conectar
- Esto automáticamente seteará DATABASE_URL

## PASO 6: Desplegar

1. Click "Deploy" en Render
2. Esperar a que compile e instale (2-3 minutos)
3. Ver logs en tiempo real

## PASO 7: Crear Superusuario en Producción

```bash
# Una vez deployado, en tu terminal local:
# O acceder a Render Shell en el dashboard
python manage.py createsuperuser
```

O desde el Render Shell:
1. En el dashboard del Web Service
2. "Shell" (arriba a la derecha)
3. Ejecutar: `python manage.py createsuperuser`

## Verificación

✅ Sitio accesible en: https://carreta-romeria.onrender.com
✅ Login en: https://carreta-romeria.onrender.com/login
✅ Admin en: https://carreta-romeria.onrender.com/admin

## Solución de problemas

**Error: "DisallowedHost"**
- Verificar ALLOWED_HOSTS en variables de entorno

**Error: "Connection refused"**
- Verificar que el PostgreSQL está conectado
- Revisar DATABASE_URL en variables

**Error de Static Files**
- Ejecutar: `python manage.py collectstatic`
- Ya está configurado en settings.py

**Ver Logs:**
- En Render dashboard → "Logs"
- O comando: `render logs -n 100`

## Comandos Útiles

Ejecutar migraciones en producción:
```bash
render run python manage.py migrate
```

Crear superusuario:
```bash
render run python manage.py createsuperuser
```

Redeployar:
```
git push origin main
# Render redeploya automáticamente
```

---

¡Listo! Tu aplicación Carreta Romería estará en vivo en Render 🎉
