from django import template
from ASHMC.treasury.models import SchoolYear

register = template.Library()

@register.filter
def ledger_format(amount):
    if amount < 0:
        return "%.02f" % -amount
    else:
        return "(%.02f)" % amount

@register.filter
def amount_format(amount):
    if amount < 0:
        return "(%.02f)" % -amount
    else:
        return "%.02f" % amount

@register.filter
def amount_class(amount):
    if amount < 0:
        return 'inthered'
    else:
        return 'black'

@register.filter
def ledger_class(amount):
    if amount <= 0:
        return 'black'
    else:
        return 'inthered'
