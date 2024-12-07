# psychopy-bids

A [PsychoPy](https://www.psychopy.org/) plugin to work with the [Brain Imaging Data Structure (BIDS)](https://bids-specification.readthedocs.io/)

* **Website:** [https://psygraz.gitlab.io/psychopy-bids](https://psygraz.gitlab.io/psychopy-bids)
* **Documentation:** [https://psychopy-bids.readthedocs.io](https://psychopy-bids.readthedocs.io)
* **Source code:** [https://gitlab.com/psygraz/psychopy-bids](https://gitlab.com/psygraz/psychopy-bids)
* **Contributing:** [https://psychopy-bids.readthedocs.io/en/latest/contributing](https://psychopy-bids.readthedocs.io/en/latest/contributing)
* **Bug reports:** [https://gitlab.com/psygraz/psychopy-bids/issues](https://gitlab.com/psygraz/psychopy-bids/issues)
* **Code of Conduct:** [https://psychopy-bids.readthedocs.io/en/latest/conduct](https://psychopy-bids.readthedocs.io/en/latest/conduct)

## Installation

We recommend installation in a virtual environment.

```console
pip install psychopy-bids
```

## Usage

The psychopy bids plugin can be used to create valid BIDS valid datasets by creating [behavioral](https://bids-specification.readthedocs.io/en/stable/modality-specific-files/behavioral-experiments.html#example-_behtsv) or [task events](https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/05-task-events.html) in Psychopy. This can be done directly in python code or using the psychopy builder.

In code, the *BIDSHandler* can create or extend an existing BIDS dataset, including directory structure and necessary metadata files. Individual BIDS events can be added during the experiment and are passed to the *BIDSHandler* to write event `.tsv` files and accompanying `.json` files.

```py
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

handler.addStimuliFolder(event_file="example/sub-01/beh/sub-01_task-A_run-1_events.tsv")
```

## Contributing

Interested in contributing? Check out the [contributing guidelines](https://psychopy-bids.readthedocs.io/en/latest/contributing/). Please note that this project is released with a [Code of Conduct](https://psychopy-bids.readthedocs.io/en/latest/conduct/). By contributing to this project, you agree to abide by its terms.

## License

`psychopy-bids` was created by Christoph Anzengruber & Florian Schöngaßner. It is licensed under the terms of the GNU General Public License v3.0 license.

## Credits

`psychopy-bids` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
