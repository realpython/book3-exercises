from django.conf.urls import include, url
from payments import views
from django.contrib import admin
from main.views import index as main_index
from contact.views import contact
from about.views import about

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', main_index, name='home'),
    #url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'^about', about, name='about'),
    url(r'^contact/', contact, name='contact'),

    # user registration/authentication
    url(r'^sign_in$', views.sign_in, name='sign_in'),
    url(r'^sign_out$', views.sign_out, name='sign_out'),
    url(r'^register$', views.register, name='register'),
    url(r'^edit$', views.edit, name='edit'),
]
