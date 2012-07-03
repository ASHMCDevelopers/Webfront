from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals
from django.core.exceptions import ValidationError

from MultiDB import models as crossmodels

import datetime
import re
# Create your models here.


class Utility(object):
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


class SafeObjectManager(models.Manager):
    def get_query_set(self):
        return super(SafeObjectManager, self).get_query_set().filter(needs_attention=False)


class ActiveCourseManager(SafeObjectManager):
    def get_query_set(self):
        return super(ActiveCourseManager, self).get_query_set()\
            .annotate(num_sections=models.Count('section'))\
            .filter(num_sections__gte=1)\
            .annotate(num_meetings=models.Count('section__meeting'))\
            .filter(num_meetings__gte=1)


class Semester(models.Model):
    """Model representing Spring/Fall/Summer sessions"""
    year = models.IntegerField()
    half = models.CharField(max_length=2,
                            choices=(('FA', "Fall"),
                                     ('SP', "Spring"),
                                     ('SM', "Summer"))
                            )

    @classmethod
    def get_this_semester(cls):
        half = Utility().current_semester()
        year = datetime.datetime.now().year
        return cls.objects.get(half=half,
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

    def __unicode__(self):
        return u"{}".format(self.year)


class Student(crossmodels.MultiDBProxyModel):
    """
    Student is a sorta-proxy for User, since they're (probably)
    stored on different databases.

    This means that direct FK and M2M relations aren't supported by Django, so we have
    to 'coerce' them.
    """
    _linked_model = User

    class_of = models.ForeignKey(GradYear)
    at = models.ForeignKey('Campus')  # This will default to HMC
    studentid = models.IntegerField(unique=True)
    credit_requirement = models.IntegerField(default=128)

    class Meta:
        unique_together = ('_linked_id',)

    def __unicode__(self):
        return u"{} {}".format(self.linked_model.first_name,
                               self.linked_model.last_name)
# Attach a property to simulate reverse relationship
Student._linked_model.student_profile = property(lambda u: Student.objects.get(_linked_id=u.id))


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
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=2, unique=True)

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


class Department(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    code = models.CharField(max_length=50)
    campus = models.ForeignKey(Campus)

    class Meta:
        unique_together = (('code', 'campus'))

    def __unicode__(self):
        return u"{} at {}".format(self.code, self.campus)


class CourseArea(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    hard_science = models.BooleanField(default=False)
    is_req_area = models.BooleanField(default=False)

    def __unicode__(self):
        return u"[{}] {}".format(self.code, self.name)


class Professor(models.Model):
    first_name = models.CharField(max_length=50, null=True)  # allow null first names for 'Staff', etc.
    last_name = models.CharField(max_length=50)
    gender = models.CharField(choices=(('M', "Male"),
                                       ('F', "Female"),
                                       ('O', "Other"),
                                       ('U', "Unknown")),
                              default='U',
                              max_length=1)

    departments = models.ManyToManyField(Department,
                                         blank=True,
                                         null=True)
    bio = models.TextField(blank=True,
                           default="No bio available.")

    def __unicode__(self):
        return "{}, {}".format(self.last_name, self.first_name, )


class Major(models.Model):
    title = models.CharField(max_length=50)
    # departments has to be a M2M because some majors are
    # jointly held by departments (Math/Bio, for example)
    departments = models.ManyToManyField(Department)
    primary_campus = models.ForeignKey(Campus)
    students = models.ManyToManyField(Student,
                                      related_name="majors",
                                      null=True,
                                      blank=True)

    required_courses = models.ManyToManyField("Course",
                                              related_name="is_required_for",
                                              through="MajorCourseRequirement")
    electives = models.ManyToManyField("Course",
                                       related_name="is_elective_for",
                                       null=True,
                                       blank=True,)

    electives_required = models.IntegerField(default=3)
    elective_credits = models.IntegerField(default=8)

    def __unicode__(self):
        return u"{} through {}".format(self.title,
                                             self.primary_campus)


class NonStandardElective(models.Model):
    """Models a non-standard but approved elective choice,
    on a student-by-student basis."""

    major = models.ForeignKey(Major, related_name='+')
    student = models.ForeignKey(Student)
    course = models.ForeignKey('Course', related_name='+')

    def __unicode__(self):
        return u"{} under {} ({})".format(self.course,
                                          self.major,
                                          self.student)


class CourseExchange(models.Model):
    """Models a 'swapped' pair of courses, on a student-by-student basis."""

    original = models.ForeignKey('Course',
                                 related_name='+')
    new = models.ForeignKey('Course',
                            related_name='+')
    student = models.ForeignKey(Student)
    major = models.ForeignKey(Major)

    def __unicode__(self):
        return u"{} instead of {} ({})".format(self.new,
                                               self.original,
                                               self.student)


class MajorCourseRequirement(models.Model):
    major = models.ForeignKey(Major)
    course = models.ForeignKey('Course')
    times_to_take = models.IntegerField(default=1)
    alternates = models.ManyToManyField('Course',
                                        related_name='major_req_alts',
                                        null=True)

    def __unicode__(self):
        return "{}:{} x{}".format(self.major.title,
                                  self.course.code,
                                  self.times_to_take)


class Course(models.Model):
    """The abstract idea of a course, given Django form."""
    title = models.CharField(max_length=100)

    listable = models.BooleanField(default=True)

    departments = models.ManyToManyField(Department, null=True)

    areas = models.ManyToManyField(CourseArea, null=True, blank=True)
    codeletters = models.CharField(max_length=4, blank=True)
    number = models.IntegerField(default=0, blank=True)
    codenumber = models.CharField(max_length=5)
    campus = models.ForeignKey(Campus)
    codecampus = models.CharField(max_length=2)

    code = models.CharField(max_length=12)  # should only be 11, but just in case

    classtype = models.CharField(choices=(('L', "Lecture"),
                                          ('S', "Seminar"),
                                          ('B', 'Lab')),
                                 max_length=2,
                                 default='L')

    credit_multiplier = models.DecimalField(decimal_places=2,
                                       max_digits=3,
                                       default=3.00,
                                       null=True,
                                       blank=True)
    min_hours = models.DecimalField(decimal_places=2,
                                    max_digits=4,
                                    default=3.00)
    max_hours = models.DecimalField(decimal_places=2,
                                    max_digits=4,
                                    default=3.00)

    grade_type = models.CharField(choices=(('G', 'Letter Grade'),
                                           ('P', 'P/NP'),
                                           ('N', "Ungraded")),
                                  max_length=2,
                                  default='G')

    is_jointscience = models.BooleanField(default=False)

    prerequisites = models.ManyToManyField('self',
                                           through='Prerequisite',
                                           symmetrical=False)
    concurrent_with = models.ManyToManyField('self', blank=True, null=True,)
    corequisites = models.ManyToManyField('self', blank=True, null=True)
    crosslisted_as = models.ManyToManyField('self', blank=True)

    can_passfail = models.BooleanField(default=True)

    description = models.TextField(blank=True, default="No description available.")

    repeatable = models.BooleanField(default=False)

    needs_attention = models.BooleanField(default=False)

    objects = models.Manager()
    safe_objects = SafeObjectManager()
    active_objects = ActiveCourseManager()

    def get_active_sections(self):
        """
        Creates a queryset of 'acceptable' :model:`courses.Section` associated
        with this course
        """
        qs = self.section_set.all()
        qs = qs.annotate(num_meetings=models.Count('meeting'))\
               .filter(num_meetings__gte=1)
        qs = qs.exclude(meeting__needs_attention=True)
        qs = qs.filter(semester=Semester.get_this_semester().next())
        return qs.order_by('number')

    def set_writingintense(self, sem=None):
        if sem == None:
            sem = Semester.get_this_semester().next()
        self.section_set.filter(semester=sem).update(is_mudd_writingintense=True)

    def save(self, *args, **kwargs):
        try:
            # try to preserve numbering even if courses have letters
            # in their codenumbers
            self.number = int(re.match(r'^\d+', self.codenumber).group())
        except:
            pass

        super(Course, self).save(*args, **kwargs)

    def construct_code(self):
        return u"{}{}{}".format(self.codeletters, self.codenumber, self.codecampus)

    def __unicode__(self):
        if not self.codeletters:
            return u"{}{}{}".format(self.area.code.rjust(4),
                                    self.codenumber.zfill(3).ljust(5),
                                    self.codecampus)
        else:
            return u"{}{}{}".format(self.codeletters.rjust(4),
                                    self.codenumber.zfill(3).ljust(5),
                                    self.codecampus)


class Prerequisite(models.Model):
    course = models.ForeignKey(Course)
    requisite = models.ForeignKey(Course,
                                  related_name="prereq_for")
    alternates = models.ManyToManyField(Course,
                                        related_name="alternate_prereq_for",
                                        null=True)
    exempt_students = models.ManyToManyField(Student,
                                             null=True,
                                             blank=True,
                                             related_name="exempted_prereqs")

    oldest_year = models.IntegerField(default=2003)

    def __unicode__(self):
        return "{} > {}".format(self.requisite.code, self.course.code)


class Section(models.Model):
    course = models.ForeignKey(Course)
    title = models.CharField(max_length=100, blank=True, null=True)
    number = models.IntegerField(default=1)

    credit_hours = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    credit_multiplier = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    is_mudd_writingintense = models.BooleanField(default=False)  # need this here instead of Course,
                                                                 # because writingintensity might expire
                                                                 # but shouldn't expire for all time, just
                                                                 # the future semeesters.

    semester = models.ForeignKey('Semester', null=True)

    campus_restricted = models.BooleanField(default=False)
    seats = models.IntegerField(null=True)
    openseats = models.IntegerField(null=True)
    mudd_seats = models.IntegerField(null=True)
    mudd_seats_open = models.IntegerField(null=True)
    is_still_open = models.BooleanField(default=True)

    students = models.ManyToManyField(Student, through="Enrollment")

    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)

    needs_attention = models.BooleanField(default=False)

    objects = models.Manager()
    safe_objects = SafeObjectManager()

    @property
    def is_open(self):
        """Shorthand for a common check against openness."""
        return self.is_still_open and (self.openseats > 0)

    @property
    def has_times(self):
        return self.meeting_set.count() > 0 and \
            RoomInfo.objects.filter(meeting__section=self).count() > 0

    @property
    def mudd_creds(self):
        if self.credit_multiplier:
            return self.credit_hours * self.credit_multiplier

        return self.credit_hours * self.course.credit_multiplier

    class Meta:
        unique_together = (('course', 'number', 'semester'))

    def get_instructors(self):
        qs = self.meeting_set.all()
        return qs.values_list('teachers__last_name', 'teachers__first_name').distinct()

    def __unicode__(self):
        return u"{} - {} ({})".format(self.course, str(self.number).zfill(2),
                                      self.semester)


class RoomInfo(models.Model):
    """
    Associates :model:`courses.Meeting` with :model:`courses.Timeslot`.

    Also keeps track of additional information:

    - room: specifies physical meeting place for this pairing through the Room model
    - is_tba: see below
    - is_arr: see below
    """

    meeting = models.ForeignKey("Meeting")
    timeslot = models.ForeignKey("Timeslot")
    room = models.ForeignKey(Room)
    is_tba = models.BooleanField(default=False, help_text="To-be-arranged room situation")
    is_arr = models.BooleanField(default=False, help_text="Arranged-per-student room situation")

    # Consider giving RoomInfo a foreignkey to Course, for easy filtering?
    """
    course = models.ForeignKey(Course)

    def save(self, *args, **kwargs):
        if not self.course:
            self.course = self.meeting.section.course
        super(RoomInfo, self).save(*args, **kwargs)
    """

    #class Meta:
        # Unfuckingbelievably, this no-nonsense constraint is also not true;
        # because of 'rooms' like ARR and TBA.
        #unique_together = (('timeslot', 'room'), # can't have multiple meetings at the same time in the same room
        #)

    def validate_unique(self, exclude=None):
        if not (self.is_tba or self.is_arr) and \
           RoomInfo.objects.exclude(pk=self.pk).filter(timeslot=self.timeslot,
                                                       room=self.room)\
                                               .exists():
            raise ValidationError('RoomInfo (non-ARR, non-TBA) with timeslot_id={} and room_id={} already exists'.format(self.timeslot.id,
                                                                                                                         self.room.id))
        super(RoomInfo, self).validate_unique(exclude=exclude)

    def __unicode__(self):
        return u"{} {} - {}".format(self.meeting,
                                    self.timeslot,
                                    self.room)


class Meeting(models.Model):
    section = models.ForeignKey(Section)
    campus = models.ForeignKey(Campus, null=True)
    timeslots = models.ManyToManyField("Timeslot", through="RoomInfo")
    teachers = models.ManyToManyField(Professor)
    meeting_code = models.IntegerField()    # Unfuckingbelievable, but these aren't unique,
                                            # even between SECTIONS.

    needs_attention = models.BooleanField(default=False)

    objects = models.Manager()
    safe_objects = SafeObjectManager()

    @property
    def is_not_set(self):
        return Utility().conjunct(self.timeslots.all())

    class Meta:
        unique_together = ('section', 'meeting_code')

    def get_timeslot_tuples(self):
        times = self.timeslots.all()
        if times.count() > 0:  # sometimes there's not a meeting time
            time_copy = self.timeslots.all()
            all_times = []
            for slot in time_copy:
                slots = times.filter(starts=slot.starts,
                                     ends=slot.ends)
                times = times.exclude(starts=slot.starts,
                                              ends=slot.ends)
                time_copy = times
                if len(slots) == 0:
                    break
                subtimes = ("".join([x.day.code for x in slots]),
                                             slot.starts,
                                             slot.ends, slot)

                all_times += [subtimes]
            times = all_times
        else:
            times = []
        return times

    def get_roominfos(self):
        return RoomInfo.objects.filter(meeting=self)

    def __unicode__(self):
        return u"{} - {}".format(self.section, self.get_timeslot_tuples())


class Timeslot(models.Model):
    starts = models.TimeField(null=True)
    ends = models.TimeField(null=True)
    day = models.ForeignKey('Day')

    class Meta:
        unique_together = (('starts', 'ends', 'day'),)

    def does_not_overlap(self, other):
        if other.day != self.day:
            return False
        starts_within = (self.starts > other.starts and self.starts < other.ends)
        ends_within = (self.ends > other.starts and self.ends < other.ends)

        return not (starts_within or ends_within)

    def __unicode__(self):
        return u"{}: {}-{}".format(self.day.code, self.starts, self.ends)


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
    name = models.CharField(max_length=15, unique=True)
    code = models.CharField(max_length=1, unique=True)
    short = models.CharField(max_length=15, unique=True)

    def __unicode__(self):
        return u"{}".format(self.code)


class Enrollment(models.Model):
    """
    Keeps track of which students are in which courses
    """

    student = models.ForeignKey(Student)
    section = models.ForeignKey(Section)

    grade = models.CharField(max_length=2,
                             choices=([(x, x) for x in Utility().create_grades()]),
                             default='NR')

    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return u'{} in {}'.format(self.student, self.section)


class HMCHumReq(models.Model):
    """
    Models the HMC humanities requirement: both concentration(depth) and distribution(breadth).

    May not apply to students graduating before 2015.
    """
    DEPTH = 4
    BREADTH = 5
    MUDDHUMS = 6
    NOT_HUM_CODES = CourseArea.objects.filter(hard_science=True)\
                                      .values_list('code', flat=True)

    #One student per HumReq
    student = models.ForeignKey(Student)

    # Students choose a concentration department
    concentration = models.ForeignKey(Department, null=True)

    # And take classes to fulfill the breadth requirement
    breadth = models.ManyToManyField('Course', null=True)

    @property
    def muddhums_taken(self):

        hmc = self.student.at
        # only this student's courses, only those courses at mudd
        # only those courses that aren't hard sciences
        hmccourses = Enrollment.objects\
                        .filter(student=self.student, course__campus=hmc)\
                        .exclude(course__department__code__in=self.NOT_HUM_CODES)

        return hmccourses.count()

    @property
    def depth_taken(self):
        return Enrollment.objects\
                .filter(student=self.student,
                        course__department=self.concentration)\
                .count()

    @property
    def breadth_taken(self):
        hums = Enrollment.objects.filter(student=self.student)\
                                 .exclude(course__department__in=self.NOT_HUM_CODES)\
                                 .exclude(course__department=self.concentration)
        return hums.count()

    def __unicode__(self):
        return u"({})".format(self.student)


class ReviewModel(models.Model):
    RATING_CHOICES = (
                    (1, '1'),
                    (2, '2'),
                    (3, '3'),
                    (4, '4'),
                    (5, '5'),
                    (6, '6'),
                    (7, '7'),
                    (8, '8'),
                    (9, '9'),
                    (10, '10'),
                )

    class Meta:
        abstract = True

"""class CourseReview(ReviewModel):
    reviewer = models.ForeignKey(Student)
    course = models.ForeignKey(Course)
    date = models.DateTimeField(auto_now=True)

    toughness = models.PositiveIntegerField(choices=ReviewModel.RATING_CHOICES, help_text="1 being the easiest")
    quality = models.PositiveIntegerField(choices=ReviewModel.RATING_CHOICES, help_text="1 being the worst")

    review = models.TextField()
    review_html = models.TextField()

    class Meta:
        unique_together = (('reviewer', 'course'),)

    def __unicode__(self):
        return "Review of {} by {}".format(self.course, self.reviewer)
"""


class Log(models.Model):
    last_course_update = models.DateTimeField(default=datetime.datetime.now)
    last_enrollment_update = models.DateTimeField(default=datetime.datetime.now)

########################################
#"""                                """#
#"""            SIGNALS             """#
#"""                                """#
########################################


def attach_core_to_mudders(sender, **kwargs):
    """Automatically adds CORE to HMC students' list of majors"""
    student = kwargs['instance']
    if student.at.code == 'HM':  # only mudders experience core.
        try:
            core = Major.objects.get(title='Core', primary_campus__code='HM')
            student.majors.add(core)
        except Exception, e:
            e.args = ("Couldn't find HMC Core",) + e.args
            raise e
        try:
            # Attach Hum requirements
            h, new = HMCHumReq.objects.get_or_create(student=student)
        except Exception, e:
            e.args = ("Couldn't attach HMC hum reqs") + e.args
            raise e
signals.post_save.connect(attach_core_to_mudders, sender=Student)

