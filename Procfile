release: python manage.py migrate --noinput && python create_admin.py || true
web: gunicorn --bind 0.0.0.0:$PORT --workers 4 --worker-class sync --access-logfile - --error-logfile - carretaRomeria.wsgi:application
