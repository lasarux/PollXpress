from django import forms
from django.contrib.admin import widgets # FIXME
from django.utils.translation import ugettext, ugettext_lazy as _
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
    date_finish = forms.DateField()
    time_finish = forms.CharField(max_length=5)
    
    def __init__(self, user, *args, **kwargs):
        super(PollGenerationForm, self).__init__(*args, **kwargs)
        if user.is_superuser:
            self.fields['space'].queryset = Space.objects.all()
        else:
            self.fields['space'].queryset = Space.objects.filter(admin=user)
    
    def clean(self):
        cleaned_data = self.cleaned_data
        date = cleaned_data['date_finish']
        time = cleaned_data['time_finish']
        try:
            hour, minute = time.split(":")
        except: # check for exact error
            raise forms.ValidationError(_("Bad time format"))
        try:
            date_finish = datetime.datetime(date.year, date.month, date.day, int(hour), int(minute))
        except:
            raise forms.ValidationError(_("Bad time format"))
        # no past dates
        if date_finish <= datetime.datetime.now():
            raise forms.ValidationError(_("Old datetime"))
        return cleaned_data

