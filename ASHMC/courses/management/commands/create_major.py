'''
Created on May 5, 2012

@author: Haak Saxberg
'''
from django.core.management.base import BaseCommand, CommandError

from ...models import Campus, Course, Department, \
                      MajorCourseRequirement, Major

from optparse import make_option


class Command(BaseCommand):
    # add elements to this as more become supported.
    supported_majors = {
                        'HM':{
                              'computer science':{
                                                  'depts':['HCSI',],
                                                  'kernel':[
                                                            ('CSCI005  ',
                                                             'CSCI042  '),
                                                            ('CSCI060  ',
                                                             'CSCI042  '),
                                                            'MATH055  ',
                                                            'CSCI070  ',
                                                            'CSCI081  ',
                                                            'CSCI105  ',
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
                              'biology':{
                                         'depts':['HBIO'],
                                         'kernel':['BIOL054  ',
                                                   'CHEM056  ',
                                                   'CHEM058  ',
                                                   'BIOL101  ',
                                                   'CHEM105  HM',
                                                   'BIOL108  ',
                                                   'BIOL109  ',
                                                   'BIOL113  ',
                                                   'BIOL191  HM 2',
                                                   'BIOL192  HM 2',
                                                   ('BIOL193  HM',
                                                    'BIOL195  HM'),
                                                   ('BIOL194  HM',
                                                    'BIOL196  HM'),
                                                   ],
                                         'electives':[],
                                         'elec_creds':13,
                                         'elec_req':3
                                         },
                              'computer science and mathematics':{
                                                                  'depts':['HCSI','HMTH'],
                                                                  'kernel':['MATH055  ',
                                                                            ('CSCI005',
                                                                             'CSCI060  '),
                                                                            'CSCI081  ',
                                                                            'CSCI140  ',
                                                                            'CSCI070  ',
                                                                            'CSCI105  ',
                                                                            'CSCI131  ',
                                                                            'MATH131  ',
                                                                            ('MATH164  ',
                                                                             'MATH165'),
                                                                            'MATH171  ',
                                                                            ('CSCI183  HM',
                                                                             'MATH193  HM',
                                                                             'CSMT183  HM'),
                                                                            ('CSCI184  HM',
                                                                             'MATH193  HM',
                                                                             'CSMT184  HM'),
                                                                            'CSCI195  HM 2',
                                                                            'MATH199  HM',
                                                                            'MATH198  HM'
                                                                            ],
                                                                  'electives':[],
                                                                  'elec_creds':8,
                                                                  'elec_req':0
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
                                                ('CSCI005  HM', 'CSCI005GRHM', 'CSCI042  HM'),
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
                d = Department.objects.get(code=dept)
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
