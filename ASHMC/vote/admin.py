from django.contrib import admin

from .models import *


class CandidateInline(admin.TabularInline):
    model = Candidate


class BallotInline(admin.TabularInline):
    model = Ballot
    ordering = ('display_position',)


class RestrictionsInline(admin.StackedInline):
    model = Restrictions


class CandidateUserInline(admin.TabularInline):
    model = CandidateUser


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
        RestrictionsInline,
        BallotInline,
    ]
admin.site.register(Measure, MeasureAdmin)


class RestrictionsAdmin(admin.ModelAdmin):
    pass
admin.site.register(Restrictions, RestrictionsAdmin)


class VoteAdmin(admin.ModelAdmin):
    pass
admin.site.register(Vote, VoteAdmin)


def get_measure(obj):
    return obj.ballot.measure


class PopularityVoteAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', get_measure, 'ballot')
admin.site.register(PopularityVote, PopularityVoteAdmin)


class PreferentialVoteAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', get_measure, 'ballot')
admin.site.register(PreferentialVote, PreferentialVoteAdmin)


class CandidateAdmin(admin.ModelAdmin):
    def get_title(obj):
        return u'{}'.format(obj.cast())
    list_display = (get_title, 'ballot',)
    list_filter = ('ballot__measure__vote_start', 'ballot', 'ballot__measure',)
admin.site.register(Candidate, CandidateAdmin)


class PersonCandidateAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'ballot',)
    list_filter = ('ballot', 'ballot__measure',)
    inlines = [CandidateUserInline,]
admin.site.register(PersonCandidate, PersonCandidateAdmin)
