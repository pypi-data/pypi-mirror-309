import json
import os

fname = os.path.join(os.path.dirname(__file__), 'params_default.json')
#if os.path.isfile(fname):
#  with open(fname, 'r') as f:
#      params_default = json.load(f)
#else:
#  print(f'File {fname} does not exist.')
try:
  with open(fname, 'r') as f:
      params_default = json.load(f)
except:
  #print(f'Could not find {fname}. Continuingwith backup solution.')
  params_default = {
    "path_grid": "/work/mh0033/m300602/icon/grids/",
    "path_example_data": "/work/mh0033/m300602/pyicon_example_data_download/"
  }

fname = os.path.join(os.path.dirname(__file__), 'params_user.json')
if os.path.isfile(fname):
  with open(fname, 'r') as f:
      params_user = json.load(f)
else:
  #print(f'File {fname} does not exist.')
  pass

try:
  params = params_default | params_user
except:
  params = params_default
