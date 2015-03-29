from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
from registration import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SecureWitness.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    (r'^registration/login', login),
    (r'^registration/create', views.add_user),
    (r'^registration/confirm', views.confirm),
    (r'^profile', views.profile)
)
