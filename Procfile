release: python manage.py migrate && python create_admin.py
web: gunicorn --bind 0.0.0.0:$PORT --workers 4 carretaRomeria.wsgi:application
