from django.db.models.signals import post_save
from django.contrib.sites.models import Site
from django.conf import settings

from blogger.models import Entry, User, new_entry, entry_updated

def send_tweet_after_new_entry(sender, **kwargs):
    """Sends a tweet with an entry's title and the author's name,
    along with a link."""
    assert kwargs.has_key('entry_id')
    assert kwargs.has_key('author_id')



    entry = Entry.objects.get(pk=kwargs['entry_id'])
    author = User.objects.get(pk=kwargs['author_id'])

    tweet_body = """New story from {}: {} http://{}{}""".format(
        author.first_name,
        entry.title,
        Site.objects.get_current().domain,
        entry.get_absolute_url(),
    )

    settings.TWITTER_AGENT.statuses.update(status=tweet_body)

new_entry.connect(send_tweet_after_new_entry,dispatch_uid="canonical_entry_tweet")
