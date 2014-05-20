from django.db import models

class Poll(models.Model):
    title = models.CharField(max_length=255)
    publish_date = models.DateTimeField(auto_now=True)
    #completion date -- add exercise to add countdown later

class PollItem(models.Model):

    poll = models.ForeignKey(Poll)
    name = models.CharField(max_length=30)
    text = models.CharField(max_length=300)
    votes = models.IntegerField(default=0)
    percentage = models.Field(default = 0.0)



