from django.conf.urls import patterns, url, include
from main import json_views

urlpatterns = patterns('main.json_views',
    url(r'^$', 'api_root'),
    url(r'^status_reports/$', json_views.StatusCollection.as_view(),
        name='status_reports_collection'),
    url(r'^status_reports/(?P<pk>[0-9]+)/$',json_views.StatusMember.as_view()),
    url(r'^badges/$', json_views.BadgeCollection.as_view(),
        name='badges_collection'),
    url(r'^badges/(?P<pk>[0-9]+)/$', json_views.BadgeMember.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    )
