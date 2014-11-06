from django.conf.urls import patterns, include, url
from payments import views
from main.urls import urlpatterns as main_json_urls
from djangular_polls.urls import urlpatterns as djangular_polls_json_urls
from payments.urls import urlpatterns as payments_json_urls
from usermap.urls import urlpatterns as usermap_json_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib import admin
admin.autodiscover()

main_json_urls.extend(djangular_polls_json_urls)
main_json_urls.extend(payments_json_urls)
main_json_urls.extend(usermap_json_urls)

urlpatterns = patterns('',
    url(r'^admin/password_reset/$', auth_views.password_reset, 
        name='admin_password_reset'),
    url(r'^admin/password_reset/done/$', auth_views.password_reset_done, 
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', 
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, 
        name='password_reset_complete'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'main.views.index', name='home'),
    #('^pages/', include('django.contrib.flatpages.urls')),
    url(r'^contact/', 'contact.views.contact', name='contact'),
    url(r'^sign_in$', views.sign_in, name='sign_in'),
    url(r'^sign_out$', views.sign_out, name='sign_out'),
    url(r'^register$', views.register, name='register'),
    url(r'^edit$', views.edit, name='edit'),
    url(r'^report$', 'main.views.report', name="report"),
    url(r'^api/v1/', include(main_json_urls)),
    url(r'^usermap/', 'usermap.views.usermap', name='usermap'),
    #serve media files during deployment
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
