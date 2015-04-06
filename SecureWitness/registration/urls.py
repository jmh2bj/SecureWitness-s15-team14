from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
from registration import views

urlpatterns = patterns('',
    (r'^registration/login', views.login),
    (r'^registration/create', views.add_user),
    (r'^registration/confirm', views.confirm),
    (r'^registration/logout', views.logout),
    url(r'^reports/$', views.reports),
    url(r'^reports/(?P<pk>[\w]+)', views.reportinfo),
    url(r'^groups/$', views.groups),
    url(r'^groups/(?P<groupname>[\w]+)', views.groupinfo),
    (r'^searchform/$', views.searchform),
    (r'^search/$', views.search),
)
