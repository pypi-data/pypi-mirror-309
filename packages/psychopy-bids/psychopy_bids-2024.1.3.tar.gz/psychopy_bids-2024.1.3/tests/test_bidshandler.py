import os
import tempfile
import unittest
from io import StringIO
from unittest.mock import patch

from psychopy_bids import bids


class TestBIDSHandler(unittest.TestCase):
    """
    Providing all unit tests for the class BIDSHandler
    """

    def test_init(self):
        with self.assertRaises(TypeError):
            bids.BIDSHandler()
            bids.BIDSHandler(dataset="A")
            bids.BIDSHandler(subject="A")
            bids.BIDSHandler(task="A")
            bids.BIDSHandler(dataset="A", subject="A")
            bids.BIDSHandler(dataset="A", task="A")
            bids.BIDSHandler(subject="A", task="A")

    # -------------------------------------------------------------------------------------------- #

    def test_addChanges(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.abspath(tmpdir)
            subject = {"participant_id": "01", "sex": "male", "age": 20}

            handler = bids.BIDSHandler(
                dataset=f"{path}{os.sep}A",
                subject=subject["participant_id"],
                task="task1",
            )
            handler.createDataset()
            handler.addChanges(["Init dataset"], version="MAJOR")
            handler.addChanges(["Added subject"], version="MINOR")
            handler.addChanges(["Added session"], version="PATCH")

    # -------------------------------------------------------------------------------------------- #

    def test_addDatasetDescription(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.abspath(tmpdir)
            subject = {"participant_id": "01", "sex": "male", "age": 20}

            handler = bids.BIDSHandler(
                dataset=f"{path}{os.sep}A",
                subject=subject["participant_id"],
                task="task1",
            )
            handler.createDataset()
            handler.addDatasetDescription()
            handler.addDatasetDescription(force=True)

    # -------------------------------------------------------------------------------------------- #

    def test_addLicense(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.abspath(tmpdir)
            subject = {"participant_id": "01", "sex": "male", "age": 20}

            handler = bids.BIDSHandler(
                dataset=f"{path}{os.sep}A",
                subject=subject["participant_id"],
                task="task1",
            )
            handler.createDataset(lic=False)

            with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
                handler.addLicense(identifier="ABC")
            expected = "License 'ABC' not found or could not be downloaded.\n"
            actual = mock_stderr.getvalue()
            self.assertEqual(expected, actual)

            handler.addLicense(identifier="CC0-1.0")
            with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
                handler.addLicense(identifier="CC0-1.0")
            expected = "File 'LICENSE' already exists, use force for overwriting it!\n"
            actual = mock_stderr.getvalue()
            self.assertEqual(expected, actual)
            handler.addLicense(identifier="CC0-1.0", force=True)

    # -------------------------------------------------------------------------------------------- #

    def test_addReadme(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.abspath(tmpdir)
            subject = {"participant_id": "01", "sex": "male", "age": 20}

            handler = bids.BIDSHandler(
                dataset=f"{path}{os.sep}A",
                subject=subject["participant_id"],
                task="task1",
            )
            handler.createDataset()
            with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
                handler.addReadme()
            expected = "File 'README' already exists, use force for overwriting it!\n"
            actual = mock_stderr.getvalue()
            self.assertEqual(expected, actual)

    # -------------------------------------------------------------------------------------------- #

    def test_addStimuliFolder(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.abspath(tmpdir)
            subject = {"participant_id": "01", "sex": "male", "age": 20}

            handler = bids.BIDSHandler(
                dataset=f"{path}{os.sep}A",
                subject=subject["participant_id"],
                task="task1",
            )
            handler.createDataset()

            image = bids.BIDSTaskEvent(
                onset=0,
                duration=0,
                trial_type="start",
                stim_file="images/orig_BIDS.png"
            )
            handler.addEvent(image)

            error = bids.BIDSTaskEvent(
                onset=0,
                duration=0,
                trial_type="start",
                stim_file="orig_BIDS.png"
            )
            handler.addEvent(error)

            tsv_file = handler.writeTaskEvents(participant_info=subject)
            handler.addStimuliFolder(tsv_file, "tests")
            self.assertIn("stimuli", os.listdir(f"{path}{os.sep}A"))
            self.assertEqual(
                os.listdir(f"{path}{os.sep}A{os.sep}stimuli{os.sep}images"), ["orig_BIDS.png"]
            )

            with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
                handler.addStimuliFolder(tsv_file, "tests")
                expected = "File 'orig_BIDS.png' does not exist!\n"
                actual = mock_stderr.getvalue()
                self.assertEqual(expected, actual)

    # -------------------------------------------------------------------------------------------- #

    def test_checkDSwithAcq(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.abspath(tmpdir)
            subject = {"participant_id": "01", "sex": "male", "age": 20}

            start = bids.BIDSTaskEvent(onset=0, duration=0, trial_type="start")
            presentation = bids.BIDSTaskEvent(
                onset=0.5, duration=5, trial_type="presentation"
            )
            stop = bids.BIDSTaskEvent(onset=10, duration=0, trial_type="stop")

            events = [start, presentation, stop]

            handler = bids.BIDSHandler(
                dataset=f"{path}{os.sep}A",
                subject=subject["participant_id"],
                acq="highres",
                task="task1",
            )
            handler.createDataset()
            
            for event in events:
                handler.addEvent(event)

            tsv_file = handler.writeTaskEvents(participant_info=subject)
            handler.addJSONSidecar(tsv_file)
            self.assertEqual(
                set(os.listdir(f"{path}{os.sep}A")),
                set([
                    "CHANGES",
                    "dataset_description.json",
                    "LICENSE",
                    "participants.json",
                    "participants.tsv",
                    "README",
                    "sub-01"
                ])
            )
            self.assertEqual(os.listdir(f"{path}{os.sep}A{os.sep}sub-01"), ["beh"])
            self.assertEqual(
                set(os.listdir(f"{path}{os.sep}A{os.sep}sub-01{os.sep}beh")),
                set([
                    "sub-01_task-task1_acq-highres_run-1_events.json",
                    "sub-01_task-task1_acq-highres_run-1_events.tsv",
                ])
            )

    # -------------------------------------------------------------------------------------------- #

    def test_checkDSMultipleSessions(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.abspath(tmpdir)
            subject = {"participant_id": "01", "sex": "male", "age": 20}

            start = bids.BIDSTaskEvent(onset=0, duration=0, trial_type="start")
            presentation = bids.BIDSTaskEvent(
                onset=0.5, duration=5, trial_type="presentation"
            )
            stop = bids.BIDSTaskEvent(onset=10, duration=0, trial_type="stop")

            events = [start, presentation, stop]

            handler1 = bids.BIDSHandler(
                dataset=f"{path}{os.sep}A",
                subject=subject["participant_id"],
                session='1',
                task="task1",
            )
            handler1.createDataset()
            for event in events:
                handler1.addEvent(event)
            tsv_file1 = handler1.writeTaskEvents(participant_info=subject)
            handler1.addJSONSidecar(tsv_file1)
            handler2 = bids.BIDSHandler(
                dataset=f"{path}{os.sep}A",
                subject=subject["participant_id"],
                session='2',
                task="task1",
            )
            handler2.createDataset(chg=False, readme=False, lic=False, force=False)
            for event in events:
                handler2.addEvent(event)
            tsv_file2 = handler2.writeTaskEvents(participant_info=subject)
            handler2.addJSONSidecar(tsv_file2)
            self.assertEqual(
                set(os.listdir(f"{path}{os.sep}A")),
                set([
                    "CHANGES",
                    "dataset_description.json",
                    "LICENSE",
                    "participants.json",
                    "participants.tsv",
                    "README",
                    "sub-01"
                ])
            )
            self.assertEqual(
                sorted(os.listdir(f"{path}{os.sep}A{os.sep}sub-01")), 
                sorted(["ses-1", "ses-2"])
            )
            self.assertEqual(
                set(os.listdir(f"{path}{os.sep}A{os.sep}sub-01{os.sep}ses-1{os.sep}beh")),
                set([
                    "sub-01_ses-1_task-task1_run-1_events.json",
                    "sub-01_ses-1_task-task1_run-1_events.tsv",
                ])
            )
            self.assertEqual(
                set(os.listdir(f"{path}{os.sep}A{os.sep}sub-01{os.sep}ses-2{os.sep}beh")),
                set([
                    "sub-01_ses-2_task-task1_run-1_events.json",
                    "sub-01_ses-2_task-task1_run-1_events.tsv",
                ])
            )

    # -------------------------------------------------------------------------------------------- #

    def test_checkDSMultipleSubjects(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.abspath(tmpdir)
            subject1 = {"participant_id": "01", "sex": "male", "age": 20}
            subject2 = {"participant_id": "02", "sex": "female", "age": 22}

            start = bids.BIDSBehEvent(onset=0, duration=0, trial_type="start")
            presentation = bids.BIDSBehEvent(
                onset=0.5, duration=5, trial_type="presentation"
            )
            stop = bids.BIDSBehEvent(onset=10, duration=0, trial_type="stop")

            events = [start, presentation, stop]

            handler1 = bids.BIDSHandler(
                dataset=f"{path}{os.sep}A",
                subject=subject1["participant_id"],
                task="task1",
                runs=False
            )
            handler1.createDataset()

            for event in events:
                handler1.addEvent(event)

            tsv_file1 = handler1.writeBehEvents(participant_info=subject1)
            handler1.addJSONSidecar(tsv_file1)
            
            handler2 = bids.BIDSHandler(
                dataset=f"{path}{os.sep}A",
                subject=subject2["participant_id"],
                task="task1",
                runs=False
            )
            handler2.createDataset()

            for event in events:
                handler2.addEvent(event)

            tsv_file2 = handler2.writeBehEvents(participant_info=subject2)
            handler2.addJSONSidecar(tsv_file2)
            
            self.assertEqual(
                set(os.listdir(f"{path}{os.sep}A")),
                set([
                    "CHANGES",
                    "dataset_description.json",
                    "LICENSE",
                    "participants.json",
                    "participants.tsv",
                    "README",
                    "sub-01",
                    "sub-02"
                ]),
            )
            self.assertEqual(os.listdir(f"{path}{os.sep}A{os.sep}sub-01"), ["beh"])
            self.assertEqual(
                set(os.listdir(f"{path}{os.sep}A{os.sep}sub-01{os.sep}beh")),
                set([
                    "sub-01_task-task1_beh.json",
                    "sub-01_task-task1_beh.tsv",
                ]),
            )
            self.assertEqual(os.listdir(f"{path}{os.sep}A{os.sep}sub-02"), ["beh"])
            self.assertEqual(
                set(os.listdir(f"{path}{os.sep}A{os.sep}sub-02{os.sep}beh")),
                set([
                    "sub-02_task-task1_beh.json",
                    "sub-02_task-task1_beh.tsv",
                ]),
            )

    # -------------------------------------------------------------------------------------------- #

    def test_parseLog(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.abspath(tmpdir)
            handler = bids.BIDSHandler(
                dataset=f"{path}{os.sep}A",
                subject="01",
                task="task1",
            )
        events = handler.parseLog(f"tests{os.sep}simple1.log")
        self.assertEqual(len(events), 3)
        regex = r"duration-(?P<duration>\d{1})_trial-(?P<trial>\d{1})"
        events = handler.parseLog(f"tests{os.sep}simple2.log", regex=regex)
        self.assertEqual(len(events), 3)
        with self.assertWarns(UserWarning):
            events = handler.parseLog(f"tests{os.sep}simple3.log")

    # -------------------------------------------------------------------------------------------- #

    def test_subject(self):
        handler = bids.BIDSHandler(dataset="A", subject="sub-01", task="A")
        self.assertEqual(handler.subject, "sub-01")
        handler = bids.BIDSHandler(dataset="A", subject="01", task="A")
        self.assertEqual(handler.subject, "sub-01")

    # -------------------------------------------------------------------------------------------- #

    def test_task(self):
        handler = bids.BIDSHandler(dataset="A", subject="01", task="task-A")
        self.assertEqual(handler.task, "task-A")
        handler = bids.BIDSHandler(dataset="A", subject="01", task="A")
        self.assertEqual(handler.task, "task-A")

    # -------------------------------------------------------------------------------------------- #

    def test_session(self):
        handler = bids.BIDSHandler(dataset="A", subject="01", task="A", session="ses-1")
        self.assertEqual(handler.session, "ses-1")
        handler = bids.BIDSHandler(dataset="A", subject="01", task="A", session="1")
        self.assertEqual(handler.session, "ses-1")

    # -------------------------------------------------------------------------------------------- #

    def test_data_type(self):
        handler = bids.BIDSHandler(
            dataset="A", subject="01", task="A", session="1", data_type="beh"
        )
        dt = [
            "anat",
            "beh",
            "dwi",
            "eeg",
            "fmap",
            "func",
            "ieeg",
            "meg",
            "micr",
            "perf",
            "pet",
        ]
        self.assertTrue(handler.data_type in dt)
        with self.assertRaises(SystemExit):
            bids.BIDSHandler(
                dataset="A", subject="01", task="A", session="1", data_type="abc"
            )

    # -------------------------------------------------------------------------------------------- #

    def test_acq(self):
        handler = bids.BIDSHandler(dataset="A", subject="01", task="A", acq="acq-1")
        self.assertEqual(handler.acq, "acq-1")
        handler = bids.BIDSHandler(dataset="A", subject="01", task="A", acq="1")
        self.assertEqual(handler.acq, "acq-1")


# ----------------------------------------------------------------------------------------------- #


if __name__ == "__main__":
    unittest.main()
