from django import template
from urllib.parse import urlencode
import hashlib
from django.utils.html import mark_safe, escape

register = template.Library()


@register.simple_tag
def gravatar_img(email, size=140):
    url = get_url(email, size)
    return mark_safe('''<img class="img-circle"
                         src="%s" height="%s" width="%s"
                         alt="user.avatar" />''' %
                     (escape(url), escape(size), escape(size))
                    )


def get_url(email, size=140):
    default = ('http://upload.wikimedia.org/wikipedia/en/9/9b/'
               'Yoda_Empire_Strikes_Back.png')

    query_params = urlencode([('s', str(size)),
                              ('d', default)])
    email = hashlib.md5(email.lower().encode('utf-8')).hexdigest()

    return 'http://www.gravatar.com/avatar/%s?%s' % (email,query_params)
