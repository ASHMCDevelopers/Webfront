from django.db.models.signals import post_save
from django.contrib.sites.models import Site
from django.conf import settings

from blogger.models import Entry

from .models import TopNewsItem


def send_tweet_after_new_entry(sender, **kwargs):
    """Sends a tweet with an entry's title and the author's name,
    along with a link."""

    # Don't do anything if it's not a new entry.
    if 'created' in kwargs and not kwargs['created']:
        return

    instance = kwargs['instance']

    tweet_body = """New story from {}: {} http://{}{}""".format(
        instance.author.first_name,
        instance.title,
        Site.objects.get_current().domain,
        instance.get_absolute_url(),
    )

    settings.TWITTER_AGENT.statuses.update(status=tweet_body)

post_save.connect(send_tweet_after_new_entry, sender=Entry)


def send_tweet_after_top_story(sender, **kwargs):
    """Sends a tweet after a top story about a top story."""

    if 'created' in kwargs and not kwargs['created']:
        return

    instance = kwargs['instance']

    tweet_body = """Top News from ASHMC: {}""".format(
        instance.slug,
    )

    settings.TWITTER_AGENT.statuses.update(status=tweet_body)

post_save.connect(send_tweet_after_top_story, sender=TopNewsItem)
