# coding=utf-8
from __future__ import unicode_literals
from django.test.testcases import TestCase
from rest_framework.test import APIClient

from account.models import User, AdminType


class APITestCase(TestCase):
    client_class = APIClient

    def create_user(self, username, password, admin_type=AdminType.REGULAR_USER, login=False):
        user = User.objects.create(username=username, admin_type=admin_type)
        user.set_password(password)
        user.save()
        if login:
            self.client.login(username=username, password=password)
        return user

    def create_admin(self, username="admin", password="admin", login=False):
        return self.create_user(username=username, password=password, admin_type=AdminType.ADMIN, login=login)

    def create_super_admin(self, username="root", password="root", login=False):
        return self.create_user(username=username, password=password, admin_type=AdminType.SUPER_ADMIN, login=login)

    def assertSuccess(self, response):
        self.assertTrue(response.data["error"] is None)

    def assertFailed(self, response):
        self.assertTrue(response.data["error"] is not None)