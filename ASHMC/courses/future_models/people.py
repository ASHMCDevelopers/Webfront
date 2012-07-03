'''
Created on Apr 26, 2012

@author: Haak Saxberg
'''
from django.db import models
from django.contrib.auth.models import User

from .temporal import GradYear
from .courses import Department

from MultiDB import models as crossmodels


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
        
class Major(models.Model):
    title = models.CharField(max_length = 50)
    # departments has to be a M2M because some majors are
    # jointly held by departments (Math/Bio, for example)
    departments = models.ManyToManyField(Department)
    
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
                                       blank=True)
    
    electives_required = models.IntegerField(default=3)
    elective_credits = models.IntegerField(default=8)
    def __unicode__(self):
        return u"{} through {}".format(self.title,
                                             self.departments.all())

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


class Professor(models.Model):
    first_name = models.CharField(max_length=50, null=True) # allow null first names for 'Staff', etc. 
    last_name = models.CharField(max_length=50)
    gender = models.CharField(choices=(('M',"Male"),
                                       ('F',"Female"),
                                       ('O',"Other"),
                                       ('U',"Unknown")), 
                              default='U',
                              max_length=1)
    
    departments = models.ManyToManyField(Department, 
                                         blank=True, 
                                         null=True)
    bio = models.TextField(blank=True, 
                           default="No bio available.")
    
    def __unicode__(self):
        return "{} {}".format(self.first_name, self.last_name)