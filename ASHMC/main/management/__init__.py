from ..models import Dorm
from .. import models as features
from django.db.models import signals


def create_dorms(sender, **kwargs):
    kwargs.setdefault('verbosity', 0)
    for name, code in Dorm.DORMS:
        if kwargs['verbosity'] > 0:
            print "Creating {}".format(code)

        d, _ = Dorm.objects.get_or_create(
                name=name,
                code=code,
            )
signals.post_syncdb.connect(create_dorms, sender=features)
