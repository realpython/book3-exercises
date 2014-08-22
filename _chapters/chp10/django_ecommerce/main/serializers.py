from django.forms import widgets
from rest_framework import serializers
from main.models import StatusReport
from payments.models import User


class RelatedUserField(serializers.RelatedField):

    read_only = False

    def from_native(self, data):
        return User.objects.get(email=data)


class StatusReportSerializer(serializers.ModelSerializer):
    user = RelatedUserField(many=False)

    class Meta:
        model = StatusReport
        fields = ('id', 'user', 'when', 'status')
