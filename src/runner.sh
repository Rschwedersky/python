/app/manage.py collectstatic --noinput
/app/manage.py migrate
daphne -b 0.0.0.0 -p 8000 portal.asgi:application
