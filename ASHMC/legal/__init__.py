from django.db.models.signals import post_syncdb

from .models import *

def create_constitution(sender, **kwargs):

    if Article.documents.filter(title="ASHMC Constitution").count()> 0:
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
    section = Article.objects.create(
        parent=article,
        number=4,
        title="Procedures",
    )
    subsection = Article.objects.create(
        parent=section,
        number=1,
        body="ASHMC elections shall be directed by the Student Council.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=2,
        body="The quorum for ASHMC, and class, and dormitory elections shall be one half of the respective constituency, not including blank and illegal votes.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=3,
        body="All elections authorized by this Constitution shall be loosely guided by Robert's Rules of Order, Newly Revised and the ASHMC Bylaws.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=4,
        body="ASHMC office candidates shall be nominated by petitions bearing the signatures of ten percent of the members of ASHMC. No member of ASHMC may sign more then one petition per office per election.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=5,
        body="All voting for all ASHMC elections shall be by secret ballot.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=6,
        body="A simple majority of total votes cast excluding blanks and illegal votes is required for election.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=7,
        body="Runoff elections with two candidates on the ballot shall be decided by a simple majority of total votes cast, excluding blanks, illegal votes and write-ins.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=8,
        body="Recall of any elected officers may be initiated by a petition bearing the signatures of one-third of the respective constituency. Successful removal of such an officer shall require a three-fourths majority of the total votes cast, excluding blanks and illegal votes, of a two-thirds quorum of the respective constituency. The recall vote shall be held within two weeks, excluding vacation periods, following the presentation of the petition to Student Council.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=9,
        body="Legal votes (for an office) shall be defined as votes cast for eligible members of ASHMC.",
    )

    section = Article.objects.create(
        parent=article,
        number=5,
        title="Term of Office",
    )
    subsection = Article.objects.create(
        parent=section,
        number=1,
        body="The term of office for all elected student government officers shall begin the day following their election, and shall expire whenever they resign, are recalled, or their successor is elected, whichever comes first. Terms may overlap if agreed upon and the officers shall share a vote during that transition period.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=2,
        body="The new Judiciary and Disciplinary Boards shall be constituted and vote as specified for the Fall semester and shall be responsible for all new and continuing cases, effective upon a day to be determined by the new and outgoing Judiciary and Disciplinary Board chairs, within one month following the election of the new board.",
    )

    section = Article.objects.create(
        parent=article,
        number=6,
        body="Council shall fill any vacancy in an ASHMC office by holding a special election within a month after the vacancy occurs. Interim appointments by Student Council shall not exceed one month in duration.",
    )

    section = Article.objects.create(
        parent=article,
        number=7,
        body="If a vacancy occurs in the office of president, the vice president treasurer shall assume the duties of president until a new president is elected in accordance with Sections 3 and 4 of this article.",
    )

    section = Article.objects.create(
        parent=article,
        number=8,
        title="Appointed Offices",
    )
    subsection = Article.objects.create(
        parent=section,
        number=1,
        body="All appointed officers shall be responsible to the Student Council for the proper functioning of their offices.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=2,
        body="All officers appointed by Student Council must be members of ASHMC.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=3,
        body="The terms for the appointed offices shall not exceed the length of one school year.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=4,
        body="Vacancies in ASHMC appointed offices shall be filled within one month of their occurrence.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=5,
        body="Student Council shall create or destroy any appointed offices it deems necessary.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=6,
        body="All appointed officers and club presidents receiving ASHMC funds shall report to ASHMC upon request to give the status of their appointed office or club.",
    )

    section = Article.objects.create(
        parent=article,
        number=9,
        body="If a co-holder of an ASHMC, class, or dormitory elected office is unable to perform the duties of that office, the remaining co-holder(s) may continue to fill the office. If the co-holder who was previously unable to perform the duties of the office becomes able to resume the office, he or she may do so.",
    )

    article = Article.objects.create(
        parent=root,
        number=3,
        title="The Student Council",
    )

    section = Article.objects.create(
        parent=article,
        number=1,
        body="Student Council shall be the ASHMC legislative body. Each member of Student Council shall have one vote, except for the chair, who shall vote only in case of a tie. The vice president shall act as chair in the absence of the president at any given meeting.",
    )

    section = Article.objects.create(
        parent=article,
        number=2,
        title="Members of the Student Council",
    )
    subsection = Article.objects.create(
        parent=section,
        number=1,
        body="Student Council shall consist of the President, Vice President, Treasurer, Social Chair, Athletics Director, Dormitory Presidents, Dormitory Affairs Committee Chair, Committee for Activities Planning Chair, and the Senior, Junior, Sophomore, and Freshman class presidents.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=2,
        body="Every member of ASHMC shall be represented on Student Council by elected ASHMC officials.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=3,
        body="A quorum for any Student Council meeting shall be a majority of the entire membership.",
    )

    section = Article.objects.create(
        parent=article,
        number=3,
        title="The Student Council Shall",
    )
    subsection = Article.objects.create(
        parent=section,
        number=1,
        body="Have the power in all matters concerning ASHMC as a whole that are not specifically delegated to another authority.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=2,
        body="Be responsible for the enforcement of this Constitution and its Bylaws.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=3,
        body="Have sole authority and responsibility for the allocation of ASHMC funds. Any member of ASHMC may call for an annual audit of the financial records of ASHMC.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="Student referendum is required for the allocation of ASHMC general funds exceeding $1,500, regardless of their source or sources. A referendum is also required for any organization whose total budget requests, including mid-year budget requests, exceed $1,500 of ASHMC general funds.  In the case of charges that ASHMC is legally bound to pay, no student referendum is needed, but the student body shall be informed of this cost.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=2,
        body="Amounts not exceeding $1,000 are subject to change by Council vote for one week following their appropriation by Student Council.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=3,
        body="Any non-budgeted financial obligation entered into by Student Council shall not take effect until after the next Student Council meeting following the allocation of funds by Student Council.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=4,
        body="The fee set for the ASHMC tax filing shall be considered a fixed expense as set by ASHMC's accountant.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=5,
        body="The amount each dormitory is entitled to receive per dormitory member per semester, from ASHMC, shall be a fixed fee.",
    )

    section = Article.objects.create(
        parent=article,
        number=4,
        title="Duties of the Officers",
    )
    subsection = Article.objects.create(
        parent=section,
        number=1,
        title="The President Shall",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="Act as the executive head of ASHMC.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=2,
        body="Represent the best interests of ASHMC to members of the administration and faculty of Harvey Mudd College, and to organizations of The Claremont Colleges and in the Claremont community.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=3,
        body="Prepare an Agenda for every Council meeting.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=4,
        body="Attend or appoint someone to attend 5-College Executive Council meetings.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=5,
        body="Attend or appoint someone to attend  Faculty Executive Committee meeetings and Board of Trustees meetings.",
    )

    subsection = Article.objects.create(
        parent=section,
        number=2,
        title="The Vice President Shall",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="Record the business of all the Student Council meetings and post the minutes within three days of those meetings.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=2,
        body="Carry on all official correspondence of ASHMC.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=3,
        body="Be responsible for keeping all communications of the ASHMC Council.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=4,
        body="Be responsible for conducting ASHMC elections that Student Council shall direct.",
    )

    subsection = Article.objects.create(
        parent=section,
        number=3,
        title="The Treasurer Shall",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="Be responsible for the handling of all ASHMC funds.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=2,
        body="Maintain precise and up-to-date financial records of ASHMC's general fund.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=3,
        body="Be responsible for auditing ASHMC's finances by 2 weeks before ASHMC budgeting.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=4,
        body="Make an annual survey of investment opportunities available and report to the council which is the optimum investment for ASHMC.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=5,
        body="Assure that the year end cash balance does not exceed $500, excluding the following fiscal year's financial bubble and any funds set aside for a planned purchase of long-life assets. If a surplus will exist at the end of the fiscal year, purchases of long-life assets of use or value to ASHMC will be made or planned.",
    )

    subsection = Article.objects.create(
        parent=section,
        number=4,
        title="The Social Chair Shall",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="Be chair of the Social Committee and be responsible to Student Council for its proper functioning.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=2,
        body="Be responsible to regularly inform the dormitory social directors of upcoming social events to aid dormitories in scheduling events.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=3,
        body="Attend or appoint someone to attend 5-College Social Affairs Council meetings.",
    )

    subsection = Article.objects.create(
        parent=section,
        number=5,
        title="The Athletic Director Shall",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=3,
        body="Be chair of the Athletic Committee and be responsible to the Student Council for its proper functioning.",
    )

    subsection = Article.objects.create(
        parent=section,
        number=6,
        title="Each of the Dormitory Presidents Shall",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="Be the chief spokesman for the dormitory and represent its best interests to members of the college community.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=2,
        body="Be a member of the Dormitory Affairs Committee.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=3,
        body="Be responsible for developing dormitory regulations to be approved by the dormitory within two weeks after the beginning of the school year.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=4,
        body="Be responsible for the actions of every official dormitory officer, insuring that these officers fulfill their obligations.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=5,
        body="Keep the dormitory updated on developments in student government.",
    )

    subsection = Article.objects.create(
        parent=section,
        number=7,
        title="The Senoir, Junior, Sophomore and Freshman Class Presidents Shall",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="Be the chief spokesman for their class and represent its best interests to members of the college community.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=2,
        body="Be members on the Class Presidents Committee.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=3,
        body="Keep their class updated on relevant developments in student government and campus events.",
    )

    subsection = Article.objects.create(
        parent=section,
        number=8,
        title="The Committee for Activities Planning Shall",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="Be chair of the Committee for Activities Planning and be responsible to the student council for its proper functioning.",
    )

    subsection = Article.objects.create(
        parent=section,
        number=9,
        title="The Dormitory Affairs Committee Chair Shall",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="Be chair of the Dormitory Affairs Committee and be responsible to the Student Council for its proper functioning.",
    )

    article = Article.objects.create(
        parent=root,
        number=4,
        title="ASHMC Legislative Procedures",
    )
    section = Article.objects.create(
        parent=article,
        number=1,
        body="Student Council shall maintain a system of Bylaws to supplement this Constitution. A Bylaw may be added, deleted, modified or temporarily suspended by a three-fourths majority vote of the entire membership of Student Council for a maximum duration of the remaining length of the current Student Council's term.",
    )
    section = Article.objects.create(
        parent=article,
        number=2,
        title="Initiative and Referendum",
    )
    subsection = Article.objects.create(
        parent=section,
        number=1,
        body="Members of ASHMC may institute an initiative or referendum by petition of at least one-third of the members of ASHMC.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=2,
        body="Student Council, by a majority vote of the entire membership, may hold a referendum concerning any seconded motion made during a Student Council meeting.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=3,
        body="Student Council shall call an ASHMC convocation for the purpose of discussing any properly instituted initiative or referendum and shall hold an election for its ratification within four weeks of its presentation to Student Council.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=4,
        body="A simple majority of votes cast with a quorum of half of ASHMC is necessary for the passage of such measures.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=5,
        body="The results of all properly instituted and executed initiatives and referenda are binding.",
    )

    section = Article.objects.create(
        parent=article,
        number=3,
        title="Proposed Constitutional Amendments and New ASHMC Constitutions",
    )
    subsubsection = Article.objects.create(
        parent=section,
        number=1,
        body="Amendments to this Constitution or new ASHMC Constitutions may be proposed by Student Council or by petition of at least one-third of the members of ASHMC.",
    )
    subsubsection = Article.objects.create(
        parent=section,
        number=2,
        body="Student Council shall call an ASHMC convocation for the purpose of discussing the constitutional amendment or the new ASHMC Constitution and shall hold an election for its ratification within four weeks of its presentation to Student Council. An amendment or new Constitution shall be established by a two-thirds majority of the total votes cast, excluding blanks, with a quorum of three-fifths of the members of ASHMC.",
    )
    subsubsection = Article.objects.create(
        parent=section,
        number=3,
        body="Article VII, Sections 1 and 2 of this Constitution dealing with the Honor Code and the Disciplinary Code at Harvey Mudd College can be changed only with the approval of the faculty and administration in a manner they see appropriate, and with the approval of the students as outlined in this Constitution.",
    )

    article = Article.objects.create(
        parent=root,
        number=5,
        title="ASHMC Committees",
    )
    section = Article.objects.create(
        parent=article,
        number=1,
        title="Social Committee",
    )
    subsection = Article.objects.create(
        parent=section,
        number=1,
        body="The Social Committee shall consist of the social chair and the dormitory social directors.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=2,
        title="The Social Committee Shall",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="Coordinate budgeting of all social activities for ASHMC.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=2,
        body="Be responsible for the execution of dorm events subject to review by Student Council.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=3,
        body="Promote 5-College activities.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=3,
        body="All Social Committee policy, operating procedures, and expenditures exceeding $60 shall be determined by a majority vote of the entire membership, excluding blanks and abstentions.",
    )

    section = Article.objects.create(
        parent=article,
        number=2,
        title="Athletic Committee",
    )
    subsection = Article.objects.create(
        parent=section,
        number=1,
        body="The Athletic Committee shall consist of the athletic director and the dormitory athletic directors.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=2,
        body="The Athletic Committee Shall",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="Promote intramural competition.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=2,
        body="Promote support for the college's intercollegiate athletic program.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=3,
        body="Valuate and fund requests for dorm athletic equipment.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=3,
        body="All expenditures over $100 shall be determined by a majority vote of the entire Athletics Committee membership. All other Athletics Committee policy and operating procedures shall be determined by a majority vote of the entire membership.",
    )

    section = Article.objects.create(
        parent=article,
        number=3,
        title="Committee for Activities Planning",
    )
    subsection = Article.objects.create(
        parent=section,
        number=1,
        title="Composition",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="The Committee for Activities Planning shall consist of an elected chair and a representative from each dorm. A representative from the Dean of Students Office is a nonvoting member.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=2,
        title="Duties of Officers",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="The chair shall run committee meetings, be a member of student council, and be responsible for the proper functioning of the Committee for Activities Planning.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=2,
        body="Coordinate events with the Linde Activities Center events planning group, the Dean of Students Activities Planners, and related clubs.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=3,
        title="Duties of the Campus Center Committee",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="The Committee for Activities Planning shall provide for the planning and promotion of non-dorm based events. This committee shall also establish and promulgate rules of personal conduct for Campus Center activities.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=2,
        body="All Committee for Activities Planning policy and operating procedures shall be determined by a majority vote of the entire membership, excluding blanks and abstentions.",
    )

    section = Article.objects.create(
        parent=article,
        number=4,
        title="Dormitory Affairs Committee",
    )
    subsection = Article.objects.create(
        parent=section,
        number=1,
        title="Composition",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="The Dormitory Affairs Committee shall consist of an elected chair, the social chair, and the dormitory presidents. A representative of the Dean of Students Office and a representative from the Facilities and Maintenance Office are nonvoting members.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=2,
        title="Duties of Officers",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="The chair shall run committee meetings, appoint a secretary, be a member of Student Council, and be responsible for the execution of committee policies.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=2,
        body="The secretary shall take, distribute, and post minutes of all committee meetings within three days of their occurrence.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=3,
        title="Duties of the Dormitory Affairs Committee",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="The Dormitory Affairs Committee has the power to propose new dormitory and campus policies, subject to approval by Student Council.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=2,
        body="After approval by Student Council, the dean of students is to be given a copy of the proposed policy. Upon approval, the policy shall go into effect immediately. Otherwise, the Dean must veto the proposal and state all objections in writing within ten days, excluding vacation periods. If this ten-day period passes with no response from the dean of students, the policy shall go into effect immediately.",
    )

    section = Article.objects.create(
        parent=article,
        number=5,
        title="Class Presidents Committee",
    )
    subsection = Article.objects.create(
        parent=section,
        number=1,
        body="The Class Presidents Committee shall consist of the Senior, Junior, Sophomore, and Freshman class presidents.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=2,
        body="The Senior Class President shall chair the Class Presidents Committee.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=3,
        title="Duties of the Officers",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="Each officer shall be responsible for allocating their funding to be used for the benefit of their class.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=2,
        body="The Senior Class President shall be responsible for setting agendas and running the meetings of the Class Presidents Committee.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=3,
        body="The Class Presidents Committee shall work with relevant clubs to organize the Frosh-Soph games and the Five Class Competition.",
    )

    section = Article.objects.create(
        parent=article,
        number=6,
        body="ASHMC committees shall make regular and timely reports to Student Council.",
    )

    section = Article.objects.create(
        parent=article,
        number=7,
        body="Student Council shall establish any other committees it deems necessary and dissolve any committees it deems unnecessary.",
    )

    section = Article.objects.create(
        parent=article,
        number=8,
        body="All ASHMC Committees shall hold regular meetings, with a minimum of one per month.",
    )

    article = Article.objects.create(
        parent=root,
        number=6,
        title="Class and Dormitory Government",
    )
    section = Article.objects.create(
        parent=article,
        number=1,
        title="Class Officers",
    )
    subsection = Article.objects.create(
        parent=section,
        number=1,
        body="All class offices are to be filled by individuals or to be shared between two individuals.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=2,
        body="The rising Sophomores shall elect at large the Sophomore Class President(s) and four Judiciary Board members within five weeks of the close of the school year. The rising Junior and Senior classes shall elect at large their class president(s), and six Judiciary Board members, and one Appeals Board member within five weeks of the close of the school year.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=3,
        body="The incoming freshman class shall elect at large the Freshman Class President(s) within one month of its arrival. During the last month of the first semester, the freshman class shall elect at large four Judiciary Board members who will serve during the second semester.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=4,
        body="The election of all class officers must conform with Article II.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=5,
        title="Each class president shall",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="Be the chief spokesmen for their class and represent its best interest to the members of the college.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=2,
        body="Be a member of the ASHMC council and the Class Presidents Committee",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=3,
        body="Coordinate activities for his/her class.",
    )
    section = Article.objects.create(
        parent=article,
        number=2,
        title="Dormitory Officers",
    )
    subsection = Article.objects.create(
        parent=section,
        number=5,
        body="Each dormitory shall elect a president, a treasurer, an athletic director, a social director, a recycling director, and a Committee for Activities Planning representative, within three weeks of the close of the school year.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=5,
        title="The election of all dormitory officers will consist of the following",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="A one-week nominating period.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=2,
        body="A one-week voting period.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=3,
        body="The Student Council retains power to review and resolve all dormitory voting procedures.",
    )

    section = Article.objects.create(
        parent=article,
        number=3,
        body="If a vacancy occurs in one of the sets of officers mentioned in Article VI, Sections 1 or 2, the group concerned must fill it by a special election within a month (not including vacation periods) of the vacancy. The election must conform with Article II. The class vice president shall assume the duties of the class president until a new class president is elected.",
    )

    section = Article.objects.create(
        parent=article,
        number=4,
        body="Each dormitory shall be responsible for the enforcement of its dormitory regulations and those legislated by the Dormitory Affairs Committee.",
    )

    section = Article.objects.create(
        parent=article,
        number=5,
        body="All rights not given to the Student Council, Judiciary Board, Disciplinary Board, or Appeals Board shall be reserved for the classes and dormitories.",
    )

    article = Article.objects.create(
        parent=root,
        number=7,
        title="The Student Judicial System",
    )
    section = Article.objects.create(
        parent=article,
        number=1,
        title="The Honor Code",
    )
    subsection = Article.objects.create(
        parent=section,
        number=1,
        body="All members of ASHMC are responsible for maintaining their integrity and the integrity of the college community in all academic matters and in all affairs concerning the community.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=2,
        body="Any member of the Harvey Mudd College community who observes an Honor Code violation shall report the violation to the Judiciary Board chair stating the offense and the names of all parties involved. Either party may request a hearing or may seek an out-of court settlement in consultation with the Judiciary Board chair. The Judiciary Board chair shall keep a complete record of all such settlements. The procedures for pursuing a Judiciary Board hearing shall be specified in the Bylaws of Constitution.",
    )
    section = Article.objects.create(
        parent=article,
        number=2,
        title="The Disciplinary Code",
    )
    subsection = Article.objects.create(
        parent=section,
        number=1,
        body="All members of ASHMC are responsible for observing all nonacademic college rules and regulations, including those related to college property.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=2,
        body="All members of the Harvey Mudd College community agree to report violations of the Disciplinary Code to the Disciplinary Board chair. Either party may request a hearing or may seek an out-of-court settlement in consultation with the Disciplinary Board chair. The Disciplinary Board chair will keep a complete record of all such settlements. The procedures for pursuing a Disciplinary Board hearing shall be specified in the Bylaws of Constitution.",
    )
    section = Article.objects.create(
        parent=article,
        number=3,
    )
    subsection = Article.objects.create(
        parent=section,
        number=1,
        title="The Judiciary Board Chair shall",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="Arrange for a meeting between the Judicial Board and the appropriate faculty to discuss the Honor Code and the Judicial System. After this meeting the chair shall prepare a presentation to the entire faculty describing the HMC community's views regarding these topics as soon as possible.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=2,
        body="Present to the entering freshman class with the Disciplinary Board chair during orientation a thorough description of the HMC community's views regarding the Honor Code and the Judicial System, including possible punishments.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=3,
        body="Fulfill all other duties as specified in the Honor System.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=2,
        title="The Disciplinary Board Chair shall",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="Present to the entering freshman class with the Judiciary Board chair during orientation a thorough description of the HMC community's views regarding the Honor Code and the Judicial System, including possible punishments.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=2,
        body="Fulfill all other duties as specified in the Honor System.",
    )
    article = Article.objects.create(
        parent=root,
        number=8,
        title="Interpretation of the Constitution",
    )
    section = Article.objects.create(
        parent=article,
        number=1,
        body="The Judiciary Board shall interpret any clause of the ASHMC Constitution as it pertains to any specific situation, within two weeks (excluding vacation periods) following a request to do so by any member of ASHMC.",
    )

    article = Article.objects.create(
        parent=root,
        number=9,
        title="Ratification and Government Continuity",
    )
    section = Article.objects.create(
        parent=article,
        number=1,
        body="All debts contracted and engagements entered into by ASHMC before this Constitution came into effect will continue to be honored after it has come into effect.",
    )
    section = Article.objects.create(
        parent=article,
        number=2,
        body="All laws and regulations passed by previous Student Councils shall remain valid provided they do not conflict with this Constitution.",
    )
    section = Article.objects.create(
        parent=article,
        number=3,
        body="This Constitution shall go into effect on May 1, 1977."
    )
    section = Article.objects.create(
        parent=article,
        number=4,
        body="Revised and approved on October 1, 2007",
    )

post_syncdb.connect(create_constitution, dispatch_uid="legal_canonical_constitution")


def create_bylaws(sender, **kwargs):
    if Article.documents.filter(title='ASHMC Bylaws').count() > 0:
        return
    root = Article.objects.create(
        title="ASHMC Bylaws",
    )

    article = Article.objects.create(
        parent=root,
        number=1,
        title="ASHMC Policies",
    )
    section = Article.objects.create(
        parent=article,
        number=1,
        body="ASHMC will not, per terms of the articles, act in any substantial part of its activities, attempt to influence legislation, or participate to any extent in a political campaign for or against any candidate for public office.",
    )
    section = Article.objects.create(
        parent=article,
        number=2,
        body="ASHMC will not operate for benefit of private interests.",
    )
    section = Article.objects.create(
        parent=article,
        number=3,
        body="ASHMC does not and will not discriminate on the basis of race, color, sex, gender, sexual orientation, age, marital status, religion, disability, national origin, ethnic origin, or prior military service in any of its policies, procedures and practices.",
    )

    article = Article.objects.create(
        parent=root,
        number=2,
        title="Dormitory Status",
    )
    section = Article.objects.create(
        parent=article,
        number=1,
        body="The dormitories are Mildred E. Mudd (East), Marks (South), North, West, Atwood, Case, Linde and Sontag.",
    )

    article = Article.objects.create(
        parent=root,
        number=3,
        title="The Student Council",
    )
    section = Article.objects.create(
        parent=article,
        number=1,
        body="Student Council shall hold weekly meetings. Regular meetings may be rescheduled by the ASHMC president if there are no objections by the Council. In case of an objection, the rescheduling may be approved by a majority vote of the Student Council. Meetings may be canceled by a majority vote of the entire membership of the Student Council.",
    )
    section = Article.objects.create(
        parent=article,
        number=2,
        body="If a voting member of the Student Council does not attend or send a proxy to a scheduled Student Council meeting, they will be given a verbal or written warning. The second missed meeting in a semester will result in a written warning. If a member misses any further meetings (greater than two), then the elected official will be fined a sum of $50 for each meeting missed. All fines collected will go into the ASHMC general fund. Fines not paid in full by the end of the semester will result in a withholding of the following semester's budgeted funds. Fines not paid in full before the election of the new council will result in a formal charge to the Judiciary Board.",
    )
    section = Article.objects.create(
        parent=article,
        number=3,
        body="If a member is not present for a full meeting of the Student Council, then by a two-thirds majority vote, the remainder of Council can declare this as an absence.",
    )

    article = Article.objects.create(
        parent=root,
        number=4,
        title="Elections",
    )
    section = Article.objects.create(
        parent=article,
        number=1,
        body="During all student elections on the HMC campus, ASHMC members shall not:",
    )
    subsection = Article.objects.create(
        parent=section,
        number=1,
        body="Display campaign signs or actively campaign within the dining hall.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=2,
        body="Deface or remove Dean of Students approved campaign signs posted in public areas on the HMC campus prior to the election to which they pertain.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=3,
        body="Vote or attempt to vote more than once in any given election.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=4,
        body="Interfere with any ASHMC member during the voting process.",
    )

    section = Article.objects.create(
        parent=article,
        number=2,
        title="General Procedures",
    )
    subsection = Article.objects.create(
        parent=section,
        number=1,
        body="Election polls will be open during the normal hours for lunch and dinner on at least two consecutive days.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=2,
        body="The ASHMC Executive Assistant shall post signs on the dining hall to inform ASHMC members of the upcoming election.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=3,
        body="All ASHMC signs must contain the dates of the election, the place where the election is being held, and the hours during which the polls will be open.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=4,
        body="All dormitory presidents shall inform their dorm members of the upcoming election.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=5,
        body="The election shall be staffed by officers of the group holding the election or their designated representatives. Candidates in the election may not run the ballot boxes. People running the ballot boxes during elections are not allowed to recommend candidates, even if asked to do so by voters.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=6,
        body="Official ballots shall contain only legal candidates as specified in Article II of the ASHMC Constitution, and must have a write-in option, except in runoff elections.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=7,
        body="Students studying abroad may cast their votes by e-mail through the Dean of Students office.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=8,
        body="After quorum is met, the Vice President shall send out notification to the student body that quorum has been reached and that the elections will continue for one additional day during normal hours for lunch and dinner.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=9,
        body="A recount of votes shall be conducted in each election by the President of ASHMC, If this recount does not agree with the Vice President's initial count, both parties shall recount ballots until the two counts agree.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=10,
        body="Results will be announced no less than 24 and no more than 36 hours after the election has concluded. Any protest must be filed with the Judiciary Board chair within 24 hours of the announcement of the results.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=11,
        body="After an election, ballots shall remain intact for one week after the results have been announced. After this point, all ballots must be destroyed.",
    )

    section = Article.objects.create(
        parent=article,
        number=3,
        title="Electronic Voting Procedures",
    )
    subsection = Article.objects.create(
        parent=section,
        number=1,
        body="In place of the process described in Section 2, any ASHMC election may be run with an electronic voting system, at the discretion of the officer responsible for the election. The system to be used must have been previously approved by Student Council.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=2,
        body="An electronic voting system must be approved by three-fourths majority vote of the entire membership of Student Council. They should consider whether the system is easy to use, anonymous, and secure against fraud. Approval of a system may later be withdrawn by a simple majority of Student Council.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=3,
        body="An electronic election begins when ASHMC members are notified that they may vote. The election ends at midnight (or other pre-specified time) after quorum is reached except that the election shall last at least 48 hours.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=4,
        body="Elections shall be announced by e-mail, and by other means as desired. E. The voting system shall be administered by the ASHMC secretary or his or her representative. No candidate in the election shall administer the voting system.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=5,
        body="The provisions of Section 2, Paragraphs F and G apply to electronic elections.",
    )
    section = Article.objects.create(
        parent=article,
        number=4,
        title="Order of Yearly Elections",
    )
    subsection = Article.objects.create(
        parent=section,
        number=1,
        body="The first election for new officers shall be for the offices of Judiciary Board chair, Disciplinary Board chair, and all other ASHMC-elected and dormitory officers.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=2,
        body="The second election shall begin before commencement. This election shall contain any items over $1,500 in the next year's budget. This election shall also be for class officers under the following rules.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="Current dormitory presidents are responsible for holding elections for new dormitory officers. Those offices are president, treasurer, recycler and representatives to the ASHMC Social Committee, Athletics Committee, Food Committee, Committee for Activities Planning and any other elected positions that the dormitory has established.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=2,
        body="Current dormitory presidents shall notify their respective dormitories and solicit candidates for the upcoming election.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=3,
        body="Current dormitory presidents shall announce the candidates, and must have a write-in option, except in runoff elections. Eligible candidates for a dorm election are those students who have legitimately pulled into a room in that specific dorm during room draw of the current year.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=4,
        body="Eligible voters for a dorm election are those students who have legitimately pulled into a room in that specific dorm during room draw of the current year, seniors currently living in that dorm, and students who have not pulled into a room but have chosen to affiliate themselves with that dorm. A list of eligible voters shall be obtained from the Dormitory Affairs Committee chair following room draw. All eligible voters are entitled to one vote for each office.",
    )

    article = Article.objects.create(
        parent=root,
        number=5,
        title="Appointed Positions",
    )
    section = Article.objects.create(
        parent=article,
        number=1,
        body="As soon as is practical, the new Student Council shall appoint:",
    )
    subsection = Article.objects.create(
        parent=section,
        number=1,
        body="An ASHMC Executive Assistant (EA)",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="The EA reports to the President, Vice President and Treasurer (Executive Council) in that order.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=2,
        body="The duties of the EA shall be to",
    )
    subsubsubsection = Article.objects.create(
        parent=subsubsection,
        number=1,
        body="Record the business of all the student council meetings and post the minutes within three days of those meetings.",
    )
    subsubsubsection = Article.objects.create(
        parent=subsubsection,
        number=2,
        body="Be available to assist members of the executive council at any events pertinent to ASHMC.",
    )
    subsubsubsection = Article.objects.create(
        parent=subsubsection,
        number=3,
        body="Be responsible for carrying out misc. tasks assigned by the Executive Council",
    )
    subsubsubsection = Article.objects.create(
        parent=subsubsection,
        number=4,
        body="Manage ashmc@hmc.edu e-mail account (i.e. forward to the proper person)",
    )
    subsubsubsection = Article.objects.create(
        parent=subsubsection,
        number=5,
        body="Be responsible for advertising all ASHMC sponsored activities and events.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=3,
        body=" In the case that the Dean of Students office (DOS) is willing to donate work study hours, the EA position can be a work study job hired by the Executive Council and supervised by DOS. Otherwise, this position will be unpaid like other ASHMC positions.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=2,
        body="An ASHMC Historian.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="The ASHMC historian shall, in the historical records, try to capture the spirit of student life, past and present.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=2,
        body="The duties of the ASHMC Historian shall be to:",
    )
    subsubsubsection = Article.objects.create(
        parent=subsubsection,
        number=1,
        body="Research and prepare written histories of the various traditions of Harvey Mudd College student life.",
    )
    subsubsubsection = Article.objects.create(
        parent=subsubsection,
        number=2,
        body="Maintain written records of the various ASHMC and dormitory officials and chronicle the noteworthy events of their office.",
    )
    subsubsubsection = Article.objects.create(
        parent=subsubsection,
        number=3,
        body="Maintain written records of important developments among the faculty and administration.",
    )
    subsubsubsection = Article.objects.create(
        parent=subsubsection,
        number=4,
        body="Maintain written records of any other events that are deemed to be important.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=3,
        body="The ASHMC Historian shall be empowered to",
    )
    subsubsubsection = Article.objects.create(
        parent=subsubsection,
        number=1,
        body="Appoint a staff as needed to fulfill the duties of the office.",
    )
    subsubsubsection = Article.objects.create(
        parent=subsubsection,
        number=2,
        body="Receive the written minutes or summaries of the various committees.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=3,
        body="An ASHMC Film Director.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="The ASHMC film director shall preside over the regular, scheduled showing of films according to the wants and desires of the Harvey Mudd College community. The ASHMC film director shall decide on both a location and time for the films to be shown, as well as publicize the event beforehand.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=4,
        body="An ASHMC Recycling Director.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="The ASHMC recycling director shall be responsible for finding a representative from each dorm to assist in moving each dorm's recycling bin to the campus collection center each week. The ASHMC recycling director shall also act as a liaison to Facilities and Maintenance regarding recycling issues.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=5,
        body="An ASHMC Director of Student Security",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="The ASHMC director of Student Security shall be responsible for selecting members of ASHMC to be student security officers, and shall be responsible to the ASHMC Student Council for the proper functioning of ASHMC student security.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=6,
        body="An ASHMC Newspaper Editor.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="The ASHMC newspaper editor shall act as editor in chief for the ASHMC sponsored student newspaper.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=7,
        body="An ASHMC Food Committee Chair.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="The ASHMC food committee chair shall be chair of the Food Committee and be responsible to the ASHMC Student Council for its proper functioning.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=8,
        body="An ASHMC Students-L Moderator.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="The ASHMC students-l moderator shall be responsible for assuring that all messages sent to the students-l electronic mailing list conform to the official students-l policy listed in the Policies section of the student handbook.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=2,
        body="The students-l moderator shall receive a yearly stipend as determined by the Student Council.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=9,
        body="An ASHMC Volunteer Activities Coordinator.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="The duties of the ASHMC volunteer activities coordinator shall be to",
    )
    subsubsubsection = Article.objects.create(
        parent=subsubsection,
        number=1,
        body="Hold monthly or bimonthly meetings open and advertised to the students, faculty and staff of Harvey Mudd College. Said meetings will describe upcoming opportunities to enrich the college community or the community at large through volunteer service. The first meeting of the school year shall be before McAlister Center's Volunteer Study Break.",
    )
    subsubsubsection = Article.objects.create(
        parent=subsubsection,
        number=2,
        body="See to the upkeep and currency of the Volunteer Opportunities board, by removing outdated notices and posting new community service articles.",
    )
    subsubsubsection = Article.objects.create(
        parent=subsubsection,
        number=3,
        body="Organize or find community members to organize traditional Harvey Mudd College volunteer events, such as but not limited to the Red Cross Blood Drive (both semesters), the Oxfam Fast for the Hungry (November), and Shoes that Fit (both semesters).",
    )
    subsubsubsection = Article.objects.create(
        parent=subsubsection,
        number=4,
        body="Meet at least once a semester with the Dean of Students Office and the volunteer activities faculty contact to share ideas and discuss possible faculty and staff involvement. If no faculty contact exists, the ASHMC volunteer activities coordinator shall make a reasonable search for a new faculty contact.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=10,
        body="An ASHMC Alumni Board Representative.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="The duties of the ASHMC Alumni Board representative shall be to",
    )
    subsubsubsection = Article.objects.create(
        parent=subsubsection,
        number=1,
        body="Be the student representative to the Alumni Board and be represented at a majority of the Alumni Board meetings.",
    )
    subsubsubsection = Article.objects.create(
        parent=subsubsection,
        number=2,
        body="Report to Student Council on the results of all Alumni Board meetings.",
    )
    subsubsubsection = Article.objects.create(
        parent=subsubsection,
        number=3,
        body="Work closely with all student government groups in order to best represent ASHMC to the Alumni Board.",
    )
    subsubsubsection = Article.objects.create(
        parent=subsubsection,
        number=4,
        body="Promote communication between alumni and students.",
    )
    subsubsubsection = Article.objects.create(
        parent=subsubsection,
        number=5,
        body="Promote the activities of the Alumni Office to the students.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=11,
        body="An ASHMC Representative to the Traffic Appeals Board.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="The ASHMC representative to the Traffic Appeals Board shall be responsible for presenting the opinions and concerns of ASHMC to the Traffic Appeals Board and participating in its regular business.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=12,
        body="An ASHMC Representative to the HMC Computer Committee.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="The ASHMC representative to the HMC Computer Committee shall be responsible for presenting the opinions and concerns of ASHMC to the HMC Computer Committee.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=13,
        body="An ASHMC Representative to the Student Relations Subcommittee of the Library Council.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="The ASHMC representative to the Student Relations Subcommittee of the Library Council shall be responsible for presenting the opinions and concerns of ASHMC to the Student Relations Subcommittee of the Library Council.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=14,
        body="Five ASHMC representatives to the Student Health Advisory Committee.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="The ASHMC representatives to the Student Health Advisory Committee shall be responsible for presenting the opinions and concerns of ASHMC to the Student Health Advisory Committee, Baxter Health Center and Monsour Counseling Center. The representatives shall also be responsible for promoting student health and wellness issues.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=15,
        body="Two ASHMC Representatives to the Teaching and Learning Committee.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="The ASHMC representatives to the Teaching and Learning Committee shall be responsible for presenting the opinions and concerns of ASHMC to the Teaching and Learning Committee.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=16,
        body="One ASHMC Representative to the Curriculum Committee.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="The ASHMC representative to the Curriculum Committee shall be responsible for presenting the opinions and concerns of ASHMC to the Curriculum Committee.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=17,
        body="An ASHMC Librarian",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="The ASHMC Librarian's duties shall include",
    )
    subsubsubsection = Article.objects.create(
        parent=subsubsection,
        number=1,
        body="Organizing the ASHMC Library (the Joe Platt collection). This may include discarding unwanted material, devising a way to store the library that is in accordance with the wishes of ASHMC, and/or creating a system for the use of the library.",
    )
    subsubsubsection = Article.objects.create(
        parent=subsubsection,
        number=2,
        body="Carrying out the wishes of the ASHMC council in regards to valuable books contained in the ASHMC library.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=18,
        body="Representative to \"Writing in the Curriculum\"",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="Representative's duties are to be a part of a committee whose purpose is to monitor and improve the quality and extent of writing throughout the curriculum.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=19,
        body="Representative to the 5-College Environmental Review Committee",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body=" Representative's duties are to be a part of the 5-College Environmental Review Committee.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=20,
        body="Representative to the Board of Trustees Educational Planning Committee",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="Be the student representative to the Educational Planning Committee of the Harvey Mudd College Board of Trustees.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=2,
        body="Attend all appropriate student government meetings in order to keep informed of all pertinent developments.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=3,
        body="Report to Student Council on the results of all Board of Trustees Educational Planning Committee meetings.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=4,
        body="Work closely with all student government groups in order to best represent ASHMC to the Board of Trustees.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=5,
        body="Work with the student representative to the Board of Trustees Student Affairs Committee and the student representative to the Board of Trustees Campus Planning and Physical Plant Committee to promote communication between the students and the BOT.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=6,
        body="Present to ASHMC Council ideas for promoting communication between students and the BOT.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=21,
        body="Representative to the Board of Trustees Student Affairs Committee",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="Be the student representative to the Student Affairs Committee of the Harvey Mudd College Board of Trustees.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=2,
        body="Attend all appropriate student government meetings in order to keep informed of all pertinent developments.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=3,
        body="Report to Student Council on the results of all Board of Trustees Student Affairs Committee meetings.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=4,
        body="Work closely with all student government groups in order to best represent ASHMC to the Board of Trustees.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=5,
        body="Work with the student representative to the Board of Trustees Educational Planning Committee and the student representative to the Board of Trustees Campus Planning and Physical Plant Committee to promote communication between the students and the BOT.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=6,
        body="Present to ASHMC Council ideas for promoting communication between students and the BOT.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=22,
        body="Representative to the Board of Trustees Campus Planning and Physical Plant Committee",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="Be the student representative to the Campus Planning and Physical Plant Committee of the Harvey Mudd College Board of Trustees.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=2,
        body="Attend all appropriate student government meetings in order to keep informed of all pertinent developments.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=3,
        body="Report to Student Council on the results of all Board of Trustees Campus Planning and Physical Plant Committee meetings.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=4,
        body="Work closely with all student government groups in order to best represent ASHMC to the Board of Trustees.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=5,
        body="Work with the student representative to the Board of Trustees Educational Planning Committee and the student representative to the Board of Trustees Student Affairs Committee to promote communication between the students and the BOT.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=6,
        body="Present to ASHMC Council ideas for promoting communication between students and the BOT.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=7,
        body="Be a nonvoting member of the ASHMC Dormitory Affairs Committee.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=23,
        body="Representative to Career Services",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="The representative will work with the Career Services Director to provide student input and ideas for improving the effectiveness of Career Services.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=24,
        body="Representative to the committee on Student Personal Development",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="The representative will serve on the Committee on Student Personal Development, present to the committee issues that are relevant to the student body, and report to ASHMC on the activities of the committee when appropriate.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=25,
        body="Representative to Campus Party Security Committee",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="The CPS Chair shall chair weekly meetings with appointed members from each dorm to discuss party security issues.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=2,
        body="The CPS Chair will report back to ASHMC regarding decisions made by the CPS Committee.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=3,
        body="The CPS Chair shall ensure that parties are using the most recent security measures that have been ratified by the CPS Committee.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=26,
        body="Representative to the Claremont City Council",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="The Representative to the Claremont City Council shall be responsible for presenting the opinions and concerns of ASHMC to the City of Claremont Council members.",
    )
    section = Article.objects.create(
        parent=article,
        number=2,
        body="As soon as is practical, the new Student Council shall:",
    )
    subsection = Article.objects.create(
        parent=section,
        number=1,
        body="Approve the ASHMC Yearbook editor",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="The yearbook editor shall act as editor in chief of the yearbook and shall act in accordance with all guidelines set forth in Article X of the bylaws."
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=2,
        body="The yearbook editor is responsible for ensuring that the yearbook is published and distributed in a timely manner."
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=3,
        body="The yearbook editor shall be responsible for notifying the Student Council if the contract between ASHMC and the publisher has changed or been broken in any way or if any charges are incurred under that contract beyond those nominally necessary for preparation and publication of the yearbook. Such notice shall be given before the next council meeting occurring after the editor becomes aware of such charge or change in the contract."
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=4,
        body="The yearbook editor shall receive a yearly stipend as determined by the Student Council."
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=5,
        body="The yearbook editor shall make regular reports on the status of the yearbook as specified in Article X, Section 3."
    )
    subsection = Article.objects.create(
        parent=section,
        number=2,
        body="Approve the Orientation Lookbook editor",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="The Lookbook editor will be appointed by the orientation directors prior to the beginning of the midterm break of spring semester."
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=2,
        body="The Lookbook editor must be approved by a majority vote of Student Council."
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=3,
        body="The Lookbook editor shall act as editor in chief of the lookbook and shall act in accordance with all guidelines set forth in Article X of the bylaws."
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=4,
        body="The Lookbook editor can only be removed by a majority vote of Student Council."
    )
    section = Article.objects.create(
        parent=article,
        number=3,
        body="The Student Council shall require appointed officers to appear before the Council or send a status report to the Council at least once a year.",
    )
    section = Article.objects.create(
        parent=article,
        number=4,
        body="During the course of the year, should the Student Council determine that an appointed officer is not properly fulfilling the duties of that office, the officer may be removed by a three-fourths vote of the Student Council.",
    )

    article = Article.objects.create(
        parent=root,
        number=6,
        title="Committees",
    )
    section = Article.objects.create(
        parent=article,
        number=1,
        title="Four-Class Competition Committee:",
    )
    subsection = Article.objects.create(
        parent=section,
        number=1,
        body="The 4-Class Competition Committee shall consist of the class presidents and class vice presidents. The senior class president shall act as chair of the committee.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=2,
        body="Duties of Officers",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="The chair shall run committee meetings, and be responsible for the proper  functioning of the 4-Class Competition Committee.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=3,
        body="Duties of the 4-Class Competition Committee",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="The 4-Class Competition Committee shall provide for the planning and promotion of the 4-Class Competition and for the maintenance of all ASHMC property used in connection with the 4-Class Competition."
    )

    section = Article.objects.create(
        parent=article,
        number=2,
        title="Food Committee:",
    )
    subsection = Article.objects.create(
        parent=section,
        number=1,
        body="The Food Committee shall consist of an appointed chair and a representative from each dormitory."
    )
    subsection = Article.objects.create(
        parent=section,
        number=2,
        body="The Food Committee shall be responsible for representing and promoting the interest of ASHMC to the food service. Its duties shall include:"
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="Maintaining communication between the food service and ASHMC by meeting regularly. Meetings shall be announced beforehand."
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=2,
        body="Conveying students' satisfaction, dissatisfaction, and suggestions regarding specific aspects of the food service to the director."
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=3,
        body="Being involved in the planning and implementation, when appropriate, of special events within the board program."
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=4,
        body="Reporting to ASHMC on matters of importance relating to the board program. Minutes of Food Committee meetings shall be posted within three days of the meeting."
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=5,
        body="Being aware of specific provisions in the food service contract, and reporting violations when they occur to the appropriate administrative official at HMC."
    )


    article = Article.objects.create(
        parent=root,
        number=7,
        title="Student Organization Charters",
    )
    section = Article.objects.create(
        parent=article,
        number=1,
        body="A charter informs the Student Council of an organization's purpose, method and structure. Student Council should include in its consideration of a charter questions of the organization's uniqueness, student support, efficiency and likelihood of continuation.",
    )
    section = Article.objects.create(
        parent=article,
        number=2,
        body="All HMC organizations that wish to be funded in the ASHMC regular yearly budget must have a charter approved by a majority of Student Council and on file with the ASHMC treasurer.",
    )
    section = Article.objects.create(
        parent=article,
        number=3,
        body="The charter for an organization must include the following paragraph or a substitute suitable to Student Council: \"No member or officer of this ASHMC chartered organization shall be selected, dismissed, or discriminated against on the basis of age, race, religion, color, creed, sex, sexual orientation, national origin or political affiliation.\"",
    )
    section = Article.objects.create(
        parent=article,
        number=4,
        body="Student Council reserves the right to review and/or revoke any organization's charter, provided that officers of that organization have had the opportunity to participate in Council's review.",
    )
    section = Article.objects.create(
        parent=article,
        number=5,
        body="Each ASHMC chartered organization must submit a charter at the yearly budgeting meeting in order for that organization's charter to be renewed for the following year.",
    )

    article = Article.objects.create(
        parent=root,
        number=8,
        title="Financial Policy",
    )
    section = Article.objects.create(
        parent=article,
        number=1,
        body="The only persons authorized to charge goods and services to ASHMC are those persons specifically designated by Student Council to do so or ASHMC officers implementing ASHMC business.",
    )
    section = Article.objects.create(
        parent=article,
        number=2,
        body="Members of ASHMC shall not use appropriated ASHMC funds for purposes other than those for which the funds were appropriated.",
    )
    section = Article.objects.create(
        parent=article,
        number=3,
        body="Student body fees may be changed by a majority vote of ASHMC, subject to approval by the Board of Trustees.",
    )
    section = Article.objects.create(
        parent=article,
        number=4,
        title="Default Appropriations",
    )
    subsection = Article.objects.create(
        parent=section,
        number=1,
        body="Each dormitory is entitled to receive $10.00 per dormitory affiliate per semester from ASHMC, payable on demand.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="All ASHMC members living on campus must be affiliated with the dormitory in which they reside at the beginning of each semester. This affiliation is set seven days after the first day of classes of the semester.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=2,
        body="All ASHMC members living off campus must specify dorm affiliation within 14 days of the first day of classes of the semester. It is assumed that affiliation will remain the same for both semesters unless informed otherwise. The choice to not affiliate with a dorm will result in the forfeiture of this allocation. In this case, the allocation will be returned to the ASHMC general budget.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=2,
        body="Each class is entitled to receive $50.00 per semester from ASHMC, payable on demand.",
    )
    section = Article.objects.create(
        parent=article,
        number=5,
        body="ASHMC property may be loaned or rented to members of The Claremont Colleges under terms to be specified and regulated by the member or members of ASHMC responsible for such property, subject to approval by the ASHMC Student Council.",
    )
    section = Article.objects.create(
        parent=article,
        number=6,
        body="ASHMC members shall not violate said terms, nor shall anyone use ASHMC property without first obtaining authorization in the prescribed manner.",
    )
    section = Article.objects.create(
        parent=article,
        number=7,
        body="The ASHMC treasurer shall compile a precise and up-to-date list of all ASHMC property from individual clubs and organizations worth more than $50.00 as well as a list of those members, clubs and organizations responsible for its safekeeping.",
    )
    section = Article.objects.create(
        parent=article,
        number=8,
        title="Priority of Funding",
    )
    subsection = Article.objects.create(
        parent=section,
        number=1,
        body="Fixed charges as stated in the constitution shall receive top priority in distribution of funds. The groups receiving these funds may request more by following the procedure outlined below.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=2,
        body="Debt service, plant expense and other necessary payments shall be paid before budget requests are received. These shall be referred to as fixed charges along with subsection A above.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=3,
        body="Major activities oriented toward HMC students and/or maintenance of ASHMC property shall receive first consideration for funding of organizations. These shall be referred to as major HMC organizations.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=4,
        body="Small Harvey Mudd College Clubs whose membership is open to all HMC students are also eligible for funding. These shall be referred to as minor HMC organizations.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=5,
        body="Five-college activities and/or organizations which by nature appeal to a variety of HMC students shall be eligible for funding. These shall be referred to as major 5-College organizations.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=6,
        body="If an organization which is eligible for funding forms in the middle of the year, the above procedure shall be followed as soon as possible. Such an organization shall understand that sufficient funds may not be available after the budget has been made.",
    )
    section = Article.objects.create(
        parent=article,
        number=9,
        title="Guidelines for Funds",
    )
    subsection = Article.objects.create(
        parent=section,
        number=1,
        body="Fixed charges will be paid in full or according to agreements made.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=2,
        body="Major HMC organizations shall receive as much funding as Student Council deems proper and necessary.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=3,
        body="Minor HMC organizations may receive as much money as Student Council deems necessary and proper. The Student Council may suggest an appropriate amount of dues be collected by such organizations.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=4,
        body="Major 5-College organizations may receive a percentage of their total proposed budget proportional to the percentage of HMC students involved.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=5,
        body="Any member of ASHMC who feels the activity or group of his/her major interest should be funded, and that group or activity was not allocated money by the Student Council, has the right to submit a written request asking that a portion of his/her student body fees go to that group. Only one such request per student shall be considered. The name of the student requesting the money shall be kept confidential upon request.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=6,
        body="Miscellaneous funds can be allocated throughout the year. Such allocations must follow the procedures outlined in the Constitution.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=7,
        body="ASHMC will review all budget requests received before the budget meeting in light of the policies listed above.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=8,
        body="The Student Council shall not appropriate money to be spent on itself unless it is necessary for the proper functioning of the Council.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=9,
        body="ASHMC shall maintain a sample organization charter and funding request form to be distributed upon request. These forms will serve as an example of ASHMC standards in sponsoring organizations.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=10,
        body="All organization funding requests must be accompanied by an organization charter and tabulated budget conforming to ASHMC standards.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=11,
        body="All HMC clubs or organizations not specifically created in the ASHMC Constitution or Bylaws is required to work on a reimbursement basis. Clubs or organizations created in the ASHMC Constitution or Bylaws must work on a reimbursement basis if they do not have a bank account specifically for that group.",
    )
    section = Article.objects.create(
        parent=article,
        number=10,
        body="Procedure for Receiving ASHMC Funding",
    )
    subsection = Article.objects.create(
        parent=section,
        number=1,
        body="A budget request for funding during the next academic year, including and up to date audit (where necessary) and charter, must be submitted to the ASHMC treasurer before ASHMC budgeting. It is the responsibility of the requesting organization to find out when the budget meeting is. The audit, charter and budget request must conform to ASHMC standards must be submitted to the ASHMC treasurer by the budget meeting.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=2,
        body="The treasurer shall notify every requesting organization of the amount allocated to them.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=3,
        body="In order to receive allocated funds, an officer of the receiving organization must submit a check request to the ASHMC Treasurer.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=4,
        body="Funding may be received in one of three ways",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="One-half of the total amount allocated each semester.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=2,
        body="Total allotment second semester.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=3,
        body="With two-thirds ASHMC Council approval, total allotment first semester.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=5,
        body="The treasurer will forward the check within a reasonable amount of time to the requesting officer.",
    )
    section = Article.objects.create(
        parent=article,
        number=11,
        body="ASHMC, for the purpose of reporting tax details, will be structured on a fiscal year which begins on May 1 and ends on April 30.",
    )

    article = Article.objects.create(
        parent=root,
        number=9,
        title="Room Draw Procedure",
    )
    section = Article.objects.create(
        parent=article,
        number=1,
        body="Room draw policy is to be decided by the Dormitory Affairs Committee and announced to the student body before the start of spring vacation.",
    )
    section = Article.objects.create(
        parent=article,
        number=2,
        body="The Dormitory Affairs Committee chair and the people appointed by him/her shall run room draw as soon as possible.",
    )
    section = Article.objects.create(
        parent=article,
        number=3,
        body="ASHMC members who do not pull into a room during room draw may choose to declare themselves affiliated with a dormitory, becoming a full member of that dormitory.",
    )

    article = Article.objects.create(
        parent=root,
        number=10,
        title="Publications",
    )
    section = Article.objects.create(
        parent=article,
        number=1,
        body="An ASHMC-funded publication is defined as any publication whose only source of funding in part or in full from a student government is ASHMC. Funding of any publication must conform to Article VIII of the Bylaws.",
    )
    section = Article.objects.create(
        parent=article,
        number=2,
        body="Any publication which is to be funded by ASHMC must have a designated editor in chief who is solely responsible for the publication's content in accordance with the provisions given below. The editor in chief shall act as the official representative of the publication in all matters, specifically with any publishing company, with the provisions given below. The editor in chief is to be designated according to:",
    )
    subsection = Article.objects.create(
        parent=section,
        number=1,
        body=" Written procedures set forth in the charter of the publishing organization in the case of a student organization, or",
    )
    subsection = Article.objects.create(
        parent=section,
        number=2,
        body="The ASHMC Bylaws in the case of an official ASHMC publication.",
    )
    section = Article.objects.create(
        parent=article,
        number=3,
        title="Yearbook",
    )
    subsection = Article.objects.create(
        parent=section,
        number=1,
        body="The cost of the publication must not exceed reasonable limits to be set by the Student Council as part of the budgeting process. Such limits may be revised by the Student Council at the request of the editor in chief of the yearbook.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=2,
        body="Any contract made with a publisher is to be made between the Associated Students of Harvey Mudd College and the publishing company. The representative of ASHMC who shall be responsible for executing the terms of the contract pertaining to ASHMC shall be the editor in chief of the yearbook. Any contract made with a publisher must be approved by the Student Council. The contract should include the following three provisions:",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=1,
        body="The editor in chief has total responsibility for the content of the Yearbook. Any revisions which the publisher wishes to make must be submitted to the editor in chief for review. If, after review, the publisher makes changes contrary to the recommendations of the editor-in-chief, the publisher must notify the editor in chief of the changes and state their reasons for doing so in writing. The editor in chief is the only individual with the right to officially authorize publication of any part of the yearbook on the behalf of ASHMC.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=2,
        body="No contract shall be made for more than one year. At the end of each one year contract, the Student Council shall meet with the editor in chief and decide whether to renew the contract, to draw up a new contract, or to enter into a contract with a different publisher.",
    )
    subsubsection = Article.objects.create(
        parent=subsection,
        number=3,
        body="The Associated Students of Harvey Mudd College, in making a contract with a publisher and producing a yearbook to be published, are acting strictly on their own behalf. They are not acting as representatives of Harvey Mudd College nor is the publication or any part therein meant to represent Harvey Mudd College. The use of the name \"Harvey Mudd College\" or any reference thereto is not intended to be an official representation of the college nor is it meant to imply any endorsement from the college itself or from any member of the Harvey Mudd College faculty, administration, or board of trustees.",
    )
    subsection = Article.objects.create(
        parent=section,
        number=3,
        body="The yearbook editor shall make monthly reports of progress toward publication of the yearbook to the President. These reports shall include contract milestones met since the last report, due dates occurring since the last report and whether they were satisfied, and similar such events set to occur in the two months thereafter. Progress with respect to due dates and milestones shall be included in such reports, in terms of pages submitted or other appropriate measure.",
    )
    section = Article.objects.create(
        parent=article,
        number=4,
        body="It is recommended that these guidelines be reviewed periodically to insure that any changes in a student opinion, the ASHMC Constitution and Bylaws, the relationship with a publisher, or any other pertinent event be taken into account and provided for.",
    )

post_syncdb.connect(create_bylaws, dispatch_uid="legal_canonical_bylaws")
