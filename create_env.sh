#!/bin/bash
# Script para generar .env en tiempo de build desde variables de entorno

cat > .env << EOF
DEBUG=${DEBUG:-False}
SECRET_KEY=${SECRET_KEY:-django-insecure-development-key}
ALLOWED_HOSTS=${ALLOWED_HOSTS:-localhost,127.0.0.1}
DATABASE_URL=${DATABASE_URL:-sqlite:///db.sqlite3}
EOF

echo ".env creado correctamente"
cat .env
