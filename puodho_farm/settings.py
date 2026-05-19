import os
import secrets
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY') or secrets.token_urlsafe(50)
DEBUG = os.environ.get('DJANGO_DEBUG', 'True').lower() == 'true'
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1,testserver').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'farm',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'farm.middleware.RateLimitMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'puodho_farm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'puodho_farm.wsgi.application'


CACHES = {
    'default': {
        'BACKEND': os.environ.get('DJANGO_CACHE_BACKEND', 'django.core.cache.backends.locmem.LocMemCache'),
        'LOCATION': os.environ.get('DJANGO_CACHE_LOCATION', 'puodho-cache'),
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static'] if (BASE_DIR / 'static').exists() else []
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard_home'
LOGOUT_REDIRECT_URL = 'home'

DATA_UPLOAD_MAX_MEMORY_SIZE = int(os.environ.get('DJANGO_DATA_UPLOAD_MAX_MEMORY_SIZE', 2_621_440))
DATA_UPLOAD_MAX_NUMBER_FIELDS = int(os.environ.get('DJANGO_DATA_UPLOAD_MAX_NUMBER_FIELDS', 200))
DATA_UPLOAD_MAX_NUMBER_FILES = int(os.environ.get('DJANGO_DATA_UPLOAD_MAX_NUMBER_FILES', 20))
FILE_UPLOAD_MAX_MEMORY_SIZE = int(os.environ.get('DJANGO_FILE_UPLOAD_MAX_MEMORY_SIZE', 2_621_440))


# Security hardening
TRUSTED_PROXY_IPS = [ip.strip() for ip in os.environ.get('DJANGO_TRUSTED_PROXY_IPS', '').split(',') if ip.strip()]
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') if os.environ.get('DJANGO_USE_PROXY_SSL', 'False').lower() == 'true' else None
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = 'same-origin'
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'
SECURE_SSL_REDIRECT = os.environ.get('DJANGO_SECURE_SSL_REDIRECT', 'False').lower() == 'true'
SECURE_HSTS_SECONDS = int(os.environ.get('DJANGO_SECURE_HSTS_SECONDS', 31536000 if not DEBUG else 0))
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.environ.get('DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', 'True').lower() == 'true'
SECURE_HSTS_PRELOAD = os.environ.get('DJANGO_SECURE_HSTS_PRELOAD', 'False').lower() == 'true'
if not DEBUG and not os.environ.get('DJANGO_SECRET_KEY'):
    raise RuntimeError('DJANGO_SECRET_KEY must be set when DEBUG=False')
if not DEBUG and 'locmem' in str(CACHES.get('default', {}).get('BACKEND', '')).lower():
    raise RuntimeError('Use a shared cache backend (e.g., Redis) when DEBUG=False for rate limiting consistency')
LOGGING = {
  'version': 1,
  'disable_existing_loggers': False,
  'formatters': {'security': {'format': '[%(asctime)s] %(levelname)s %(name)s %(message)s'}},
  'handlers': {'security_file': {'class': 'logging.FileHandler', 'filename': BASE_DIR / 'security.log', 'formatter': 'security'}},
  'loggers': {'farm.security': {'handlers': ['security_file'], 'level': os.environ.get('DJANGO_SECURITY_LOG_LEVEL', 'WARNING'), 'propagate': False}},
}
