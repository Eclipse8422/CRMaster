web: sh -c "python manage.py collectstatic --no-input && python manage.py migrate && gunicorn --worker-tmp-dir /dev/shm/ crm.wsgi"
