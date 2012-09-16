from django.forms import ModelForm

from .models import CheckRequest

class CheckRequestForm(ModelForm):
    class Meta:
        model = CheckRequest
        exclude = ('filer', 'club', 'year', 'approved', 'date_approved', 'reason_denied')
