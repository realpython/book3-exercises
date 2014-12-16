from django.conf.urls import patterns, url


urlpatterns = patterns(
    'payments.json_views',
    url(r'^users$', 'post_user'),
)
