import datetime
import factory

from ..models import (Ballot, Measure,
    Vote, PopularityVote, Candidate, PersonCandidate, User)


class UserFactory(factory.Factory):
    FACTORY_FOR = User
    first_name = 'Joe'
    last_name = 'Blow'
    email = factory.LazyAttribute(lambda a: '{0}.{1}@example.com'.format(a.first_name, a.last_name).lower())


class MeasureFactory(factory.Factory):
    FACTORY_FOR = Measure

    name = "Test Measure"
    vote_end = datetime.datetime.now() + datetime.timedelta(days=5)


class BallotFactory(factory.Factory):
    FACTORY_FOR = Ballot

    measure = factory.SubFactory(MeasureFactory)
    title = factory.Sequence(lambda n: "Ballot #{}".format(n))


class CandidateFactory(factory.Factory):
    FACTORY_FOR = Candidate
    ballot = factory.SubFactory(BallotFactory)
    description = "A Test description"


class PersonCandidateFactory(CandidateFactory):
    FACTORY_FOR = PersonCandidate
