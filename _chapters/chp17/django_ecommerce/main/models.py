from django.db import models


# Create your models here.
class MarketingItem(models.Model):
    img = models.CharField(max_length=255)
    heading = models.CharField(max_length=300)
    caption = models.TextField()
    button_link = models.URLField(null=True, default="register")
    button_title = models.CharField(max_length=20, default="View details")


class StatusReport(models.Model):
    user = models.ForeignKey('payments.User')
    when = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200)

class Announcement(models.Model):
    when = models.DateTimeField(auto_now=True)
    img = models.CharField(max_length=255, null=True)
    vid = models.URLField(null=True)
    info = models.TextField()


class Badge(models.Model):

    img = models.ImageField(upload_to="images/")
    name = models.CharField(max_length=100)
    desc = models.TextField()

    def thumbnail(self):
        if self.img:
            return u'<img src="%s" width="100" height="100" />' % (self.img.url)
        else:
            return "no image"

    thumbnail.allow_tags = True

    class Meta:
        ordering = ('name',)
