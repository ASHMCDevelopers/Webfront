'''
Created on Apr 26, 2012

@author: Haak Saxberg
'''
from django.db import models

class Campus(models.Model):
    CAMPUSES = (
                    ('SC', 'Scripps'),
                    ('PZ', 'Pitzer'),
                    ('PO', 'Pomona'),
                    ('CM', 'Claremont-Mckenna'),
                    ('HM', 'Harvey Mudd'),
                    ('CG', 'Claremont Graduate University'),
                    ('KG', 'Keck Graduate Institute'), # Keck actually doesn't offer any classes. For real.
                    ('CU', 'Claremont Consortium'),
                    ('NA', 'No Specific Campus'),
                )
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=2, unique=True)

    class Meta:
        verbose_name_plural = "campuses"

    def __unicode__(self):
        return u"{}".format(self.title)

class Building(models.Model):
    BUILDINGS = (
                    ('HM',( 
                        ('BK', "Beckman"),
                        ("GA", "Galileo"),
                        ("HOSH", "Hoch"),
                        ('JA', "Jacobs"),
                        ("KE", "Keck"),
                        ("LAC", "LAC"),
                        ("MD", "Modular"),
                        ("ON", "Olin"),
                        ("PA", "Parsons"),
                        ("PL", "Platt"),
                        ("SP", "Sprague"),
                        ("TG", "TG"),
                        ("ARR","Arranged"),
                        ("TBA","To Be Arranged"),
                        )
                    ),
                    ('PZ',(
                            ('ATN', "Atherton Hall"),
                            ('AV', "Avery Hall"),
                            ("BD", "E&E Broad Center"),
                            ("BE", "Bernard Hall"),
                            ("BH", "Broad Hall"),
                            ("FL", "Fletcher Hall"),
                            ("GC", "Gold Student Center"),
                            ("GR", "Grove House"),
                            ("HO", "Holden Hall"),
                            ("MC", "McConnell Center"),
                            ("MH", "Mead Hall"),
                            ("OT", "Pitzer in Ontario"),
                            ("SB", "Sanborn Hall"),
                            ("SC", "Scott Hall"),
                            ("WST", "WST (??)"),
                            ("ARR","Arranged"),
                            ("TBA","To Be Arranged"),
                            )
                    ),
                    ('PO', (
                            ('AN', 'Andrew Science Bldg'),
                            ('BRDG', "Bridges Auditorium"),
                            ('BT', "Brackett Observatory"),
                            ('CA', "Carnegie Building"),
                            ("CR", "Crookshank Hall"),
                            ("EDMS", "Edmunds Building"),
                            ("GIBS", "Gibson Hall"),
                            ("HN", "Social Science Bldg"),
                            ("ITB", "Information Tech Bldg"),
                            ("LB", "Bridges Hall"),
                            ("LE", "Le Bus Court"),
                            ("LINC", "Lincoln Building"),
                            ("MA", "Mason Hall"),
                            ("ML", "Millikan Lab"),
                            ("OLDB", "Oldenbourg Center"),
                            ("PD", "Pendleton Dance Center"),
                            ("PR", "Pearsons Hall"),
                            ("RA", "Rains Center"),
                            ("REM", "Rembrandt Hall"),
                            ("SA", "Seaver Computing Ctr"),
                            ("SCC", "Smith Campus Center"),
                            ("SCOM", "Seaver Commons"),
                            ("SE", "Seaver South Lab"),
                            ("SL", "Seeley Science Library"),
                            ("SN", "Seaver North Lab"),
                            ("SVBI", "Seaver Bio Bldg"),
                            ("TE", "Seaver Theatre"),
                            ("THAT", "Thatcher Music Bldg"),
                            ("TR", "Biology Trailers"),
                            ("ARR","Arranged"),
                            ("TBA","To Be Arranged"),
                            )
                    ),
                    ('SC', (
                            ('AT', "Athletic Facility"),
                            ("BL", "Balch Hall"),
                            ("BX", "BX (??)"),
                            ("DN", "Richardson Studio"),
                            ("FRA", "Frankel Hall"),
                            ('HM', 'Edwards Humanities'),
                            ("LA", "Lang Art Studios"),
                            ("MT", "Malott Commons"),
                            ("PAC", "Performing Arts Center"),
                            ("ST", "Steele Hall"),
                            ("TIER", "Tiernant Field House"),
                            ("VN", "Vita Nova Hall"),
                            ("ARR","Arranged"),
                            ("TBA","To Be Arranged"),
                            )
                    ),                    
                    ('CM', (
                            ('AD', 'Adams Hall'),
                            ('BC', "Bauer South"),
                            ('BZ', 'Biszantz Tennis Center'),
                            ("DU", "Ducey Gym"),
                            ('KRV', "Kravitz Center"),
                            ('RN', "Roberts North"),
                            ('RS', "Roberts South"),
                            ("SM", "Seaman Hall"),
                            ("ARR","Arranged"),
                            ("TBA","To Be Arranged"),
                            )
                    ),
                    ('CG', (
                            ('BU', 'Burkle Building'),
                            ("ARR","Arranged"),
                            ("TBA","To Be Arranged"),
                            )
                    ),
                    ('CU',(
                        ('HD', "Honnold/Mudd Library"),
                        ("KS", "Keck Science Center"),
                        ("SSC", "Student Services Center"),
                        ("ARR","Arranged"),
                        ("TBA","To Be Arranged"),
                        )
                    ),
                )
    
    campus = models.ForeignKey(Campus)
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)
    
    class Meta:
        unique_together = (('campus','code'),)
    
    def __unicode__(self):
        return u"{} {}".format(self.campus.code, self.name)
    def __repr__(self):
        return u"<Building: {}:{}>".format(self.campus.code, self.code)

class Room(models.Model):    
    building = models.ForeignKey(Building)
    title = models.CharField(max_length=50)
    class Meta:
        unique_together = (('building','title'),)
        
    def __unicode__(self):
        return u"{} {} {}".format(self.building.campus.code, 
                                  self.building.code, 
                                  self.title)