# Configurar Neon PostgreSQL con GitHub Secrets

## Paso 1: Crear Base de Datos en Neon

1. Ir a [neon.tech](https://neon.tech) y registrarse (gratis)
2. Crear un nuevo proyecto
3. En el dashboard, ir a **Connection string** → **Pooler**
4. Copiar la URL (será algo como: `postgresql://usuario:password@ep-xxxxx-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require`)

## Paso 2: Agregar GitHub Secrets

En tu repositorio en GitHub:

1. Settings → Secrets and variables → Actions → New repository secret
2. Agregar estos secrets:

| Nombre | Valor | Ejemplo |
|--------|-------|---------|
| `SECRET_KEY` | Tu Django SECRET_KEY | `django-insecure-xxx...` |
| `ALLOWED_HOSTS` | Tu dominio Render | `carreta-romeria.onrender.com` |
| `DATABASE_URL` | Connection string de Neon | `postgresql://usuario:password@ep-xxxxx-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require` |
| `SUPERUSER_USERNAME` | Usuario admin | `admin_carreta` |
| `SUPERUSER_PASSWORD` | Contraseña admin | `Carreta2026!Seg#Admin` |
| `SUPERUSER_EMAIL` | Email del admin | `admin@carreta.local` |

## Paso 3: Configurar Render (Opcional Manual)

Si quieres activar deploys automáticos desde GitHub:

1. En Render.com, ir al Web Service
2. Settings → Environment variables
3. Agregar los mismos secrets manualmente (O usar el webhook de deploy)

### Opción A: GitHub Actions Webhook (Automático)

1. En Render, ir a Settings → Deploy hook
2. Copiar el webhook URL
3. En GitHub, crear un secret `RENDER_DEPLOY_HOOK_ID` con el ID
4. Ya está - cada push a `main` dispara el deploy automático

### Opción B: Variables en Render (Manual)

1. En Render → Environment, agregar manualmente:
   - `SECRET_KEY`
   - `ALLOWED_HOSTS`
   - `DATABASE_URL`
   - `SUPERUSER_USERNAME`
   - `SUPERUSER_PASSWORD`
   - `SUPERUSER_EMAIL`

## Paso 4: Hacer Push y Deploy

```bash
git add .github/workflows/deploy.yml
git commit -m "Update GitHub Actions workflow to use Neon DATABASE_URL"
git push origin main
```

El workflow ejecutará:
1. Crea `.env` con secrets desde GitHub
2. Render detecta el cambio en `main`
3. Ejecuta migrations con la BD de Neon
4. Crea/actualiza usuario admin

## Verificación

1. En Render, ver logs de deploy
2. Debería ejecutar: `python manage.py migrate --noinput`
3. Luego: `python create_admin.py`

## Si hay errores

### Error: "ProgrammingError: database ... does not exist"
- La BD en Neon no se creó automáticamente
- Solución: Ir a Neon dashboard y crear manualmente la BD `neondb` (o el nombre que uses)

### Error: "psycopg2.OperationalError: connection failed"
- DATABASE_URL inválida o conexión rechazada
- Verificar que el string es exacto de Neon
- Usar **Pooler** (recomendado) no **Direct**

### Error: "FATAL: remaining connection slots reserved"
- Demasiadas conexiones abiertas
- Usar **Connection Pooler** en Neon

## Notas de Seguridad

- ✅ Nunca commitear `.env` (está en `.gitignore`)
- ✅ Los secrets en GitHub están encriptados
- ✅ Solo exponemos `DATABASE_URL` al servidor de Render en deploy time
- ✅ Usar **Pooler mode** en Neon para mejor rendimiento

## Documentación Útil

- [Neon Docs](https://neon.tech/docs/introduction)
- [Render Environment Variables](https://render.com/docs/environment-variables)
- [Django dj-database-url](https://github.com/jazzband/dj-database-url)
