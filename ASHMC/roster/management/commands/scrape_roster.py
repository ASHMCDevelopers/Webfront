from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

from ASHMC.main.models import Campus, GradYear, Semester, Student
from ...models import DormRoom, UserRoom, Dorm

import datetime
import xlrd


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
        ROSTER_ROW_START = 3

        # TODO: make this more programmatic?
        FIELD_ORDERING = [
            'ID',
            'Fullname',
            'Nickname',
            'Class',
            'Dorm',
            'Room',
            'Phonenumber',
            'Email Address',
        ]
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

        for r in xrange(ROSTER_ROW_START, s.nrows):
            row = s.row(r)

            year = CLASS_TO_GRADYEAR[row[FIELD_ORDERING.index('Class')].value]

            if year < GradYear.senior_class().year and not kwargs['old_data']:
                continue

            gradyear, _ = GradYear.objects.get_or_create(
                year=year,
            )
            print row

            hmc = Campus.objects.get(code='HM')

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

            new_student.middle_name = middle_name,
            new_student.temp_pass = temp_password,

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
