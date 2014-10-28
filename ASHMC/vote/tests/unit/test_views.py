import datetime
from django.http.response import Http404
import mock

from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test import RequestFactory

from ASHMC.vote.views import GenCandidateForm
from ASHMC.vote.views import GenBallotForm
from ASHMC.vote.views import MeasureDetail
from ASHMC.vote.views import MeasureListing
from ASHMC.vote.views import MeasureResultList


def setup_view(view, request, *args, **kwargs):
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view


class MeasureListingTestCase(TestCase):

    def test_template_name(self):
        self.assertEqual(MeasureListing.template_name, "vote/measure_list.html")


class MeasureResultListTestCase(TestCase):

    def test_template_name(self):
        self.assertEqual(MeasureResultList.template_name, "vote/measure_results.html")

    def test_superuser_sees_all_measures(self):
        request = RequestFactory().get(reverse('vote_measure_results'))
        request.user = mock.Mock(is_superuser=True)
        view = setup_view(MeasureResultList(), request)

        with mock.patch('ASHMC.vote.views.Measure.objects.all') as all_measures:
            result = view.get_queryset()

        self.assertEqual(result, all_measures().order_by('-vote_end'))

    def test_user_without_room_denied(self):
        request = RequestFactory().get(reverse('vote_measure_results'))
        request.user = mock.Mock(is_superuser=False)
        view = setup_view(MeasureResultList(), request)

        with mock.patch('ASHMC.vote.views.UserRoom.objects.filter') as user_room_filter:
            # simulate not finding a room
            user_room_filter.return_value = []
            with self.assertRaises(PermissionDenied):
                view.get_queryset()

    @mock.patch('ASHMC.vote.views.Q')
    @mock.patch('ASHMC.vote.views.datetime')
    def test_VP_or_higher_sees_studentbody_measures(self, datetime, Q):
        request = RequestFactory().get(reverse('vote_measure_results'))
        request.user = mock.Mock(is_superuser=False, highest_ashmc_role=1)
        view = setup_view(MeasureResultList(), request)


        with mock.patch('ASHMC.vote.views.UserRoom.objects.filter') as user_room_filter:
            user_room = mock.Mock()
            user_room_filter.return_value = [user_room]

            # pretend that ASHMCRoles are integers, because that's basically what we're using
            # them as in this context
            with mock.patch('ASHMC.vote.views.ASHMCRole.objects.get') as ashmc_role_get:
                ashmc_role_get.return_value = 0

                with mock.patch('ASHMC.vote.views.Measure.objects.filter') as measure_filter:

                    expected_q = (
                        Q(restrictions__dorms=user_room.dorm) |  # always and only see your own dorms measures
                        Q(restrictions__dorms=None)
                    )

                    view.get_queryset()

                measure_filter.assert_called_once_with(
                    expected_q,
                    vote_end__lte=datetime.datetime.now(mock.ANY),
                )

    @mock.patch('ASHMC.vote.views.Q')
    @mock.patch('ASHMC.vote.views.datetime')
    def test_everybody_else_sees_their_dorm_and_class_measures(self, datetime, Q):
        request = RequestFactory().get(reverse('vote_measure_results'))
        request.user = mock.Mock(is_superuser=False, highest_ashmc_role=0)
        view = setup_view(MeasureResultList(), request)


        with mock.patch('ASHMC.vote.views.UserRoom.objects.filter') as user_room_filter:
            user_room = mock.Mock()
            user_room_filter.return_value = [user_room]

            with mock.patch('ASHMC.vote.views.ASHMCRole.objects.get') as ashmc_role_get:
                ashmc_role_get.return_value = 1

                with mock.patch('ASHMC.vote.views.Measure.objects.filter') as measure_filter:

                    expected_q = (
                        Q(restrictions__dorms=user_room.dorm) |  # always and only see your own dorms measures
                        Q(restrictions__dorms=None)
                    ) & (
                        Q(restrictions__gradyears=request.user.student.class_of) | # always and only see your own class's measures
                        Q(restrictions__gradyears=None)
                    )

                    view.get_queryset()

                measure_filter.assert_called_once_with(
                    expected_q,
                    vote_end__lte=datetime.datetime.now(mock.ANY),
                )


class MeasureDetailTestCase(TestCase):

    def setUp(self):
        user = mock.Mock(is_superuser=False)
        self.measure = mock.Mock(
            id=15,
            banned_accounts=mock.Mock(
                # no banned accounts for this measure by default
                all=mock.Mock(return_value=[]),
            ),
            is_open=True,
            vote_end=None,
        )

        self.request = RequestFactory().get(reverse('measure_detail', args=[self.measure.id]))
        self.request.user = user
        self.view = setup_view(MeasureDetail(), self.request)

    def test_superuser_always_gets_measure(self):
        self.request.user = mock.Mock(is_superuser=True)
        self.view = setup_view(MeasureDetail(), self.request)

        with mock.patch('ASHMC.vote.views.DetailView.get_object') as super_get_object:
            super_get_object.return_value = self.measure

            result = self.view.get_object()

        self.assertEqual(result, self.measure)

    def test_eligible_voter_gets_measure(self):
        self.measure.eligible_voters = [self.request.user]
        with mock.patch('ASHMC.vote.views.DetailView.get_object') as super_get_object:
            super_get_object.return_value = self.measure
            with mock.patch('ASHMC.vote.views.Vote.objects.filter') as vote_filter:
                vote_filter.return_value.count.return_value = 0

                result = self.view.get_object()

        self.assertEqual(result, self.measure)

    def test_closed_measures_404(self):
        self.measure.is_open = False
        with mock.patch('ASHMC.vote.views.DetailView.get_object') as super_get_object:
            super_get_object.return_value = self.measure

            with self.assertRaises(Http404):
                self.view.get_object()

    def test_ended_measures_404(self):
        self.measure.vote_end = datetime.datetime(2014, 10, 27)
        with mock.patch('ASHMC.vote.views.DetailView.get_object') as super_get_object:
            super_get_object.return_value = self.measure
            with mock.patch('ASHMC.vote.views.datetime') as mock_datetime:
                # pretend we're hitting the page one day after vote_end, above
                mock_datetime.datetime.now.return_value = datetime.datetime(2014, 10, 28)

                with self.assertRaises(Http404):
                    self.view.get_object()

    def test_banned_account_denied(self):
        # make this request's user a banned account for the measure
        self.measure.banned_accounts.all.return_value = [self.request.user]
        with mock.patch('ASHMC.vote.views.DetailView.get_object') as super_get_object:
            super_get_object.return_value = self.measure

            with self.assertRaises(PermissionDenied):
                self.view.get_object()

    def test_ineligible_voter_404(self):
        self.measure.eligible_voters = []
        with mock.patch('ASHMC.vote.views.DetailView.get_object') as super_get_object:
            super_get_object.return_value = self.measure

            with self.assertRaises(Http404):
                self.view.get_object()

    def test_voted_on_measure_404(self):
        self.measure.eligible_voters = [self.request.user]
        with mock.patch('ASHMC.vote.views.Vote.objects.filter') as vote_filter:
            vote_filter.return_value.count.return_value = 1
            with mock.patch('ASHMC.vote.views.DetailView.get_object') as super_get_object:
                super_get_object.return_value = self.measure

                with self.assertRaises(Http404):
                    self.view.get_object()

            vote_filter.assert_called_once_with(
                account=self.request.user,
                measure=self.measure,
            )


class GetCandidateFormTestCase(TestCase):

    def test_template_name(self):
        self.assertEqual(GenCandidateForm.template_name, "vote/candidate_create_form_fields.html")


class GenBallotFormTestCase(TestCase):

    def test_template_name(self):
        self.assertEqual(GenBallotForm.template_name, "vote/ballot_create_form_fields.html")
