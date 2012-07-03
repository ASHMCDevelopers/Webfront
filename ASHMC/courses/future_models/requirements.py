'''
Created on Apr 26, 2012

@author: Haak Saxberg
'''
from django.db import models

from .courses import Department, CourseArea, Enrollment
from .people import Major, Student

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

class HMCHumReq(models.Model):
    DEPTH = 4
    BREADTH = 5
    MUDDHUMS = 6
    NOT_HUM_CODES = CourseArea.objects.filter(hard_science=True).values_list('code',flat=True)
    
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