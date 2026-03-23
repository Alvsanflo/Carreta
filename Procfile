release: python manage.py migrate && python create_admin.py
web: python -m gunicorn --config gunicorn_config.py carretaRomeria.wsgi:application
