from django.contrib import admin

from .models import *


class BallotAdmin(admin.ModelAdmin):
    pass
admin.site.register(Ballot, BallotAdmin)


class BallotInline(admin.TabularInline):
    model = Ballot


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
