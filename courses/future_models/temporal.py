'''
Created on Apr 26, 2012

@author: Haak Saxberg
'''
from django.db import models

import datetime

from .utils import current_semester

class GradYear(models.Model):
    year = models.IntegerField()
    
    def __unicode__(self):
        return u"{}".format(self.year)

class Timeslot(models.Model):
    starts = models.TimeField(null=True)
    ends = models.TimeField(null=True)
    day = models.ForeignKey('Day')
    
    class Meta:
        unique_together = (('starts','ends','day'),)

    def __unicode__(self):
        return u"{}: {}-{}".format(self.day.code, self.starts, self.ends)

class Day(models.Model):
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
    short = models.CharField(max_length=4, unique=True)

    def __unicode__(self):
        return u"{}".format(self.code)

class Semester(models.Model):
    """Model representing Spring/Fall/Summer sessions"""
    year = models.IntegerField()
    half = models.CharField(max_length=2,
                            choices=(('FA',"Fall"),
                                     ('SP',"Spring"),
                                     ('SM',"Summer"))
                            )
    @classmethod
    def get_this_semester(cls):
        half = current_semester()
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
        unique_together = (('year','half'),)

    def __unicode__(self):
        return u"{}{}".format(self.half,self.year)