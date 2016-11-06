from rest_framework import serializers
from main.models import StatusReport
from payments.models import User


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

'''
class StatusReportSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    user = serializers.StringRelatedField()
    when = serializers.DateTimeField()
    status = serializers.CharField(max_length=200)

    def create(self, validated_data):
        return StatusReport(**validated_data)

    def update(self, instance, validated_data):
        from pprint import pprint
        pprint(validated_data)
        instance.user = validated_data.get('user', instance.user)
        instance.when = validated_data.get('when', instance.when)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
'''
