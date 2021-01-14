from .common import *
import environ

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

DEBUG = True

# https://pypi.org/project/django-environ-docker/
env = environ.Env()
env.read_env()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY")

INSTALLED_APPS = [
    *INSTALLED_APPS,
    "debug_toolbar",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    *MIDDLEWARE,
]

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# MEDIA_ROOT
# https://docs.djangoproject.com/en/3.1/ref/settings/#std:setting-MEDIA_ROOT
MEDIA_ROOT = BASE_DIR / "backend" / "media"  # use dev upload file path

INTERNAL_IPS = [
    "127.0.0.1",
]

# DJANGO REST FRAMEWORK JWT
# https://jpadilla.github.io/django-rest-framework-jwt/
JWT_AUTH = {
    "JWT_SECRET_KEY": env("DJANGO_JWT_SECRET_KEY"),
    "JWT_ALLOW_REFRESH": True,
}