'''
Created on Apr 26, 2012

@author: Haak Saxberg
'''
from django.db import models

from .courses import Course
from .people import Student

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
        return "{} > {}".format(self.requisite.code,self.course.code)