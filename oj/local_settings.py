# coding=utf-8
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    # submission 的 name 和 engine 请勿修改，其他代码会用到
    'submission': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db1.sqlite3'),
    }
}

REDIS_CACHE = {
    "host": "127.0.0.1",
    "port": 6379,
    "db": 1
}

REDIS_QUEUE = {
    "host": "127.0.0.1",
    "port": 6379,
    "db": 2
}

DEBUG = True

ALLOWED_HOSTS = ["*"]

TEST_CASE_DIR = "/tmp"

