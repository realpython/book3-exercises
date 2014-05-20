from django.db import models

class Poll(models.Model):
    title = models.CharField(max_length=255)
    publish_date = models.DateTimeField(auto_now=True)
    #completion date -- add exercise to add countdown later

    def poll_items(self):
        return self.items.all()

class PollItem(models.Model):

    poll = models.ForeignKey(Poll, related_name='items')
    name = models.CharField(max_length=30)
    text = models.CharField(max_length=300)
    votes = models.IntegerField(default=0)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)



