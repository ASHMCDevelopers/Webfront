#from django.db.models import signals

from .. import models as features
from ..models import Dorm, DormRoom

import itertools


def create_dorms(sender, **kwargs):
    kwargs.setdefault('verbosity', 0)
    for name, code in Dorm.DORMS:
        if kwargs['verbosity'] > 0:
            print "Creating {}".format(code)

        d, _ = Dorm.objects.get_or_create(
                name=name,
                code=code,
            )
#signals.post_syncdb.connect(create_dorms, sender=features)


def create_dorm_rooms(sender, **kwargs):
    DORM_ROOM_MAP = {
        'AT': map(str, range(100, 128)) + map(str, range(200, 228)) + map(str, range(300, 328)),
        'EA': (
            map(str, range(101, 117)) + map(str, range(119, 129))
            + map(str, range(151, 167)) + map(str, range(169, 179))
        ),
        'BPA': [],
        'SU': (
            list(itertools.chain.from_iterable(
                map(lambda x: [x + c for c in "ABCD" if x not in ['104', '105']],
                    map(str, range(101, 109))),
            ))
            + ['104D', '105A', '105B', '105D']
            + list(itertools.chain.from_iterable(
                map(lambda x: [x + c for c in "ABCD" if x not in ['204', '205']],
                    map(str, range(201, 209))),
            ))
            + ['204A', '204B', '204D', '205A', '205B', '205D', '209D', '210D']
        ),
        'LI': [
            '101', '102', '103', '105',
            '107', '110', '111',
            '112', '113', '116', '117',
            '129', '130', '132', '135',
            '136', '138', '140',
            '141', '144', '145', '146',
            '201', '202', '203', '204',
            '207', '208', '211',
            '212', '213', '216', '217',
            '230', '231', '232', '233', '236',
            '237', '239', '240',
            '243', '244', '246', '247',
        ],
        'NO': map(str, range(201, 217)) + map(str, range(219, 229)),
        'WE': (
            map(str, range(401, 417))
            + map(str, range(419, 429))
            + map(str, range(451, 467))
            + map(str, range(469, 479))
        ),
        'SO': (
            list(itertools.chain.from_iterable(
                map(lambda x: [x + c for c in "ABCD"],
                    map(str, [301, 302, 307, 308, 351, 352, 357, 358])
                )
            ))
            + list(itertools.chain.from_iterable(
                map(lambda x: [x + c for c in "ABC"],
                    map(str, [303, 305, 304, 306, 353, 354, 355, 356])
                )
            ))
            + map(str, range(309, 313) + range(359, 367))
        ),
        'CA': (
            map(str, range(100, 109)) + map(str, range(118, 126)) + map(str, range(140, 148))
            + map(str, range(148, 156)) + map(str, range(200, 209)) + map(str, range(218, 226)) + map(str, range(240, 248))
            + map(str, range(248, 256))
            + ['Q1D', 'Q2D', 'Q1B', 'Q2C', 'Q2B']
        ),
    }

    for code in DORM_ROOM_MAP:
        dorm = Dorm.objects.get(code=code)
        if kwargs['verbosity'] > 0:
            print "Creating rooms for dorm {}...".format(dorm)
        for numberish in DORM_ROOM_MAP[code]:
            if kwargs['verbosity'] > 1:
                print "\tCreating {}".format(numberish),
            dr, _ = DormRoom.objects.get_or_create(
                dorm=dorm,
                number=numberish,
            )
            if kwargs['verbosity'] > 1:
                print "done."
#signals.post_syncdb.connect(create_dorm_rooms, sender=features)
