# Solución de problemas: Migraciones de Neon

## Síntoma
La BD de Neon está vacía después del deploy, sin tablas.

## Causa probable
El comando `python manage.py migrate` en el Procfile falla silenciosamente o `DATABASE_URL` no se está usando.

## Diagnóstico

### 1. Verificar logs de Render
En Render dashboard:
- Go to Web Service → Logs
- Busca líneas con `migrate` o `ERROR`
- Si ves `ERROR`, ese es el problema

### 2. Prueba local con DATABASE_URL

Crea un archivo `.env.local` con:
```
DATABASE_URL=postgresql://neondb_owner:npg_SNhupkLQ58sa@ep-divine-leaf-abfywul9-pooler.eu-west-2.aws.neon.tech/carreta?sslmode=require&channel_binding=require
DEBUG=False
ALLOWED_HOSTS=localhost
SECRET_KEY=test-key-123
```

Luego ejecuta:
```bash
# Cargar variables
export $(cat .env.local | xargs)

# Probar conexión
python test_neon_connection.py

# Si funciona, ejecutar migraciones
python manage.py migrate --noinput --verbosity 2

# Crear admin
python create_admin.py
```

### 3. Verificar DATABASE_URL en Render

En Render Settings → Environment variables:
- Verifica que `DATABASE_URL` existe
- Verifica que no hay espacios extra al principio/final
- Copia desde Neon nuevamente si es necesario

### 4. Verificar en Neon

En Neon console:
- Ve a SQL editor
- Ejecuta:
```sql
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public';
```
- Si está vacío, las migraciones no se ejecutaron

## Soluciones

### A. Forzar migrate manualmente en Render

1. En Render, ve a **Deployments**
2. Haz clic en el último deploy
3. En **Deploy Log**, busca errores
4. Si necesitas reintentar:
   - Ve a **Settings** → **Build & Deploy**
   - Haz clic en **Clear build cache**
   - Haz clic en **Deploy**

### B. Ejecutar desde terminal SSH en Render (plan pagado)

Si tienes plan Pro:
```bash
# Entrar en shell
render shell

# Ejecutar migraciones
python manage.py migrate --noinput --verbosity 2

# Crear admin
python create_admin.py
```

### C. Crear migraciones frescas

Si aún hay problemas, puede ser un issue con las migraciones antiguas:

```bash
# Localmente, crear nueva migración
python manage.py makemigrations --empty personas --name reset_database

# Abre el archivo y reemplaza con:
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('personas', '0003_alter_persona_alcohol_alter_persona_bebida_principal_and_more'),
    ]

    operations = []  # Sin operaciones, solo depender de la anterior
```

## Verificación final

Una vez resuelto, verifica:

1. **En Neon SQL editor:**
```sql
SELECT COUNT(*) FROM auth_user;
SELECT COUNT(*) FROM personas_persona;
```
Deberías ver al menos 1 user (el admin) y potencialmente personas.

2. **Acceder a la app:**
   - Ve a https://carreta-romeria.onrender.com
   - Intenta login con `admin_carreta` / `Carreta2026!Seg#Admin`
   - Si ves la app, ¡todo funciona!

## Contacto

Si persisten los problemas:
1. Copia el error exacto de los logs
2. Verifica que psycopg[binary] versión 3.2.13+ está en requirements.txt
3. Verifica que dj-database-url==2.2.0 está en requirements.txt
