#!/usr/bin/env python
"""
Script para crear automáticamente un superusuario
Se ejecuta después de las migraciones en build de Render
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carretaRomeria.settings')
django.setup()

from django.contrib.auth.models import User

try:
    # Datos del superusuario (usar variables de entorno o defaults)
    USERNAME = os.getenv('SUPERUSER_USERNAME', 'admin_carreta')
    PASSWORD = os.getenv('SUPERUSER_PASSWORD', 'Carreta2026!Seg#Admin')
    EMAIL = os.getenv('SUPERUSER_EMAIL', 'admin@carreta.local')

    # Crear superusuario si no existe
    if not User.objects.filter(username=USERNAME).exists():
        User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
        print('✓ Superusuario creado exitosamente')
        print('=' * 50)
        print('CREDENCIALES DE ACCESO:')
        print('=' * 50)
        print(f'Usuario: {USERNAME}')
        print(f'Contraseña: {PASSWORD}')
        print(f'Email: {EMAIL}')
        print('=' * 50)
    else:
        print(f'✓ Superusuario "{USERNAME}" ya existe')
except Exception as e:
    print(f'⚠️  Error al crear superusuario: {e}')
    print('Esto es normal si la BD aún no está inicializada')
    sys.exit(0)  # No fallar el deploy si hay error

