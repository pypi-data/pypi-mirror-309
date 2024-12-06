"""Top-level package for pyicon."""

print('----Start loading pyicon.')

__author__ = """pyicon development team"""
from .version import __version__

# --- import pyicon basic modules
#print('-----params')
from .pyicon_params import params
#print('-----calc')
from .pyicon_calc import *
#print('-----calc_xr')
from .pyicon_calc_xr import *
#print('-----tb')
from .pyicon_tb import *
#print('-----IconData')
from .pyicon_IconData import *
#print('-----plotting')
from .pyicon_plotting import *
#print('-----accessor')
from .pyicon_accessor import *
#print('-----simulation')
from .pyicon_simulation import *
from .pyicon_thermo import *

# --- import pyicon.view
#print('-----view')
from . import view
# --- import pyicon.quickplots
#print('-----quickplots')
from . import quickplots

print('----Pyicon was loaded successfully.')
