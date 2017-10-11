from django.contrib.auth.models import AbstractBaseUser
from django.conf import settings
from django.db import models
from utils.models import JSONField


class AdminType(object):
    REGULAR_USER = "Regular User"
    ADMIN = "Admin"
    SUPER_ADMIN = "Super Admin"


class ProblemPermission(object):
    NONE = "None"
    OWN = "Own"
    ALL = "All"


class UserManager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})


class User(AbstractBaseUser):
    username = models.CharField(max_length=32, unique=True)
    email = models.EmailField(max_length=64, null=True)
    create_time = models.DateTimeField(auto_now_add=True, null=True)
    # One of UserType
    admin_type = models.CharField(max_length=32, default=AdminType.REGULAR_USER)
    problem_permission = models.CharField(max_length=32, default=ProblemPermission.NONE)
    reset_password_token = models.CharField(max_length=32, null=True)
    reset_password_token_expire_time = models.DateTimeField(null=True)
    # SSO auth token
    auth_token = models.CharField(max_length=32, null=True)
    two_factor_auth = models.BooleanField(default=False)
    tfa_token = models.CharField(max_length=32, null=True)
    session_keys = JSONField(default=list)
    # open api key
    open_api = models.BooleanField(default=False)
    open_api_appkey = models.CharField(max_length=32, null=True)
    is_disabled = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def is_admin(self):
        return self.admin_type == AdminType.ADMIN

    def is_super_admin(self):
        return self.admin_type == AdminType.SUPER_ADMIN

    def is_admin_role(self):
        return self.admin_type in [AdminType.ADMIN, AdminType.SUPER_ADMIN]

    def can_mgmt_all_problem(self):
        return self.problem_permission == ProblemPermission.ALL

    class Meta:
        db_table = "user"


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    # acm_problems_status examples:
    # {
    #     "problems": {
    #         "1": {
    #             "status": JudgeStatus.ACCEPTED,
    #             "_id": "1000"
    #         }
    #     },
    #     "contest_problems": {
    #     }
    # }
    acm_problems_status = JSONField(default=dict)
    # like acm_problems_status, merely add "score" field
    oi_problems_status = JSONField(default=dict)

    real_name = models.CharField(max_length=32, blank=True, null=True)
    avatar = models.CharField(max_length=256, default=f"/{settings.IMAGE_UPLOAD_DIR}/default.png")
    blog = models.URLField(blank=True, null=True)
    mood = models.CharField(max_length=256, blank=True, null=True)
    github = models.CharField(max_length=64, blank=True, null=True)
    school = models.CharField(max_length=64, blank=True, null=True)
    major = models.CharField(max_length=64, blank=True, null=True)
    # for ACM
    accepted_number = models.IntegerField(default=0)
    # for OI
    total_score = models.BigIntegerField(default=0)
    submission_number = models.IntegerField(default=0)

    def add_accepted_problem_number(self):
        self.accepted_number = models.F("accepted_number") + 1
        self.save()

    def add_submission_number(self):
        self.submission_number = models.F("submission_number") + 1
        self.save()

    # 计算总分时， 应先减掉上次该题所得分数， 然后再加上本次所得分数
    def add_score(self, this_time_score, last_time_score=None):
        last_time_score = last_time_score or 0
        self.total_score = models.F("total_score") - last_time_score + this_time_score
        self.save()

    class Meta:
        db_table = "user_profile"
