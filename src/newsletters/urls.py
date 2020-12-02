from django.conf.urls import url

from .views import (
	newsletter_signup,
	newsletter_unsubscribe,
	)

urlpatterns = [
	url(r'^sign_up/$', newsletter_signup, name='newsletter_signup'),
    url(r'^unsubscribe/$', newsletter_unsubscribe, name='newsletter_unsubscribe'),
]
