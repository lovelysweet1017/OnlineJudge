from django.conf.urls import url

from ..views.admin import ContestProblemAPI, ProblemAPI, TestCaseUploadAPI, MakeContestProblemPublicAPIView

urlpatterns = [
    url(r"^test_case/upload/?$", TestCaseUploadAPI.as_view(), name="test_case_upload_api"),
    url(r"^problem/?$", ProblemAPI.as_view(), name="problem_admin_api"),
    url(r"^contest/problem/?$", ContestProblemAPI.as_view(), name="contest_problem_admin_api"),
    url(r"^contest_problem/make_public/?$", MakeContestProblemPublicAPIView.as_view(), name="make_public_api"),
]
