#!/usr/bin/env python3
"""
Script para generar y mostrar instrucciones de GitHub Secrets
Uso: python setup_github_secrets.py
"""

import os
import json

# Connection string de Neon
DATABASE_URL = "postgresql://neondb_owner:npg_SNhupkLQ58sa@ep-divine-leaf-abfywul9-pooler.eu-west-2.aws.neon.tech/carreta?sslmode=require&channel_binding=require"

# Otros secrets (actualizar según necesites)
SECRETS = {
    "DATABASE_URL": DATABASE_URL,
    "SECRET_KEY": "django-insecure-617+j#278c9celk-nzx-)7_wyh&r!8!6&7wwbkp6g-_wpxhzyl",  # CAMBIAR EN PRODUCCIÓN
    "ALLOWED_HOSTS": "carreta-romeria.onrender.com",
    "SUPERUSER_USERNAME": "admin_carreta",
    "SUPERUSER_PASSWORD": "Carreta2026!Seg#Admin",
    "SUPERUSER_EMAIL": "admin@carreta.local",
}

def print_secrets():
    """Imprime los secrets en formato legible"""
    print("\n" + "="*70)
    print("GITHUB SECRETS A CONFIGURAR")
    print("="*70)
    print("\n📍 Ir a: https://github.com/Alvsanflo/Carreta/settings/secrets/actions")
    print("\n📋 Crear los siguientes secrets:\n")
    
    for i, (key, value) in enumerate(SECRETS.items(), 1):
        # Ocultar valores sensibles en la salida
        display_value = value if len(value) < 50 else value[:40] + "..."
        
        print(f"{i}. Nombre: {key}")
        print(f"   Valor: {display_value}")
        
        # Para SECRET_KEY, advertencia
        if key == "SECRET_KEY" and "insecure" in value:
            print("   ⚠️  CAMBIAR ESTO EN PRODUCCIÓN!")
        print()

def print_github_ui_steps():
    """Imprime los pasos para agregar secrets en GitHub UI"""
    print("\n" + "="*70)
    print("PASOS EN GITHUB (UI MANUAL)")
    print("="*70)
    print("""
1. Ve a: https://github.com/Alvsanflo/Carreta/settings/secrets/actions

2. Haz clic en "New repository secret"

3. Para CADA secret:
   - Nombre: (copiar exactamente, ej: DATABASE_URL)
   - Valor: (copiar el valor)
   - Haz clic en "Add secret"

4. Listo. El workflow tomará estos valores automáticamente.
""")

def print_cli_instructions():
    """Imprime instrucciones para usar GitHub CLI"""
    print("\n" + "="*70)
    print("OPCIÓN: USAR GITHUB CLI (MÁS RÁPIDO)")
    print("="*70)
    print("""
Si tienes GitHub CLI instalado (gh):

1. Primero login: gh auth login

2. Copia-pega estos comandos:
""")
    
    for key, value in SECRETS.items():
        # Escapar caracteres especiales para shell
        safe_value = value.replace("'", "'\\''")
        print(f'gh secret set {key} -b "{safe_value}"')
    
    print("""
O todo junto:
gh secret set DATABASE_URL -b "postgresql://..."
gh secret set SECRET_KEY -b "..."
# ... etc
""")

def print_env_file():
    """Imprime contenido para .env local"""
    print("\n" + "="*70)
    print("CONTENIDO PARA .env LOCAL (OPCIONAL)")
    print("="*70)
    print("\n# Archivo .env para desarrollo local\n")
    
    for key, value in SECRETS.items():
        if key != "SUPERUSER_PASSWORD":  # No mostrar contraseña
            print(f"{key}={value}")
        else:
            print(f"{key}=***cambiar_por_seguridad***")

if __name__ == "__main__":
    print_secrets()
    print_github_ui_steps()
    print_cli_instructions()
    print_env_file()
    
    print("\n" + "="*70)
    print("✅ Una vez agregues los secrets, el próximo push a 'main' disparará:")
    print("   1. GitHub Actions: genera .env con los secrets")
    print("   2. Render: detecta cambios y redeploya")
    print("   3. Migrations: se ejecutan contra Neon PostgreSQL")
    print("   4. Admin: se crea/actualiza automáticamente")
    print("="*70 + "\n")
