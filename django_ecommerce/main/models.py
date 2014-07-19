from django.db import models
from datetime import datetime

<<<<<<< HEAD
# Create your models here.
class Marketing_items(models.Model):
=======
class MarketingItem(models.Model):
>>>>>>> abe8bb86f1cf84d3b030cc1e77193d2909d60e28
    img = models.CharField(max_length=255)
    heading = models.CharField(max_length=300)
    caption = models.TextField()
    button_link = models.URLField(null=True, default="register")
    button_title = models.CharField(max_length=20,default="View details")

<<<<<<< HEAD


=======
class StatusReport(models.Model):

    user = models.ForeignKey('payments.User')
    when = models.DateTimeField(blank=True)
    status = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        if self.when is None:
            self.when = self._getNowNoMicroseconds()
        super(StatusReport, self).save(*args, **kwargs)

    def _getNowNoMicroseconds(self):
        '''we want to get time without microseconds so it
        converts to javascript time correctly'''
        t = datetime.now()
        return datetime(t.year, t.month,t.day,t.hour,
                        t.minute,t.second,0,t.tzinfo)

class Announcement(models.Model):

    when = models.DateTimeField(auto_now=True)
    img = models.CharField(max_length=255, null=True)
    vid = models.URLField(null=True)
    info = models.TextField()

class Badge(models.Model):

    img = models.CharField(max_length=255)
    name = models.CharField(max_length=100)
    desc = models.TextField()

    class Meta:
        ordering = ('name',)
>>>>>>> abe8bb86f1cf84d3b030cc1e77193d2909d60e28
