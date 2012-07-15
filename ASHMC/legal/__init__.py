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
