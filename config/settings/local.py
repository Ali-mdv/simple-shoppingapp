import socket
from .base import *

DEBUG = True
ALLOWED_HOSTS = []


# APPS
# ------------------------------------------------------------------------------
THIRD_PARTY_APPS += [
    "debug_toobar"
]


# MIDDLEWARE
# ------------------------------------------------------------------------------
MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware"
]


# DATABASE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config("POSTGRES_DB"),
        'USER': config("POSTGRES_USER"),
        'HOST': 'localhost',
        'PORT': config("POSTGRES_PORT"),
        'PASSWORD': config("POSTGRES_PASSWORD")
    }
}


# djangi-debug_toolbar
# ------------------------------------------------------------------------------
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[:-1] + "1" for ip in ips]


# SSL security
# ------------------------------------------------------------------------------
SECURE_SSL_REDIRECT = config(
    'DJANGO_SECURE_SSL_REDIRECT', cast=bool, default=False)


# HSHS
# ------------------------------------------------------------------------------
SECURE_HSTS_SECONDS = config(
    "DJANGO_SECURE_HSTS_SECONDS", cast=int, default=0)
SECURE_HSTS_INCLUDE_SUBDOMAINS = config(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", cast=bool, default=False)
SECURE_HSTS_PRELOAD = config(
    "DJANGO_SECURE_HSTS_PRELOAD", cast=bool, default=False)


# secure coockies
# ------------------------------------------------------------------------------
SESSION_COOKIE_SECURE = config(
    "DJANGO_SESSION_COOCKIE_SECURE", default=False)
CSRF_COOKIE_SECURE = config("DJANGO_CSRF_COOCKIE_SECURE", default=False)


# EMAIL BACKEND
# ------------------------------------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
