from django.contrib.sessions.models import Session
from django.contrib.auth.models import User

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    args = '<sessionid>'
    help = 'Identifies the user associated with a certain sessionid'

    def handle(self, *args, **kwargs):
        if len(args) != 1:
            raise CommandError("Just the sessionid, please")

        session_key = args[0]
        try:
            session = Session.objects.get(session_key=session_key)
        except ObjectDoesNotExist:
            print "no such session"
            return

        uid = session.get_decoded().get('_auth_user_id')
        user = User.objects.get(pk=uid)

        print user.username, user.get_full_name(), user.email
