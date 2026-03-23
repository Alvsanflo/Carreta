release: python manage.py migrate && python create_admin.py
web: gunicorn carretaRomeria.wsgi --log-file -
