# Django settings for running gui tests with django_ecommerce project.
from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'test_django_db',
        'USER': 'djangousr',
        'PASSWORD': 'djangousr',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

SERVER_ADDR = "127.0.0.1:9001"
