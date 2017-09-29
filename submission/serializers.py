from .models import Submission
from utils.api import serializers
from judge.languages import language_names


class CreateSubmissionSerializer(serializers.Serializer):
    problem_id = serializers.IntegerField()
    language = serializers.ChoiceField(choices=language_names)
    code = serializers.CharField(max_length=20000)
    contest_id = serializers.IntegerField(required=False)


class SubmissionModelSerializer(serializers.ModelSerializer):
    info = serializers.JSONField()
    statistic_info = serializers.JSONField()

    class Meta:
        model = Submission


# 不显示submission info的serializer, 用于ACM rule_type
class SubmissionSafeSerializer(serializers.ModelSerializer):
    problem = serializers.SlugRelatedField(read_only=True, slug_field="_id")
    statistic_info = serializers.JSONField()

    class Meta:
        model = Submission
        exclude = ("info", "contest")


class SubmissionListSerializer(serializers.ModelSerializer):
    problem = serializers.SlugRelatedField(read_only=True, slug_field="_id")
    statistic_info = serializers.JSONField()
    show_link = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Submission
        exclude = ("info", "contest", "code")

    def get_show_link(self, obj):
        # 没传user或为匿名user
        if self.user is None or self.user.id is None:
            return False
        return obj.check_user_permission(self.user)
