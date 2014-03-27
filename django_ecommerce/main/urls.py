from django.conf.urls import patterns, url
from main import json_views

urlpatterns = patterns('main.json_views',
    url(r'^status_reports/$', json_views.StatusCollection.as_view()),
    url(r'^status_reports/(?P<pk>[0-9]+)/$',json_views.StatusMember.as_view()),
    url(r'^badges/$', json_views.BadgeCollection.as_view()),
    url(r'^badges/(?P<pk>[0-9]+)/$', json_views.BadgeMember.as_view())
    )
