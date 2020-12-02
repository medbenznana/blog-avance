from django import forms

from pagedown.widgets import PagedownWidget

from django.utils.text import slugify

from .models import Post


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview=False))
    #publish = forms.DateField(widget=forms.SelectDateWidget)
    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            #"image",
            "draft",
            "publish",
            "restrict_comment",
        ]

        widgets = {'publish': forms.DateTimeInput(attrs={'class': 'date-input'})}

    def save(self):
        instance = super(PostForm, self).save(commit=False)
        instance.slug = slugify(instance.title)
        instance.save()

        return instance