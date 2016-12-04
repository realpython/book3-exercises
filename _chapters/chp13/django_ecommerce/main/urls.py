from django.conf.urls import url
from main.json_views import status_collection, status_member

urlpatterns = [
    url(r'^status_reports/$', status_collection),
    url(r'^status_reports/(?P<id>[0-9]+)$', status_member),
]
