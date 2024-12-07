from django import forms
from .models import Discussion, Comment

class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion
        exclude = ['user']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']