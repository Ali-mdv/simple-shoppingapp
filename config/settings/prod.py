from .base import *


DEBUG = config('DEBUG', cast=bool, default=False)

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]


# MIDDLEWARE
# ------------------------------------------------------------------------------
MIDDLEWARE += [
    "django.middleware.cache.FetchFromCacheMiddleware",
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


# Static files (CSS, JavaScript, Images)
# ------------------------------------------------------------------------------
STATICFILES_DIRS = [
    APP_DIR / "staticfiles",
]


# EMAIL BACKEND
# ------------------------------------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
