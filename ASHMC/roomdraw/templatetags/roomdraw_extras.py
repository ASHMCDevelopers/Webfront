from django import template


from ASHMC.roomdraw.models import RoomInterest

register = template.Library()


@register.filter
def get_highest_number(dormroom):
    if isinstance(dormroom, RoomInterest):
        return max([u.drawnumber for u in dormroom.interested_users.all()])
    interested_parties = [ri.interested_users.all() for ri in dormroom.roominterest_set.all()]

    best = None
    for user_list in interested_parties:
        best = max(max([u.drawnumber for u in user_list]), best)

    return best


@register.filter
def prettify(a_list):
    return [u.get_full_name() for u in a_list]
