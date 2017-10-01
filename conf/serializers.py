from utils.api import DateTimeTZField, serializers

from .models import JudgeServer


class EditSMTPConfigSerializer(serializers.Serializer):
    server = serializers.CharField(max_length=128)
    port = serializers.IntegerField(default=25)
    email = serializers.EmailField(max_length=128)
    password = serializers.CharField(max_length=128, required=False, allow_null=True, allow_blank=True)
    tls = serializers.BooleanField()


class CreateSMTPConfigSerializer(EditSMTPConfigSerializer):
    password = serializers.CharField(max_length=128)


class TestSMTPConfigSerializer(serializers.Serializer):
    email = serializers.EmailField()


class CreateEditWebsiteConfigSerializer(serializers.Serializer):
    website_base_url = serializers.CharField(max_length=128)
    website_name = serializers.CharField(max_length=32)
    website_name_shortcut = serializers.CharField(max_length=32)
    website_footer = serializers.CharField(max_length=1024)
    allow_register = serializers.BooleanField()
    submission_list_show_all = serializers.BooleanField()


class JudgeServerSerializer(serializers.ModelSerializer):
    create_time = DateTimeTZField()
    last_heartbeat = DateTimeTZField()
    status = serializers.CharField()

    class Meta:
        model = JudgeServer
        fields = "__all__"


class JudgeServerHeartbeatSerializer(serializers.Serializer):
    hostname = serializers.CharField(max_length=64)
    judger_version = serializers.CharField(max_length=24)
    cpu_core = serializers.IntegerField(min_value=1)
    memory = serializers.FloatField(min_value=0, max_value=100)
    cpu = serializers.FloatField(min_value=0, max_value=100)
    action = serializers.ChoiceField(choices=("heartbeat", ))
    service_url = serializers.CharField(max_length=128, required=False)
