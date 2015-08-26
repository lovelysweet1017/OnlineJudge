# coding=utf-8
import json
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from account.models import User, REGULAR_USER, ADMIN, SUPER_ADMIN
from problem.models import Problem
from contest.models import Contest, ContestProblem
from submission.models import Submission
from rest_framework.test import APITestCase, APIClient


class ContestSubmissionAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('contest_submission_api')
        self.user1 = User.objects.create(username="test1", admin_type=SUPER_ADMIN)
        self.user1.set_password("testaa")
        self.user1.save()
        self.user2 = User.objects.create(username="test2", admin_type=REGULAR_USER)
        self.user2.set_password("testbb")
        self.user2.save()
        self.global_contest = Contest.objects.create(title="titlex", description="descriptionx", mode=1,
                                                     contest_type=1, show_rank=True, show_user_submission=True,
                                                     start_time="2015-08-15T10:00:00.000Z",
                                                     end_time="2015-08-30T12:00:00.000Z",
                                                     created_by=User.objects.get(username="test1"))
        self.contest_problem = ContestProblem.objects.create(title="titlex",
                                                             description="descriptionx",
                                                             input_description="input1_description",
                                                             output_description="output1_description",
                                                             test_case_id="1",
                                                             samples=json.dumps([{"input": "1 1", "output": "2"}]),
                                                             time_limit=100,
                                                             memory_limit=1000,
                                                             hint="hint1",
                                                             created_by=User.objects.get(username="test1"),
                                                             contest=Contest.objects.get(title="titlex"),
                                                             sort_index="a")

    # 以下是创建比赛的提交
    def test_invalid_format(self):
        self.client.login(username="test1", password="testaa")
        data = {"contest_id": self.global_contest.id, "language": 1}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.data["code"], 1)

    def test_contest_submission_successfully(self):
        self.client.login(username="test1", password="testaa")
        data = {"contest_id": self.global_contest.id, "problem_id": self.contest_problem.id,
                "language": 1, "code": '#include "stdio.h"\nint main(){\n\treturn 0;\n}'}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.data["code"], 0)

    def test_contest_problem_does_not_exist(self):
        self.client.login(username="test1", password="testaa")
        data = {"contest_id": self.global_contest.id, "problem_id": self.contest_problem.id + 10,
                "language": 1, "code": '#include "stdio.h"\nint main(){\n\treturn 0;\n}'}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.data, {"code": 1, "data": u"题目不存在"})


class ContestProblemMySubmissionListTest(TestCase):
    # 以下是我比赛单个题目的提交列表的测试
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create(username="test1", admin_type=SUPER_ADMIN)
        self.user1.set_password("testaa")
        self.user1.save()
        self.user2 = User.objects.create(username="test2", admin_type=REGULAR_USER)
        self.user2.set_password("testbb")
        self.user2.save()
        self.global_contest = Contest.objects.create(title="titlex", description="descriptionx", mode=1,
                                                     contest_type=1, show_rank=True, show_user_submission=True,
                                                     start_time="2015-08-15T10:00:00.000Z",
                                                     end_time="2015-08-30T12:00:00.000Z",
                                                     created_by=User.objects.get(username="test1"))
        self.contest_problem = ContestProblem.objects.create(title="titlex",
                                                             description="descriptionx",
                                                             input_description="input1_description",
                                                             output_description="output1_description",
                                                             test_case_id="1",
                                                             samples=json.dumps([{"input": "1 1", "output": "2"}]),
                                                             time_limit=100,
                                                             memory_limit=1000,
                                                             hint="hint1",
                                                             created_by=self.user1,
                                                             contest=self.global_contest,
                                                             sort_index="a")
