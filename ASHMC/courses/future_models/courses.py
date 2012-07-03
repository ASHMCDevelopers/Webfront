'''
Created on Apr 26, 2012

@author: Haak Saxberg
'''
from django.db import models
from django.core.exceptions import ValidationError

from .utils import SafeObjectManager

from .people import Student, Professor
from .physical import Campus

import re

class Department(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)    
    code = models.CharField(max_length=50)
    campus = models.ForeignKey(Campus)
    class Meta:
        unique_together = (('code','campus'))

    def __unicode__(self):
        return u"{} at {}".format(self.code, self.campus)


class CourseArea(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    hard_science = models.BooleanField(default=False)
    is_req_area = models.BooleanField(default=False)
    def __unicode__(self):
        return u"[{}] {}".format(self.code, self.name)
    
    
class Course(models.Model):
    
    title = models.CharField(max_length=100)
    
    departments = models.ManyToManyField(Department, null=True)
    areas = models.ManyToManyField(CourseArea, null=True, blank=True)
    codeletters = models.CharField(max_length=4,blank=True)
    number = models.IntegerField(default=0, blank=True)
    codenumber = models.CharField(max_length=5)
    campus = models.ForeignKey(Campus)
    
    classtype = models.CharField(choices=(('L',"Lecture"),
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
    
    grade_type = models.CharField(choices=(('G','Letter Grade'),
                                           ('P','P/NP'),
                                           ('N', "Ungraded")), 
                                  max_length=2, 
                                  default='G')
    
    is_jointscience = models.BooleanField(default=False)
    
    prerequisites = models.ManyToManyField('self',
                                           through='Prerequisite', 
                                           symmetrical=False)
    concurrent_with = models.ManyToManyField('self',blank=True, null=True)
    corequisites = models.ManyToManyField('self', blank=True, null=True)
    crosslisted_as = models.ManyToManyField('self',blank=True)
    
    can_passfail = models.BooleanField(default=True)
    
    description = models.TextField(blank=True, default="No description available.")
    
    repeatable = models.BooleanField(default=False)
    
    needs_attention = models.BooleanField(default=False)
    
    objects = models.Manager()
    safe_objects = SafeObjectManager()
    
    def save(self, *args, **kwargs):
        try:
            # try to preserve numbering even if courses have letters
            # in their codenumbers
            self.number = int(re.match(r'^\d+',self.codenumber).group())
        except:
            pass

        super(Course,self).save(*args,**kwargs)
    
    @property
    def code(self):
        letters = self.area.code if not self.codeletters else self.codeletters
        return u"{}{}".format(letters, self.codenumber.zfill(3))
    
    def __unicode__(self):
        if not self.codeletters:
            return u"{}{} {}".format(self.area.code,
                                    self.codenumber.zfill(3),
                                    self.campus.code)
        else:
            return u"{}{} {}".format(self.codeletters,
                                    self.codenumber.zfill(3),
                                    self.campus.code)
            
class Section(models.Model):
    course = models.ForeignKey(Course)
    title = models.CharField(max_length=100,blank=True, null=True)
    number = models.IntegerField(default=1)
    
    credit_hours = models.DecimalField(max_digits=3,decimal_places=2)
    is_mudd_writingintense = models.BooleanField(default=False) # need this here instead of Course,
                                                                # because writingintensity might expire
                                                                # but shouldn't expire for all time, just
                                                                # the future semeesters.
    
    semester = models.ForeignKey('Semester')
    
    campus_restricted = models.BooleanField(default=False)
    seats = models.IntegerField()
    openseats = models.IntegerField()
    mudd_seats = models.IntegerField(null=True)
    mudd_seats_open = models.IntegerField(null=True)
    is_still_open = models.BooleanField(default=True)
    
    students = models.ManyToManyField(Student, through="Enrollment")
    
    
    start_date = models.DateField()
    end_date = models.DateField()
    
    
    needs_attention = models.BooleanField(default=False)
    
    objects = models.Manager()
    safe_objects = SafeObjectManager()
    
    @property
    def is_open(self):
        """Shorthand for a common check against openness."""
        return self.is_still_open and (self.openseats > 0) 
    
    class Meta:
        unique_together = (('course','number',))

    def __unicode__(self):
        return u"{} - {:02d}".format(self.course, self.number)

class Meeting(models.Model):
    section = models.ForeignKey(Section)
    campus = models.ForeignKey(Campus)
    timeslots = models.ManyToManyField("Timeslot", through="RoomInfo")
    teachers = models.ManyToManyField(Professor)
    meeting_code = models.IntegerField()    # Unfuckingbelievable, but these aren't unique,
                                            # even between SECTIONS.
    
    needs_attention = models.BooleanField(default=False)
    
    objects = models.Manager()
    safe_objects = SafeObjectManager()
    
    class Meta:
        unique_together = ('section','meeting_code')
    
    def get_timeslot_tuples(self):
        times = self.timeslots.all()
        if times.count() > 0: # sometimes there's not a meeting time
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
                                             slot.ends)
                
                all_times += [subtimes]
            times = all_times
        else:
            times = ()
        return times
    
    def __unicode__(self):
        
        
        return u"{} - {}".format(self.section, self.get_timeslot_tuples())

class RoomInfo(models.Model):
    meeting = models.ForeignKey(Meeting)
    timeslot = models.ForeignKey("Timeslot")
    room = models.ForeignKey(Room)
    is_tba = models.BooleanField(default=False)
    is_arr = models.BooleanField(default=False)
    #class Meta:
        # Unfuckingbelievably, this no-nonsense constraint is also not true;
        # because of 'rooms' like ARR and TBA.
        #unique_together = (('timeslot', 'room'), # can't have multiple meetings at the same time in the same room
        #)
    
    def validate_unique(self, exclude=None):
        if not (self.is_tba or self.is_arr) and \
           RoomInfo.objects.exclude(pk=self.pk).filter(timeslot=self.timeslot, room=self.room).exists():
            raise ValidationError('RoomInfo (non-ARR, non-TBA) with timeslot_id={} and room_id={} already exists'.format(self.timeslot.id,
                                                                                                                         self.room.id))
        super(RoomInfo, self).validate_unique(exclude=exclude)
    
    def __unicode__(self):
        return u"{} {} - {}".format(self.meeting,
                                    self.timeslot,
                                    self.room)

class Enrollment(models.Model):
    """Keeps track of which students are in which courses"""
    student = models.ForeignKey(Student)
    section = models.ForeignKey(Section)
    
    def __unicode__(self):
        return u'{} in {}'.format(self.student, self.section)