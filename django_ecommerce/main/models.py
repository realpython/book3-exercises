from django.db import models
from payments.models import User

# Create your models here.
class MarketingItem(models.Model):
    img = models.CharField(max_length=255)
    heading = models.CharField(max_length=300)
    caption = models.TextField()
    button_link = models.URLField(null=True, default="register")
    button_title = models.CharField(max_length=20,default="View details")

class StatusReportQuerySet(models.QuerySet):
    def latest(self):
        return self.all().order_by('-when')[:20]

class StatusReport(models.Model):
    user = models.ForeignKey(User)
    when = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=200)
    objects = StatusReportQuerySet.as_manager()

class Announcement(models.Model):

    when = models.DateTimeField(auto_now=True)
    img = models.CharField(max_length=255, null=True)
    vid = models.URLField(null=True)
    info = models.TextField()



    





