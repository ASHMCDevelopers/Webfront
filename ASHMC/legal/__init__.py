from django.db.models.signals import post_syncdb

from .models import *

def create_constitution(sender, **kwargs):

    if Article.objects.count() != 0:
        return

    root = Article.objects.create(
        title="ASHMC Constitution"
    )

    article = Article.objects.create(
        parent=root,
        number=1,
        title="Name and Membership",
    )
    section = Article.objects.create(
        parent=article,
        number=1,
        body="This organization shall be known as the Associated Students of Harvey Mudd College, which is officially designated by the initials ASHMC.",
    )
    section = Article.objects.create(
        parent=article,
        number=2,
        body="All registered students of Harvey Mudd College shall be members of ASHMC. Students who are on official Leave of Absence, and are planning to return to HMC, may petition the student council to allow them to remain members of ASHMC. They must petition at least three weeks before they wish to be a member and must pay ASHMC dues as usual. Members of ASHMC shall have one vote each in ASHMC elections as well as in all properly instituted referendums and initiatives. Members of a class/dormitory shall have one vote each in the corresponding class/dormitory elections.",
    )

    article = Article.objects.create(
        parent=root,
        number=2,
        title="Elected and Appointed Offices",
    )
    section = Article.objects.create(
        parent=article,
        number=1,
        title="Elected Offices",
    )
    subsec = Article.objects.create(
        parent=section,
        number=1,
        body="The elected officers of ASHMC shall be President, Vice President, Treasurer, Social Chair, Committee for Activities Planning chair, Athletics Director, Judiciary Board Chair, Disciplinary Board chair, Dormitory Affairs Committee chair, and Senior, Junior, Sophomore, and Freshman Class Presidents.",
    )
    subsec = Article.objects.create(
        parent=section,
        number=2,
        body="All elected officers of ASHMC must be members of ASHMC.",
    )
    subsec = Article.objects.create(
        parent=section,
        number=3,
        body="No person shall hold two or more ASHMC elected offices and/or voting Council positions at the same time.",
    )
    subsec = Article.objects.create(
        parent=section,
        number=4,
        body="The offices of ASHMC president, treasurer, JB chair, and DB chair shall be filled by individuals.",
    )
    section = Article.objects.create(
        parent=article,
        number=2,
        body="Elections for ASHMC offices shall be held and offices elected between seven and five weeks before commencement.",
    )
    section = Article.objects.create(
        parent=article,
        number=3,
        title="Eligibility",
    )
    subsection = Article.objects.create(
        parent=section,
        number=1,
        body="All candidates must be members of ASHMC. Dormitory/class office candidates must be members of their respective dormitory/class.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=2,
        body="ASHMC presidential candidates must be either juniors or seniors during the academic year of their term of office.",
    )

post_syncdb.connect(create_constitution, dispatch_uid="legal_canonical_constitution")
