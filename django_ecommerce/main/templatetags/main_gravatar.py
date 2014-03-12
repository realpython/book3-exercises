from django import template
from urllib.parse import urlencode
import hashlib

register = template.Library()

@register.simple_tag
def gravatar(email, size=140):
    url = get_url(email, size)
    return '''<img class="img-circle" src="%s" height="%s" width="%s"
            alt="user.avatar" />''' % (url, size, size)

def get_url(email, size=140):
    default = 'http://starwars.com//img/explore/encyclopedia/characters/anakinskywalker_relationship.png'
    query_params = urlencode([('s', str(size)),
                              ('d', default)])



    return ('http://www.gravatar.com/avatar/' +
           hashlib.md5(email.lower().encode('utf-8')).hexdigest() + 
           '?' + query_params)


