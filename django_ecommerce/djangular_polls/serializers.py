from rest_framework import serializers
from djangular_polls.models import Poll, PollItem

class PollItemSerializer(serializers.ModelSerializer):
    percentage = serializers.Field(source='percentage')

    class Meta:
        model = PollItem
        fields = ('id','poll','name','text','votes','percentage')

class PollSerializer(serializers.ModelSerializer):
    items = PollItemSerializer(many=True, required=False)
    total_votes = serializers.Field(source='total_votes')

    class Meta:
        model = Poll
        fields = ('title','publish_date', 'items','total_votes')
        
