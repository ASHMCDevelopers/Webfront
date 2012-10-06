from django import template
from ASHMC.treasury.models import TreasuryYear

register = template.Library()

@register.simple_tag
def school_year():
    return str(TreasuryYear.objects.get_current())
