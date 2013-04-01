from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template import Context
from django.template.loader import get_template

from vote.models import Measure, Vote

from datetime import datetime, timedelta


class Command(BaseCommand):
    args = '<sessionid>'
    help = 'Identifies the user associated with a certain sessionid'

    def handle(self, *args, **kwargs):
        if len(args) > 0:
            measure_ids = args
        else:
            measure_ids = None

        if measure_ids:
            measures = Measure.objects.filter(
                id__in=measure_ids,
            )
        else:
            measures = Measure.objects.exclude(
                vote_end__lte=datetime.today(),
            ).filter(
                is_open=True,
                vote_start__lte=datetime.today() - timedelta(days=5),
            )

        for measure in measures:
            for user in measure.eligible_voters:
                try:
                    # only send emails to people who haven't voted in
                    # this measure
                    Vote.objects.get(account=user, measure=measure)
                    continue
                except Vote.DoesNotExist:
                    pass

                htmly = get_template("vote/reminder_email.html")
                plaintext = get_template("vote/reminder_email.txt")
                d = Context({'user': user, 'measure': measure})
                subject = "A friendly ASHMC reminder"
                from_email = "automatic@ashmc.hmc.edu"
                to_email = user.email
                msg = EmailMultiAlternatives(
                    subject,
                    plaintext.render(d),
                    from_email,
                    [to_email],
                )
                msg.attach_alternative(htmly.render(d), "text/html")
                msg.send()

                print "sent reminder email to", user.id, "about", measure.id
