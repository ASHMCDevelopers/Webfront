'''
Created on May 5, 2012

@author: Haak Saxberg
'''
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError

from ...models import Campus, Course, Prerequisite, Department, \
                      MajorCourseRequirement, Major

from optparse import make_option

def from_requirements(course_list, major,**kwargs):
    for course in course_list:
        if type(course) is tuple:
            if kwargs['verbosity'] > 2: print "\t\tAssigning alternate course for {}: {}".format(course[0],course[1])
            # this is a set of exchangeable courses.
            c, new = MajorCourseRequirement.objects.get_or_create(
                         major=major,
                         course=course[0],
                         )
            for alt in course[1:]:
                c.alternates.add(alt)
            c.save()
        else:
            if kwargs['verbosity'] > 2: print "\t\tAssigning {} to core".format(course)
            c, new = MajorCourseRequirement.objects.get_or_create(
                        major=major,
                        course=course
                        )

#signals.post_syncdb.connect(prepopulate_core, sender=features)   

def create_hm_computer_science(**kwargs):
    hmc = Campus.objects.get(code="HM")
    csci = Department.objects.get(code="CSCI", campus=hmc)
    math = Department.objects.get(code="MATH", campus=hmc)
    cs60, new = Course.objects.get_or_create(
                 title="Principles of Computer Science",
                 codenumber="60",
                 department=csci,
                 campus=hmc,
                )
    cs70, new = Course.objects.get_or_create(
                 title="Data Structures and Program Development",
                 codenumber="70",
                 department=csci,
                 campus=hmc,
                )
    cs81, new = Course.objects.get_or_create(
                 title="Computability and Logic",
                 codenumber="81",
                 department=csci,
                 campus=hmc,
                )
    cs105, new = Course.objects.get_or_create(
                 title="Computer Systems",
                 codenumber="105",
                 department=csci,
                 campus=hmc,
                )
    cs121, new = Course.objects.get_or_create(
                 title="Software Development",
                 codenumber="121",
                 department=csci,
                 campus=hmc,
                )
    cs131, new = Course.objects.get_or_create(
                 title="Programming Languages",
                 codenumber="131",
                 department=csci,
                 campus=hmc,
                )
    cs140, new = Course.objects.get_or_create(
                 title="Algorithms",
                 codenumber="140",
                 department=csci,
                 campus=hmc,
                )
    
    math55, new = Course.objects.get_or_create(
                 title="Discrete Mathematics",
                 codenumber="55",
                 department=math,
                 campus=hmc,
                )
    cs42 = Course.objects.get(codenumber=42, department=csci)
    cs5s = Course.objects.filter(number=5, department=csci, classtype__in=["L","S"])
    
    cp, new = Prerequisite.objects.get_or_create(
               course=cs60,
               requisite=cs5s[0],
               )
    cp.alternates = cs5s[1:]
    cp, new = Prerequisite.objects.get_or_create(
               course=cs70,
               requisite=cs60,
               )
    cp.alternates = cs5s[1:]
    cp, new = Prerequisite.objects.get_or_create(
               course=cs81,
               requisite=cs60,
               )
    cp.alternates = [cs42,]
    Prerequisite.objects.get_or_create(
               course=cs81,
               requisite=math55,
               )
    Prerequisite.objects.get_or_create(
               course=cs105,
               requisite=cs70,
               )
    Prerequisite.objects.get_or_create(
               course=cs121,
               requisite=cs70,
               )
    Prerequisite.objects.get_or_create(
               course=cs131,
               requisite=cs70,
               )
    Prerequisite.objects.get_or_create(
               course=cs131,
               requisite=cs81,
               )
    Prerequisite.objects.get_or_create(
               course=cs140,
               requisite=cs70,
               )
    Prerequisite.objects.get_or_create(
               course=cs140,
               requisite=math55,
               )
    requirements = [(cs60,cs42),
                    cs70,
                    cs81,
                    cs105,
                    cs121,
                    cs131,
                    cs140,
                    math55]
    cs, new = Major.objects.get_or_create(title="Computer Science")
    cs.departments.add(csci)
    from_requirements(requirements, cs, **kwargs)
    
    
    
def create_majors(sender, **kwargs):
    create_hm_computer_science(**kwargs)
#signals.post_syncdb.connect(create_majors, features)

class Command(BaseCommand):
    # add elements to this as more become supported.
    supported_majors = {
                        'HM':{
                              'computer science':{
                                                  'depts':['HCSI',],
                                                  'kernel':[
                                                            ('CSCI005  ', 'CSCI042  '),
                                                            ('CSCI060  ', 'CSCI042  '),
                                                            'MATH055  ',
                                                            'CSCI070  ',
                                                            'CSCI081  ',
                                                            ('CSCI105  ', 'CSCI105  '),
                                                            'CSCI121  ',
                                                            'CSCI131  ',
                                                            'CSCI140  ',
                                                            'CSCI183  HM',
                                                            'CSCI184  HM',
                                                            'CSCI195  HM 4',
                                                            ],
                                                  'electives':[
                                                               'CSCI124  ',
                                                               'CSCI125  ',
                                                               'CSCI132  ',
                                                               'CSCI133  ',
                                                               'CSCI134  ',
                                                               'CSCI135  ',
                                                               'CSCI136  ',
                                                               'CSCI141  ',
                                                               'CSCI142  ',
                                                               'CSCI144  ',
                                                               'CSCI147  ',
                                                               'CSCI151  ',
                                                               'CSCI152  ',
                                                               'CSCI153  ',
                                                               'CSCI154  ',
                                                               'CSCI155  ',
                                                               'CSCI156  ',
                                                               'CSCI157  ',
                                                               'CSCI181',
                                                               'CSCI185  ',
                                                               'CSCI189  ',
                                                               ],
                                                  },
                              'core':{
                                      'elec_creds':0,
                                      'elec_req':0,
                                      'depts':['HCHM',
                                               'HBIO',
                                               'HEGR',
                                               'HHSS',
                                               'HPHY',
                                               'HCSI',
                                               'HMTH',
                                               ],
                                      'kernel':['ENGR059  HM',
                                                'CHEM023D HM',
                                                'CHEM023S HM',
                                                'CHEM024  HM',
                                                'PHYS022  HM',
                                                'PHYS023  HM',
                                                'PHYS024  HM',
                                                'PHYS051  HM',
                                                ('CSCI005GRHM', 'CSCI005  HM', 'CSCI042  HM'),
                                                ('MATH030B HM', 'MATH030G HM'),
                                                'MATH040  HM',
                                                'MATH045  HM',
                                                'MATH060  HM',
                                                'MATH065  HM',
                                                'BIOL052  HM',
                                                'CL  057  HM',
                                                'WRIT001  HM',
                                                ],
                                      'electives':[],
                                      },
                              }
                        }
    
    option_list = BaseCommand.option_list + (
                  make_option('-c','--campus',
                        action='store',
                        type='string',
                        dest='campus_code',
                        default='HM',
                        help='The code of the campus which holds the major you\'re after; i.e., HM',
                  ),
                 )
    
    args = '<"major title" "major title"...>'
    
    help = 'creates a major for a specified campus. If no campus specified, assumes HM campus.'
    
    def handle(self, *args, **options):
        print args, options
        # do all supported majors
        if len(args) > 0 and args[0].lower() == 'all':
            args = Command.supported_majors[options['campus_code']].keys()
            
        print args
        for arg in args:
            arg = arg.lower()
            if not arg in Command.supported_majors[options['campus_code']].keys():
                raise NotImplementedError()
            
            campus = Campus.objects.get(code=options['campus_code'])
            print "campus", campus
            major = Command.supported_majors[options['campus_code']][arg]
            print "finding major", major ,"..."
            
            m, new = Major.objects.get_or_create(title=arg.title(),
                                                 electives_required=major['elec_req'] if major.has_key('elec_req') else 3,
                                                 elective_credits=major['elec_creds'] if major.has_key('elec_creds') else 8,
                                                 primary_campus=campus)
            print "\tmajor: ", m
           
            # attach departments to major 
            for dept in major['depts']:
                d, new = Department.objects.get_or_create(code=dept)
                print "adding dept", d
                m.departments.add(d)
            
            # attach kernels to major
            for code in major['kernel']:
                if type(code) is tuple:
                    alts = code[1:]
                    code = code[0]
                    alt_c = []
                        
                else: 
                    alts = ()
                #print code
                alt_c = []
                for alt in alts:
                    print "alt: ", alt
                    try:
                        c_code = alt[9:11]
                    except IndexError:
                        # this kernel course is not campus specific 
                        c_code = ''
                        
                    try:
                        n_code = alt[4:9]
                    except IndexError:
                        raise CommandError('Malformed code in {}:{} -- {}'.format(
                                                          campus, major, alt
                                                          ))
                    
                    try:
                        a_code = alt[0:4]
                    except IndexError:
                        raise CommandError('Malformed code in {}:{} -- {}'.format(
                                                          campus, major, alt
                                                          ))
                    courses = Course.objects.filter(codecampus__startswith=c_code,
                                                codenumber__startswith=n_code,
                                                codeletters__startswith=a_code)
                    if len(courses) < 1:
                        raise CommandError("Must be a mistake: found no courses for alternate {}".format(alt))
                    alt_c += list(courses)
                #print "alternates: ", alt_c
                print "code: ", code
                try:
                    c_code = code[9:11]
                except IndexError:
                    # this kernel course is not campus specific 
                    c_code = ''
                    
                try:
                    n_code = code[4:9]
                except IndexError:
                    raise CommandError('Malformed code in {}:{} -- {}'.format(
                                                      campus, major, code
                                                      ))
                
                try:
                    a_code = code[0:4]
                except IndexError:
                    raise CommandError('Malformed code in {}:{} -- {}'.format(
                                                      campus, major, code
                                                      ))
                # if all specified, that should be enough to uniquely identify 
                # any course. But, not all are always specified.
                #print c_code, n_code, a_code
                courses = Course.objects.filter(codecampus__startswith=c_code,
                                                codenumber__startswith=n_code,
                                                codeletters__startswith=a_code)
                if len(courses) < 1:
                    raise CommandError("Must be a mistake: found no courses for requirement {}".format(code))
                #print courses
                c = courses[0]
                alt_c += courses[1:]
                if len(code) > 11:
                    times = int(code[12:])
                else:
                    times = 1
                mcr, new = MajorCourseRequirement.objects.get_or_create(
                                                                        major=m,
                                                                        course=c,
                                                                        times_to_take=times
                                                                        )
                mcr.alternates.add(*alt_c)
            
            for code in major['electives']:
                print "elective: ", code
                try:
                    c_code = code[9:11]
                except IndexError:
                    # this kernel course is not campus specific 
                    c_code = ''
                    
                try:
                    n_code = code[4:9]
                except IndexError:
                    raise CommandError('Malformed code in {}:{} -- {}'.format(
                                                      campus, major, code
                                                      ))
                
                try:
                    a_code = code[0:4]
                except IndexError:
                    raise CommandError('Malformed code in {}:{} -- {}'.format(
                                                      campus, major, code
                                                      ))
                #print c_code, n_code, a_code
                courses = Course.objects.filter(codecampus__startswith=c_code,
                                                codenumber__startswith=n_code,
                                                codeletters__startswith=a_code)
                if len(courses) < 1:
                    raise CommandError("Must be a mistake: found no courses for requirement {}".format(code))
                #print courses
                
                m.electives.add(*courses)
                courses = None