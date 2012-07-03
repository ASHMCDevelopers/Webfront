'''
Created on May 2, 2012

@author: Haak Saxberg
'''
from django import template
from django.utils.safestring import mark_safe
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.db.models.query import QuerySet

register = template.Library()

from ..models import RoomInfo, Timeslot, Campus, Room, Major,\
                    Enrollment, Student

@register.filter
def clean_sections(value, qex=None):
    """
    Does a bit of extra filtering that is awkward to do as part of the view function.
    
    Expects a QS of :model:`courses.Section` as its ``value``; the optional keyword argument ``qex`` is
    expected (but NOT CHECKED) to be a ``Q`` expression. If ``qex`` is provided, it's used to
    perform a preparatory filter on ``value``, before the cleaning.
    """
    if qex:
        value = value.filter(qex)
    return value.filter(meeting__needs_attention=False)


@register.filter
def get_room(value, timeslottuple):
    """
    Finds the :model:`courses.RoomInfo` for a give :model:`courses.Meeting` and 
    :model:`courses.Timeslot`.
    
    ``value`` is expected to be the ``Meeting`` and it requires a second argument, ``timeslottuple``
    which should be a tuple (_,_,_, :model:`courses.Timeslot`)---much like the output of Meeting.get_timeslot_tuples().
    
    """
    if len(timeslottuple) < 3:
        return "TBA"
    ri = RoomInfo.objects.get(meeting=value,
                                timeslot=timeslottuple[3])
    return ri

@register.filter
def prettify(value, flag=None):
    """
    Creates pretty (specialized) output for ``value``, depending its type:
    
    =========================  ====================================================================
    Model                      Output
    =========================  ====================================================================
    :model:`courses.Campus`    ``<span class="colored {{Campus.code}}">{{campus.code}}</span>``
    :model:`courses.Room`      Decides whether to prepend the title of ``value`` with "Room" or not, depending on which building the room is in.
    :model:`courses.RoomInfo`  Prints building name and room of ``value``, leveraging pretty(Room).
    QuerySet                   See below.
    =========================  ====================================================================
    
    ``prettify`` also accepts a kwarg, ``flag``, which defaults to none. This flag is used to determine
    the output format of a QuerySet. currently, the flags supported are
    
    * "``instructor``": Used to print a QS of instructors in "last, first" format.
        
    If no flag is specified, ``prettify`` simply joins the elements of the QuerySet with ``", "``.
    """
    
    if isinstance(value, Campus):
        ret = "<span class=\"colored {}\">{}</span>".format(value.code, value.code)
    elif isinstance(value, Room):
        if value.building.code not in ['LAC','TIER','DU']:
            ret = "Room {}a".format(value.title)
        else:
            if value.title: ret = value.title
            else: ret = "TBD"
    elif isinstance(value, RoomInfo):
        if value.room.building.code in ['ARR', 'TBA']:
            ret = '{}'.format(value.room.building.name)
        else:
            ret = "{}, {}".format(value.room.building.name, 
                              prettify(value.room)) # yeahhh recursion
    elif isinstance(value, QuerySet):
        if flag == None:
            ret = ', '.join(value)
        elif flag == 'instructors':
            ret = []
            for tup in value:
                if not tup[1]:
                    ret += ["{}".format(tup[0])]
                else:
                    ret += ["{}, {}".format(tup[0],
                                        tup[1])]
            ret = '; '.join(ret)
    else:
        ret = "??"

    return mark_safe(ret)
prettify.is_safe = True

@register.filter
def make_nbsp(value):
    """
    A very naive string-replacement wrapper; simply performs ``value.replace(' ', '&nbsp')``.
    """
    ret = value.replace(' ', '&nbsp;')
    return mark_safe(ret)
make_nbsp.is_safe = True

@register.filter
def has_taken(value, course):
    """
    Returns ``True`` if value (an instance of :model:`courses.Student` or ``User``) has taken ``course`` (an
    instance of :model:`courses.Course`.
    """
    if not isinstance(value, Student):
        try: value = value.student_profile
        except AttributeError: return False # AnonymousUser
        
    return Enrollment.objects.filter(student=value)\
                            .filter(section__course=course) > 0


@register.filter
def get_next_page_count(value):
    """
    Expects ``value`` to be an instance of ``Paginator.Page``.
    
    Returns the number of items on the next page, if any; does not check
    for the existence of the next page. 
    """
    p = value.paginator.page(value.next_page_number())
    
    return p.end_index() - p.start_index() + 1

@register.filter
def get_hidden_store(value):
    """
    Expects a :model:`courses.Section` instance as ``value``.
    
    Returns the hiddenstore form for use in adding things to schedules.
    """
    return "??"

@register.filter
def replace_space(value, new):
    return value.replace(' ', new)

@register.tag
def create_major_divs(parser,token):
    
    try:
        tag_name, = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r takes no arguments" % token.contents.split()[0])
    
    return CreateMajorDivs()

@register.filter
def prereq_order(value):
    return value.annotate(num_prereqs=Count('prerequisites')).order_by('num_prereqs')

class CreateMajorDivs(template.Node):
    def __init__(self):
        self.majors = Major.objects.filter(primary_campus__code="HM").exclude(title='Core')
        
    
    def render(self, context):
        t = template.loader.get_template("major_track.html")
        return t.render(template.Context({'majors':self.majors},autoescape=context.autoescape))
                
                
    