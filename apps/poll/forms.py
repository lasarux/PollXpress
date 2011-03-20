from django import forms
from django.contrib.admin import widgets  
from models import Query, Option, Person, Space
import datetime

class QueryForm(forms.ModelForm):
    """Form for query"""
    class Meta:
        model = Query
        exclude = ('user', 'date_creation')

class OptionForm(forms.ModelForm):
    """Form for option"""
    class Meta:
        model = Option
        exclude = ('query')

class PersonForm(forms.ModelForm):
    """Form for person"""
    class Meta:
        model = Person
        exclude = ('date')

class SpaceForm(forms.ModelForm):
    """Form for person"""
    class Meta:
        model = Space
        exclude = ('admin')

class PollGenerationForm(forms.Form):
    space = forms.ModelChoiceField(queryset=Space.objects.none())
    date_finish = forms.DateTimeField()
    
    def __init__(self, user, *args, **kwargs):
        super(PollGenerationForm, self).__init__(*args, **kwargs)
        if user.is_superuser:
            self.fields['space'].queryset = Space.objects.all()
        else:
            self.fields['space'].queryset = Space.objects.filter(admin=user)

