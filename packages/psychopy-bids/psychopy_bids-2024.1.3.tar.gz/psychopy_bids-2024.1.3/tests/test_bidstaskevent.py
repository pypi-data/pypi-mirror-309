"""
This file combines the two frameworks doctest and unittest to test various aspects of the
BIDSTaskEvent class.
"""

import doctest
import unittest

from psychopy_bids import bids
from psychopy_bids.bids.bidstaskevent import (BIDSTaskEvent, DatabaseError,
                                              DurationError, HedError,
                                              IdentifierError, OnsetError,
                                              ResponseTimeError, SampleError,
                                              StimFileError, TrialTypeError)


class TestBIDSTaskEvent(unittest.TestCase):
    """
    Providing all unit tests for the class BIDSTaskEvent
    """

    def test_init(self):
        with self.assertRaises(TypeError):
            BIDSTaskEvent()
            BIDSTaskEvent(onset=1.0)
            BIDSTaskEvent(duration=0)

    # -------------------------------------------------------------------------------------------- #

    def test_custom_column(self):
        custom = BIDSTaskEvent(onset=1.0, duration=0, trial=1)
        self.assertEqual(custom.trial, 1)

    # -------------------------------------------------------------------------------------------- #

    def test_repr(self):
        self.assertEqual(
            repr(BIDSTaskEvent(onset=1.0, duration=0)),
            "BIDSTaskEvent(onset=1.0, duration=0)",
        )

    # -------------------------------------------------------------------------------------------- #

    def test_set_item(self):
        event = BIDSTaskEvent(0, 0, trial_type="begin")
        event.onset = 2.5
        self.assertEqual(event.onset, 2.5)
        event.duration = "n/a"
        self.assertEqual(event.duration, "n/a")
        event.trial_type = "start"
        self.assertEqual(event.trial_type, "start")
        event.sample = 1
        self.assertEqual(event.sample, 1)
        event.response_time = 1
        self.assertEqual(event.response_time, 1)
        event.value = "value"
        self.assertEqual(event.value, "value")
        event.hed = "hed"
        self.assertEqual(event.hed, "hed")
        event.stim_file = "stim_file"
        self.assertEqual(event.stim_file, "stim_file")
        event.identifier = "identifier"
        self.assertEqual(event.identifier, "identifier")
        event.database = "database"
        self.assertEqual(event.database, "database")
        event.trial = 1
        self.assertEqual(event.trial, 1)

    # -------------------------------------------------------------------------------------------- #

    def test_onset(self):
        event = BIDSTaskEvent(onset=1.0, duration=0)
        self.assertTrue(isinstance(event.onset, (int, float)))
        event = BIDSTaskEvent(onset="1", duration=0)
        self.assertTrue(isinstance(event.onset, (int, float)))

        with self.assertRaises(OnsetError):
            BIDSTaskEvent(onset=[0, 1, 2], duration=0)

        with self.assertRaises(OnsetError):
            BIDSTaskEvent(onset="A", duration=0)

    # -------------------------------------------------------------------------------------------- #

    def test_duration(self):
        event = BIDSTaskEvent(onset=1.0, duration=0)
        self.assertTrue(isinstance(event.onset, (int, float)))
        self.assertTrue(event.duration >= 0)

        with self.assertRaises(DurationError):
            BIDSTaskEvent(onset=1.0, duration="A")

        with self.assertRaises(DurationError):
            BIDSTaskEvent(onset=1.0, duration=-1)

        event = BIDSTaskEvent(onset=1.0, duration="1")
        self.assertEqual(event.duration, 1)

        event = BIDSTaskEvent(onset=1.0, duration="n/a")
        self.assertEqual(event.duration, "n/a")

    # -------------------------------------------------------------------------------------------- #

    def test_trial_type(self):
        event = BIDSTaskEvent(onset=1.0, duration=0, trial_type="go")
        self.assertTrue(isinstance(event.trial_type, str))

        with self.assertRaises(TrialTypeError):
            BIDSTaskEvent(onset=1.0, duration=0, trial_type=1)

    # -------------------------------------------------------------------------------------------- #

    def test_value(self):
        event = BIDSTaskEvent(onset=1.0, duration=0, value=0)
        self.assertEqual(event.value, 0)

    # -------------------------------------------------------------------------------------------- #

    def test_sample(self):
        event = BIDSTaskEvent(onset=1.0, duration=0, sample=1)
        self.assertTrue(isinstance(event.sample, (int, float)))

        event = BIDSTaskEvent(onset=1.0, duration=0, sample="1")
        self.assertTrue(isinstance(event.sample, (int, float)))

        with self.assertRaises(SampleError):
            BIDSTaskEvent(onset=1.0, duration=0, sample="A1")

    # -------------------------------------------------------------------------------------------- #

    def test_response_time(self):
        event = BIDSTaskEvent(onset=1.0, duration=0, response_time=1.0)
        self.assertTrue(isinstance(event.response_time, (int, float)))
        self.assertTrue(event.response_time >= 0)

        with self.assertRaises(ResponseTimeError):
            BIDSTaskEvent(onset=1.0, duration=0, response_time="A")

        with self.assertRaises(ResponseTimeError):
            BIDSTaskEvent(onset=1.0, duration=0, response_time=[0, 1, 2])

        event = BIDSTaskEvent(onset=1.0, duration=0, response_time="1")
        self.assertEqual(event.response_time, 1)

        event = BIDSTaskEvent(onset=1.0, duration=0, response_time="n/a")
        self.assertEqual(event.response_time, "n/a")

    # -------------------------------------------------------------------------------------------- #

    def test_hed(self):
        event = BIDSTaskEvent(onset=1.0, duration=0, hed="go")
        self.assertTrue(isinstance(event.hed, str))

        with self.assertRaises(HedError):
            BIDSTaskEvent(onset=1.0, duration=0, hed=1)

    # -------------------------------------------------------------------------------------------- #

    def test_stim_file(self):
        event = BIDSTaskEvent(onset=1.0, duration=0, stim_file="file.txt")
        self.assertTrue(isinstance(event.stim_file, str))

        with self.assertRaises(StimFileError):
            BIDSTaskEvent(onset=1.0, duration=0, stim_file=1)

    # -------------------------------------------------------------------------------------------- #

    def test_identifier(self):
        event = BIDSTaskEvent(onset=1.0, duration=0, identifier="a")
        self.assertTrue(isinstance(event.identifier, str))

        with self.assertRaises(IdentifierError):
            BIDSTaskEvent(onset=1.0, duration=0, identifier=1)

    # -------------------------------------------------------------------------------------------- #

    def test_database(self):
        event = BIDSTaskEvent(onset=1.0, duration=0, database="a")
        self.assertTrue(isinstance(event.database, str))

        with self.assertRaises(DatabaseError):
            BIDSTaskEvent(onset=1.0, duration=0, database=1)

    # -------------------------------------------------------------------------------------------- #

    def test_exceptions(self):
        self.assertEqual(str(OnsetError("A")), "A -> Property 'onset' MUST be a number")
        msg = "A -> Property 'duration' MUST be either zero or positive (or n/a if unavailable)"
        self.assertEqual(str(DurationError("A")), msg)
        self.assertEqual(
            str(TrialTypeError(1)), "1 -> Property 'trial_type' MUST be a string"
        )
        self.assertEqual(
            str(SampleError("A")), "A -> Property 'sample' MUST be an integer"
        )
        msg = "A -> Property 'response_time' MUST be a number (or n/a if unavailable)"
        self.assertEqual(str(ResponseTimeError("A")), msg)
        self.assertEqual(str(HedError(1)), "1 -> Property 'hed' MUST be a string")
        self.assertEqual(
            str(StimFileError("A")), "A -> Property 'stim_file' MUST be a string"
        )
        self.assertEqual(
            str(IdentifierError("A")), "A -> Property 'identifier' MUST be a string"
        )
        self.assertEqual(
            str(DatabaseError("A")), "A -> Property 'database' MUST be a string"
        )


# ------------------------------------------------------------------------------------------------ #


if __name__ == "__main__":
    doctest.testmod(bids.bidstaskevent)
    unittest.main()
