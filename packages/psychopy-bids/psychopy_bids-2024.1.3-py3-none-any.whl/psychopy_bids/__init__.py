"""
    Package to support the creation of valid bids-datasets.
"""

from importlib.metadata import version

__version__ = version("psychopy_bids")

from .bids_beh import BidsBehEventComponent
from .bids_settings import BidsExportRoutine
from .bids_task import BidsTaskEventComponent

__all__ = ["BidsBehEventComponent", "BidsTaskEventComponent", "BidsExportRoutine"]
