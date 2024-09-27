web: gunicorn crm.wsgi --log-file - 
#or works good with external database
web: python manage.py migrate && gunicorn crm.wsgi