from django import template

import calendar
import datetime
import pytz

register = template.Library()


@register.filter
def date_presenter(datet):
    now = datetime.datetime.now(pytz.utc)

    if datet - now < datetime.timedelta(days=1):
        return datet.strftime("%H:%M")

    return datet.strftime("%h %d")


@register.filter
def calendarize(date):
    return calendar.monthcalendar(date.year, date.month)
