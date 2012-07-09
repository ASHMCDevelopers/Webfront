from django.template import Library

from ..models import Entry

from BeautifulSoup import BeautifulSoup

register = Library()


@register.filter
def has_been_updated(post):
    """Determines whether a post has been updated since being published.

    Return code indicates the 'severity' of update:
        1 - updated after a day-break
        2 - updated after an hour-break
        3 - updated after 15 minutes
        4 - updated within 15 minutes
        5 - not updated
    """
    # TODO: Make these return codes an ENUM somewhere.
    pubdate = post.start_publication
    updated = post.last_update

    if ((pubdate.month, pubdate.day, pubdate.year) !=
        (updated.month, updated.day, updated.year)):
        return 1

    elif pubdate.hour != updated.hour:
        return 2

    elif pubdate.minute < updated.minute - 15:
        return 3

    elif pubdate.minute != updated.minute - 15:
        return 5

    return 4


@register.filter
def naive_excerpt(post):
    assert isinstance(post, Entry), "{} is not an instance of Entry".format(post)

    soup = BeautifulSoup(post.html_content)

    return soup.find('p')
