# Copyright (c) 2019, Hitoshi Ozawa
# see LICENSE for license details
__doc__ = """AgateReport report_info generation library."""
__version__ = "0.0.1"
__date__ = '20190308'

import sys

if sys.version_info < (3, 6):
    raise ImportError("""agatereports requires Python 3.6+; Previous versions are not supported.""")
