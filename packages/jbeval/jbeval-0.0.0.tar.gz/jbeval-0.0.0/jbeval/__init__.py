from __future__ import absolute_import, division, print_function

name = "JBEval"
__version__ = '0.0.0'
__author__ = 'Jesús Requena Carrión and Nikesh Bajaj'



import sys, os

sys.path.append(os.path.dirname(__file__))

from .interface import JBEval_GUI
from .processing import jNotebook
