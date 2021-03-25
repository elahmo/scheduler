release: python manage.py migrate

web: gunicorn config.wsgi:application
tasks: python manage.py run_scheduler