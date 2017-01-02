from django.shortcuts import render
from payments.models import User
from main.models import MarketingItem, StatusReport, Announcement
from datetime import date, timedelta

class market_item(object):

    def __init__(self, img, heading, caption, button_link="register",
                 button_title="View details"):
        self.img = img
        self.heading = heading
        self.caption = caption
        self.button_link = button_link
        self.button_title = button_title

def index(request):
    uid = request.session.get('user')
    if uid is None:
        # main landing page
        market_items = MarketingItem.objects.all()
        return render(
            request,
            'main/index.html',
            {'marketing_items': market_items}
        )
    else:
        # membership page
        status = StatusReport.objects.latest()
        announce_date = date.today() - timedelta(days=30)
        announce = (Announcement.objects.filter(
            when__gt=announce_date).order_by('-when')
        )
        usr = User.get_by_id(uid)
        badges = usr.badges.all()

        return render(
            request,
            'main/user.html',
            {
             'user': usr,
             'badges' : badges,
             'reports': status,
             'announce': announce
            }
        )

def report(request):
    if request.method == "POST":
        status = request.POST.get("status", "")
        #update the database with the status
        if status:
            uid = request.session.get('user')
            user = User.get_by_id(uid)
            StatusReport(user=user, status=status).save()

        #always return something
        return index(request)
