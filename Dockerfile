FROM python:3.8.5
WORKDIR /code
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
RUN python manage.py migrate --noinput
RUN python manage.py collectstatic --no-input
RUN DJANGO_SUPERUSER_PASSWORD=Tr0ub4dor@3 python manage.py createsuperuser --noinput administator
CMD gunicorn Support_test_project.wsgi:application --bind 0.0.0.0:8000
