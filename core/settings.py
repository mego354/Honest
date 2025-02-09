import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-a@6vc)g=-8&u$dyg^p*0-ig_-(4la%^la%y7hi!mxik*l&osjk'
DEBUG = True
ALLOWED_HOSTS = []
STATIC_URL = 'static/'
STATIC_ROOT = 'cloth/static'
MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

Hosted = True
# Hosted = False 
if Hosted:
    DEBUG = False
    ALLOWED_HOSTS = ['honestfabrics.pythonanywhere.com', 'www.honestfactory.top']
    STATIC_ROOT = '/home/honestfabrics/Honest/cloth/static'
    MEDIA_ROOT = '/home/honestfabrics/Honest/media'

# Application definition
INSTALLED_APPS = [
    'production',
    'cloth',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'core.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

SECURE_API_PASSCODE = os.getenv('SECURE_API_PASSCODE', 'AhMeDnAbIl_passcode_564654')

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



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Etc/GMT-2'
USE_I18N = True
USE_TZ = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'mahmoudmegahd010000@gmail.com'
EMAIL_HOST_PASSWORD = 'nuiovtbksdoxoemb'
DEFAULT_FROM_EMAIL = 'Honest Factory'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
