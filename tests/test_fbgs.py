import os

import pytest
from sdypy_sep005.sep005 import assert_sep005

from sep005_io_fbgs import read_fbgs

current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, 'static')
GOOD_FILES = os.listdir(os.path.join(static_dir, 'good'))


@pytest.mark.parametrize("filename", GOOD_FILES)
def test_compliance_sep005(filename):
    """
        Test the compliance with the SEP005 guidelines
        """
    file_path = os.path.join(static_dir, 'good', filename)
    signals = read_fbgs(file_path)  # should already not crash here

    assert len(signals) != 0  # Not an empty response
    assert_sep005(signals)

