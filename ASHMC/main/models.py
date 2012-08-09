from django.contrib.contenttypes.models import ContentType

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _

import datetime
# Create your models here.


class _Utility(object):
    """
    Collects useful functions, allows them to share attributes if desired.

    If not, it's not too much overhead.
    """
    def disjunct(self, lister, funct=lambda x: x):
        for x in lister:
            if funct(x):
                return True
        return False

    def conjunct(self, lister, funct=lambda x: x):
        for x in lister:
            if not funct(x):
                return False
        return True

    def current_semester(self):
        """Determines whether today is in the spring, fall, or summer semesters"""
        today = datetime.datetime.now()

        if today.month < 5:
            return "SP"
        elif today.month < 8:
            return "SM"
        else:
            return "FA"

    def possible_grad_years(self):
        """Returns a range of current students' possible graduation dates"""
        today = datetime.datetime.now()

        if self.current_semester() == 'SP':  # second semester
            grad_range = range(today.year, today.year + 4)
        else:  # first semester
            grad_range = range(today.year + 1, today.year + 5)

        return grad_range

    def enum(*sequential, **named):
        """Generates an enum using *args and **kwargs. If you want a special class
        name to be used to enum members, pass the 'type_name' kwarg in."""
        type_name = named.pop('type_name', 'Enum')
        enums = dict(zip(sequential, range(len(sequential))), **named)
        return type(type_name, (), enums)

    def create_grades(self):
        letters = ['A', 'B', 'C', 'D', 'F', 'P', 'HP',
                   'INC',  # incomplete
                   'N',  # first half of a two-semester course
                   'NC',  # no credie
                   'W',  # late withdrawal
                   'AP',  # ap credit
                   'EX',  # exam credit
                   'NR',  # not reporting
                   ]
        final_letters = []
        for letter in letters:
            if letter in ['A', 'B', 'C', 'D']:
                final_letters += ['{}+'.format(letter),
                                  letter,
                                  '{}-'.format(letter), ]
            else:
                final_letters += [letter]
        return final_letters
Utility = _Utility()


class Role(models.Model):

    title = models.CharField(max_length=50)

    description = models.TextField(blank=True, null=True)

    # This FK is what makes the polymorphic magic work (esp. for printing)
    real_type = models.ForeignKey(ContentType, editable=False, null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.real_type = self._get_real_type()
        super(Role, self).save(*args, **kwargs)

    def _get_real_type(self):
        return ContentType.objects.get_for_model(type(self))

    def cast(self):
        return self.real_type.get_object_for_this_type(pk=self.pk)

    class Meta:
        abstract = True


class ASHMCAppointment(models.Model):
    semesters = models.ManyToManyField("Semester")
    user = models.ForeignKey(User)
    role = models.ForeignKey("ASHMCRole")

    bio = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return u"{} - {} ({})".format(self.user, self.role.cast(), self.semesters.all())


class ASHMCRole(Role):
    """Describes a role in ASHMC, i.e. President"""

    COUNCIL_MAIN = (
        'President',
        'Vice-President',
        'Treasurer',
        'Social Chair',
        'Committee for Activities Planning Chair',
        'Athletics Director',
        'Dormitory Affairs Committee Chair',
        'Senior Class President',
        'Junior Class President',
        'Sophomore Class President',
        'Freshman Class President',
    )

    COUNCIL_ADDITIONAL = (
        'Judiciary Board Chair',
        'Disciplinary Board Chair',
        'Appeals Board Chair',
        'Appeals Board Representative',
        'Food Committee Chair',
        'Honor Board Representative',
    )

    COUNCIL_APPOINTED = (
        'Language Tables Director',
        'Representative to the HMC Computer Committee',
        'Student Security Director',
        'Students-l Moderator',
        'Representative to the Educational Planning Committee',
        'Representative to the Student Affairs Committee',
        'Representative to the Campus Planning and Physical Plant Committee',
        'ASHMC Executive Assistant',
        'ASHMC Publicity Director',
        'ASHMC Web Editor',
    )

    # This defines the hierarchy of roles.
    # Naturally, the president is at the top.
    COUNCIL_ROLES = (
        'President',
        'Vice-President',
        'Dorm President',
        'Treasurer',
        'Social Chair',
        'Committee for Activities Planning Chair',
        'Webmaster',
        'Athletics Director',
        'Dormitory Affairs Committee Chair',
        'Senior Class President',
        'Junior Class President',
        'Sophomore Class President',
        'Freshman Class President',
        'Judiciary Board Chair',
        'Disciplinary Board Chair',
        'Appeals Board Chair',
        'Appeals Board Representative',
        'Food Committee Chair',
        'Honor Board Representative',
    )
    appointee = models.ManyToManyField(User, through="ASHMCAppointment")

    def __lt__(self, other):
        assert isinstance(other, ASHMCRole)
        try:
            my_index = ASHMCRole.COUNCIL_ROLES.index(self.title)
        except ValueError:
            my_index = ASHMCRole.COUNCIL_ROLES.index("Dorm President")

        try:
            their_index = ASHMCRole.COUNCIL_ROLES.index(other.title)
        except ValueError:
            their_index = ASHMCRole.COUNCIL_ROLES.index("Dorm President")

        return my_index > their_index

    def __unicode__(self):
        return u"ASHMC {}".format(self.title)

    def short_repr(self):
        return u"{}".format(self.title)

setattr(User, "highest_ashmc_role", property(lambda x: max(x.ashmcrole_set.all())))


class DormPresident(ASHMCRole):
    """Subclass of ASHMCRole specifically for Dorm Presidents,
    since they have to be associated with a dorm."""

    dorm = models.ForeignKey('roster.Dorm')

    def __unicode__(self):
        return u"{} President".format(self.dorm)

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = " "
        super(DormPresident, self).save(*args, **kwargs)


class DormAppointment(models.Model):
    user = models.ForeignKey(User)
    dorm_role = models.ForeignKey("DormRole")
    semesters = models.ManyToManyField("Semester")

    @property
    def dorm(self):
        return self.dorm_role.dorm


class DormRole(Role):

    OFFICIAL_TITLES = (
        'Treasurer',
        'Social Representative',
        'Jock',
    )

    dorm = models.ForeignKey('roster.Dorm')
    is_unofficial = models.BooleanField(default=False)
    appointees = models.ManyToManyField(User, through=DormAppointment)

    class Meta:
        verbose_name = _('DormRole')
        verbose_name_plural = _('DormRoles')

    def __unicode__(self):
        return u"{} {}".format(self.dorm, self.title)


class TopNewsItem(models.Model):

    slug = models.CharField(max_length=80)
    panel_html = models.TextField()
    panel_css = models.TextField()
    render_css = models.TextField(null=True, blank=True)

    author = models.ForeignKey(User)

    date_published = models.DateTimeField()
    date_expired = models.DateTimeField()
    should_display = models.BooleanField(default=True)

    def __unicode__(self):
        return u"{}".format(self.slug)

    def save(self, *args, **kwargs):
        if self.id is None:
            super(TopNewsItem, self).save(*args, **kwargs)
            self.save(*args, **kwargs)

        # TODO: Make this less janky
        css = self.panel_css
        lines = []
        for line in css.split('\n'):
            lines += ["#slider{} {}".format(self.id, line)]

        self.render_css = '\n'.join(lines)

        super(TopNewsItem, self).save(*args, **kwargs)


class Semester(models.Model):
    """Model representing Spring/Fall/Summer sessions"""
    year = models.IntegerField()
    half = models.CharField(max_length=2,
                            choices=(('FA', "Fall"),
                                     ('SP', "Spring"),
                                     ('SM', "Summer"))
                            )

    @staticmethod
    def get_this_semester():
        half = Utility.current_semester()
        year = datetime.datetime.now().year
        return Semester.objects.get(half=half,
                               year=year)

    def next_with_summer(self):
        if self.half == 'FA':
            half = "SP"
            year = self.year + 1
        elif self.half == "SP":
            half = "SM"
            year = self.year
        elif self.half == "SM":
            half = "FA"
            year = self.year

        return Semester.objects.get(half=half,
                                    year=year)

    def next(self):
        if self.half == 'FA':
            half = "SP"
            year = self.year + 1
        elif self.half == "SP":
            half = "FA"
            year = self.year
        else:
            half = "FA"
            year = self.year

        return Semester.objects.get(half=half,
                                    year=year)

    class Meta:
        unique_together = (('year', 'half'),)

    def __unicode__(self):
        return u"{}{}".format(self.half, self.year)


class GradYear(models.Model):
    year = models.IntegerField()

    @staticmethod
    def senior_class(sem=None):
        if sem is None:
            sem = Semester.get_this_semester()
        if sem.half in ['SP', 'SM']:
            return GradYear.objects.get_or_create(year=sem.year)[0]
        else:
            return GradYear.objects.get_or_create(year=sem.year + 1)[0]

    def __unicode__(self):
        return u"{}".format(self.year)


class Student(models.Model):
    user = models.OneToOneField(User)

    class_of = models.ForeignKey(GradYear)
    last_semester = models.ForeignKey(Semester, null=True, blank=True)

    nickname = models.CharField(null=True, blank=True, max_length=50)

    middle_name = models.CharField(null=True, blank=True, max_length=50)

    at = models.ForeignKey('Campus')  # This will default to HMC
    studentid = models.IntegerField(unique=True, null=True)
    credit_requirement = models.IntegerField(default=128)
    birthdate = models.DateField(null=True, blank=True)
    phonenumber = models.CharField(null=True, blank=True, max_length=20)

    temp_pass = models.CharField(max_length=50, null=True, blank=True)

    def __unicode__(self):
        return u"{}".format(self.user.get_full_name())


class Campus(models.Model):
    CAMPUSES = (
                    ('SC', 'Scripps'),
                    ('PZ', 'Pitzer'),
                    ('PO', 'Pomona'),
                    ('CM', 'Claremont-Mckenna'),
                    ('HM', 'Harvey Mudd'),
                    ('CG', 'Claremont Graduate University'),
                    ('KG', 'Keck Graduate Institute'),  # Keck actually doesn't offer any classes. For real.
                    ('CU', 'Claremont Consortium'),
                    ('NA', 'No Specific Campus'),
                    ('UN', 'Unknown Campus'),
                )
    ABSTRACTIONS = ['NA', 'UN']
    title = models.CharField(max_length=100, choices=((x[1], x[1]) for x in CAMPUSES))
    code = models.CharField(max_length=2, unique=True, choices=CAMPUSES)

    class Meta:
        verbose_name_plural = "campuses"

    def __unicode__(self):
        return u"{}".format(self.title)


class Building(models.Model):
    BUILDINGS = (
                    ('HM', (
                        ('BK', "Beckman"),
                        ("GA", "Galileo"),
                        ("HOSH", "Hoch"),
                        ('JA', "Jacobs"),
                        ("KE", "Keck"),
                        ("LAC", "LAC"),
                        ("MD", "Modular"),
                        ("ON", "Olin"),
                        ("PA", "Parsons"),
                        ("PL", "Platt"),
                        ("SP", "Sprague"),
                        ("TG", "TG"),
                        ("ARR", "Arranged"),
                        ("TBA", "To Be Arranged"),
                        )
                    ),
                    ('PZ', (
                            ('ATN', "Atherton Hall"),
                            ('AV', "Avery Hall"),
                            ("BD", "E&E Broad Center"),
                            ("BE", "Bernard Hall"),
                            ("BH", "Broad Hall"),
                            ("FL", "Fletcher Hall"),
                            ("GC", "Gold Student Center"),
                            ("GR", "Grove House"),
                            ("HO", "Holden Hall"),
                            ("MC", "McConnell Center"),
                            ("MH", "Mead Hall"),
                            ("OT", "Pitzer in Ontario"),
                            ("SB", "Sanborn Hall"),
                            ("SC", "Scott Hall"),
                            ("WST", "WST (??)"),
                            ("ARR", "Arranged"),
                            ("TBA", "To Be Arranged"),
                            )
                    ),
                    ('PO', (
                            ('AN', 'Andrew Science Bldg'),
                            ('BRDG', "Bridges Auditorium"),
                            ('BT', "Brackett Observatory"),
                            ('CA', "Carnegie Building"),
                            ("CR", "Crookshank Hall"),
                            ("EDMS", "Edmunds Building"),
                            ("GIBS", "Gibson Hall"),
                            ("HN", "Social Science Bldg"),
                            ("ITB", "Information Tech Bldg"),
                            ("LB", "Bridges Hall"),
                            ("LE", "Le Bus Court"),
                            ("LINC", "Lincoln Building"),
                            ("MA", "Mason Hall"),
                            ("ML", "Millikan Lab"),
                            ("OLDB", "Oldenbourg Center"),
                            ("PD", "Pendleton Dance Center"),
                            ("PENP", "Pool (??)"),
                            ("POM", "Pomona (??)"),
                            ("PR", "Pearsons Hall"),
                            ("RA", "Rains Center"),
                            ("REM", "Rembrandt Hall"),
                            ("SA", "Seaver Computing Ctr"),
                            ("SCC", "Smith Campus Center"),
                            ("SCOM", "Seaver Commons"),
                            ("SE", "Seaver South Lab"),
                            ("SL", "Seeley Science Library"),
                            ("SN", "Seaver North Lab"),
                            ("SVBI", "Seaver Bio Bldg"),
                            ("TE", "Seaver Theatre"),
                            ("THAT", "Thatcher Music Bldg"),
                            ("TR", "Biology Trailers"),
                            ("ARR", "Arranged"),
                            ("TBA", "To Be Arranged"),
                            )
                    ),
                    ('SC', (
                            ('AT', "Athletic Facility"),
                            ("BL", "Balch Hall"),
                            ("BX", "BX (??)"),
                            ("DN", "Richardson Studio"),
                            ("FRA", "Frankel Hall"),
                            ('HM', 'Edwards Humanities'),
                            ("LA", "Lang Art Studios"),
                            ("LCAB", "Arty something?"),
                            ("MT", "Malott Commons"),
                            ("PAC", "Performing Arts Center"),
                            ("ST", "Steele Hall"),
                            ("TIER", "Tiernant Field House"),
                            ("VN", "Vita Nova Hall"),
                            ("ARR", "Arranged"),
                            ("TBA", "To Be Arranged"),
                            )
                    ),
                    ('CM', (
                            ('AD', 'Adams Hall'),
                            ('BC', "Bauer South"),
                            ('BZ', 'Biszantz Tennis Center'),
                            ("DU", "Ducey Gym"),
                            ('KRV', "Kravitz Center"),
                            ('RN', "Roberts North"),
                            ('RS', "Roberts South"),
                            ("SM", "Seaman Hall"),
                            ("ARR", "Arranged"),
                            ("TBA", "To Be Arranged"),
                            )
                    ),
                    ('CG', (
                            ('BU', 'Burkle Building'),
                            ("ARR", "Arranged"),
                            ("TBA", "To Be Arranged"),
                            )
                    ),
                    ('CU', (
                        ('HD', "Honnold/Mudd Library"),
                        ("KS", "Keck Science Center"),
                        ("SSC", "Student Services Center"),
                        ("ARR", "Arranged"),
                        ("TBA", "To Be Arranged"),
                        )
                    ),
                    ('UN', (
                        ('ARR', "To Be Arranged"),
                        ('TBD', "To Be Determined"),
                        ('TBA', "To Be Announced"),
                        )
                    ),
                )

    campus = models.ForeignKey(Campus)
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)

    class Meta:
        unique_together = (('campus', 'code'),)

    def __unicode__(self):
        return u"{} {}".format(self.campus.code, self.name)

    def __repr__(self):
        return u"<Building: {}:{}>".format(self.campus.code, self.code)


class Room(models.Model):
    building = models.ForeignKey(Building)
    title = models.CharField(max_length=50)

    class Meta:
        unique_together = (('building', 'title'),)

    def __unicode__(self):
        return u"{} {} {}".format(self.building.campus.code,
                                  self.building.code,
                                  self.title)


class Day(models.Model):
    """
    A day of the week.

    Keeps track of code and name, as well as providing a shorthand name."""

    DAY_CHOICES = (
            ("M", "Monday"),
            ("T", "Tuesday"),
            ("W", "Wednesday"),
            ("R", "Thursday"),
            ("F", "Friday"),
            ("S", "Saturday"),
            ("U", "Sunday")
        )
    name = models.CharField(max_length=15, unique=True, choices=((x[1], x[1]) for x in DAY_CHOICES))
    code = models.CharField(max_length=1, unique=True, choices=DAY_CHOICES)
    short = models.CharField(max_length=15, unique=True)

    def __unicode__(self):
        return u"{}".format(self.code)

### SIGNALS ###
