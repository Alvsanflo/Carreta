from django.contrib.auth import get_user_model
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carretaRomeria.settings')
django.setup()

User = get_user_model()

# Eliminar si existe
User.objects.filter(username='admin_carreta').delete()

# Crear superusuario
user = User.objects.create_superuser(
    username='admin_carreta',
    email='admin@carretaromeria.local',
    password='Cr@rr3t@2026!Seg#7x9Kp$mN'
)

print('✅ Superusuario creado exitosamente')
print('=' * 50)
print('CREDENCIALES DE ACCESO:')
print('=' * 50)
print('Usuario: admin_carreta')
print('Contraseña: Cr@rr3t@2026!Seg#7x9Kp$mN')
print('Email: admin@carretaromeria.local')
print('=' * 50)
print('Acceso admin: http://127.0.0.1:8000/admin/')
print('=' * 50)
