from .base import *


DEBUG = config('DEBUG', cast=bool, default=False)

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]


# MIDDLEWARE
# ------------------------------------------------------------------------------
MIDDLEWARE += [
    "django.middleware.cache.FetchFromCacheMiddleware",
]


# Cache Config
# ------------------------------------------------------------------------------
CACHE_MIDDLEWARE_ALIAS = "default"
CACHE_MIDDLEWARE_SECONDS = 604800
CACHE_MIDDLEWARE_KEY_PREFIX = ""


# SSL security
# ------------------------------------------------------------------------------
SECURE_SSL_REDIRECT = config(
    'DJANGO_SECURE_SSL_REDIRECT', cast=bool, default=True)


# HSHS
# ------------------------------------------------------------------------------
SECURE_HSTS_SECONDS = config(
    "DJANGO_SECURE_HSTS_SECONDS", cast=int, default=2592000)
SECURE_HSTS_INCLUDE_SUBDOMAINS = config(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", cast=bool, default=True)
SECURE_HSTS_PRELOAD = config(
    "DJANGO_SECURE_HSTS_PRELOAD", cast=bool, default=True)

# secure coockies
# ------------------------------------------------------------------------------
SESSION_COOKIE_SECURE = config(
    "DJANGO_SESSION_COOCKIE_SECURE", default=True)
CSRF_COOKIE_SECURE = config("DJANGO_CSRF_COOCKIE_SECURE", default=True)


# EMAIL BACKEND
# ------------------------------------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
