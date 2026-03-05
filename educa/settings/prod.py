from decouple import config
from .base import *

DEBUG = False

ADMINS = [
    ('Sachin Barali', 'baralisachin472@gmail.com')
]

# Allow localhost for Docker testing; in production, only allow your domain
ALLOWED_HOSTS = [
    'educaproject.com',
    'www.educaproject.com',
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
    '*'  # Allow all hosts for Docker development
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DB'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': 5432
    }
}

REDIS_URL = 'redis://cache:6379/0'
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': REDIS_URL,
    }
}

# Update channel layers for Docker
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('cache', 6379)],
        },
    },
}
