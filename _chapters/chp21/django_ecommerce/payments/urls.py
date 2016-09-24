from django.conf.urls import patterns, url
from .json_views import ChangePassword


urlpatterns = patterns(
    'payments.json_views',
    url(r'^users$', 'post_user'),
    url(r'^users/password/(?P<pk>[0-9]+)$', ChangePassword.as_view(),
        name='change_password'),
)
