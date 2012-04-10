from django import forms
from .models import *

class CourseSearch(forms.Form):
    title = forms.CharField(required=False, label="called ")
    
    campus = forms.ModelMultipleChoiceField(queryset=Campus.objects.all(), 
                                       required=False, 
                                       widget=forms.CheckboxSelectMultiple)
    
    numberlow = forms.IntegerField(required=False, 
                                   label="numbered above", 
                                   min_value=0,
                                   max_value=999,
                                   widget=forms.TextInput(
                                                          attrs={'class':'numericfield',
                                                                 'maxlength':3,
                                                                 'placeholder':0}),)
    numberhigh = forms.IntegerField(required=False, 
                                    label="numbered below", 
                                    min_value=0,
                                    max_value=999,
                                    widget=forms.TextInput(
                                                          attrs={'class':'numericfield',
                                                                 'maxlength':3,
                                                                 'placeholder':999}),)
    
    code = forms.CharField(required=False)
    timestart = forms.TimeField(input_formats="%H:%M",
                                widget=forms.TextInput(attrs={'class':'timefield'}))
    
    timeend = forms.TimeField(input_formats="%H:%M", 
                              widget=forms.TextInput(attrs={'class':'timefield'}))
    
    day_limit = forms.ChoiceField(choices=(('incl','at least'),('excl','only')))
    
    days = forms.MultipleChoiceField(choices=DAY_CHOICES, 
                                     required=False, 
                                     widget=forms.CheckboxSelectMultiple)
    
    professors = forms.ModelMultipleChoiceField(queryset=Professor.objects.all())
    
    department = forms.ChoiceField(choices=Department.flat_listing(for_form=True),
                                   required=False)
    
    only_open = forms.BooleanField(required=False,
                                   widget=forms.CheckboxInput(
                                                                attrs={'checked':'True'}
                                                             ))