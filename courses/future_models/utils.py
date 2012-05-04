'''
Created on Apr 26, 2012

@author: Haak Saxberg
'''
from django.db import models

import datetime

class SafeObjectManager(models.Manager):
    def get_query_set(self):
        return super(SafeObjectManager, self).get_query_set().filter(needs_attention=False)

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


class Log(models.Model):
    last_course_update = models.DateTimeField(default=datetime.datetime.now)
    last_enrollment_update = models.DateTimeField(default=datetime.datetime.now)