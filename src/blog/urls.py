"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from accounts import views as account_views

from rest_framework_jwt.views import obtain_jwt_token

from accounts.views import (login_view, register_view, logout_view, change_password, create_profile)

from django.contrib.auth.views import (
    password_reset, 
    password_reset_done,
    password_reset_confirm, 
    password_reset_complete,
)

from posts.feeds import ArchiveFeed, AtomSiteNewsFeed

urlpatterns = [
    
    url(r'^jet/', include('jet.urls', 'jet')),
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    url(r'^admin/', admin.site.urls),
    url(r'^comments/', include("comments.urls", namespace='comments')),
    url(r'^profile/', account_views.profile, name='profile'),
    url(r'^register/', register_view, name='register'),
    url(r'^login/', login_view, name='login'),
    url(r'^logout/', logout_view, name='logout'),
    url(r'^change-password/', change_password, name='change-password'),
    url(r'^create-profile/', create_profile, name='create_profile'),
    url(r'^', include("posts.urls", namespace='posts')),
    url(r'^api/posts/', include("posts.api.urls", namespace='posts-api')),
    url(r'^api/comments/', include("comments.api.urls", namespace='comments-api')),
    url(r'^api/users/', include("accounts.api.urls", namespace='users-api')),

    url(r'^newsletter/', include("newsletters.urls", namespace='newsletters')),

    url(r'^api/auth/token/', obtain_jwt_token),
    # url(r'^api/auth/token/', obtain_jwt_token),
    #url(r'^posts/$', "<appname>.views.<function_name>"),

    url(r'^account/reset-password/', password_reset,  name='reset_password'),
    url(r'^account/password-reset/done/$', password_reset_done, name='password_reset_done'),
    url(r'^account/password-reset/confirm/(?P<uidb64>[\w-]+)/(?P<token>[\w-]+)/$', password_reset_confirm, name='password_reset_confirm'),
    url(r'^account/password-reset/complete/$', password_reset_complete, name='password_reset_complete'),


    url(r'^oauth/', include("social_django.urls", namespace='social')),

    #url(r'^rss/', include("rss.urls", namespace='rss')),

    url(r'^feed/archive/$', ArchiveFeed(), name='archive-feed'),
    #url(r'^feed/atom/$', AtomSiteNewsFeed()),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)