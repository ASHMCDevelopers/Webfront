from django.contrib import admin

from .models import *


class BallotInline(admin.TabularInline):
    model = Ballot


class CandidateInline(admin.TabularInline):
    model = Candidate


class BallotAdmin(admin.ModelAdmin):
    inlines = [
        CandidateInline,
    ]
admin.site.register(Ballot, BallotAdmin)


class MeasureAdmin(admin.ModelAdmin):
    inlines = [
        BallotInline,
    ]
admin.site.register(Measure, MeasureAdmin)


class VoteAdmin(admin.ModelAdmin):
    pass
admin.site.register(Vote, VoteAdmin)


class CandidateAdmin(admin.ModelAdmin):
    pass
admin.site.register(Candidate, CandidateAdmin)


class PersonCandidateAdmin(admin.ModelAdmin):
    pass
admin.site.register(PersonCandidate, PersonCandidateAdmin)
