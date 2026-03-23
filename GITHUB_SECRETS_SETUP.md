# 🔐 CONFIGURACIÓN CON GITHUB SECRETS Y RENDER

## PASO 1: Crear GitHub Secrets

En tu repositorio GitHub (https://github.com/Alvsanflo/Carreta):

1. **Settings** → **Secrets and variables** → **Actions**
2. Click en **"New repository secret"**

Añade estos 4 secrets:

### `SECRET_KEY`
Genera uno ejecutando:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
Copia el resultado (debe empezar con `django-insecure-` o similar)

**Ejemplo:**
```
django-insecure-g8@2_*q7p&8q^k9$5^j#@3_8&7^l$k9@2^q*8&7j#k9@2^q*8&7j#k9@
```

### `ALLOWED_HOSTS`
```
carreta-romeria.onrender.com
```

### `DATABASE_URL`
Lo obtendrás de Render después de crear PostgreSQL:
```
postgresql://carreta_user:PASSWORD@dpg-xxxxx.onrender.com:5432/carreta
```

### `RENDER_DEPLOY_HOOK_ID` (Opcional, para auto-deploy)
Lo obtendrás después de crear el Web Service en Render

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

5. **NO agregues variables de entorno aquí**, déjalas vacías

6. Click **"Create Web Service"**

---

## PASO 3: Crear PostgreSQL en Render

1. Click **"New +"** → **"PostgreSQL"**
2. Configura:
   - **Name:** `carreta-db`
   - **Database:** `carreta`
   - **User:** `carreta_user`

3. Copia la **Internal Database URL** que aparece
4. Pégala en GitHub Secret `DATABASE_URL`

---

## PASO 4: Obtener Deploy Hook (Para Auto-Deploy)

En tu **Web Service** (carreta-romeria):

1. **Settings** → **Deploy Hook**
2. Click **"Create Deploy Hook"**
3. **URL:** Cópiala
4. Ve a GitHub → **Settings** → **Secrets** → Nuevo secret:
   - **Name:** `RENDER_DEPLOY_HOOK_ID`
   - **Value:** Pega la URL

---

## PASO 5: Conectar Base de Datos

En **Carreta Web Service** en Render:

1. **Environment** → **Add Variable**
   - Espera, no hagas esto todavía
2. Ve a tu PostgreSQL service
3. Copia el **Internal Database URL**
4. Vuelve al Web Service
5. **Connect** → Selecciona `carreta-db`

Render automáticamente agregará `DATABASE_URL`

---

## PASO 6: Test de Despliegue

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

## PASO 7: Crear Superusuario en Render

En el **Web Service**:
1. **Shell** (arriba a la derecha)
2. Ejecuta:
   ```bash
   python manage.py createsuperuser
   ```

3. Llena los datos

---

## 🔑 Resumen de Secrets Necesarios

```
SECRET_KEY = tu-secret-key-generado
ALLOWED_HOSTS = carreta-romeria.onrender.com
DATABASE_URL = postgresql://carreta_user:PASS@dpg-xxxxx.onrender.com:5432/carreta
RENDER_DEPLOY_HOOK_ID = https://api.render.com/deploy/xxxxx (opcional)
```

---

## ✅ Checklist

- [ ] 4 GitHub Secrets creados
- [ ] Web Service creado en Render
- [ ] PostgreSQL creado en Render
- [ ] DATABASE_URL en GitHub Secret
- [ ] PostgreSQL conectado a Web Service
- [ ] Deploy Hook configurado (opcional)
- [ ] Test de push a main
- [ ] Superusuario creado en Render

---

## URLs Finales

- **App:** https://carreta-romeria.onrender.com
- **Login:** https://carreta-romeria.onrender.com/login
- **Admin:** https://carreta-romeria.onrender.com/admin

¡Listo! 🎉
