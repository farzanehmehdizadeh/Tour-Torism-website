from django import forms
from .models import tour


class tourform(forms.ModelForm):
    class Meta:
        model = tour
        fields = ['title','idtour', 'firstdistination','lastDestination','capacity', 'image', 'startdate', 'finishdate', 'ticket_type']


# class SearchForm(forms.Form):
#     query = forms.CharField(label='Search', max_length=100)


class TourSearchForm(forms.Form):
    firstdistination = forms.CharField(required=False, max_length=255, label='مبدا')
    lastDistination = forms.CharField(required=False, max_length=255, label='مقصد')

    startdate = forms.DateField(required=False, label='تاریخ رفت', widget=forms.SelectDateWidget())
    finishdate = forms.DateField(required=False, label='تاریخ برگشت', widget=forms.SelectDateWidget())