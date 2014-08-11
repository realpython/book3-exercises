from django.conf.urls import patterns, url, include
from usermap import json_views

urlpatterns = patterns('usermap.json_views',
    #url(r'^user_locations$', json_views.UserLocationCollection.as_view(),
    #    name='user_locations_collection'),
    url(r'^user_locations$', 'user_locations_list'),
)
