from django import template
register = template.Library()


@register.inclusion_tag(
    'main/templatetags/circle_item.html',
    takes_context=True
)
def marketing__circle_item(context):
    return context
