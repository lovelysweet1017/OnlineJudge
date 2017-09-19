# coding=utf-8
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# For celery
REDIS_QUEUE = {
    "host": "127.0.0.1",
    "port": 6379,
    "db": 4
}

DEBUG = True

ALLOWED_HOSTS = ["*"]

TEST_CASE_DIR = "/tmp"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

LOG_PATH = "log/"
