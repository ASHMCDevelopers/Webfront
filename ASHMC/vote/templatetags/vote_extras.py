from django import template

register = template.Library()

@register.filter
def get_candidate(ballot, choice):
    candidates = ballot.candidate_set.filter(title=choice.choice_label)

    if len(candidates) != 1:
        return ""

    return candidates[0]


@register.filter
def dir_this(thing):
    return dir(thing)
