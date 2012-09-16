from django import template
from ASHMC.treasury.models import SchoolYear

register = template.Library()

@register.simple_tag
def school_year():
    return str(SchoolYear.get_current())
