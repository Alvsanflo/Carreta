#!/bin/bash
# Script de inicialización para Render

echo "Ejecutando migraciones..."
python manage.py migrate

echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "✓ Inicialización completada"
