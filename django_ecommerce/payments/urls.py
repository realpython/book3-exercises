from django.conf.urls import patterns, url, include
from payments import json_views

urlpatterns = patterns('payments.json_views',
    url(r'^users$', 'post_user'),
    #url(r'^users$', json_views.UserCollection.as_view(),
    #    name='users_collection'),
)
