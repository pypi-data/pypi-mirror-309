"""
This file combines the two frameworks doctest and unittest to test various aspects of the
BIDSBehEvent class.
"""

import doctest
import os
import unittest

import psychopy
from psychopy.app.builder import experiment

from psychopy_bids import bids

#import codecs


class TestBIDSBehEventComponent(unittest.TestCase):
    """Providing unit tests for the class BIDSBehEventComponent"""

    def test_init(self):
        """Test case for the __init__ method of BIDSBehEvent"""
        exp = experiment.Experiment(prefs = None)
        exp.loadFromXML(f"tests{os.sep}minimal.psyexp")
        script = exp.writeScript(f"tests{os.sep}minimal.psyexp")
        print(script)
        #if scriptObj is None:
        #    raise RuntimeError('No script generated for %s' %xmlExpFile)    
        #codecs.open(pyExpFile, 'w', 'utf-8').write(scriptObj.getvalue())


# ------------------------------------------------------------------------------------------------ #


if __name__ == "__main__":
    #doctest.testmod(bids.bidsbehevent)
    unittest.main()
