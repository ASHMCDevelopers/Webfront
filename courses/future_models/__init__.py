from django.db import models
from django.db.models import signals

from .people import Student, Major
from .requirements import HMCHumReq

import datetime


    
    
########################################
#"""                                """#
#"""            SIGNALS             """#
#"""                                """#
########################################

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
        try:
            # Attach Hum requirements
            h = HMCHumReq.objects.get_or_create(student=student)
        except Exception, e:
            e.args = ("Couldn't attach HMC hum reqs") + e.args
            raise e
signals.post_save.connect(attach_core_to_mudders,sender=Student)
