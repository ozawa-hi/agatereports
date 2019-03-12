# Copyright (c) 2019, Hitoshi Ozawa
# see LICENSE for license details
__doc__="""AgateReport report_info generation library."""
Version = "0.0.1"
__version__=Version
__date__='20190308'

import sys, os

if sys.version_info<(3, 6):
    raise ImportError("""agatereports requires Python 3.6+; Previous versions are not supported.""")
