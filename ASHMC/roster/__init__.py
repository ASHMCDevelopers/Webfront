from django.conf import settings

from django_auth_ldap.backend import populate_user

from ASHMC.main.models import Campus, GradYear, Semester, Student
from .models import Dorm, DormRoom, UserRoom

import xlrd


def create_user_related_things(*args, **kwargs):
    if 'user' not in kwargs or 'ldap_user' not in kwargs:
        return

    new_user = kwargs['user']
    print new_user, new_user.email
    # don't repopulate if we've already done the dance.
    if Student.objects.filter(user=new_user).count():
        return

    if settings.DEBUG:
        print "Creating user-related things..."
    try:
        this_sem = Semester.get_this_semester()
        workbook = xlrd.open_workbook(settings.ROSTER_DIRECTORY + "{}.xlsx".format(
            this_sem.verbose_unicode()
        ))
    except IOError:
        if settings.DEBUG:
            print "Couldn't open workbook {}".format(this_sem.verbose_unicode())
        return

    s = workbook.sheets()[0]

    # On what row does the actual information start?
    ROSTER_ROW_START = settings.ROSTER_ROW_START

    # TODO: make this more programmatic?
    FIELD_ORDERING = settings.ROSTER_FIELD_ORDERING

    senior = GradYear.senior_class(
        sem=this_sem,
    ).year
    if settings.DEBUG:
        print "\tsenior year:", senior
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

        if row[FIELD_ORDERING.index('Email')].value != new_user.email:
            if settings.DEBUG:
                print "\tSkipping row", r, row[FIELD_ORDERING.index('Email')].value
            continue

        if settings.DEBUG:
            print "\tFound relevant row."

        year = CLASS_TO_GRADYEAR[row[FIELD_ORDERING.index('Class')].value]

        gradyear, _ = GradYear.objects.get_or_create(
            year=year,
        )

        hmc = Campus.objects.get(code='HM')

        studentid = int(row[FIELD_ORDERING.index('ID')].value),
        studentid = None
        new_student, _ = Student.objects.get_or_create(
            user=new_user,
            class_of=gradyear,
            at=hmc,
            studentid=studentid,
            phonenumber=row[FIELD_ORDERING.index('Phone')].value,
            #birthdate=datetime.datetime.strptime(row[FIELD_ORDERING.index('Birthdate')].value, '%b %d, %Y').date(),
        )

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

            ur.semesters.add(this_sem)

        return
populate_user.connect(create_user_related_things)
