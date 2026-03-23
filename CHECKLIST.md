# 🚀 CHECKLIST PARA SUBIR A GITHUB Y RENDER

## ✅ CAMBIOS REALIZADOS PARA RESPONSIVIDAD Y PRODUCCIÓN

### Responsividad Mobile
- ✅ Tabla de personas optimizada para móvil con columnas ocultas en pantallas pequeñas
- ✅ Bootstrap 5 (mobile-first) ya integrado
- ✅ Viewport meta tag configurado
- ✅ Formularios y filtros responsive
- ✅ Botones agrupados en mobile

### Archivos de Configuración
- ✅ `requirements.txt` - Todas las dependencias
- ✅ `Procfile` - Comandos para Render
- ✅ `.gitignore` - Archivos a ignorar
- ✅ `.env.example` - Variables de entorno
- ✅ `settings.py` - Actualizado para producción
- ✅ `README.md` - Documentación completa
- ✅ `DEPLOYMENT.md` - Instrucciones paso a paso

## 📝 PRÓXIMOS PASOS

### 1. INICIALIZAR GIT Y HACER PUSH

```bash
cd "c:\Users\gerne\OneDrive\Escritorio\Carreta"

# Inicializar git (si no está)
git init

# Configurar usuario (si no está configurado)
git config user.email "tu-email@example.com"
git config user.name "Tu Nombre"

# Agregar todos los archivos
git add .

# Hacer commit
git commit -m "Carreta Romería: App Django con responsividad y filtros"

# Renombrar rama a main
git branch -M main

# Agregar remote (reemplaza URL)
git remote add origin https://github.com/tu-usuario/carreta.git

# Hacer push
git push -u origin main
```

### 2. VERIFICAR ANTES DE SUBIR

- [ ] ¿Existe cuenta en render.com?
- [ ] ¿GitHub conectado a Render?
- [ ] ¿Archivo `.env.example` en la raíz?
- [ ] ¿`requirements.txt` con todas las dependencias?
- [ ] ¿`Procfile` con comandos correctos?

### 3. CREAR PROYECTO EN RENDER

Seguir el archivo `DEPLOYMENT.md` paso a paso.

## 📦 ARCHIVOS CLAVE LISTOS

```
✅ requirements.txt - Dependencias instaladas
✅ Procfile - Configuración de Render
✅ .gitignore - Excluye archivos innecesarios
✅ .env.example - Plantilla de variables
✅ settings.py - Configurado para producción
✅ README.md - Documentación
✅ DEPLOYMENT.md - Guía completa de despliegue
```

## 🔒 SEGURIDAD

En Render, SIEMPRE configurar:
```
DEBUG=False
SECRET_KEY=<generar uno nuevo>
ALLOWED_HOSTS=tu-dominio.onrender.com
DATABASE_URL=postgresql://...
```

NO usar los valores de desarrollo.

## 🎯 COMANDOS RÁPIDOS

```bash
# Ver estado de git
git status

# Ver commits
git log --oneline

# Cambios pendientes
git diff

# Hacer push después de cambios
git add .
git commit -m "descripción"
git push origin main
```

---

¿Listo para hacer push a GitHub? 🚀
