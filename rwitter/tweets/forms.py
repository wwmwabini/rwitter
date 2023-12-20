from django import forms

class SearchHistoryForm(forms.Form):
    searchterm = forms.CharField(label='Search Rwitter', 
                                 max_length=512, 
                                 widget=forms.TextInput(attrs={'placeholder': 'type your search term here...'})
                                 )