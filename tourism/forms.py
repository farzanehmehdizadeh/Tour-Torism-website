from django import forms
from .models import tourism


class tourismform(forms.ModelForm):
    class Meta:
        model = tourism
        fields = ['title_tourism','firstdistination_tourism','capacity_tourism', 'image_tourism', 'startdate_tourism', 'price_tourism', 'ticket_typetourism', ]


# class SearchForm(forms.Form):
#     query = forms.CharField(label='Search', max_length=100)


class TourismSearchForm(forms.Form):
    firstdistination_tourism = forms.CharField(required=False, max_length=255, label='مبدا')
    # lastDistination = forms.CharField(required=False, max_length=255, label='مقصد')
    #
    # startdate = forms.DateField(required=False, label='تاریخ رفت', widget=forms.SelectDateWidget())
    # finishdate = forms.DateField(required=False, label='تاریخ برگشت', widget=forms.SelectDateWidget())