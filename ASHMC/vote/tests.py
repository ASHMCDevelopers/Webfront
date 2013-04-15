"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import datetime


from django.utils import unittest as T
from django.db import IntegrityError

from .models import *
from .testing.factories import *


class MeasureCreationTest(T.TestCase):
    def test_default_settings(self):
        """Tests that sensible defaults are held to."""
        measure = MeasureFactory.create()

        self.assertAlmostEqual(
            measure.vote_start, datetime.datetime.now(),
            delta=datetime.timedelta(seconds=5),
        )
        self.assertTrue(measure.is_open)

    def test_cannot_create_measure_without_required_fields(self):
        required_fields = [x[0].name for x in Measure._meta.get_fields_with_model() if (x[0].null == False and x[0].blank == False)]

        for f in required_fields:
            kwargs = {f: None}
            measure = MeasureFactory.build(
                **kwargs
            )

            with self.assertRaises(IntegrityError) as cm:
                measure.save()

            exc = cm.exception

            self.assertEqual(exc.message, "vote_measure.{} may not be NULL".format(f))


class BallotCreationTest(T.TestCase):
    def setUp(self):
        self.measure = MeasureFactory.create()

    def test_default_settings(self):
        ballot = BallotFactory(
            measure=self.measure
        )

        self.assertEqual(ballot.measure, self.measure)
        self.assertEqual(ballot.is_secret, False)
        self.assertEqual(ballot.can_write_in, False)
