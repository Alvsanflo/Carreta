release: python manage.py migrate && python create_admin.py
web: gunicorn --bind 0.0.0.0:$PORT --workers 4 --worker-class sync --access-logfile - --error-logfile - carretaRomeria.wsgi:application
