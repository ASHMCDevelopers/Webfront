from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

from ASHMC.main.models import Campus, GradYear, Semester, Student
from ...models import DormRoom, UserRoom, Dorm

import datetime
import ldap
import logging
import xlrd


logger = logging.getLogger(__name__)


"""
LDAP gives us a list of the following things:

[
('CN=Bryan J Visser,OU=HMC_2013,OU=Academic Students,DC=HMC,DC=Edu',
  {'accountExpires': ['0'],
   'badPasswordTime': ['129925765252435691'],
   'badPwdCount': ['0'],
   'cn': ['Bryan J Visser'],
   'codePage': ['0'],
   'countryCode': ['0'],
   'dSCorePropagationData': ['16010101000000.0Z'],
   'department': ['HMC_2013'],
   'description': ['HMC_2013'],
   'displayName': ['Bryan J Visser'],
   'distinguishedName': ['CN=Bryan J Visser,OU=HMC_2013,OU=Academic Students,DC=HMC,DC=Edu'],
   'employeeID': ['b44AY8Jy'],
   'givenName': ['Bryan'],
   'homeDirectory': ['\\\\hmc.edu\\hmcdfs\\HMC_2013\\bvisser'],
   'homeDrive': ['H:'],
   'instanceType': ['4'],
   'lastLogon': ['129925765338862461'],
   'lastLogonTimestamp': ['129922331557056934'],
   'lockoutTime': ['0'],
   'logonCount': ['1'],
   'logonHours': ['\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'],
   'mail': ['Bryan_Visser@HMC.Edu'],
   'memberOf': ['CN=PaperCutStudents,OU=Systems,OU=Groups,DC=HMC,DC=Edu',
    'CN=PaperCutUsers,OU=Systems,OU=Groups,DC=HMC,DC=Edu',
    'CN=Class2013,OU=StudentGroups,OU=Groups,DC=HMC,DC=Edu',
    'CN=Students,OU=StudentGroups,OU=Groups,DC=HMC,DC=Edu'],
   'name': ['Bryan J Visser'],
   'objectCategory': ['CN=Person,CN=Schema,CN=Configuration,DC=HMC,DC=Edu'],
   'objectClass': ['top', 'person', 'organizationalPerson', 'user'],
   'objectGUID': ['\xces\xea\xabe\x83\xe1C\xa6\x7f\xf9o\x94i\xab\xc0'],
   'objectSid': ['\x01\x05\x00\x00\x00\x00\x00\x05\x15\x00\x00\x00\x92\xe0<w.C\xac@\x82\x8b\xa6(\xf6E\x00\x00'],
   'primaryGroupID': ['513'],
   'pwdLastSet': ['129893587778284380'],
   'sAMAccountName': ['bvisser'],
   'sAMAccountType': ['805306368'],
   'sn': ['Visser'],
   'uSNChanged': ['1550653'],
   'uSNCreated': ['30068'],
   'userAccountControl': ['66048'],
   'userPrincipalName': ['bvisser@HMC.Edu'],
   'whenChanged': ['20120916013915.0Z'],
   'whenCreated': ['20090825233010.0Z']}),
]
"""


class Command(BaseCommand):
    args = '<path_to_roster_file>'
    help = 'Scrapes a roster to add entires to the database - creates both a User and a Student object for them. '

    option_list = BaseCommand.option_list + (
        make_option('--year',
            action='store',
            dest='year',
            default=datetime.date.today().year,
            help='The year this roster is for',
        ),
        make_option('--semester-code',
            action='store',
            dest='semester',
            default='FA',
            help="The semester code this roster is for. [default: %default]",
        ),
        make_option('--include-old-things',
            action='store_true',
            dest='old_data',
            default=False,
            help="*don't* ignore students who have already graduated",
        ),
        make_option('--dryrun',
            action='store_true',
            dest='dryrun',
            default=False,
            help="Don't save changes",
        ),
    )

    def handle(self, *args, **kwargs):
        if len(args) != 1:
            raise CommandError("This command accepts only one argument")

        try:
            workbook = xlrd.open_workbook(args[0])
        except IOError:
            raise CommandError("Couldn't open roster: {}".format(args[0]))

        s = workbook.sheets()[0]

        # TODO: make this more programmatic?
        FIELD_ORDERING = settings.ROSTER_FIELD_ORDERING

        senior = GradYear.senior_class(
            sem=Semester.objects.get(half=kwargs['semester'], year=kwargs['year'])
        )
        logger.info("Senior year: %s", senior)
        CLASS_TO_GRADYEAR = {
            'FE': senior + 3,  # Freshmen have three codes
            'FF': senior + 3,
            'FR': senior + 3,
            'SO': senior + 2,
            'JR': senior + 1,
            'SR': senior,
        }

        # Initialize and bind to the LDAP connection
        lconn = ldap.initialize(
                uri=settings.AUTH_LDAP_SERVER_URI,
        )
        lconn.simple_bind_s(
            who=settings.AUTH_LDAP_BIND_DN,
            cred=settings.AUTH_LDAP_BIND_PASSWORD,
        )

        dryrun=kwargs['dryrun']
        # get hmc for easy access later
        hmc = Campus.objects.get(code='HM')

        if not dryrun: 
            this_sem, _ = Semester.objects.get_or_create(
                year=kwargs['year'],
                half=kwargs['semester'],
            )
        else:
            this_sem = Semester.objects.get(
                year=kwargs['year'],
                half=kwargs['semester'],
            )

        logger.info("Semester: %s", this_sem)

        active_users = []
        for r in xrange(settings.ROSTER_ROW_START, s.nrows):
            row = s.row(r)

            try:
                gradyear = CLASS_TO_GRADYEAR[row[FIELD_ORDERING.index('Class')].value]
            except KeyError:
                logger.error("%d No such class: %s", r, row[FIELD_ORDERING.index('Class')].value)
                continue

            # Skip people who've already graduated - we don't care about them
            if gradyear < CLASS_TO_GRADYEAR['SR'] and not kwargs['old_data']:
                continue

            email = row[FIELD_ORDERING.index('Email')].value
            try:
                new_user = User.objects.get(
                    email=email,
                )
                active_users += [new_user.id]
            except ObjectDoesNotExist:
                # Check LDAP for user
                student_results = lconn.search_s(
                    "OU=Academic Students,DC=HMC,DC=EDU", ldap.SCOPE_SUBTREE, filterstr="(mail={})".format(
                        email,
                    )
                )

                if len(student_results) < 1:
                    logger.error("%d Couldn't find user with email %s", r, email)
                    continue
                elif len(student_results) > 1:
                    logger.error("%d Multiple students matching email %s", r, email)
                    continue

                ldap_student = student_results[0][1]

                try:
                    new_user = User.objects.create_user(
                        username=ldap_student['sAMAccountName'][0],
                        email=email,
                    )
                except Exception:
                    new_user = User.objects.get(
                        username=ldap_student['sAMAccountName'][0],
                    )
                    # In case they were previously inactivated...
                    new_user.is_active = True

                new_user.first_name = ldap_student['givenName'][0]
                new_user.last_name = ldap_student['sn'][0]
                if not dryrun: new_user.save()
                # keep track of which users we HAVE seen this time through
                active_users += [new_user.id]
                
                if not dryrun: 
                    new_student, _ = Student.objects.get_or_create(
                        user=new_user,
                        class_of=gradyear,
                        at=hmc,
                        studentid=None,
                    )
                else: 
                    new_student = Student.objects.get(
                        user=new_user,
                        class_of=gradyear,
                        at=hmc,
                        studentid=None,
                    )

            dormcode = row[FIELD_ORDERING.index('Dorm')].value.split(' ')

            if dormcode[0] == '':
                logger.error("%d Couldn't match dormcode %s", r, dormcode)
                continue

            # Roster has CGUA, whereas DB has CGA.
            if dormcode[0].startswith("CGU"):
                dormcode = "CG{}".format(dormcode[0][-1])
            else:
                dormcode = dormcode[0]

            try:
                dorm = Dorm.all_objects.get(code__iexact=dormcode)
            except ObjectDoesNotExist:
                # If all else fails, see if there's a name match
                logger.warn("No such code %s - trying name match", dormcode)
                try:
                    dorm = Dorm.all_objects.get(name__istartswith=dormcode)
                except (ObjectDoesNotExist, MultipleObjectsReturned):
                    logger.error(
                        "{} ldap population failed for {} (on failed dorm lookup {}) - assuming OFF".format(r, new_user, dormcode),
                    )
                    dorm = Dorm.objects.get(code="OFF")

            if dorm.code == "OFF":
                room = DormRoom.objects.get(
                    dorm=dorm,
                    number="Symbolic Room",
                )

            else:
                number = row[FIELD_ORDERING.index("Room")].value,
                try:
                    number = int(number[0])
                except ValueError:
                    number = str(number[0]).encode('ascii')

                if not dryrun: 
                    room, _ = DormRoom.objects.get_or_create(
                        dorm=dorm,
                        number=number,
                    )
                else: room = DormRoom.objects.get(dorm=dorm, number=number,)

            if dorm.code in Dorm.all_objects.filter(official_dorm=False).values_list('code', flat=True)\
              and dorm.code != "ABR":
                # If they're off-campus, make sure they're 'symbollically'
                # a part of the Offcampus dorm for voting purposes.
                if not dryrun:
                    symoff, _ = DormRoom.objects.get_or_create(
                        dorm__code="OFF",
                        number="Symbolic Room",
                    )
                else: 
                    symoff = DormRoom.objects.get(
                        dorm__code="OFF",
                        number="Symbolic Room",
                    )
                # Symroom is going to be full of people.
                if not dryrun: 
                    symroomur, _ = UserRoom.objects.get_or_create(
                        user=new_user,
                        room=symoff,
                        )
                else: 
                    symroomur  = UserRoom.objects.get_or_create(
                        user=new_user,
                        room=symoff,
                        )
                if not dryrun: symroomur.semesters.add(this_sem)

                logger.info("Created symoblic room entry for %s", new_user)

            if not dryrun: 
                ur, _ = UserRoom.objects.get_or_create(
                user=new_user,
                room=room,
                )
            else: ur = UserRoom.objects.get(
                user=new_user, room=room, 
                )

            if not dryrun: ur.semesters.add(this_sem)

        # inactivate missing users - except the super.
        for user in User.objects.exclude(is_superuser=True).exclude(id__in=active_users):
            logger.info("Inactivating {}".format(user.username))
            user.is_active = False
            if not dryrun: user.save()
