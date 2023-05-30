FROM python:alpine

RUN mkdir /app
WORKDIR /app
RUN mkdir /requirement
COPY requirement/* requirement/

RUN pip install --upgrade pip
RUN pip install -r requirement/local.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  
ENV DJANGO_SUPERUSER_PASSWORD admin
ENV PYTHONPATH shopping_app
ENV DJANGO_SETTINGS_MODULE config.settings.local

ENV SECRET_KEY YOUR_SECRET_KEY

# for google smtp
ENV EMAIL_HOST smtp.gmail.com
ENV EMAIL_USE_SSL True
ENV EMAIL_HOST_USER your_gmail@gmail.com
ENV EMAIL_HOST_PASSWORD your_gmail_pass
ENV EMAIL_PORT 465

# merchant_id for zarinpal payment gateway
ENV MERCHANT_ID your_merchant_id

# for database
ENV POSTGRES_USER admin
ENV POSTGRES_PASSWORD 123
ENV POSTGRES_DB shop
ENV POSTGRES_PORT 5432


COPY . .

CMD python3 manage.py makemigrations --no-input && \
	python3 manage.py migrate --no-input && \
	python3 manage.py collectstatic --no-input && \
	python3 manage.py createsuperuser --user admin --email admin@dev.com --no-input ; \
	gunicorn -b 0.0.0.0:8000 config.wsgi
