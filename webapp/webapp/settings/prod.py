from os import getenv

SECRET_KEY = getenv('DJANGO_SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': getenv('DB_NAME'),
        'USER': getenv('DB_USER_NM'),
        'PASSWORD': getenv('DB_USER_PW'),
        'HOST': getenv('DB_HOST', 'db'),
        'PORT': getenv('DB_PORT', '5432'),
    }
}
