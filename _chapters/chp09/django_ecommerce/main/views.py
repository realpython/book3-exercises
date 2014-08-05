from django.shortcuts import render_to_response
from payments.models import User
from main.models import MarketingItem
#from main.templatetags.main_marketing import marketing__circle_item


class market_item(object):

    def __init__(self, img, heading, caption, button_link="register",
                 button_title="View details"):
        self.img = img
        self.heading = heading
        self.caption = caption
        self.button_link = button_link
        self.button_title = button_title

market_items = [
    market_item(
        img="yoda.jpg",
        heading="Hone your Jedi Skills",
        caption="All members have access to our unique"
        " training and achievements latters. Show off "
        "your Star Wars skills, progress through the "
        "levels and show everyone who the top Jedi Master is!"
    ),
    market_item(
        img="clone_army.jpg",
        heading="Build your Clan",
        caption="Engage in meaningful conversation, or "
        "bloodthirsty battle! If it's related to "
        "Star Wars you better believe we do it."
    ),
    market_item(
        img="leia.jpg",
        heading="Find Love",
        caption="Everybody knows Star Wars fans are the "
        "best mates for Star Wars fans. Find your "
        "Princess Leia or Han Solo and explore the "
        "stars together.", button_title="Sign Up Now"
    ),
]


def index(request):
    uid = request.session.get('user')
    market_items = MarketingItem.objects.all()
    if uid is None:
        return render_to_response(
            'main/index.html',
            {'marketing_items': market_items}
        )
    else:
        return render_to_response(
            'main/user.html',
            {'marketing_items': market_items,
            'user': User.get_by_id(uid)}
        )
