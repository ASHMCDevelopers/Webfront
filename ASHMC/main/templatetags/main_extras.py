from django import template
from django.utils.safestring import mark_safe

import feedparser

from ..models import ASHMCRole, DormPresident, DormRole, DormAppointment, ASHMCAppointment, Semester
from ASHMC.roster.models import UserRoom, TransientSuiteMembership

import random
import re
import datetime


register = template.Library()


@register.filter
def maximum(iterable):
    return max(iterable)


@register.filter
def current_roles(user, type=None):
    if type is None:
        return []

    sem = Semester.get_this_semester()

    if type == 'ashmc':
        return sorted(
        [x.role for x in ASHMCAppointment.objects.filter(
            user=user,
            semesters__id=sem.id
        )])

    elif type == 'dorm':
        return sorted(
        [x.dorm_role for x in DormAppointment.objects.filter(
            user=user,
            semesters__id=sem.id,
        )]
        )

    return []


@register.filter
def get_living_situation(user):
    sem = Semester.get_this_semester()
    try:
        room = UserRoom.objects.get(
            user=user,
            semesters__id=sem.id,
        )
    except:
        return ""

    return room


@register.filter
def current_suites(user, type="transient"):
    sem = Semester.get_this_semester()

    room = UserRoom.objects.get(
        user=user,
        semesters__id=sem.id,
    )

    if type == 'dorm':
        if room.room.suite:
            suites = [room.room.suite]
        else:
            suites = []
        return suites

    elif type == 'transient':
        tsms = TransientSuiteMembership.objects.filter(
            user=user,
            semesters__id=sem.id,
        )
        return [tsm.tsuite for tsm in tsms]

    return []


@register.filter
def split(str, splitter):
    return str.split(splitter)


@register.filter
def is_today(value):
    assert isinstance(value, datetime.date)
    now = datetime.datetime.now()
    return (
        value.day == now.day and
        value.month == now.month and
        value.year == now.year
        )


@register.filter
def prettify_error_listings(form):
    errordict = form.errors
    print "errordict ", errordict

    response = """<ul class='errors'>"""

    response += '\n'.join(["""<li>{}</li>""".format(e) for e in errordict.pop('__all__', [])])

    for key, values in errordict.iteritems():
        if key != "__all__":
            response += """<li class='fielderror'>"""
            response += """{}:<ul>""".format(key)

        for error in values:
            response += """<li>{}</li>""".format(error)

        if key != "__all__":
            response += """</ul>"""
            response += """</li>"""

    response += """</ul>"""

    return mark_safe(response)


@register.filter
def shorten_role(role):
    return role


@register.filter
def order_by(qset, ordering):
    return qset.order_by(ordering)


@register.filter
def council_ordered(dictionary):
    try:
        return sorted(dictionary.iteritems(), key=lambda (x, y): ASHMCRole.COUNCIL_MAIN.index(x))
    except ValueError:
        try:
            return sorted(dictionary.iteritems(), key=lambda (x, y): ASHMCRole.COUNCIL_ADDITIONAL.index(x))
        except ValueError:
            try:
                return sorted(dictionary.iteritems(), key=lambda (x, y): ASHMCRole.COUNCIL_APPOINTED.index(x))
            except ValueError:
                return dictionary


@register.filter
def current_presidents(dorm):
    president_roles = DormPresident.objects.filter(dorm=dorm)
    this_sem = Semester.get_this_semester()
    current_appointments = ASHMCAppointment.objects.filter(
        role__in=president_roles,
        semesters__id=this_sem.id,
    )

    return current_appointments


@register.filter
def current_appointments(role):
    this_sem = Semester.get_this_semester()
    if isinstance(role, ASHMCRole):
        return ASHMCAppointment.objects.filter(role=role, semesters__id=this_sem.id)
    elif isinstance(role, DormRole):
        return DormAppointment.objects.filter(dorm_role=role, semesters__id=this_sem.id)
    else:
        return []


class RssParserNode(template.Node):
    def __init__(self, var_name, url=None, url_var_name=None):
        self.url = url
        self.url_var_name = url_var_name
        self.var_name = var_name

    def render(self, context):
        if self.url:
            context[self.var_name] = feedparser.parse(self.url)
        else:
            try:
                context[self.var_name] = feedparser.parse(context[self.url_var_name])
            except KeyError:
                raise template.TemplateSyntaxError, "the variable \"%s\" can't be found in the context" % self.url_var_name
        return ''


@register.tag(name="get_rss")
def get_rss(parser, token):
    # This version uses a regular expression to parse tag contents.
    try:
        # Splitting by None == splitting by spaces.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires arguments" % token.contents.split()[0]

    m = re.search(r'(.*?) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%r tag had invalid arguments" % tag_name
    url, var_name = m.groups()

    if url[0] == url[-1] and url[0] in ('"', "'"):
        return RssParserNode(var_name, url=url[1:-1])
    else:
        return RssParserNode(var_name, url_var_name=url)

"""
example usage:

{% load cache %}
{% load rss %}

{% cache 500 rss_display %}
    {% get_rss "http://www.freesound.org/blog/?feed=rss2" as rss %}
    {% for entry in rss.entries %}
        <h1>{{entry.title}}</h1>
        <p>
            {{entry.summary|safe}}
        </p>
        <p>
            <a href="{{entry.link}}">read more...</a>
        </p>
    {% endfor %}
{% endcache %}
"""


class RandomGreetingNode(template.Node):
    GREETING_CHOICES = (
        "Welcome, ",
        "Hi there, ",
        "Hello, ",
        "Greetings, ",
        "Salutations, ",
        "Salve, ",
    )

    def render(self, context):
        return random.choice(self.GREETING_CHOICES)


@register.tag(name='greeting')
def greeting(parser, token):
    tag_name = token.contents.split(None, 1)
    if isinstance(tag_name, tuple):
        raise template.TemplateSyntaxError, "%r tag takes no arguments" % token.contents.split()[0]

    return RandomGreetingNode()
