from django.conf.urls import patterns, url, include
from payments import json_views

urlpatterns = patterns('payments.json_views',
    url(r'^users$', 'post_user'),
    url(r'^users/password/(?P<pk>[0-9]+)$', json_views.ChangePassword.as_view(),
        name='change_password'),
)
