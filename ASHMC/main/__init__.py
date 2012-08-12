from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.conf import settings
from django.db.models.signals import post_save

from blogger.models import Entry

from .models import TopNewsItem

from urllib2 import URLError


def send_tweet_after_new_entry(sender, **kwargs):
    """Sends a tweet with an entry's title and the author's name,
    along with a link."""

    # Don't do anything if it's not a new entry.
    if 'created' in kwargs and not kwargs['created']:
        return

    instance = kwargs['instance']

    tweet_body = """New story from {}: {} http://{}{}""".format(
        instance.primary_author.first_name,
        instance.title,
        Site.objects.get_current().domain,
        instance.get_absolute_url(),
    )

    try:
        settings.TWITTER_AGENT.statuses.update(status=tweet_body)
    except URLError:
        pass

post_save.connect(send_tweet_after_new_entry, sender=Entry)


def send_tweet_after_top_story(sender, **kwargs):
    """Sends a tweet after a top story about a top story."""

    if 'created' in kwargs and not kwargs['created']:
        return

    instance = kwargs['instance']

    tweet_body = """Top News from ASHMC: {}""".format(
        instance.slug,
    )

    try:
        settings.TWITTER_AGENT.statuses.update(status=tweet_body)
    except URLError:
        pass

post_save.connect(send_tweet_after_top_story, sender=TopNewsItem)


def create_welcoming_blog_post(sender, **kwargs):
    if Entry.objects.count() > 0:
        return

    Entry.objects.create(
        tags="welcome",
        title="Welcome to ASHMC",
        slug="welcome-to-ashmc",
        comment_enabled=False,
        primary_author=User.objects.all()[0],
        content="""
Welcome to the new and improved ASHMC presence.

Here, you'll find lots of useful tools for interacting with the student body;
these range from easy-to-setup
        """,
    )
