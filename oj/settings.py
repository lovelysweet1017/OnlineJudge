# coding=utf-8
"""
Django settings for oj project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

# 判断运行环境
ENV = os.environ.get("oj_env", "local")

if ENV == "local":
    from .local_settings import *
elif ENV == "server":
    from .server_settings import *

BROKER_BACKEND = "redis"
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'hzfp^8mbgapc&x%$#xv)0=t8s7_ilingw(q3!@h&2fty6v6fxz'


# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'account',
    'announcement',
    'utils',
    'group',
    'problem',
    'admin',
    'submission',
    'contest',
    'mail',
    'judge',
    'judge_dispatcher',

    'django_extensions',
    'rest_framework',
    'django_rq',
)

if DEBUG:
    INSTALLED_APPS += (
        # 'debug_toolbar',
        'rest_framework_swagger',
    )

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'admin.middleware.AdminRequiredMiddleware',
    'account.middleware.SessionSecurityMiddleware'
)

ROOT_URLCONF = 'oj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': TEMPLATE_DIRS,
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

WSGI_APPLICATION = 'oj.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

AUTH_USER_MODEL = 'account.User'

LOG_PATH = "log/"


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s'}
        # 日志格式
    },
    'handlers': {
        'django_error': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_PATH + 'django.log',
            'formatter': 'standard'
        },
        'app_info': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_PATH + 'app_info.log',
            'formatter': 'standard'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        }
    },
    'loggers': {
        'app_info': {
            'handlers': ['app_info', "console"],
            'level': 'DEBUG',
            'propagate': True
        },
        'django.request': {
            'handlers': ['django_error', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        }
    },
}

if DEBUG:
    REST_FRAMEWORK = {
        'TEST_REQUEST_DEFAULT_FORMAT': 'json'
    }
else:
    REST_FRAMEWORK = {
        'TEST_REQUEST_DEFAULT_FORMAT': 'json',
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
        )
    }

DATABASE_ROUTERS = ['oj.db_router.DBRouter']

TEST_CASE_DIR = os.path.join(BASE_DIR, 'test_case/')

IMAGE_UPLOAD_DIR = os.path.join(BASE_DIR, 'upload/')

WEBSITE_INFO = {"website_name": "qduoj",
                "website_footer": u"青岛大学信息工程学院 创新实验室",
                "url": "https://qduoj.com"}

RQ_QUEUES = {
    'judge': {
        'HOST': REDIS_QUEUE["host"],
        'PORT': REDIS_QUEUE["port"],
        'DB': 2,
        'DEFAULT_TIMEOUT': 60,
    },
    'mail': {
        'HOST': REDIS_QUEUE["host"],
        'PORT': REDIS_QUEUE["port"],
        'DB': 3,
        'DEFAULT_TIMEOUT': 60,
    }
}