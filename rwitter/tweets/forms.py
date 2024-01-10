from django import forms
from .models import Feedback
from django.forms import Textarea, FileField



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
