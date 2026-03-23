release: python manage.py migrate && python create_admin.py
web: gunicorn --bind 0.0.0.0:$PORT --workers 2 carretaRomeria.wsgi
