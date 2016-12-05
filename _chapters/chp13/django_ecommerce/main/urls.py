from django.conf.urls import url
from main import json_views

urlpatterns = [
    url(r'^status_reports/$', json_views.StatusCollection.as_view()),
    url(r'^status_reports/(?P<id>[0-9]+)$', json_views.StatusMember.as_view()),
]
