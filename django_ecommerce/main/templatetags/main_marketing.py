from django import template
register = template.Library()

@register.inclusion_tag('main/templatetags/circle_item.html')
def marketing__circle_item(img_name="yoda.jpg", heading="yoda", caption="yoda",
                       button_link="register", button_title="View details"):
    return  {'img' : img_name,
             'heading'     : heading,
             'caption'     : caption,
             'button_link' : button_link,
             'button_title' : button_title}
