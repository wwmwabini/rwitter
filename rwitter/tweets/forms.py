from django import forms
from .models import Feedback, Story, Comment
from django.forms import Textarea



class SearchHistoryForm(forms.Form):
    searchterm = forms.CharField(label='Search Rwitter', 
                                 max_length=512,
                                 required=False,
                                 widget=forms.TextInput(attrs={'placeholder': 'Try search a username, post or trend.'})
                                 )

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['subject', 'content', 'media']

        widgets = {
            'subject': forms.Select(),
            'content': Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'media': forms.FileInput(),
        }
    
class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['story']

        widgets = {
            'story': forms.FileInput(),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

        widgets = {
            'content': Textarea(attrs={'class': 'form-control form-control-lg rounded-pill bg-gray', 'rows':1, 'placeholder': 'Write a comment'}),
        }

        labels = {
            'content': '',
        }
