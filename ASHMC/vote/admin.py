from django.contrib import admin

from .models import *


class BallotInline(admin.TabularInline):
    model = Ballot


class CandidateInline(admin.TabularInline):
    model = Candidate


class BallotAdmin(admin.ModelAdmin):

    list_filter = ('measure',)

    list_display = ('__unicode__', 'measure')

    inlines = [
        CandidateInline,
    ]
admin.site.register(Ballot, BallotAdmin)


class MeasureAdmin(admin.ModelAdmin):

    list_display = (
        'id', '__unicode__', 'actual_quorum',
        'quorum', 'is_open', 'vote_start'
    )
    list_display_links = ('id', '__unicode__')
    list_editable = ('quorum', )
    list_filter = ('is_open', 'vote_start', 'vote_end',)

    inlines = [
        BallotInline,
    ]
admin.site.register(Measure, MeasureAdmin)


class VoteAdmin(admin.ModelAdmin):
    pass
admin.site.register(Vote, VoteAdmin)


def get_measure(obj):
    return obj.ballot.measure


class PopularityVoteAdmin(admin.ModelAdmin):

    list_display = ('__unicode__', get_measure, 'ballot')

admin.site.register(PopularityVote, PopularityVoteAdmin)


class CandidateAdmin(admin.ModelAdmin):
    pass
admin.site.register(Candidate, CandidateAdmin)


class PersonCandidateAdmin(admin.ModelAdmin):
    pass
admin.site.register(PersonCandidate, PersonCandidateAdmin)
