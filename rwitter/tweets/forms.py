from django import forms

class SearchHistoryForm(forms.Form):
    searchterm = forms.CharField(label='Search Rwitter', 
                                 max_length=512,
                                 required=False,
                                 widget=forms.TextInput(attrs={'placeholder': 'Try search a username, post or trend.'})
                                 )
