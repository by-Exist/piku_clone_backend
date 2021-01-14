from .common import *
import environ

DEBUG = False

# https://pypi.org/project/django-environ-docker/
env = environ.Env()
env.read_docker_secrets()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = []  # FIXME: Set ALLOWED_HOSTS, ex) env.list("ALLOWED_HOSTS")

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {}  # FIXME: Set DATABASES

# Logging
# https://docs.djangoproject.com/en/3.1/topics/logging/
LOGGING = {}  # FIXME: Set LOGGING

# DJANGO REST FRAMEWORK JWT
# https://jpadilla.github.io/django-rest-framework-jwt/
JWT_AUTH = {
    "JWT_SECRET_KEY": env("DJANGO_JWT_SECRET_KEY"),
    "JWT_ALLOW_REFRESH": True,
}