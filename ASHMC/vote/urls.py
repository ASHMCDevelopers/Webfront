from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required


from .views import (CreateMeasure, GenBallotForm, GenCandidateForm, MeasureListing,
                    MeasureDetail, MeasureResultList)

urlpatterns = patterns('vote.views',
       url('^$', login_required(MeasureListing.as_view()), name='vote_main'),
       url('^measure/create$', login_required(CreateMeasure.as_view()), name='vote_measure_create'),
       url('^measure/create/ballot/(?P<num>\d+)$', login_required(GenBallotForm.as_view()), name="vote_gen_ballot_form"),
       url('^measure/create/candidate/(?P<bnum>\d+)/(?P<cnum>\d+)$', login_required(GenCandidateForm.as_view()), name="vote_gen_ballot_form"),
       url('^measures/$', login_required(MeasureListing.as_view()), name='measure_list'),
       url('^measure/(?P<pk>\d+)/$', login_required(MeasureDetail.as_view()), name='measure_detail'),
       url('^results/$', login_required(MeasureResultList.as_view()), name='vote_measure_results'),
)
