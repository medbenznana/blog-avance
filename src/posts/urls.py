from django.conf.urls import url
from django.contrib import admin

from .views import (
	about,
	post_list,
	post_create,
	post_detail,
	post_update,
	post_delete,
	favourite_post,
	PostLikeToggle,
	PostLikeAPIToggle,
	PostnoLikeToggle,
	PostnoLikeAPIToggle,
	post_favourite_list,
	)

urlpatterns = [
	url(r'^$', post_list, name='list'),
	url(r'^about/$', about, name='about'),
    url(r'^create/$', post_create, name='create'),
    url(r'^(?P<id>\d+)/(?P<slug>[\w-]+)/$', post_detail, name='detail'),
    url(r'^(?P<id>\d+)/(?P<slug>[\w-]+)/like/$', PostLikeToggle.as_view(), name='like-toggle'),
    url(r'^api/(?P<id>\d+)/(?P<slug>[\w-]+)/like/$', PostLikeAPIToggle.as_view(), name='like-api-toggle'),
    url(r'^(?P<id>\d+)/(?P<slug>[\w-]+)/nolike/$', PostnoLikeToggle.as_view(), name='no-like-toggle'),
    url(r'^api/(?P<id>\d+)/(?P<slug>[\w-]+)/nolike/$', PostnoLikeAPIToggle.as_view(), name='no-like-api-toggle'),
    url(r'^(?P<id>\d+)/(?P<slug>[\w-]+)/edit/$', post_update, name='update'),
    url(r'^(?P<id>\d+)/(?P<slug>[\w-]+)/delete/$', post_delete, name='delete'),
    url(r'^(?P<id>\d+)/(?P<slug>[\w-]+)/favourite_post/$', favourite_post, name='favourite_post'),
    url(r'^favourite/$', post_favourite_list, name='post_favourite_list'),
    #url(r'^posts/$', "<appname>.views.<function_name>"),
]
