from django.db import models
from django.db.models import Sum


class Poll(models.Model):
    title = models.CharField(max_length=255)
    publish_date = models.DateTimeField(auto_now=True)

    @property
    def total_votes(self):
        return self.poll_items().aggregate(Sum('votes')).get('votes__sum', 0)

    def poll_items(self):
        return self.items.all()


class PollItem(models.Model):

    poll = models.ForeignKey(Poll, related_name='items')
    name = models.CharField(max_length=30)
    text = models.CharField(max_length=300)
    votes = models.IntegerField(default=0)

    @property
    def percentage(self):
        total = self.poll.total_votes
        if total:
            return self.votes / total * 100
        return 0

    class Meta:
        ordering = ['-text']
