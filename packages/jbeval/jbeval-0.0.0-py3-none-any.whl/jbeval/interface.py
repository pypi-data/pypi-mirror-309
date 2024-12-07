'''
API .
Version : 0.0.0, Date: 20 Nov 2024
'''

from __future__ import absolute_import, division, print_function
name = "JBEval | Interface"
import sys


import sys, os, six, time, collections, glob
from six.moves.urllib.error import HTTPError, URLError
from six.moves.urllib.request import urlopen, urlretrieve
import tarfile

from pathlib import Path

try:
    import queue
except ImportError:
    import Queue as queue

import spkit as sp
import pandas as pd
import numpy as np
import json, warnings


class JBEval_GUI():
    def __init__(self):
        self.file = ''

    