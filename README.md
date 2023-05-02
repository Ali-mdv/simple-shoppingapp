# simple-ShoppingApp

### this is a simple shopping web-application django-provided

**Set these 2 environmental variables before starting**

```bash
export DJANGO_SETTINGS_MODULE=config.settings.local
export PYTHONPATH=shopping_app
```

**Also create dotenv file and set this variables**

```python
SECRET_KEY = 'YOUR_SECRET_KEY'
DEBUG = False

#email config
EMAIL_USE_TLS = True
EMAIL_HOST_USER = your_email@gmail.com
EMAIL_HOST_PASSWORD = your_password
EMAIL_PORT = 587
MERCHANT_ID = "YOUR_MERCHANT_ID"

#database config
POSTGRES_USER = 'YOUR_POSTGRES_USER'
POSTGRES_PASSWORD = "YOUR_POSTGRES_PASSWORD"
POSTGRES_DB = "YOUR_POSTGRES_DB"
POSTGRES_PORT = 5432
```
