#!/usr/bin/env python

def main():
    import argparse
    import json
    
    help_text = """
    Figure of horizontal lon/lat ICON data.
    
    Usage notes:
    ------------
    Basic usage:
    pyic_fig netcdf_file.nc var_name [options]
    
    Use with HEALPix / Zarr / Intake catalog:
    pyic_fig.py ngc3028 to --catalog="https://data.nextgems-h2020.eu/catalog.yaml"
    
    Change color limits, colorbar:
    pyic_fig netcdf_file.nc var_name --clim=-10,32 --cmap=viridis
    
    Select time step and depth level by indices:
    pyic_fig netcdf_file.nc var_name --it=3 --iz=0
    
    Select date and depth:
    pyic_fig netcdf_files_*.nc var_name --time=2010-03-02 --depth=1000
    
    Change region:
    pyic_fig netcdf_file.nc var_name --lon_reg=-20,30 --lat_reg=-45,-20
    
    Change region accross dateline:
    pyic_fig netcdf_file.nc var_name --lon_reg=120,90 --lat_reg=-90,90
    
    Plot across dateline for global plot (central_longitude should probably only be specified for global plot, it is calculated otherwise):
    pyic_fig netcdf_file.nc var_name --central_longitude=180
    
    Plot on original triangle grid (it is recommended to cut the domain otherwise, it takes a long time):
    pyic_fig netcdf_file.nc var_name --use_tgrid --lon_reg=-72,-68 --lat_reg=33,35
    
    Change projection to North Polar Stereographic projection:
    pyic_fig netcdf_file.nc var_name --projection=np
    
    Save the figure:
    pyic_fig netcdf_file.nc var_name --fpath_fig=/path/to/figure.png
    
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
                        help='Colormap used for plot. Use "cmo.name" for cmocean colormaps.')
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
                        help='Title string right. Use --title-right="full_time" for time str without rounding.')
    parser.add_argument('--xlabel', type=str, default='',
                        help='String for xlabel.')
    parser.add_argument('--ylabel', type=str, default='',
                        help='String for ylabel.')
    parser.add_argument('--cbar_str', type=str, default='auto',
                        help='String for colorbar. Default is name of variable and its units.')
    parser.add_argument('--cbar_pos', type=str, default='bottom',
                        help='Position of colorbar. It is possible to choose between \'right\' and \'bottom\'.')
    parser.add_argument('--fig_size_fac', type=float, default=2.,
                        help='Factor to increase the figure relative to text (default --fig_size_fac=2.).')
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
    parser.add_argument('--zoom', type=int, default=7,
                        help='Zoom level of HEALPix grid.')
    
    # --- specific for horizontal plot
    parser.add_argument('--use_tgrid', default=False,
                        action='store_true',
                        help='If specified, the plot is made on the original triangular grid.')
    parser.add_argument('--res', type=float, default=0.3,
                        help='Resolution of the interpolated data which will be plotted. So far, 1.0, 0.3, 0.1 are supported.')
    parser.add_argument('--projection', type=str, default='pc',
                        help='Map projection, choose \'None\' to deactivate cartopy, \'pc\' for normal lon/lat projection and \'np\' or \'sp\' for Norh- South-pole stereographic projections.')
    parser.add_argument('--iz', type=int, default=0,
                        help='Depth index which should be plotted.')
    parser.add_argument('--depth', type=float, default=-1.,
                        help='Depth value in m which should be plotted (if specified overwrites \'iz\').')
    parser.add_argument('--lon_reg', type=str, default=None,
                        help='Longitude range of the plot.')
    parser.add_argument('--lat_reg', type=str, default=None,
                        help='Latitude range of the plot.')
    parser.add_argument('--central_longitude', type=float, default=None,
                        help='Central longitude for cartopy plot.')
    parser.add_argument('--coastlines_color', type=str, default='k',
                        help='Color of coastlines. Default is \'k\'. To disable set to \'none\'.')
    parser.add_argument('--land_facecolor', type=str, default='0.7',
                        help='Color of land masses. Default is \'0.7\'. To disable set to \'none\'.')
    parser.add_argument('--noland', default=False,
                        action='store_true',
                        help='If specified, continents are not filled and land_facecolor is overwritten.')
    parser.add_argument('--lonlat_for_mask', default=False,
                        action='store_true',
                        help='If specified, mask for triangles which are swapped at periodic boundaries is calculated from clon and clat (and not only from clon). Relevant for torus setup.')
    
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
    
    if iopts.cmap.startswith('cmo.'):
      import cmocean
      iopts.cmap = getattr(cmocean.cm, iopts.cmap.split('.')[1])
    
    # --- limits
    if iopts.clim!='auto':
      iopts.clim = str_to_array(iopts.clim)
    if iopts.lon_reg:
      iopts.lon_reg = str_to_array(iopts.lon_reg)
    if iopts.lat_reg:
      iopts.lat_reg = str_to_array(iopts.lat_reg)
    if iopts.central_longitude is None:
      iopts.central_longitude = 'auto'
    
    # --- check whether run name or path to data is specified
    if iopts.data[0].endswith('.nc'):
      fpath_data = iopts.data
      concat_dim='time'
    elif iopts.data[0].endswith('.grb'):
      fpath_data = iopts.data
      concat_dim='step'
    else:
      run = iopts.data[0]
      fpath_data = 'none'
      concat_dim='time'
    
    # --- open dataset and select data
    mfdset_kwargs = dict(combine='nested', concat_dim=concat_dim, 
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
        reduced_cat = cat[iopts.model][run](zoom=iopts.zoom)
      ds = reduced_cat.to_dask()
    data = ds[iopts.var]
    
    # --- get grid uuidOfHGrid
    try:
      data = data.assign_attrs({"uuidOfHGrid": ds.uuidOfHGrid})
    except:
      pass
    
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
    if depth_name!='none':
      chunks[depth_name] = 1
    data = data.chunk(chunks)
    
    # --- select time coordinate
    if 'time' in data.dims:
      if iopts.time=='none':
        data = data.isel(time=iopts.it)
      else:
        data = data.sel(time=iops.time, method='nearest')
    # --- select vertical coordinate
    if depth_name!='none':
      if iopts.depth!=-1:
        data = data.sel({depth_name: iopts.depth}, method='nearest')
      else:
        data = data.isel({depth_name: iopts.iz})
    
    # --- apply factor
    if iopts.factor:
      data *= iopts.factor
    
    # --- masking variable
    if iopts.var in ['mld', 'mlotst']:
      data = data.where(data!=data.min())
    else:
      data = data.where(data!=0.)
    
    # --- get plotting arguments
    pkws = vars(iopts).copy()
    drop_items = [
      'data', 'var', 'fpath_fig', 'dontshow',
      'it', 'time', 'iz', 'depth', 
      'use_tgrid',
      'catalog', 'catdict', 'model', 'zoom',
      'factor',
    ]
    for key in drop_items:
      pkws.pop(key, None)
    
    # --- identify plotting method
    if iopts.use_tgrid:
      plot_method = 'tgrid'
    elif use_healpix:
      plot_method = 'healpix'
    else:
      plot_method = 'nn'
    pkws['plot_method'] = plot_method
    
    # -------------------------
    # main plotting command
    # -------------------------
    pyic.plot(data, **pkws)
    
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
