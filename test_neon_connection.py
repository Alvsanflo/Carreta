#!/usr/bin/env python
"""
Script para probar la conexión a Neon y ejecutar migraciones localmente
"""

import os
import sys
import django

print("="*70)
print("TEST DE CONEXIÓN A NEON Y MIGRACIONES")
print("="*70)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carretaRomeria.settings')

print("\n1. Importando Django...")
try:
    import django
    print(f"   ✓ Django {django.VERSION} importado correctamente")
except ImportError as e:
    print(f"   ✗ Error: {e}")
    sys.exit(1)

print("\n2. Leyendo variables de entorno...")
database_url = os.getenv('DATABASE_URL')
if database_url:
    print(f"   ✓ DATABASE_URL detectada")
    # Ocultar credenciales
    masked = database_url[:30] + "..." + database_url[-10:]
    print(f"     {masked}")
else:
    print(f"   ⚠️  DATABASE_URL no configurada - usando SQLite")

print("\n3. Configurando Django...")
try:
    django.setup()
    print("   ✓ Django configurado correctamente")
except Exception as e:
    print(f"   ✗ Error: {e}")
    sys.exit(1)

print("\n4. Probando conexión a la BD...")
try:
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"   ✓ Conexión exitosa")
        print(f"     {version[0][:50]}...")
except Exception as e:
    print(f"   ✗ Error de conexión: {e}")
    sys.exit(1)

print("\n5. Mostrando migraciones pendientes...")
try:
    from django.core.management import call_command
    from io import StringIO
    
    out = StringIO()
    call_command('showmigrations', stdout=out, no_color=True)
    output = out.getvalue()
    
    # Mostrar solo primeras líneas
    lines = output.split('\n')[:15]
    for line in lines:
        print(f"     {line}")
    
    if "[ ]" in output:
        print(f"\n   ⚠️  Hay migraciones pendientes (sin aplicar)")
    else:
        print(f"\n   ✓ Todas las migraciones aplicadas")
        
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "="*70)
print("Para ejecutar migraciones:")
print("  python manage.py migrate --noinput")
print("\nPara crear usuario admin:")
print("  python create_admin.py")
print("="*70 + "\n")
