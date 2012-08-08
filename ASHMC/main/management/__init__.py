from django.db.models.signals import post_save

from ASHMC.roster.models import Dorm
from ..models import Utility, Day, Semester, Building, GradYear, Campus, DormRole, DormPresident
from .. import models as features
from django.db.models import signals

import datetime

""" The following methods are attached to the post_syncdb signal
and are used to ensure that certain objects never need to be created
on the fly."""


def prepopulate_days(sender, **kwargs):
    """Creates the seven day objects"""
    if not 'verbosity' in kwargs:
        kwargs['verbosity'] = 0
    if kwargs['verbosity'] > 0:
        print "Creating days of the week..."
    for (code, name) in Day.DAY_CHOICES:
        if code not in ['T', 'W', 'R']:
            short = name[:3]
        elif code in ['T', 'R']:
            short = name[:-3]
        elif code == 'W':
            short = "Weds"
        if kwargs['verbosity'] > 1:
            print "\tCreating {}...".format(name)
        Day.objects.get_or_create(name=name,
                                  code=code,
                                  short=short)
signals.post_syncdb.connect(prepopulate_days, sender=features)


def prepopulate_semesters(sender, **kwargs):
    """Creates semesterly objects."""
    if not 'verbosity' in kwargs:
        kwargs['verbosity'] = 0
    if kwargs['verbosity'] > 0:
        print "Creating semester objects..."
    for year in range(datetime.datetime.now().year - 4, datetime.datetime.now().year + 2):
        fa, new = Semester.objects.get_or_create(year=year,
                                                 half='FA')
        sp, new = Semester.objects.get_or_create(year=year,
                                                 half='SP')
        sm, new = Semester.objects.get_or_create(year=year,
                                                 half='SM')

signals.post_syncdb.connect(prepopulate_semesters, sender=features)


def prepopulate_campuses(sender, **kwargs):
    """ Create objects for the campuses if they don't exist"""
    if not 'verbosity' in kwargs:
        kwargs['verbosity'] = 0
    for pair in Campus.CAMPUSES:
        if kwargs['verbosity'] > 0:
            print "Creating campus {}...".format(pair[0])
        c, new = Campus.objects.get_or_create(code=pair[0])
        c.title = pair[1]  # update title if necessary
        c.save()
signals.post_syncdb.connect(prepopulate_campuses, sender=features)


def prepopulate_buildings(sender, **kwargs):
    """Create objects for buildings automatically"""
    if not 'verbosity' in kwargs:
        kwargs['verbosity'] = 0
    for campus in Building.BUILDINGS:
        c = Campus.objects.get(code=campus[0])
        if kwargs['verbosity'] > 0:
            print "Creating buildings for campus: {}...".format(c)
        for building in campus[1]:
            if kwargs['verbosity'] > 1:
                print "\t Creating building: {}...".format(building[0]),
            b, new = Building.objects.get_or_create(campus=c,
                                           code=building[0])
            b.name = building[1]
            b.save()
            if kwargs['verbosity'] > 1:
                print 'done.'
signals.post_syncdb.connect(prepopulate_buildings, sender=features)


def prepopulate_gradyears(sender, **kwargs):
    """Create graduation years"""
    if not 'verbosity' in kwargs:
        kwargs['verbosity'] = 0
    if kwargs['verbosity'] > 0:
        print "Creating possible GradYears..."
    for year in Utility.possible_grad_years():
        if kwargs['verbosity'] > 1:
            print "\tCreating GradYear:{}...".format(year),
        y, new = GradYear.objects.get_or_create(year=year)
        if kwargs['verbosity'] > 1:
            print "done."
signals.post_syncdb.connect(prepopulate_gradyears, sender=features)


def create_official_dorm_roles(sender, **kwargs):
    dorm = kwargs['instance']
    if not 'verbosity' in kwargs:
        kwargs['verbosity'] = 0
    for title in DormRole.OFFICIAL_TITLES:
        if kwargs['verbosity'] > 0:
            print "\t {} - {}".format(dorm, title)

        dr, _ = DormRole.objects.get_or_create(
            dorm=dorm,
            title=title,
        )
post_save.connect(create_official_dorm_roles, sender=Dorm)


def create_dorm_presidents(sender, **kwargs):
    dorm = kwargs['instance']
    if not 'verbosity' in kwargs:
        kwargs['verbosity'] = 0
    if kwargs['verbosity'] > 0:
        print "Creating President for dorm {}".format(dorm)

    dp, _ = DormPresident.objects.get_or_create(
        dorm=dorm,
        title=" ",
    )
post_save.connect(create_dorm_presidents, sender=Dorm)
