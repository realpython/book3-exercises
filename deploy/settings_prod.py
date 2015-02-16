#turn of debugging were in production
DEBUG=False

#settings for the production database
DATABASES = {
        'default': {
                    'ENGINE': 'django.db.backends.postgresql_psycopg2',
                    'NAME': 'django_db',
                    'USER': 'djangousr',
                    'PASSWORD': 'djangousr',
                    'HOST' : 'localhost',
                    'PORT' : '5432',
                }
} 

#allowed hosts for our production site
ALLOWED_HOSTS = ['128.199.202.178']

STATIC_ROOT = '/opt/mec_env/static/'
MEDIA_ROOT = '/opt/mec_env/media/'

