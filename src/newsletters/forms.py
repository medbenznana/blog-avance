from django import forms
from .models import NewsletterUser

class NewsletterUserSignUpForm(forms.ModelForm):
	email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your@email.com'}))
	class Meta:
		model = NewsletterUser
		fields = [
            "email",
        ]

		def clean_email(self):
			email = self.cleaned_data.get('email')

			return email