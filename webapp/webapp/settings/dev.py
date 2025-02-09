from .base import BASE_DIR

SECRET_KEY = 'django-insecure-goyh@_ibkx)#(^7#gcsu5!#d0(e-oqkhkf0whwwynq!ww2w1oj'

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
