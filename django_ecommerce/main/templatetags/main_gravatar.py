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
    default = 'http://starwars.com//img/explore/encyclopedia/characters/anakinskywalker_relationship.png'

    #mainly for unit testing with a mock object
    if not(isinstance(email,str)):
        return default

    query_params = urlencode([('s', str(size)),
                              ('d', default)])

    return ('http://www.gravatar.com/avatar/' +
           hashlib.md5(email.lower().encode('utf-8')).hexdigest() + 
           '?' + query_params)


