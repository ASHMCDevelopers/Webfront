from django.db.models import signals
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

from .. import models as features
from ..models import Club

# Set up club admin permission
def create_club_admin_permission(sender, **kwargs):
    print "Creating club admin permission..."
    club_content_type = ContentType.objects.get_for_model(Club)
    if len(Permission.objects.filter(codename='full_club_admin')) == 0:
        club_admin_permission = Permission(name='Full Club Admin Access', codename='full_club_admin', content_type=club_content_type)
        club_admin_permission.save()

signals.post_syncdb.connect(create_club_admin_permission, sender=features)
