from django.db import models
from datetime import datetime
from embed_video.fields import EmbedVideoField

class ThumbnailMixin(object):
    '''use this mixin if you want to easily show thumbnails for an image field
    in your admin view
    '''

    def thumbnail(self):
        if self.img:
            return u'<img src="%s" width="100" height="100" />' % (self.img.url)
        else:
            return "no image"

    thumbnail.allow_tags = True

class MarketingItem(models.Model, ThumbnailMixin):
    img = models.ImageField(upload_to="marketing/")
    heading = models.CharField(max_length=300)
    caption = models.TextField()
    button_link = models.CharField(null=True, blank=True, max_length=200, default="register")
    button_title = models.CharField(max_length=20,default="View details")

class StatusReportQuerySet(models.QuerySet):
    def latest(self):
        return self.all().order_by('-when')[:20]

class StatusReport(models.Model):

    user = models.ForeignKey('payments.User')
    when = models.DateTimeField(blank=True)
    status = models.CharField(max_length=200)
    objects = StatusReportQuerySet.as_manager()

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

class Announcement(models.Model, ThumbnailMixin):

    when = models.DateTimeField(auto_now=True)
    img = models.ImageField(upload_to="announce/", null=True, blank=True)
    vid = EmbedVideoField(null=True, blank=True)
    info = models.TextField()

class Badge(models.Model,ThumbnailMixin):

    img = models.ImageField(upload_to="images/")
    name = models.CharField(max_length=100)
    desc = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
