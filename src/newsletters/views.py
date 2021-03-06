from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template

from .models import NewsletterUser
from .forms import NewsletterUserSignUpForm
# Create your views here.

def newsletter_signup(request):
	form = NewsletterUserSignUpForm(request.POST or None)

	if form.is_valid():
		instance = form.save(commit=False)

		if NewsletterUser.objects.filter(email=instance.email).exists():
			messages.warning(request, "Sorry! this email already exist!", "alert alert-warning alert-dismissible")
		else:
			instance.save()
			messages.success(request, "Your email has been submited.", "alert alert-success alert-dismissible")

			subject = "Thank you for joing our Newsletter"
			from_email = settings.EMAIL_HOST_USER
			to_email = [instance.email]
			#signup_message = """Welcome to our bloger site Newsletter. If you would like to unsubscribe visit http://127.0.0.1:8000/newsletter/unsubscribe"""
			#send_mail(subject=subject, from_email=from_email, recipient_list=to_email, message=signup_message, fail_silently=False)

			with open(settings.BASE_DIR + "/templates/newsletters/sign_up_email.txt") as f:
				signup_message = f.read()
			message = EmailMultiAlternatives(subject=subject, body=signup_message, from_email=from_email, to=to_email)
			html_template = get_template("newsletters/sign_up_email.html").render()
			message.attach_alternative(html_template, "text/html")
			message.send()

	context = {
		'form': form,
	}

	return render(request, "newsletters/sign_up.html", context)


def newsletter_unsubscribe(request):
	form = NewsletterUserSignUpForm(request.POST or None)

	if form.is_valid():
		instance = form.save(commit=False)

		if NewsletterUser.objects.filter(email=instance.email).exists():
			NewsletterUser.objects.filter(email=instance.email).delete()
			messages.success(request, "Your email has been removed.", "alert alert-success alert-dismissible")

			subject = "You have been unsubscribe"
			from_email = settings.EMAIL_HOST_USER
			to_email = [instance.email]
			#signup_message = """Sorry to see you go, let us know if there is an issue with our service"""
			#send_mail(subject=subject, from_email=from_email, recipient_list=to_email, message=signup_message, fail_silently=False)

			with open(settings.BASE_DIR + "/templates/newsletters/unsubscribe_email.txt") as f:
				signup_message = f.read()
			message = EmailMultiAlternatives(subject=subject, body=signup_message, from_email=from_email, to=to_email)
			html_template = get_template("newsletters/unsubscribe_email.html").render()
			message.attach_alternative(html_template, "text/html")
			message.send()
		else:
			messages.warning(request, "Sorry! but we did not found your email address", "alert alert-warning alert-dismissible")

	context = {
		'form': form,
	}

	return render(request, "newsletters/unsubscribe.html", context)
