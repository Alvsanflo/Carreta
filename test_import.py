#!/usr/bin/env python
"""
Script de prueba para verificar que los módulos se pueden importar correctamente
"""
import os
import sys
import django

# Verificar que los paths están correctos
print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print(f"sys.path: {sys.path}")

# Intentar importar Django
try:
    import django
    print(f"✓ Django {django.get_version()} importado correctamente")
except ImportError as e:
    print(f"✗ Error importando Django: {e}")
    sys.exit(1)

# Intentar cargar settings
try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carretaRomeria.settings')
    django.setup()
    print(f"✓ Django settings configurados correctamente")
except Exception as e:
    print(f"✗ Error configurando Django: {e}")
    sys.exit(1)

# Intentar importar wsgi
try:
    from carretaRomeria import wsgi
    print(f"✓ WSGI module importado correctamente")
    print(f"✓ application: {wsgi.application}")
except Exception as e:
    print(f"✗ Error importando WSGI: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✓ Todos los módulos se importaron correctamente!")
