from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.forms.widgets import RadioSelect

from .models import CheckRequest, BudgetRequest, BudgetItem

class CheckRequestForm(ModelForm):
    class Meta:
        model = CheckRequest
        exclude = ('filer', 'club', 'year', 'approved', 'date_approved', 'reason_denied')
        widgets = {'request_type': RadioSelect}

class BudgetRequestForm(ModelForm):
    class Meta:
        model = BudgetRequest
        exclude = ('club', 'date_filed', 'approved', 'date_approved',
                   'amount_allocated', 'filer')
        widgets = {'attended_budgeting_for': RadioSelect}

BudgetItemFormSet = inlineformset_factory(BudgetRequest, BudgetItem)
