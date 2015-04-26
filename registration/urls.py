from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
from registration import views

urlpatterns = patterns('',
    (r'^registration/login', views.login),
    (r'^registration/create', views.add_user),
    (r'^registration/confirm', views.confirm),
    (r'^registration/logout', views.logout),
    url(r'^registration/users/$', views.users),
    url(r'^registration/users/(?P<pk>[\w]+)', views.userinfo),
    url(r'^reports/$', views.reports),
    url(r'^reports/reports/(?P<filename>[\w|.]+)', views.download),
    url(r'^reports/(?P<pk>[\w]+)/delete', views.deletereport),
    url(r'^reports/(?P<pk>[\w]+)', views.reportinfo),
    url(r'^groups/$', views.groups),
    url(r'^groups/(?P<groupname>[\w]+)', views.groupinfo),
    url(r'^folders/$', views.folders),
    url(r'^folders/(?P<pk>[\w]+)/delete', views.deletefolder),
    url(r'^folders/(?P<pk>[\w]+)', views.folderinfo),
    (r'^searchform/$', views.searchform),
    (r'^search/$', views.search),
)
