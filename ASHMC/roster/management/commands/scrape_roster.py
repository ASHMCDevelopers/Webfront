from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

from ASHMC.main.models import Campus, GradYear, Semester, Student
from ...models import DormRoom, UserRoom, Dorm

import datetime
import ldap
import xlrd


"""

LDAP gives us a list of the following dicts:

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

search using:
l = ldap.initialize()
l.bind_s()
results = l.search_s("OU=Academic Students,DC=HMC,DC=EDU", ldap.SCOPE_SUBTREE, filterstr="(mail={})".format(
        student_email_from_roster
    )
)

"""


class Command(BaseCommand):
    args = '<path_to_roster_file>'
    help = 'Scrapes a roster to add entires to the database - creates both a User and a Student object for them. '

    option_list = BaseCommand.option_list + (
        make_option('--year',
            action='store',
            dest='year',
            default=datetime.date.today().year,
            help='The year this roster is for.',
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
            help="*don't* ignore students who have already graduated.",
        ),
    )

    def handle(self, *args, **kwargs):
        if len(args) != 1:
            raise CommandError("This command accepts only one argument")

        try:
            workbook = xlrd.open_workbook(args[0])
        except IOError:
            raise CommandError("Couldn't open workbook: {}".format(args[0]))

        s = workbook.sheets()[0]

        # On what row does the actual information start?
        ROSTER_ROW_START = settings.ROSTER_ROW_START

        # TODO: make this more programmatic?
        FIELD_ORDERING = settings.ROSTER_FIELD_ORDERING

        senior = GradYear.senior_class(
            sem=Semester.objects.get(half=kwargs['semester'], year=kwargs['year'])
        ).year
        CLASS_TO_GRADYEAR = {
            'FE': senior + 3,
            'FF': senior + 3,
            'FR': senior + 3,
            'SO': senior + 2,
            'JR': senior + 1,
            'SR': senior,
        }

        hmc = Campus.objects.get(code='HM')
        for r in xrange(ROSTER_ROW_START, s.nrows):
            row = s.row(r)

            year = CLASS_TO_GRADYEAR[row[FIELD_ORDERING.index('Class')].value]

            if year < GradYear.senior_class().year and not kwargs['old_data']:
                continue

            gradyear, _ = GradYear.objects.get_or_create(
                year=year,
            )
            print row


            fullname = row[FIELD_ORDERING.index('Fullname')].value
            l_f_m_name = fullname.split(', ')
            last_name = l_f_m_name[0]
            f_m_name = ', '.join(l_f_m_name[1:]).split(' ')
            first_name = f_m_name[0]
            middle_name = ''

            temp_password = User.objects.make_random_password()

            try:
                new_user = User.objects.get(email=row[FIELD_ORDERING.index('Email Address')].value.lower().replace('hmc.edu', 'g.hmc.edu'))
            except ObjectDoesNotExist:
                new_user = User.objects.create_user(
                    username=row[FIELD_ORDERING.index('Email Address')].value.lower().replace('hmc.edu', 'g.hmc.edu'),
                    email=row[FIELD_ORDERING.index('Email Address')].value.lower().replace('hmc.edu', 'g.hmc.edu'),
                    password=temp_password,
                )

            new_user.first_name = first_name
            new_user.last_name = last_name

            new_user.save()
            studentid = int(row[FIELD_ORDERING.index('ID')].value),
            studentid = None
            new_student, _ = Student.objects.get_or_create(
                user=new_user,
                class_of=gradyear,
                at=hmc,
                studentid=studentid,
            )

            new_student.middle_name = middle_name
            new_student.temp_pass = temp_password

            new_student.save()

            dormname = row[FIELD_ORDERING.index('Dorm')].value.split(' ')

            if dormname[0] != '':
                if dormname[0] == "CGU":
                    dormname = ' '.join(dormname)
                else:
                    dormname = dormname[0]

                dorm = Dorm.objects.get(name__startswith=dormname)

                room, _ = DormRoom.objects.get_or_create(
                    dorm=dorm,
                    number=row[FIELD_ORDERING.index("Room")].value,
                )

                ur, _ = UserRoom.objects.get_or_create(
                    user=new_user,
                    room=room,
                )

                ur.semesters.add(Semester.objects.get(half=kwargs['semester'], year=int(kwargs['year'])))
