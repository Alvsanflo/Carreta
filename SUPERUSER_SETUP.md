# 🔑 Creación Automática de Superusuario en Render

## ¿Cómo funciona?

El script `create_admin.py` se ejecuta **automáticamente** después de las migraciones en Render (sin necesidad de shell de pago).

## Superusuario por Defecto

Después del primer deploy, accede con:

```
Usuario: admin_carreta
Contraseña: Carreta2026!Seg#Admin
Email: admin@carreta.local
```

Acceso: https://carreta-romeria.onrender.com/admin/

## Personalizar Credenciales

Si quieres cambiar las credenciales, en **Render Dashboard**:

1. Ve a tu **Web Service**
2. **Environment** → **Add Variable**

Añade estas variables:

```
SUPERUSER_USERNAME=tu_usuario
SUPERUSER_PASSWORD=tu_contraseña
SUPERUSER_EMAIL=tu_email@example.com
```

3. Redeploy → El nuevo superusuario se creará automáticamente

## ¿Qué sucede en cada deploy?

✓ Se ejecutan las migraciones  
✓ Se crea el superusuario si **NO existe**  
✓ Si ya existe, no hace nada (evita sobrescribir)

## Seguridad

⚠️ **IMPORTANTE:** 
- Las credenciales por defecto son públicas en el código
- **Cámbia la contraseña en producción** después del primer login
- O configura variables de entorno personalizadas antes del primer deploy

## Workflow Recomendado

1. **Primer Deploy:**
   - Render crea el superusuario automáticamente
   - Accede con credenciales por defecto

2. **Cambio de Contraseña:**
   - Login en /admin/
   - Change Password
   - ¡Listo!

3. **Para Futuros Usuarios:**
   - Crea usuarios adicionales desde /admin/

---

**¡Sin shell de pago necesaria!** 🎉
