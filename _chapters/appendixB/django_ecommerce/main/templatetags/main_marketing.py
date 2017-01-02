from django import template
register = template.Library()
from django.template.loader import get_template
from main.views import market_item


@register.inclusion_tag('main/templatetags/circle_item.html', takes_context=True)
def marketing__circle_item(context):
    return context


def marketing__aboutus(context=None):
    template = get_template('main/templatetags/circle_item.html')
    if not context:
        context = {'marketing_items': aboutus_items}
    return template.render(context)


aboutus_items= [
    market_item(
        img="yoda.jpg",
        heading="Grandmaster Fletcher",
        caption="The original, the grandmaster"
        " the man who created it all and the `brains` behind"
        " the entire operation",
    ),
    market_item(
        img="clone_army.jpg",
        heading="Mike the Marketer",
        caption="Organizing the troops,"
        "Mike spends his days doing social stuff, publishing"
        " and of course writting his own awesome stuff.",
    ),
    market_item(
        img="leia.jpg",
        heading="j1z0 the lover",
        caption="Somebody got to spread the love"
    ),
]
