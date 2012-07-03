from django import forms
from django.db.models import Count


from .models import *
from .fields.form import CampusChoiceField, DayChoiceField, AreaChoiceField
from .fields.widgets import ColumnCheckboxSelectMultiple

TIME_INPUT_FORMATS = (
    '%H:%M',
    '%H:%M',
    '%I:%M%p',
    '%I:%M %p',
)

class CourseSearch(forms.Form):
    title = forms.CharField(required=False, label="called ",
                            widget=forms.TextInput(
                                                   attrs={'placeholder':'i.e., programming'}
                                                   ))
    
    campus = CampusChoiceField(queryset=Campus.objects.exclude(code__in=Campus.ABSTRACTIONS), 
                                       required=False, 
                                       widget=ColumnCheckboxSelectMultiple(css_class="campus_selection",
                                                                           columns=4))
    
    numberlow = forms.IntegerField(required=False, 
                                   label="numbered above", 
                                   min_value=-1,
                                   max_value=999,
                                   widget=forms.TextInput(
                                                          attrs={'class':'numericfield',
                                                                 'maxlength':3,
                                                                 'placeholder':0}),)
    numberhigh = forms.IntegerField(required=False, 
                                    label="numbered below", 
                                    min_value=-1,
                                    max_value=999,
                                    widget=forms.TextInput(
                                                          attrs={'class':'numericfield',
                                                                 'maxlength':3,
                                                                 'placeholder':999}),)
    
    code = forms.CharField(required=False,
                           widget=forms.TextInput(
                                                  attrs={'placeholder':'i.e., CSCI005GL',
                                                         'maxlength':9}
                                                  ))
    timestart = forms.TimeField(input_formats=TIME_INPUT_FORMATS,
                                widget=forms.TextInput(attrs={'class':'timefield',
                                                              'placeholder':'i.e., 9:30 am'}),
                                required=False,
                                help_text="ex: 10:00 am")
    
    timeend = forms.TimeField(input_formats=TIME_INPUT_FORMATS, 
                              widget=forms.TextInput(attrs={'class':'timefield',
                                                            'placeholder':'i.e., 13:15'}),
                              required=False,
                              help_text="ex: 10:00 am")
    
    day_limit = forms.ChoiceField(choices=(('incl','at least'),
                                           ('excl','only'),
                                           ('negl','not')),
                                  required=False)
    
    days = DayChoiceField(queryset=Day.objects.all(), 
                                     required=False, 
                                     widget=forms.CheckboxSelectMultiple)
    
    professors = forms.ModelChoiceField(queryset=Professor.objects\
                                                            .exclude(first_name=None)\
                                                            .exclude(last_name=None)\
                                                            .order_by('last_name'),
                                        required=False,
                                        empty_label="(any)")
    
    department = AreaChoiceField(
                   queryset=CourseArea.objects.annotate(course_count=Count('course'))\
                                              .filter(course_count__gte=1,
                                                      )\
                                              .exclude(is_req_area=True)\
                                              .order_by('code'),
                   required=False, empty_label="(any)")
    
    only_open = forms.BooleanField(required=False,
                                   widget=forms.CheckboxInput(
                                                                attrs={'checked':True}
                                                             ))
    pf_able = forms.BooleanField(required=False,
                                 widget=forms.CheckboxInput(
                                                            attrs={'checked':True}
                                                            ))
    not_taken = forms.BooleanField(required=False,
                                   widget=forms.CheckboxInput(
                                                              attrs={'checked':True}))
    in_reach = forms.BooleanField(required=False,
                                  #widget=forms.CheckboxInput()
                                  )
    writ_intense_only = forms.BooleanField(required=False,)
    
    interest_min = forms.ChoiceField(choices=range(0, 11), required=False)
    difficult_max = forms.ChoiceField(choices=range(0, 11), required=False)