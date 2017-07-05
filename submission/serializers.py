from .models import Submission
from account.models import User
from utils.api import serializers
from judge.languages import language_names


class CreateSubmissionSerializer(serializers.Serializer):
    problem_id = serializers.IntegerField()
    language = serializers.ChoiceField(choices=language_names)
    code = serializers.CharField(max_length=20000)


class SubmissionModelSerializer(serializers.ModelSerializer):
    info = serializers.JSONField()
    statistic_info = serializers.JSONField()

    class Meta:
        model = Submission


# 不显示submission info详情的serializer
class SubmissionSafeSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    statistic_info = serializers.JSONField()

    class Meta:
        model = Submission
        exclude = ('info', 'contest_id')

    @staticmethod
    def get_username(obj):
        return User.objects.get(id=obj.user_id).username


class SubmissionListSerializer(SubmissionSafeSerializer):
    username = serializers.SerializerMethodField()
    statistic_info = serializers.JSONField()
    show_link = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Submission
        exclude = ('info', 'contest_id', 'code')

    def get_show_link(self, obj):
        return obj.check_user_permission(self.user)

    @staticmethod
    def get_username(obj):
        return User.objects.get(id=obj.user_id).username