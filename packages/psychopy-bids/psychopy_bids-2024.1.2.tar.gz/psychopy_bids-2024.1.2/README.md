# psychopy-bids

A [PsychoPy](https://www.psychopy.org/) plugin to work with the [Brain Imaging Data Structure (BIDS)](https://bids-specification.readthedocs.io/)

* **Website:** https://psygraz.gitlab.io/psychopy-bids
* **Documentation:** https://psychopy-bids.readthedocs.io
* **Source code:** https://gitlab.com/psygraz/psychopy-bids/
* **Contributing:** https://psychopy-bids.readthedocs.io/en/doc/contributing/
* **Bug reports:** https://gitlab.com/psygraz/psychopy-bids/issues
* **Code of Conduct:** https://psychopy-bids.readthedocs.io/en/doc/conduct/

## Installation

```bash
$ pip install psychopy-bids
```

## Usage

`psychopy-bids` can be used to create valid BIDS datasets by adding the possibility of using [task events](https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/05-task-events.html) in PsychoPy.

```python
from psychopy_bids import bids

handler = bids.BIDSHandler(dataset="example", subject="01", task="A")
handler.createDataset()

events = [
    bids.BIDSTaskEvent(onset=1.0, duration=0.5, event_type="stimulus", response="correct"),
    bids.BIDSTaskEvent(onset=1.0, duration=0, trial_type="trigger")
]

for event in events:
    handler.addEvent(event)

participant_info = {"participant_id": handler.subject, "age": 18}

handler.writeTaskEvents(participant_info=participant_info)

handler.addStimuliFolder(event_file="my_dataset/sub-01/beh/sub-01_task-A_run-1_events.tsv")
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`psychopy-bids` was created by Christoph Anzengruber & Florian Schöngaßner. It is licensed under the terms of the GNU General Public License v3.0 license.

## Credits

`psychopy-bids` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
