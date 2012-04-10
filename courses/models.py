from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals
from MultiDB import models as crossmodels

import datetime, re
# Create your models here.

DAY_CHOICES = (
            ('M', "Mon"),
            ("T", "Tues"),
            ("W", "Weds"),
            ("R", "Thurs"),
            ("F", "Fri"),
            ("S", "Sat"),
            ("U", "Sun")
        )

def current_semester():
    """Determines whether today is in the spring, fall, or summer semesters"""
    today = datetime.datetime.now()
    
    if today.month < 5: 
        return "SP"
    elif today.month < 8:
        return "SM"
    else:
        return "FA"
    
def possible_grad_years():
    """Returns a range of current students' possible graduation dates"""
    today = datetime.datetime.now()
    
    if current_semester() == 'SP': # second semester
        grad_range = range(today.year, today.year+4)
    else: # first semester
        grad_range = range(today.year+1, today.year+5)

    return grad_range

class GradYear(models.Model):
    year = models.IntegerField()

class Student(crossmodels.MultiDBProxyModel):
    """Student is a sorta-proxy for User, since they're (probably)
    stored on different databases. This means that direct FK and M2M
    relations aren't supported by Django, so we have to 'coerce' them.
    """
    _linked_model = User
    
    class_of = models.ForeignKey(GradYear)
    at = models.ForeignKey('Campus') # This will default to HMC
    studentid = models.IntegerField(unique=True)
    credit_requirement = models.IntegerField(default=128)

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
                    ('KG', 'Keck Graduate Institute'),
                    ('CU', 'Claremont Consortium'),
                )
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=2, unique=True)

    def __unicode__(self):
        return u"{}".format(self.title)

class Building(models.Model):
    BUILDINGS = (
                    ('HM',( 
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
                        )
                    ),
                    ('PZ',(
                            ('ATN', "Atherton Hall"),
                            ('AV', "Avery Hall"),
                            ("BD", "E&E Broad Center"),
                            ("BE", "Bernard Hall"),
                            ("FL", "Fletcher Hall"),
                            ("GC", "Gold Student Center"),
                            ("GR", "Grove House"),
                            ("HO", "Holden Hall"),
                            ("MC", "McConnell Center"),
                            ("MH", "Mead Hall"),
                            ("OT", "Pitzer in Ontario"),
                            ("SB", "Sanborn Hall"),
                            ("SC", "Scott Hall"),
                            
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
                            )
                    ),
                    ('SC', (
                            ('AT', "Athletic Facility"),
                            ("BL", "Balch Hall"),
                            ("DN", "Richardson Studio"),
                            ("FRA", "Frankel Hall"),
                            ('HM', 'Edwards Humanities'),
                            ("LA", "Lang Art Studios"),
                            ("MT", "Malott Commons"),
                            ("PAC", "Performing Arts Center"),
                            ("ST", "Steele Hall"),
                            ("TIER", "Tiernant Field House"),
                            ("VN", "Vita Nova Hall"),
                            )
                    ),                    
                    ('CM', (
                            ('AD', 'Adams Hall'),
                            ('BC', "Bauer South"),
                            ('BZ', 'Biszantz Tennis Center'),
                            ("DU", "Ducey Gym"),
                            ('RN', "Roberts North"),
                            ('RS', "Roberts South"),
                            ("SM", "Seaman Hall"),
                            )
                    ),
                    ('CG', (
                            ('BU', 'Burkle Building'),
                            )
                    ),
                    ('CU',(
                        ('HD', "Honnold/Mudd Library"),
                        ("KS", "Keck Science Center"),
                        ("SSC", "Student Services Center"),
                        )
                    ),
                )
    
    campus = models.ForeignKey(Campus)
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10, unique=True)
    
    def __unicode__(self):
        return u"{}".format(self.name)
    def __repr__(self):
        return u"<Building: {}:{}>".format(self.campus.code, self.code)

class Room(models.Model):    
    building = models.ForeignKey(Building)
    title = models.CharField(max_length=50)
    class Meta:
        unique_together = (('building','title'),)

class Department(models.Model):
    name = models.CharField(max_length=100)    
    code = models.CharField(max_length=50)
    campus = models.ForeignKey(Campus)

    class Meta:
        unique_together = (('code','campus'))

    @classmethod
    def flat_listing(cls, **kwargs):
        """Returns a list of (code, code-title) tuples, where
        every code appears only once in the list.""" 
        codes = cls.objects.values_list('code',flat=True)
        tuples = []
        objs = cls.objects.values_list('code','name')
        for code in codes:
            obj = objs.filter(code=code)[0]
            tuples += [(obj[0],"{} - {}".format(obj[0],obj[1]))]
        
        if kwargs.has_key('for_form') and kwargs['for_form']:
            tuples = [('NONE',"(any)")]+tuples
        
        return tuples

    def __unicode__(self):
        return u"{} at {}".format(self.name, self.campus)

class Professor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(choices=(('M',"Male"),('F',"Female"),('O',"Other")), default='O',
                              max_length=1)
    departments = models.ManyToManyField(Department)
    bio = models.TextField(blank=True, default="No bio available.")

class Major(models.Model):
    title = models.CharField(max_length = 50)
    # departments has to be a M2M because some majors are
    # jointly held by departments (Math/Bio, for example)
    departments = models.ManyToManyField(Department)
    
    students = models.ManyToManyField(Student,related_name="majors", null=True)
    
    required_courses = models.ManyToManyField("Course", related_name="is_required_for", through="MajorCourseRequirement")
    electives = models.ManyToManyField("Course",related_name="is_elective_for", null=True)
    

    electives_required = models.IntegerField(default=3)

    def __unicode__(self):
        return u"{} through {}".format(self.title,
                                             self.departments.all())

class MajorCourseRequirement(models.Model):
    major = models.ForeignKey(Major)
    course = models.ForeignKey('Course')
    times_to_take = models.IntegerField(default=1)
    alternates = models.ManyToManyField('Course', related_name='major_req_alts',null=True)
    def __unicode__(self):
        return "{}:{} x{}".format(self.major.title, self.course, self.times_to_take)

class Course(models.Model):
    
    title = models.CharField(max_length=100)
    
    department = models.ForeignKey(Department)
    codeletters = models.CharField(max_length=50,blank=True)
    number = models.IntegerField(default=0)
    codenumber = models.CharField(max_length=20)
    campus = models.ForeignKey(Campus)
    classtype = models.CharField(choices=(('L',"Lecture"),('S', "Seminar"),('B', 'Lab')), max_length=2, default='L')
    credit_hours = models.DecimalField(decimal_places=2, max_digits=3, default=3.00)
    campus_restricted = models.BooleanField(default=False)
    is_jointscience = models.BooleanField(default=False)
    prerequisites = models.ManyToManyField('self',blank=True, symmetrical=False)
    concurrent_with = models.ManyToManyField('self',blank=True)
    crosslisted_as = models.ManyToManyField('self',blank=True)
    
    
    description = models.TextField(blank=True, default="No description available.")
    
    students = models.ManyToManyField(Student, through="Enrollment")
    
    class Meta:
        unique_together = (('department','codeletters','codenumber'),)
    
    def save(self, *args, **kwargs):
        try:
            # try to preserve numbering even if courses have letters
            # in their codenumbers
            self.number = int(re.match(r'^\d+',self.codenumber).group())
        except:
            pass
        super(Course,self).save(*args,**kwargs)
    
    @property
    def enrolled_students(self):
        enrollment_ids = self.enrollment_set.all().filter(semester__year=datetime.datetime.now().year,
                                                semester__half=current_semester()).values('student__id',flat=True)
        return Student.objects.filter(id__in=enrollment_ids)
    
    def __unicode__(self):
        if not self.codeletters:
            return u"{}{} {}".format(self.department.code,
                                    self.codenumber,
                                    self.campus)
        else:
            return u"{}{} {}".format(self.codeletters,
                                    self.codenumber,
                                    self.campus)
    
class Section(models.Model):
    course = models.ForeignKey(Course)
    title = models.CharField(max_length=100,blank=True)
    number = models.IntegerField(default=1)
    teachers = models.ManyToManyField(Professor)
    
    seats = models.IntegerField()
    openseats = models.IntegerField()
    
    timeslots = models.ManyToManyField("Timeslot", through="RoomInfo")
    
    class Meta:
        unique_together = (('course','number'))
    
class RoomInfo(models.Model):
    section = models.ForeignKey(Section)
    timeslot = models.ForeignKey("Timeslot")
    room = models.ForeignKey(Room)
    
    class Meta:
        unique_together = (('section', 'timeslot'))
    
class Timeslot(models.Model):
    starts = models.TimeField()
    ends = models.TimeField()
    day = models.CharField(max_length=1, choices=DAY_CHOICES)
    
    class Meta:
        unique_together = (('starts','ends','day'),)

class Semester(models.Model):
    """Model representing Spring/Fall/Summer sessions"""
    year = models.IntegerField()
    half = models.CharField(max_length=2,
                            choices=(('FA',"Fall"),('SP',"Spring"),('SM',"Summer"))
                            )

class Enrollment(models.Model):
    """Keeps track of which students are in which courses, according to Semester"""
    course = models.ForeignKey(Course)
    student = models.ForeignKey(Student)
    section = models.ForeignKey(Section)
    semester = models.ForeignKey(Semester)

class Log(models.Model):
    last_course_update = models.DateTimeField(default=datetime.datetime.now)
    last_enrollment_update = models.DateTimeField(default=datetime.datetime.now)
    
#""" ############################## """
#"""            SIGNALS             """
#""" ############################## """

def attach_core_to_mudders(sender, **kwargs):
    """Automatically adds CORE to HMC students' list of majors"""
    student = kwargs['instance']
    if student.at.code == 'HM': # only mudders experience core.
        try:
            core = Major.objects.get(title='HMC Core',)
            student.majors.add(core)
        except Exception,e:
            e.args = ("Couldn't find HMC Core",) + e.args
            raise e
signals.post_save.connect(attach_core_to_mudders,sender=Student)

