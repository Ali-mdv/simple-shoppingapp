# simple-ShoppingApp

### this is a simple shopping web-application with django, docker, postgres and nginx

install **[docker](https://docs.docker.com/engine/install/)** and **[docker compose](https://docs.docker.com/compose/install/linux/)** before running

  > set your own environment variables in Dockerfile 

**Commands:**
>```bash
>docker compose up --build
>```
#
if you want run Just run django
>1. set database from postgres to sqlite
>2. set this environment varilabes
>```bash
>export PYTHONPATH=shopping_app
>export DJANGO_SETTINGS_MODULE=config.settings.local # for porduction use prod
>```
>3. create .env file like below
>```python
>SECRET_KEY = 'YOUR_SECRET_KEY
>DEBUG = False
>
>#email config
>EMAIL_USE_TLS = True
>EMAIL_HOST_USER = your_email@gmail.com
>EMAIL_HOST_PASSWORD = your_password
>EMAIL_PORT = 587
>
># payment gateway config
>MERCHANT_ID = "YOUR_MERCHANT_ID"
>
>#if you want use sqlite database ignore it
>POSTGRES_USER = 'YOUR_POSTGRES_USER'
>POSTGRES_PASSWORD = "YOUR_POSTGRES_PASSWORD"
>POSTGRES_DB = "YOUR_POSTGRES_DB"
>POSTGRES_PORT = 5432
>```