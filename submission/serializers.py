from .models import Submission
from utils.api import serializers
from judge.languages import language_names


class CreateSubmissionSerializer(serializers.Serializer):
    problem_id = serializers.IntegerField()
    language = serializers.ChoiceField(choices=language_names)
    code = serializers.CharField(max_length=20000)


class SubmissionModelSerializer(serializers.ModelSerializer):
    info = serializers.JSONField()
    accepted_info = serializers.JSONField()

    class Meta:
        model = Submission
