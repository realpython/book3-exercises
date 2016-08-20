from rest_framework import serializers
from main.models import StatusReport
from payments.models import User, Badge


class RelatedUserField(serializers.RelatedField):

    read_only = False

    def to_representation(self, value):
        return value.email

    def to_internal_value(self, data):
        return User.objects.get(email=data)

class StatusReportSerializer(serializers.ModelSerializer):
    user = RelatedUserField(queryset=User.objects.all())

    class Meta:
        model = StatusReport
        fields = ('id', 'user', 'when', 'status')


class BadgeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Badge
        fields = ('id', 'img', 'name', 'desc')
