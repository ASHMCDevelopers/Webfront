from courses.models import GradYear,Campus,Building,possible_grad_years,\
                           Major, Course, Department,\
                           MajorCourseRequirement
from courses import models as features
from django.db.models import signals

""" The following methods are attached to the post_syncdb signal
and are used to ensure that certain objects never need to be created 
on the fly."""

def prepopulate_campuses(sender,**kwargs):
    """ Create objects for the campuses if they don't exist"""
    if not kwargs.has_key('verbosity'):
        kwargs['verbosity'] = 0
    for pair in Campus.CAMPUSES:
        if kwargs['verbosity'] > 0:
            print "Creating campus {}".format(pair[0])
        c, new = Campus.objects.get_or_create(code=pair[0])
        c.title = pair[1] # update title if necessary
        c.save()
signals.post_syncdb.connect(prepopulate_campuses, sender=features)

def prepopulate_buildings(sender, **kwargs):
    """Create objects for buildings automatically"""
    if not kwargs.has_key('verbosity'):
        kwargs['verbosity'] = 0
    for campus in Building.BUILDINGS:
        c = Campus.objects.get(code=campus[0])
        if kwargs['verbosity'] > 0:
            print "Creating buildings for campus: {}".format(c)
        for building in campus[1]:
            if kwargs['verbosity'] > 1:
                print "\t Creating building: {}".format(building[0])  
            b, new = Building.objects.get_or_create(campus=c,
                                           code=building[0])
            b.name = building[1]
            b.save()
signals.post_syncdb.connect(prepopulate_buildings, sender=features)

def prepopulate_gradyears(sender, **kwargs):
    """Create graduation years"""
    if not kwargs.has_key('verbosity'):
        kwargs['verbosity'] = 0
    if kwargs['verbosity'] > 0: print "Creating possible GradYears"
    for year in possible_grad_years():
        if kwargs['verbosity'] > 1: print "\tCreating GradYear:{}".format(year)
        y, new = GradYear.objects.get_or_create(year=year)
signals.post_syncdb.connect(prepopulate_gradyears, sender=features)

def prepopulate_core(sender, **kwargs):
    """Creates the HMC Core requirements as a major, to which all HMC students
    should be automatically added."""
    if not kwargs.has_key('verbosity'):
        kwargs['verbosity'] = 0
    if kwargs['verbosity'] > 0: print "Creating HMC Core requirements"
    core = []
    hmc, new = Campus.objects.get_or_create(code='HM') # should have been created already
    if kwargs['verbosity'] > 1: print "\tCreating HM Engineering Dept."
    engr, new = Department.objects.get_or_create(
                     name="Engineering",
                     code="ENGR",
                     campus=hmc
                     )
    if kwargs['verbosity'] > 2: print "\t\tCreating ENGR59"
    engr59 = Course.objects.create(
                    title="Introduction to Engineering Systems",
                    department=engr,
                    codenumber="59",
                    campus=hmc,
                    description="""An introduction to the concepts of modern engineering, 
                    emphasizing modeling, analysis, synthesis and design. 
                    Applications to chemical, mechanical and electrical systems. 
                    Prerequisite: sophomore standing. Corequisite: 
                    Physics 51. 3 credit hours. (Fall and Spring.)"""
                    )
    core += [engr59]
    if kwargs['verbosity'] > 1: print "\tCreating HM Chemistry Dept."
    
    chem, new = Department.objects.get_or_create(
                     name="Chemistry",
                     code="CHEM",
                     campus=hmc
                     )
    if kwargs['verbosity'] > 2: print "\t\tCreating CHEM23D"
    chem23d = Course.objects.create(
                    title="Dynamics",
                    department=chem,
                    codenumber="23D",
                    campus=hmc,
                    credit_hours=1.5,
                    )
    if kwargs['verbosity'] > 2: print "\t\tCreating CHEM23E"
    chem23e = Course.objects.create(
                    title="Energetics",
                    department=chem,
                    codenumber="23E",
                    campus=hmc,
                    credit_hours=1.5,
                    )
    if kwargs['verbosity'] > 2: print "\t\tCreating CHEM23S"
    chem23s = Course.objects.create(
                    title="Structure",
                    department=chem,
                    codenumber="23S",
                    campus=hmc,
                    credit_hours=1.5,
                    )
    if kwargs['verbosity'] > 2: print "\t\tCreating CHEM24"
    chem24 = Course.objects.create(
                    title="Chemistry Laboratory",
                    department=chem,
                    codenumber="24",
                    campus=hmc,
                    credit_hours=1.00,
                    classtype='B'
                    )
    core += [chem23d,chem23e,chem23s,chem24]
    if kwargs['verbosity'] > 1: print "\tCreating HM Physics Dept."
    phys, new = Department.objects.get_or_create(
                     name="Physics",
                     code="PHYS",
                     campus=hmc
                     )
    if kwargs['verbosity'] > 2: print "\t\tCreating PHYS22"
    phys22 = Course.objects.create(
                    title="Physics Laboratory",
                    department=phys,
                    codenumber="22",
                    campus=hmc,
                    credit_hours=1.00,
                    classtype='B'
                    )
    if kwargs['verbosity'] > 2: print "\t\tCreating PHYS23"
    phys23 = Course.objects.create(
                    title="Special Relativity",
                    department=phys,
                    codenumber="23",
                    campus=hmc,
                    credit_hours=1.5,
                    )
    if kwargs['verbosity'] > 2: print "\t\tCreating PHYS24"
    phys24 = Course.objects.create(
                    title="Mechanics & Wave Motion",
                    department=phys,
                    codenumber="24",
                    campus=hmc,
                    )
    if kwargs['verbosity'] > 2: print "\t\tCreating PHYS51"
    phys51 = Course.objects.create(
                    title="Electromagnetic Theory & Optics",
                    department=phys,
                    codenumber="51",
                    campus=hmc,
                    )
    engr59.concurrent_with.add(phys51)
    core += [phys22,phys23,phys24,phys51]
    if kwargs['verbosity'] > 1: print "\tCreating HM CompSci Dept."
    csci, new = Department.objects.get_or_create(
                     name="Computer Science",
                     code="CSCI",
                     campus=hmc
                     )
    if kwargs['verbosity'] > 2: print "\t\tCreating CSCI5"
    csci5 = Course.objects.create(
                    title="Introduction to Computer Science",
                    department=csci,
                    codenumber="5",
                    campus=hmc,
                    )
    if kwargs['verbosity'] > 2: print "\t\tCreating CSCI42"
    csci42 = Course.objects.create(
                    title="Principles & Practice: Comp Sci",
                    department=csci,
                    codenumber="42",
                    campus=hmc,
                    )
    core += [(csci5,csci42)]
    if kwargs['verbosity'] > 1: print "\tCreating HM Math Dept."
    math, new = Department.objects.get_or_create(
                     name="Mathematics",
                     code="MATH",
                     campus=hmc
                     )
    if kwargs['verbosity'] > 2: print "\t\tCreating MATH30B"
    math30b = Course.objects.create(
                    title="Calculus",
                    department=math,
                    codenumber="30B",
                    campus=hmc,
                    credit_hours=1.5,
                    )
    if kwargs['verbosity'] > 2: print "\t\tCreating MATH30G"
    math30g = Course.objects.create(
                    title="Calculus",
                    department=math,
                    codenumber="30G",
                    campus=hmc,
                    credit_hours=1.5,
                    )
    if kwargs['verbosity'] > 2: print "\t\tCreating MATH35"
    math35 = Course.objects.create(
                    title="Probability and Statistics",
                    department=math,
                    codenumber="35",
                    campus=hmc,
                    credit_hours=1.5,
                    )
    if kwargs['verbosity'] > 2: print "\t\tCreating MATH40"
    math40 = Course.objects.create(
                    title="Intro to Linear Algebra",
                    department=math,
                    codenumber="40",
                    campus=hmc,
                    credit_hours=1.5,
                    )
    if kwargs['verbosity'] > 2: print "\t\tCreating MATH45"
    math45 = Course.objects.create(
                    title="Intro to Differential Equations",
                    department=math,
                    codenumber="45",
                    campus=hmc,
                    credit_hours=1.5,
                    )
    if kwargs['verbosity'] > 2: print "\t\tCreating MATH60"
    math60 = Course.objects.create(
                    title="Multivariable Calculus",
                    department=math,
                    codenumber="45",
                    campus=hmc,
                    credit_hours=1.5,
                    )
    if kwargs['verbosity'] > 2: print "\t\tCreating MATH65"
    math65 = Course.objects.create(
                    title="Differential Eqns/Linear Alg II",
                    department=math,
                    codenumber="45",
                    campus=hmc,
                    credit_hours=1.5,
                    )
    core += [(math30b, math30g), math35, math40, math45,math60,math65]
    if kwargs['verbosity'] > 1: print "\tCreating HM Biology Dept."
    biol, new = Department.objects.get_or_create(
                     name="Biology",
                     code="BIOL",
                     campus=hmc
                     )
    if kwargs['verbosity'] > 2: print "\t\tCreating BIOL52"
    biol52 = Course.objects.create(
                    title="Introduction to Biology",
                    department=math,
                    codenumber="52",
                    campus=hmc,
                    )
    core += [biol52]
    if kwargs['verbosity'] > 1: print "\t\tCreating HMC Humanities Dept."
    coredept, new = Department.objects.get_or_create(
                     name="Humanities",
                     code="HUM",
                     campus=hmc
                     )
    if kwargs['verbosity'] > 0: print "\tCreating HMC Core major"
    hmcore = Major.objects.create(title="HMC Core")
    hmcore.departments.add(coredept)
    if kwargs['verbosity'] > 1: print "\tAttaching courses to Core major"
    for course in core:
        if type(course) is tuple:
            if kwargs['verbosity'] > 2: print "\t\tAssigning alternate course for{}: {}".format(course[0],course[1])
            # this is a set of exchangeable courses.
            c = MajorCourseRequirement.objects.create(
                         major=hmcore,
                         course=course[0],
                         )
            for alt in course[1:]:
                c.alternates.add(alt)
            c.save()
        else:
            if kwargs['verbosity'] > 2: print "\t\tAssigning {} to core".format(course)
            c = MajorCourseRequirement.objects.create(
                        major=hmcore,
                        course=course
                        )
signals.post_syncdb.connect(prepopulate_core, sender=features)   


