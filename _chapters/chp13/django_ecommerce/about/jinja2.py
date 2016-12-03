from django.contrib.staticfiles.storage import staticfiles_storage
# django 1.10
# from django.urls import reverse
# django 1.9
from django.core.urlresolvers import reverse
from main.templatetags.main_marketing import marketing__aboutus
from django.template.loader import get_template

from jinja2 import Environment

def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
        'marketing__aboutus': marketing__aboutus,
        'site_header': site_header,
        'site_footer': site_footer,
    })
    return env

def site_header():
    template = get_template('__head_and_nav.html', using='django')
    return template.render()

def site_footer():
    template = get_template('__footer.html', using='django')
    return template.render()



