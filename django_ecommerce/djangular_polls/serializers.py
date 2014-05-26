from rest_framework import serializers
from djangular_polls.models import Poll, PollItem

class PollItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollItem
        fields = ('id','poll','name','text','votes','percentage')

class PollSerializer(serializers.ModelSerializer):
    items = PollItemSerializer(many=True, required=False)

    class Meta:
        model = Poll
        fields = ('title','publish_date', 'items')
        
