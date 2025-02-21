"""
Django settings for main project.

Generated by 'django-admin startproject' using Django 3.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-#ooysxv$hd2fi(pdfzhu3!bfg*+&v=fuf^3*&am*^rck29h^j-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.getenv('DJANGO_DEBUG', 0)))

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '*').split(',')


EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_SERVER_PORT = os.getenv('EMAIL_SERVER_PORT')
EMAIL_SERVER_NAME = os.getenv('EMAIL_SERVER_NAME')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap5',
    'customer'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'customer/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]


WSGI_APPLICATION = 'main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST'),
        'PORT': os.environ.get('POSTGRES_PORT'),
        'CONN_MAX_AGE': 0,
    },
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
   {
       'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
   },
   {
       'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
   },
   {
       'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
   },
   {
       'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
   },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'uk-ua'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

TIME_ZONE = 'Europe/Kyiv'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_ROOT = Path(BASE_DIR, 'static')
MEDIA_ROOT = Path(BASE_DIR, 'media')

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REDIS_HOST = 'redis'
REDIS_PORT = '6379'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f'redis://{REDIS_HOST}:{REDIS_PORT}/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient'
        },
        'KEY_PREFIX': '',
        'TIMEOUT': None,
    }
}


CURRENCY = 'USD'

CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELRY_TASK_SERIALIZER = 'json'
CELRY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Kyiv'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'custom': {
            'format': '[%(asctime)s] %(levelname)-7s %(message)s ',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'formatter': 'custom',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'customer': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

SOCIAL_AUTH_GOOGLE_CLIENT_ID = os.getenv('SOCIAL_AUTH_GOOGLE_CLIENT_ID')
SOCIAL_AUTH_GOOGLE_SECRET = os.getenv('SOCIAL_AUTH_GOOGLE_SECRET')

SOCIAL_AUTH_GITHUB_CLIENT_ID = os.getenv('SOCIAL_AUTH_GITHUB_CLIENT_ID')
SOCIAL_AUTH_GITHUB_SECRET = os.getenv('SOCIAL_AUTH_GITHUB_SECRET')
