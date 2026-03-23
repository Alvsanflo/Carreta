# ⚠️ IMPORTANTE: Expiración de Base de Datos

## Estado Actual
- **Fecha de expiración:** 22 de Abril de 2026
- **Tipo:** Instancia PostgreSQL Free en Render
- **Acción requerida:** Upgrade a plan de pago O migrar datos antes de la fecha

## Opciones

### Opción 1: Upgrade a Plan de Pago (Recomendado)
1. En Render Dashboard → PostgreSQL service
2. Click **"Upgrade"**
3. Seleccionar plan pagado (desde $15/mes)

### Opción 2: Migrar a otra base de datos
Antes del 22 de Abril:
1. Hacer backup de datos
2. Configurar nueva instancia PostgreSQL
3. Restaurar datos
4. Actualizar DATABASE_URL en GitHub Secrets

### Opción 3: Migrar a SQLite (No recomendado para producción)
- Cambiar `DATABASE_URL` a SQLite
- Perderás algunos beneficios de PostgreSQL

## Próximos Pasos
- [ ] Decidir entre upgrade o migración
- [ ] Setear recordatorio para el 15 de Abril
- [ ] Hacer backup regular de datos

## Contacto
Si necesitas ayuda con la migración, contactar al soporte de Render.

---

**Última actualización:** 23 de Marzo de 2026
