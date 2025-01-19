from .models import Comment, Subscriber
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ('name', 'email')