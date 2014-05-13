from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.template import Context
from django.template.loader import get_template
import sys
from ASHMC.main.models import Semester
from ASHMC.roster.models import UserRoom
from ASHMC.vote.models import Measure, Vote, User

from datetime import datetime, timedelta
from optparse import make_option


class Command(BaseCommand):
    args = '(<measure_id>)*'
    help = 'sends a reminder email to users to vote'

    option_list = BaseCommand.option_list + (
        make_option(
            '--dry-run',
            action='store_true',
            dest='dry_run',
            default=False,
            help='Don\'t actually send any emails.',
        ),
    )

    def handle(self, *args, **options):
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

        for user in User.objects.filter(is_active=True, is_superuser=False):
            this_sem = Semester.get_this_semester()
            try:
                room = UserRoom.objects.get(
                    user=user,
                    semesters__id=this_sem.id,
                    room__dorm__official_dorm=True,
                ).room

            except UserRoom.DoesNotExist:
                # So they don't have an official dorm room
                # that means they should be abroad.

                try:
                    room = UserRoom.objects.get(
                        user=user,
                        semesters__id=this_sem.id,
                        room__dorm__code="ABR",
                    ).room
                except UserRoom.DoesNotExist:
                    continue

            # only send emails to people who haven't voted in
            # this measure
            try:
                delinquent_measures = measures.exclude(
                    Q(id__in=Vote.objects.filter(account=user).values_list('measure__id', flat=True)),
                    ).filter(
                    Q(restrictions__dorms=room.dorm) | Q(restrictions__dorms=None),
                    Q(restrictions__gradyears=user.student.class_of) | Q(restrictions__gradyears=None),
                    ).exclude(
                        banned_accounts__id__exact=user.id,
                        )
            except:
                print user.username + " caused an exception:", sys.exc_info()[0]
                print "(S)He probably doesn't have a student object somehow"

            if not delinquent_measures.exists():
                continue

            htmly = get_template("vote/reminder_email.html")
            plaintext = get_template("vote/reminder_email.txt")
            d = Context({'user': user, 'measures': delinquent_measures})
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
            if not options.get('dry_run'):
                msg.send()

            print "sent reminder email to", user.id, "about", [m.id for m in delinquent_measures]
