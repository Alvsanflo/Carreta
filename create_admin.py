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

    # Crear o actualizar superusuario (idempotente)
    user, created = User.objects.get_or_create(
        username=USERNAME,
        defaults={
            'email': EMAIL,
            'is_staff': True,
            'is_superuser': True,
            'is_active': True,
        }
    )

    # Forzar credenciales esperadas en cada deploy
    user.email = EMAIL
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.set_password(PASSWORD)
    user.save()

    if created:
        print('✓ Superusuario creado exitosamente')
    else:
        print(f'✓ Superusuario "{USERNAME}" actualizado correctamente')

    print('=' * 50)
    print('CREDENCIALES DE ACCESO:')
    print('=' * 50)
    print(f'Usuario: {USERNAME}')
    print(f'Contraseña: {PASSWORD}')
    print(f'Email: {EMAIL}')
    print('=' * 50)
except Exception as e:
    print(f'⚠️  Error al crear superusuario: {e}')
    print('Esto es normal si la BD aún no está inicializada')
    sys.exit(0)  # No fallar el deploy si hay error

