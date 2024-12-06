#!/usr/bin/env python
def main():
    import argparse
    
    import os
    import sys
    import glob
    import pyicon as pyic
    import matplotlib.pyplot as plt
    import xarray as xr
    
    ts = pyic.timing([0], string='')
    
    help_text = """
    Makes an animation from ICON data by first creating a jpg file for each snapshot and then creating an mp4 movie by using ffmpeg.
    
    Usage notes:
    ------------
    Basic usage:
    pyic_anim.py netcdf_file_or_list.nc var_name --fpath_out=/path/to/movie/without/file/ending/name [options]
    
    Change color limits, colorbar:
    pyic_anim.py netcdf_file_or_list.nc var_name --fpath_out=name --clim=-10,32 --cmap=viridis
    
    Select depth level by indices:
    pyic_anim.py netcdf_file_or_list.nc var_name --fpath_out=name --iz=0
    
    Select depth:
    pyic_anim.py netcdf_file_or_list.nc var_name --fpath_out=name --depth=1000
    
    Change region:
    pyic_anim.py netcdf_file_or_list.nc var_name --fpath_out=name --lon_reg=-20,30 --lat_reg=-45,-20
    
    Plot on original triangle grid (it is recommended to cut the domain otherwise, it takes a long time):
    pyic_anim.py netcdf_file_or_list.nc var_name --fpath_out=name --use_tgrid --lon_reg=-72,-68 --lat_reg=33,35
    
    Change projection to North Polar Stereographic projection:
    pyic_anim.py netcdf_file_or_list.nc var_name --fpath_out=name --projection=np
    
    Test with showing only one figure without saving anything:
    pyic_anim.py netcdf_file.nc var_name --test
    
    Only re-creating the animation if the single figures are still available under fpath_out
    pyic_anim.py netcdf_file.nc var_name --fpath_out=name --only_animation
    
    
    Argument list:
    --------------
    """
    
    # --- read input arguments
    parser = argparse.ArgumentParser(description=help_text, formatter_class=argparse.RawTextHelpFormatter)
    
    # --- necessary arguments
    parser.add_argument('fpath_data', nargs='+', metavar='fpath_data', type=str,
                        help='Path to ICON data file.')
    parser.add_argument('var', metavar='var', type=str,
                        help='Name of variable which should be plotted.')
    # --- optional arguments
    # --- figure saving / showing
    parser.add_argument('--fpath_out', type=str, default='none',
                        help='Path to save the animation (without ending).')
    parser.add_argument('--dontshow', action='store_true', default=False,
                        help='If dontshow is specified, the plot is not shown')
    parser.add_argument('--only_animation', default=False,
                        action='store_true',
                        help='If specified, only the animation and no new figures are generated.')
    parser.add_argument('--test', default=False,
                        action='store_true',
                        help='If specified, just a test plot is made.')
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
    parser.add_argument('--it', type=str, default='none',
                        help='Time index limits of the animation. Specify like this: --it=start_index,end_index,[optional:increment] If \'auto\' is specified all time instances are plotted.')
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
    
    # --- specific for horizontal plot parser.add_argument('--iz', type=int, default=0,
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
    
    # --- ffmpeg specific parameters
    parser.add_argument('--dpi', type=float, default=250.,
                        help='Resolution for the individual saved figures (default --dpi=250).')
    parser.add_argument('--ffmpeg', type=str, default="/work/mh0033/m300602/miniconda3/envs/pyicon_py39_exp/bin/ffmpeg",
                        help='Path to ffmpeg.')
    parser.add_argument('--framerate', type=int, default=10,
                        help='ffmpeg framerate (-r).')
    parser.add_argument('--vcodec', type=str, default='libx264',
                        help='ffmpeg video codec.')
    parser.add_argument('--bitrate', type=str, default='12000k',
                        help='ffmpeg video bitrate (-b:v).')
    
    iopts = parser.parse_args()
    
    # these options seem not to be used
    gname = iopts.gname
    use_tgrid = iopts.use_tgrid
    fpath_tgrid = iopts.fpath_tgrid
    fpath_ckdtree = iopts.fpath_ckdtree
    
    print('start modules')
    import matplotlib
    if iopts.dontshow:
      matplotlib.use('Agg')
    import numpy as np
    import matplotlib.pyplot as plt
    import cartopy
    import cartopy.crs as ccrs
    import xarray as xr
    import glob
    import os
    import sys
    from pathlib import Path
    sys.path.append(f'{Path.home()}/pyicon/')
    import pyicon as pyic  
    print('Done modules.')
    
    def str_to_array(string):
      string = string.replace(' ', '')
      array = np.array(string.split(','), dtype=float)
      return array
    
    path = os.path.dirname(iopts.fpath_out)
    if not os.path.exists(path):
      os.makedirs(path)
    
    if not iopts.only_animation:
      if iopts.cmap.startswith('cmo.'):
        import cmocean
        iopts.cmap = getattr(cmocean.cm, iopts.cmap.split('.')[1])
      
      #flist = glob.glob(iopts.fpath_data)
      flist = iopts.fpath_data
      flist.sort()
      
      # --- limits
      if iopts.clim!='auto':
        iopts.clim = str_to_array(iopts.clim)
      if iopts.lon_reg:
        iopts.lon_reg = str_to_array(iopts.lon_reg)
      if iopts.lat_reg:
        iopts.lat_reg = str_to_array(iopts.lat_reg)
      if iopts.central_longitude is None:
        iopts.central_longitude = 'auto'
      if iopts.it!='none':
        itsplit = iopts.it.split(',')
        if len(itsplit)==2:
          iopts.it = slice(int(itsplit[0]), int(itsplit[1]))
        elif len(itsplit)==3:
          iopts.it = slice(int(itsplit[0]), int(itsplit[1]), inst(itsplit[2]))
      if iopts.time!='none':
        timesplit = iopts.time.split(',')
        iopts.time = slice(timesplit[0], timesplit[1])
      
      # --- open dataset and select data
      ts = pyic.timing(ts, string='open_mfdataset')
      try:
        mfdset_kwargs = dict(combine='nested', concat_dim='time',
                             data_vars='minimal', coords='minimal',
                             compat='override', join='override', parallel=True)
        ds = xr.open_mfdataset(flist, **mfdset_kwargs)
      except:
        try:
          print('open_mfdset: parallel=True did not work, try without.')
          mfdset_kwargs = dict(combine='nested', concat_dim='time',
                               data_vars='minimal', coords='minimal',
                               compat='override', join='override')
          ds = xr.open_mfdataset(flist, **mfdset_kwargs)
        except:
          print('open_mfdset: mfdset options did not work, trying without...')
          ds = xr.open_mfdataset(flist)
      data = ds[iopts.var]
      data = data.assign_attrs(uuidOfHGrid=ds.attrs['uuidOfHGrid'])
    
      # --- re-chunk data to allow for plotting from big files
      chunks = dict()
      if 'time' in data.dims:
        chunks = dict(time=1)
      depth_name = pyic.identify_depth_name(data)
      if depth_name!='none':
        chunks[depth_name] = 1
      data = data.chunk(chunks)
      
      # --- select vertical coordinate
      if depth_name!='none':
        if iopts.depth!=-1:
          data = data.sel({depth_name: iopts.depth}, method='nearest')
        else:
          data = data.isel({depth_name: iopts.iz})
      # --- select time coordinate
      if not isinstance(iopts.it, str):
        data = data.isel(time=iopts.it)
      if not isinstance(iopts.time, str):
        data = data.sel(time=iopts.time)
    
      # --- get plotting arguments
      pkws = vars(iopts).copy()
      drop_items = [
        'data', 'var', 'fpath_fig', 'dontshow',
        'it', 'time', 'iz', 'depth', 
        'use_tgrid',
        'catalog', 'catdict', 'model',
        'factor',
        'fpath_data', 'bitrate', 'vcodec', 'framerate', 'ffmpeg', 'dpi',
        'fpath_out', 'only_animation', 'test',
      ]
      for key in drop_items:
        pkws.pop(key, None)
      
      # --- time loop
      nfig=-1
      for ll in range(data.time.size):
        nfig += 1
        fpath_out_final = f'{iopts.fpath_out}_{nfig:04d}.jpg'
        ts = pyic.timing(ts, string=f'll = {ll}/{data.time.size}, {str(data.time[ll].data)} {fpath_out_final}')
    
        plt.close('all')
        data_loc = data.isel(time=ll)
        ax, hm = pyic.plot(data_loc, **pkws)
        if iopts.test:
          plt.show()
          sys.exit()
        plt.savefig(fpath_out_final, dpi=iopts.dpi)
    
    ts = pyic.timing(ts, string='generate movie')
    os.system(f'{iopts.ffmpeg} -y -r {iopts.framerate} -f image2 -i {iopts.fpath_out}_%04d.jpg -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" -vcodec {iopts.vcodec} -b:v {iopts.bitrate} {iopts.fpath_out}.mp4')
    
    ts = pyic.timing(ts, string='All done!')

if __name__ == "__main__":
  main()
