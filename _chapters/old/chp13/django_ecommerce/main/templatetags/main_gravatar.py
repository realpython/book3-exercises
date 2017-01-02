from django import template
from urllib.parse import urlencode
import hashlib

register = template.Library()


@register.simple_tag
def gravatar_img(email, size=140):
    url = gravatar_url(email, size)
    return '''<img class="img-circle" src="%s" height="%s" width="%s"
            alt="user.avatar" />''' % (url, size, size)


@register.simple_tag
def gravatar_url(email, size=140):
    default = ('http://upload.wikimedia.org/wikipedia/en/9/9b/'
               'Yoda_Empire_Strikes_Back.png')

    #mainly for unit testing with a mock object
    if not(isinstance(email, str)):
        return default

    query_params = urlencode([('s', str(size)),
                              ('d', default)])

    return ('http://www.gravatar.com/avatar/' +
            hashlib.md5(email.lower().encode('utf-8')).hexdigest() +
            '?' + query_params)
