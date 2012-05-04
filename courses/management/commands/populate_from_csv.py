'''
Created on Apr 16, 2012

@author: Haak Saxberg
'''
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from ...models import Campus, Course, Professor, Section, Meeting, Timeslot, Day, Semester,\
                      CourseArea, Prerequisite, RoomInfo, Log, Department, Room, Building

from itertools import izip
import csv, pprint, re, datetime

            
class Command(BaseCommand):
    args = '<directory_of_csv_files>'
    help = 'Populates the Course tables with information from csv files.'
    
    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("Expects a single directory as an argument.")
        dir = args[0]
        if dir[-1] != '/':
            
            dir += '/'
        
        # Gather up the relevant csv files.
        # ENSURE THESE ARE ENCODED AS UTF-8 BEFORE RUNNING THIS SCRIPT
        MEETINGS = open(dir + 'meetings 1.csv')
        SECTIONS = open(dir + 'sections 1.csv')
        DESCRIPT = open(dir + 'courses 1.csv')
        AREAS = open(dir + 'courses 2.csv')
        PREREQS = open(dir + 'courses 3.csv')
        
        # Gather campuses. We'll need them later.
        CAMPUS_CODES = Campus.objects.all().values_list('code', flat=True)
        self.stderr.write("{}".format(CAMPUS_CODES))
        CAMPUS_LOOKUP = dict([ x for x in izip(CAMPUS_CODES,
                                               Campus.objects.all())])
        def find_campus(string, dictionary):
            try:
                camp = CAMPUS_LOOKUP[string]
            except KeyError, e:
                print "Invalid campus: {}".format(string)
                try:
                    camp = CAMPUS_LOOKUP[dictionary['campus']]
                except KeyError, e:
                    print "Falling back to NA"
                    camp = CAMPUS_LOOKUP['NA']
            return camp
        
        SEMESTER_LOOKUP = dict([ x for x in izip(Semester.objects.values_list('half','year'),
                                                 Semester.objects.all())])
        
        DAY_LOOKUP = dict([x for x in izip(Day.objects.values_list('code',flat=True),
                                           Day.objects.all())])
        
        self.stderr.write("{}\n{}\n{}".format(CAMPUS_LOOKUP, SEMESTER_LOOKUP, DAY_LOOKUP))
        
        meetings_r = csv.DictReader(MEETINGS)
        sections_r = csv.DictReader(SECTIONS)
        descript_r = csv.DictReader(DESCRIPT)
        areas_r = csv.DictReader(AREAS)
        prereqs_r = csv.DictReader(PREREQS)
        

        
        # First, we go through the descriptions, since that's supposedly the
        # canonical list of courses that exist.
        # As we go, populate a dictionary with keys that are the course codes,
        # creating a json-like dict of dicts. 
        courses = {}
        for row in descript_r:
            # pull out some interesting data from this csv file, for later use.
            #print row
            code = row['\xef\xbb\xbf"Course Number"'] # ugly because of unicode conversion
            course = {}
            #self.stderr.write("Parsing description for {}\n".format(code))
            
            course['code'] = code[:4]
            course['number'] = code[4:9]
            course['code_campus'] = code[-2:]
            course['title'] = row['Course Title']
            course['dept'] = row['Course Department Code']
            course['campus'] = row['Prim Assoc']
            course['minhours'] = row['Min Hrs']
            course['maxhours'] = row['Max Hrs']
            course['descr'] = row['Abstr']
            course['requisites'] = []   # empty prereq list for later.
            course['sections'] = {}     # empty section dict for later; every course should (?)
                                        # have at least one section associated with it; use number
                                        # as key.
            course['attention'] = False
            course['area'] = [] # a course can have more than one area associated with it
            courses[code] = course
        
        # populate areas; use this to filter in place of department.
        for row in areas_r:
            code = row['\xef\xbb\xbf"Course Number"']
            #self.stderr.write("Parsing area for {}\n".format(code))
            course = courses[code]
            
            course['area'] += [row["Course Area Code"]]
        
        # populate prerequisite/concurrent enrollment requirements
        for row in prereqs_r:
            code = row['\xef\xbb\xbf"Course Number"']
            #self.stderr.write("Parsing requisites for {}\n".format(code))
            course = courses[code]
            
            # C = Corequisite, P = Prerequisite, N = Concurrent Enrollment Required
            if row['Requisite Course Category'] in ['C', 'N', 'P']:
                if '*' in row['Requisite Course Number']:
                    # a * indicates a wildcard.
                    # Course codes are [4 letters for area][at least 3 and up to 5 characters for number][2 letters for campus]
                    # Ex: MATH030G HM
                    # Ex: MUS 052HNPO
                    # Ex: CSCI005GLHM
                    course['attention'] = True
                requisite = {'code':row['Requisite Course Number']}
                if courses.has_key(requisite['code']):
                    requisite['req_attention'] = False
                else:
                    requisite['req_attention'] = True
                    requisite['wildcard'] = '*' in requisite
                course['requisites'] += [(row['Requisite Course Category'], 
                                     requisite)]
                
        # get sections, associate them with specific courses
        for row in sections_r:
            code = row['\xef\xbb\xbf"Course Number"']
            
            course = courses[code]
            
            section = {}
            
            section['title'] = row['Section Title'] if len(row['Section Title']) > 0 else None
            section['number'] = row['Section Number']
            section['semester'] = row['Session Code']
            section['year'] = int(row['Year'])
            section['open'] = True if row['Section Status'] == 'O' else False
            section['starts'] = row['Section Begin Date']
            section['ends'] = row['Section End Date']
            section['cred_hours'] = row['Section Credit Hours']
            section['seats'] = row['Maximum Registration']
            section['meetings'] = {} # empty meeting dict for later use
            section['attention'] = False
            
            course['sections'][section['number']] = section
        
        # get meetings, associate them with specific sections
        for row in meetings_r:
            code = row['\xef\xbb\xbf"Course Number"']
            course = courses[code]
            if len(course['sections'].keys()) < 1:
                continue
            try:
                section = course['sections'][row['Section Number']]
            except KeyError, e:
                pprint.pprint(course, self.stderr)
                self.stderr.write("ERROR: {}\n".format(e))
                section = {}
                section['title'] = None
                section['year'] = Semester.get_this_semester().next().year
                section['open'] = 0
                section['starts'] = datetime.datetime.now() # trash values
                section['ends'] = datetime.datetime.now() # trash values
                section['cred_hours'] = 0
                section['seats'] = 0
                section['attention'] = True
                section['semester'] = Semester.get_this_semester().next().half
                section['number'] = row['Section Number']
                section['meetings'] = {}
                course['sections'][section['number']] = section
                
                
            
            if section['meetings'].has_key(row['Meeting Number']):
                meeting = section['meetings'][row["Meeting Number"]] # If we've seen this row before, don't mess with anything
            else:
                meeting = {}
                meeting['instructors'] = []
                
                meeting['meet_num'] = row['Meeting Number']
                meeting['days'] = row['Class Meeting Days']
                meeting['start_time'] = row['Class Begin Time (24 Hour)']
                meeting['end_time'] = row['Class End Time (24 Hour)']
                meeting['campus_code'] = row['Campus Code']
                meeting['building'] = row['Building Code']
                meeting['room'] = row['Room Number']
                meeting['attention'] = False
                
                section['meetings'][meeting['meet_num']] = meeting
                
                
            meeting['instructors'] += [row['Instructor Name']] # multiple instructors
            
        #self.stderr.write("{}\n".format(courses.keys()[-4]))
        #self.stderr.write("{}\n".format((courses.keys()[-4] == "SPAN033 PO")))
        #pprint.pprint(courses['PHYS051  HM'], self.stderr)
            
        # We've now gleaned all the information that we can from the csv's, and put them into a monster 
        # of a dict of nested dicts.
        non_base_courses = []
        base_courses = []
        for key in courses.keys():
            #self.stderr.write("{}\n".format(key))
            course = courses[key]
            if len(course['requisites']) > 0:
                non_base_courses += [course]
            else:
                base_courses += [course]
        
        pprint.pprint("{} base courses".format(len(base_courses)), self.stderr)
        pprint.pprint("{} non-base courses".format(len(non_base_courses)),
                        self.stderr)
        
        #created_courses = {}
        repeats = 0
        fucked_bases = []
        for course in base_courses+non_base_courses:
            # First, ensure that we have the course area and the department
            for area in course['area']:
                if area in ['BIOL','CHEM','CSCI','ENGR','MATH','PHYS']:
                    science = True
                else:
                    science = False
                if re.match(r'^\d',area):
                    req_status = True
                else:
                    req_status = False
                ca, new = CourseArea.objects.get_or_create(code=area,
                                                           name=area,
                                                           hard_science=science,
                                                           is_req_area=req_status)
                
            
            primary_campus = CAMPUS_LOOKUP[course['campus']]
            dept, new = Department.objects.get_or_create(code=course['dept'],
                                                      campus=primary_campus,
                                                      )
            
            #print course['number'],course['code_campus'], course['title']
            #print course['descr']
            
            # build the course itself
            c, new = Course.objects.get_or_create(
                                           title=course['title'],
                                           
                                           codeletters=course['code'],
                                           codenumber=course['number'],
                                           codecampus=course['code_campus'],
                                           
                                           campus=find_campus(course['code_campus'], course),
                                           
                                           min_hours=course['minhours'],
                                           max_hours=course['maxhours'],
                                           
                                           description=unicode(course['descr'],"UTF-8"),
                                           needs_attention=course['attention']
                                           )
            if not new: repeats += 1
            c.departments.add(dept)
            c.areas.add(ca)
            c.code = c.construct_code()
            c.save()
            #Now, we add sections.
            for section in course['sections'].keys():
                sec = course['sections'][section]
                #print "Section ", section
                try:
                    s, new = Section.objects.get_or_create(
                                                       course=c,
                                                       title=sec['title'],
                                                       number=sec['number'],
                                                       
                                                       credit_hours=sec['cred_hours'],
                                                       
                                                       semester=SEMESTER_LOOKUP[(sec['semester'],sec['year'])],
                                                       
                                                       seats=sec['seats'],
                                                       openseats=sec['seats'], # assume totally free classes!
                                                       
                                                       start_date=sec['starts'],
                                                       end_date=sec['ends'],
                                                       
                                                       needs_attention=sec['attention'], 
                                                       )
                except IntegrityError, e:
                    print e
                    print "Adding this course to the 'fucked' list"
                    fucked_bases += [(course, section)]
                    continue    
                # add meetings to sections
                for meet in sec['meetings'].keys():
                    print "\tMeeting code: ", meet
                    meeting = sec['meetings'][meet]
                    
                    m, new = Meeting.objects.get_or_create(section=s,
                                                           meeting_code=int(meeting['meet_num']),
                                                           )
                    m.needs_attention=meeting['attention']
                    m.campus=find_campus(meeting['campus_code'],course)
                    m.save()
                    # Add instructors to meetings
                    for teacher in meeting['instructors']:
                        names = teacher.split(',')
                        last = names[0]
                        if len(names) > 1:
                            first = names[1].split(' ')[1] # clears out middle initial, if extant
                        else:
                            first = None
                        p, new = Professor.objects.get_or_create(last_name=last,
                                                                 first_name=first,
                                                                 )
                        p.departments.add(dept)
                        m.teachers.add(p)
                    
                    
                    
                    # spatial location of this meeting
                    #print "\tBuilding: ",meeting['building']
                    print "\t Building: ", meeting['building']
                    if not meeting['building']: # no building specified
                        meeting['building'] = "TBA"
                    try:
                        b = Building.objects.get(campus=m.campus,
                                         code=meeting['building'])
                    except ObjectDoesNotExist, e:
                        print 'no building with code {} and campus {}'.format(meeting['building'], m.campus)
                        b = Building.objects.get(code=meeting['building'])
                    room, new = Room.objects.get_or_create(building=b,
                                                       title=meeting['room'])
                    
                    is_arr = b.code == "ARR"
                    is_tba = b.code == "TBA"
                        
                    # temporal location of this meeting
                    for day in meeting['days']:
                        
                        if day == '-': continue # don't care about days we don't meet on
                        #print "\t", day
                        d = DAY_LOOKUP[day]
                        
                        try:
                            starter = datetime.datetime.strptime(meeting['start_time'],"%H%M")
                        except ValueError, e:
                            print e
                            starter = datetime.datetime.strptime(meeting['start_time'].zfill(2),"%H%M")
                            
                        try:
                            ender = datetime.datetime.strptime(meeting['end_time'],"%H%M")
                        except ValueError, e:
                            print e
                            ender = datetime.datetime.strptime(meeting['end_time'].zfill(2),"%H%M")
                        
                        t, new = Timeslot.objects.get_or_create(
                                                            starts=starter,
                                                            ends=ender,
                                                            day=d
                                                            )
                    
                        # Finally register the meeting with a timeslot (in a room)
                        ri, new = RoomInfo.objects.get_or_create(meeting=m, 
                                                timeslot=t, 
                                                room=room,
                                                is_arr=is_arr,
                                                is_tba=is_tba)