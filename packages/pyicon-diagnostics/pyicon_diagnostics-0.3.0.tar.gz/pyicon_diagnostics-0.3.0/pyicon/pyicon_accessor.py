import functools
import xarray as xr
import pyicon as pyic


@xr.register_dataarray_accessor("pyic")
class pyiconDataArray:
    def __init__(self, xarray_obj, path_grid='auto'):
        self._obj = xarray_obj
        self._gname = None
        if path_grid=='auto':
          path_grid = pyic.params['path_grid']
        self.path_grid = path_grid


    @property
    def gname(self):
        if self._gname is None:
          self._gname = pyic.identify_grid(self._obj, self.path_grid)
        return self._gname

  
    @functools.wraps(pyic.plot, assigned=("__doc__", "__anotations__"))
    def plot(self, **kwargs):
        da = self._obj
        ax, hm = pyic.plot(da, **kwargs)
        return ax, hm


    @functools.wraps(pyic.plot_sec, assigned=("__doc__", "__anotations__"))
    def plot_sec(self, **kwargs):
        da = self._obj
        ax, hm = pyic.plot_sec(da, **kwargs)
        return ax, hm


    @functools.wraps(pyic.interp_to_rectgrid_xr, assigned=("__doc__", "__anotations__"))
    def interp(self, **kwargs):
        da = self._obj
        dai = pyic.interp_to_rectgrid_xr(da, **kwargs)
        return dai
