#!/usr/bin/env python

def main():
    import argparse
    import json
    
    help_text = """
    Makes a figure from ICON data
    
    Usage notes:
    ------------
    Basic usage:
    pyic_sec.py netcdf_file.nc var_name [options]
    
    Use with HEALPix / Zarr / Intake catalog:
    pyic_sec.py ngc3028 to --catalog="https://data.nextgems-h2020.eu/catalog.yaml"
    
    Specify section (with HEALPix):
    pyic_sec.py ngc3028 to --catalog="https://data.nextgems-h2020.eu/catalog.yaml" --section='80N80W-30S20E'
    
    Change color limits, colorbar:
    pyic_sec.py netcdf_file.nc var_name --clim=-10,32 --cmap=viridis
    
    Select time step by indices:
    pyic_sec.py netcdf_file.nc var_name --it=3 
    
    Select date:
    pyic_sec.py netcdf_files_*.nc var_name --time=2010-03-02 --depth=1000
    
    Change x/y-limits:
    pyic_sec.py netcdf_file.nc var_name ---xlim=-30,80 --ylim=0,3000
    
    Add contours:
    pyic_sec.py netcdf_file.nc var_name --clim=16 --cincr=2 --conts=auto --clabel
    
    Save the figure:
    pyic_sec.py netcdf_file.nc var_name --fpath_fig=/path/to/figure.png
    
    Argument list:
    --------------
    """
    
    # --- read input arguments
    parser = argparse.ArgumentParser(description=help_text, formatter_class=argparse.RawTextHelpFormatter)
    
    # --- necessary arguments
    parser.add_argument('data', nargs='+', metavar='data', type=str,
                        help='Path to ICON data file or simulation name of intake catalog.')
    parser.add_argument('var', metavar='var', type=str,
                        help='Name of variable which should be plotted.')
    # --- optional arguments
    # --- figure saving / showing
    parser.add_argument('--fpath_fig', type=str, default='none',
                        help='Path to save the figure.')
    parser.add_argument('--dontshow', action='store_true', default=False,
                        help='If dontshow is specified, the plot is not shown')
    # --- specifying the grid
    parser.add_argument('--gname', type=str, default='auto',
                        help='Grid name of the ICON data.')
    parser.add_argument('--fpath_tgrid', type=str, default='auto',
                        help='Path to triangular grid file. If \'auto\' the path is guessed automatically. Only necessary if \'--use_tgrid\' is used.')
    parser.add_argument('--fpath_ckdtree', type=str, default='auto',
                        help='Path to ckdtree interpolation file. If \'auto\' the path is guessed automatically.')
    parser.add_argument('--coordinates', type=str, default='clat clon',
                        help='Coordinates of variable which should be plotted. Choose between \'clat clon\' (default), \'vlat vlon\' or \'elat elon\'')
    # --- selecting time
    parser.add_argument('--it', type=int, default=0,
                        help='Time index which should be plotted.')
    parser.add_argument('--time', type=str, default='none',
                        help='Time string \'yyyy-mm-dd\' wich should be plotted (if specified overwrites \'it\').')
    # --- args for color / limits and settings
    parser.add_argument('--cmap', type=str, default='auto',
                        help='Colormap used for plot.')
    parser.add_argument('--clim', type=str, default='auto',
                        help='Color limits of the plot. Either specify one or two values.If one value is specified color limits are taken symetrically around zero. If \'auto\' is specified color limits are derived automatically.')
    parser.add_argument('--cincr', type=float, default=-1.0,
                        help='Increment for pcolor plot to specify levels between clims.')
    parser.add_argument('--clevs', type=str, default=None,
                        help='Color levels for pcolor plot.')
    parser.add_argument('--conts', type=str, default=None,
                        help='Contour levels for monochromatic contours.')
    parser.add_argument('--contfs', type=str, default=None,
                        help='Contour levels for filled contour patches.')
    parser.add_argument('--clabel', action='store_true', default=False,
                        help='If clabel is specified, color labels will be shown.')
    # --- args for titles and labels
    parser.add_argument('--title_center', type=str, default='auto',
                        help='Title string center.')
    parser.add_argument('--title_left', type=str, default='auto',
                        help='Title string left.')
    parser.add_argument('--title_right', type=str, default='auto',
                        help='Title string right.')
    parser.add_argument('--xlabel', type=str, default='auto',
                        help='String for xlabel.')
    parser.add_argument('--ylabel', type=str, default='depth [m]',
                        help='String for ylabel.')
    parser.add_argument('--cbar_str', type=str, default='auto',
                        help='String for colorbar. Default is name of variable and its units.')
    parser.add_argument('--cbar_pos', type=str, default='bottom',
                        help='Position of colorbar. It is possible to choose between \'right\' and \'bottom\'.')
    # --- manupilation of data
    parser.add_argument('--logplot', default=False,
                        action='store_true',
                        help='Plot logarithm of the data.')
    parser.add_argument('--factor', type=float, default=None,
                        help='Factor to mulitply data with.')
    # --- Intake catalog
    parser.add_argument('--catalog', type=str, 
                        default='https://data.nextgems-h2020.eu/catalog.yaml',
                        help='Intake catalog which contains simulation.')
    parser.add_argument('--model', type=str, 
                        default='ICON',
                        help='Model which to choose from catalog.')
    parser.add_argument('--catdict', type=json.loads,
                        help='Dictionary to reduce intake catalog, e.g. like this \'{"time": "P1D", "zoom": 7}\'.')
    # --- specific for section
    parser.add_argument('--invert_yaxis', action='store_true', default=True,
                        help='Invert y-axis, starting with largest and ending with smalles value.')
    parser.add_argument('--xdim', type=str, default='auto',
                        help='Dimension of x-axes of the plot. Choose between \{\'auto\'\}, \'lon\', or \'lat\'.')
    parser.add_argument('--section', type=str, default='170W',
                        help='''Section which is used for interpolation. 
    For HEALPix data, specify section e.g. like this: '170W' or '65S' or '80N80W-30S20E'.
    For regular data only the following sections are supported: \'30W\', \'170W\' 
    and zonal averages for global (\'gzave\', Atlantic \'azave\' and Indo-Pacific \'ipzave\'.'''
    )
    parser.add_argument('--fpath_fx', type=str, default='auto',
                        help='Path to an fx file fitting to the data.')
    parser.add_argument('--xlim', type=str, default=None,
                        help='Limits for x-axis.')
    parser.add_argument('--ylim', type=str, default=None,
                        help='Limits for y-axis.')
    parser.add_argument('--facecolor', type=str, default='0.7',
                        help='Background color')
    
    iopts = parser.parse_args()
    
    print('Start loading modules')
    import matplotlib
    if iopts.dontshow:
      matplotlib.use('Agg')
    import numpy as np
    import matplotlib.pyplot as plt
    import xarray as xr
    import glob
    import os
    import sys
    from pathlib import Path
    from ipdb import set_trace as mybreak  
    #sys.path.append(f'{Path.home()}/pyicon/')
    import pyicon as pyic  
    print('Done loading modules.')
    
    def str_to_array(string):
      string = string.replace(' ', '')
      array = np.array(string.split(','), dtype=float)
      return array
    
    # --- str_to_array
    if iopts.clim!='auto':
      iopts.clim = str_to_array(iopts.clim)
    if iopts.xlim:
      iopts.xlim = str_to_array(iopts.xlim)
    if iopts.ylim:
      iopts.ylim = str_to_array(iopts.ylim)
    if iopts.conts and iopts.conts!='auto':
      iopts.conts = str_to_array(iopts.conts)
    if iopts.contfs and iopts.contfs!='auto':
      iopts.contfs = str_to_array(iopts.contfs)
    if iopts.clevs:
      iopts.clevs = str_to_array(iopts.clevs)
    
    # --- check whether run name or path to data is specified
    if iopts.data[0].endswith('.nc') or iopts.data[0].endswith('.grb'):
      fpath_data = iopts.data
    else:
      run = iopts.data[0]
      fpath_data = 'none'
    
    # --- open dataset and select data
    mfdset_kwargs = dict(combine='nested', concat_dim='time', 
                         data_vars='minimal', coords='minimal', 
                         compat='override', join='override',)
    if fpath_data!='none':
      ds = xr.open_mfdataset(fpath_data, **mfdset_kwargs)
    else:
      import intake
      cat = intake.open_catalog(iopts.catalog)
      if iopts.catdict:
        reduced_cat = cat[iopts.model][run](**iopts.catdict)
      else:
        reduced_cat = cat[iopts.model][run](zoom=7)
      ds = reduced_cat.to_dask()
    data = ds[iopts.var]
    
    # --- check wether data is healpix data
    try:
      if data.grid_mapping=='crs':
        use_healpix = True
      else:
        use_healpix = False
    except:
      use_healpix = False
    
    # --- convert time coordinate in case of grib data
    if 'step' in data.dims:
      data = data.rename(time='time_ref')
      data = data.rename(step='time')
      data['time'] = data.time_ref+data.time
    
    # --- re-chunk data to allow for plotting from big files
    chunks = dict()
    if 'time' in data.dims:
      chunks = dict(time=1)
    depth_name = pyic.identify_depth_name(data)
    
    # --- select time coordinate
    if 'time' in data.dims:
      if iopts.time=='none':
        data = data.isel(time=iopts.it)
      else:
        data = data.sel(time=iopts.time, method='nearest')
    
    # --- apply factor
    if iopts.factor:
      data *= iopts.factor
    
    # --- masking variable
    data = data.where(data!=0)
    
    # --- get plotting arguments
    pkws = vars(iopts).copy()
    drop_items = [
      'data', 'var', 'fpath_fig', 'dontshow',
      'it', 'time', 'iz', 'depth', 
      'use_tgrid',
      'catalog', 'catdict', 'model',
      'factor',
      'xdim',
    ]
    for key in drop_items:
      pkws.pop(key, None)
    
    # --- identify plotting method
    if use_healpix:
      plot_method = 'healpix'
    else:
      plot_method = 'nn'
    pkws['plot_method'] = plot_method
    
    # -------------------------
    # main plotting command
    # -------------------------
    pyic.plot_sec(data, **pkws)
    
    # --- save figure
    fpath_fig = iopts.fpath_fig
    if fpath_fig!='none':
      if fpath_fig.startswith('~'):
        home = str(Path.home())+'/'
        fpath_fig = home + fpath_fig[1:]
      print(f'Saving figure {fpath_fig}...')
      plt.savefig(fpath_fig)
    
    # --- show figure
    if not iopts.dontshow:
      plt.show()

if __name__ == "__main__":
  main()
