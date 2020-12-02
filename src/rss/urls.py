from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^feeds/', views.rest_feeds, name='rest-feeds'),
	url(r'^feeds/(?P<pk>[0-9]+)/$', views.rest_feeds_detail, name='rest-feeds-detail'),
	url(r'^items/', views.rest_items, name='rest-items')
]