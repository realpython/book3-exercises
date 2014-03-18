from django.forms import widgets
from rest_framework import serializers
from main.models import StatusReport
from payments.models import User

class RelatedUserField(serializers.RelatedField):

    read_only = False

    def to_native(self, value):
        return str(value)

    def from_native(self, data):
        return User.objects.get(email=data)

class StatusReportSerializer(serializers.ModelSerializer):
    user = RelatedUserField(many=False)
    
    class Meta:
        model = StatusReport
        fields = ('id','user','when','status')



    '''
    pk = serializers.Field()
    user = serializers.PrimaryKeyRelatedField(many=False)
    when = serializers.DateTimeField()
    status = serializers.CharField(max_length=200)
    

    def restore_object(self, attrs, instance=None):

        if instance:
            instance.user = attrs.get('user', instance.user)
            instance.when = attrs.get('when', instance.when)
            instance.status = attrs.get('status', instance.status)
            print ("we returned and instance")
            return instance

        status = Status_Reports(**attrs)

        try:
            user = User.object.get(email=attrs['user'])
            status.user = user
        except:
            import pprint
            pprint.pprint(attrs)
        
        return status
    '''


