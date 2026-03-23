# 🔐 CONFIGURACIÓN CON GITHUB SECRETS Y RENDER (SQLite)

## PASO 1: Crear GitHub Secrets

En tu repositorio GitHub (https://github.com/Alvsanflo/Carreta):

1. **Settings** → **Secrets and variables** → **Actions**
2. Click en **"New repository secret"**

Añade estos 2 secrets (simplificado):

### `SECRET_KEY`
Genera uno ejecutando:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Ejemplo:**
```
django-insecure-m$cjpv^p0@%wfq1p8)!-1xo+v)$n5ygudlm#f*c_$e69o*a)@n
```

### `ALLOWED_HOSTS`
```
carreta-romeria.onrender.com
```

---

## PASO 2: Crear Web Service en Render

1. Ve a https://render.com/dashboard
2. Click **"New +"** → **"Web Service"**
3. Selecciona el repositorio **"Carreta"**
4. Configura:
   - **Name:** `carreta-romeria`
   - **Environment:** Python 3
   - **Build Command:**
     ```
     pip install -r requirements.txt
     ```
   - **Start Command:**
     ```
     gunicorn carretaRomeria.wsgi
     ```

5. Click **"Create Web Service"**

---

## PASO 3: Test de Despliegue

1. Haz un cambio en GitHub:
   ```bash
   git add .
   git commit -m "test deploy"
   git push origin main
   ```

2. GitHub Actions se ejecutará automáticamente
3. Render redeploya automáticamente

Ver logs:
- **GitHub:** Actions tab
- **Render:** Web Service → Logs

---

## PASO 4: Crear Superusuario en Render

En el **Web Service**:
1. **Shell** (arriba a la derecha)
2. Ejecuta:
   ```bash
   python manage.py createsuperuser
   ```

3. Llena los datos

---

## ✅ Checklist

- [ ] 2 GitHub Secrets creados (SECRET_KEY, ALLOWED_HOSTS)
- [ ] Web Service creado en Render
- [ ] Test de push a main
- [ ] Superusuario creado en Render

---

## URLs Finales

- **App:** https://carreta-romeria.onrender.com
- **Login:** https://carreta-romeria.onrender.com/login
- **Admin:** https://carreta-romeria.onrender.com/admin

¡Listo! 🎉 SQLite es mucho más simple y completamente gratuito.

