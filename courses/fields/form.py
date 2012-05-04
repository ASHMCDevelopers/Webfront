'''
Created on Apr 27, 2012

@author: Haak Saxberg
'''
from django import forms

class AreaChoiceField(forms.ModelChoiceField):
    def label_from_instance(self,obj):
        return "{} - {}".format(obj.code, obj.name)

class CampusChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return "{}".format(obj.code)

class DayChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return "{}".format(obj.code)
