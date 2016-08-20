# turn off debugging in production
DEBUG = False

# settings for the production database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'django_db',
        'USER': 'djangousr',
        'PASSWORD': '<< password you set for you new database>>',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# allowed hosts for our production site
ALLOWED_HOSTS = ['<<ip address of your server>>']

STATIC_ROOT = '/opt/mec_env/static/'
MEDIA_ROOT = '/opt/mec_env/media/'
