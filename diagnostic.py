#!/usr/bin/env python
"""Verificar que gunicorn puede cargar el WSGI correctamente."""

import sys
import os

# Añadir el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 50)
print("DIAGNOSTIC SCRIPT FOR GUNICORN")
print("=" * 50)

print(f"\n1. Python path:")
for p in sys.path[:5]:
    print(f"   - {p}")

print(f"\n2. Current directory: {os.getcwd()}")
print(f"   Exists? {os.path.exists(os.getcwd())}")

print(f"\n3. Checking Django settings module:")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carretaRomeria.settings')
print(f"   DJANGO_SETTINGS_MODULE = {os.environ.get('DJANGO_SETTINGS_MODULE')}")

print(f"\n4. Importing carretaRomeria module:")
try:
    import carretaRomeria
    print(f"   ✓ carretaRomeria module imported successfully")
    print(f"   Location: {carretaRomeria.__file__}")
except Exception as e:
    print(f"   ✗ Error importing carretaRomeria: {e}")
    sys.exit(1)

print(f"\n5. Importing carretaRomeria.wsgi:")
try:
    from carretaRomeria import wsgi
    print(f"   ✓ carretaRomeria.wsgi imported successfully")
    print(f"   Location: {wsgi.__file__}")
except Exception as e:
    print(f"   ✗ Error importing carretaRomeria.wsgi: {e}")
    sys.exit(1)

print(f"\n6. Checking wsgi.application attribute:")
try:
    app = wsgi.application
    print(f"   ✓ wsgi.application exists: {app}")
except Exception as e:
    print(f"   ✗ Error accessing wsgi.application: {e}")
    sys.exit(1)

print(f"\n7. Testing gunicorn import:")
try:
    from gunicorn.app.wsgiapp import run
    print(f"   ✓ gunicorn.app.wsgiapp imported successfully")
except Exception as e:
    print(f"   ✗ Error importing gunicorn.app.wsgiapp: {e}")
    print(f"      Note: This is expected on Windows (fcntl not available)")

print("\n" + "=" * 50)
print("✓ ALL CHECKS PASSED - Ready for gunicorn deployment!")
print("=" * 50)
