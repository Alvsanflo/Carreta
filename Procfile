release: sh -c 'echo "Starting migrations..." && python manage.py migrate --noinput --verbosity 2 && echo "Migrations completed." && python create_admin.py'
web: gunicorn --bind 0.0.0.0:$PORT --workers 4 --worker-class sync --access-logfile - --error-logfile - carretaRomeria.wsgi:application
