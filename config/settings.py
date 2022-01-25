import os
from datetime import timedelta
from pathlib import Path

# ******************************** BASIC **********************************************
from django.conf import settings

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get('SECRET')
DEBUG = bool(os.environ.get('DEVELOPMENT', True))


# ******************************** HOST ACCESS **********************************************
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', '*').split(',')
CORS_ALLOW_ALL_ORIGINS = bool(os.environ.get('DEVELOPMENT', True))
CORS_ALLOW_CREDENTIALS = bool(os.environ.get('CORS_ALLOW_CREDENTIALS', True))


# ******************************** APPS **********************************************
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # DRF
    'rest_framework',

    # FILTERS
    'django_filters',

    # JWT
    'rest_framework_simplejwt',

    # DOCS
    'drf_yasg',

    # CORS
    'corsheaders',

    # CUSTOM
    'apps.users'
    'apps.computer'
]

# ******************************** MIDDLEWARE **********************************************
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # CORS
    'corsheaders.middleware.CorsMiddleware',

    # Cache middlewares
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
]

# ******************************** CACHE **********************************************
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": os.environ.get('DJANGO_CACHING_REDIS_URL'),
    }
}

CACHE_MIDDLEWARE_ALIAS = os.environ.get('CACHE_ALIAS', 'default')
CACHE_MIDDLEWARE_SECONDS = int(os.environ.get('CACHE_TTL'))
CACHE_MIDDLEWARE_KEY_PREFIX = os.environ.get('CACHE_PREFIX', 'django-site-cache')


# ******************************** ROUTER **********************************************
ROOT_URLCONF = 'config.urls'


# ******************************** TEMPLATES **********************************************
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'apps/user/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'staticfiles': 'django.templatetags.static',
            }
        },
    },
]

# ******************************** SERVER **********************************************
WSGI_APPLICATION = 'config.wsgi.application'


# ******************************** Database **********************************************
DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.postgresql',
        "NAME": os.environ.get('POSTGRESQL_DATABASE'),
        "USER": os.environ.get('POSTGRESQL_USER'),
        "PASSWORD": os.environ.get('POSTGRESQL_PASSWORD'),
        "HOST": os.environ.get('POSTGRESQL_HOST'),
        "PORT": os.environ.get('POSTGRESQL_PORT'),
        "TEST": {
            'NAME': os.environ.get('TEST_DB_NAME', 'test-db')
        }
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.UUIDField'


# ******************************** Authentication **********************************************
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

AUTH_USER_MODEL = 'user.User'


# ******************************** Internationalization **********************************************
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# ******************************** Static files (CSS, JavaScript, Images) **********************************************
STATIC_URL = 'static/'
STATIC_ROOT = 'static'

MEDIA_ROOT = 'media'
MEDIA_URL = 'media/'


# ***************************** REST API ********************************************
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'helpers.authentication.customjwt.CustomJWT',
    ),
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler'
}


# ******************************** JWT **********************************************
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=2),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': settings.SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'helpers.authentication.customjwt.custom_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}


# ************************************* SWAGGER ******************************************************
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}


# *******************************  EMAIL *************************************************
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_FROM = os.environ.get('EMAIL_FROM')


# *******************************  REDIS *************************************************
REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')


# *******************************  CLIENT-SIDE  *************************************************
CLIENT_URL = os.environ.get('CLIENT_URL')
