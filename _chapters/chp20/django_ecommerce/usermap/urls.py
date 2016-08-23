from django.conf.urls import patterns, url


urlpatterns = patterns(
    'usermap.json_views',
    url(r'^user_locations$', 'user_locations_list'),
)
