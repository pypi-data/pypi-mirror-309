#!/usr/bin/env python
import os
import glob
import yaml
import argparse
from ipdb import set_trace as mybreak
import sys
from netCDF4 import Dataset
import pandas as pd

def combine_catalogs(catalog):
    catalog = _get_main_catalog(catalog)
    data_all = dict()
    data_all["sources"] = dict()
    
    path_catalog = os.path.dirname(os.path.abspath(catalog))
    catlist = glob.glob(f"{path_catalog}/cat_*.yaml")
    catlist.sort()
    
    # assuming that every catalog only contains one simulation
    for fname in catlist:
        with open(fname, "r") as file:
            print(f"Adding {fname}")
            data = yaml.safe_load(file)
            key = list(data["sources"])[0]
            data_all["sources"][key] = data["sources"][key]
    
    with open(catalog, "w") as file:
        yaml.dump(data_all, file, default_flow_style=False)
    return

def simulation_info_to_yaml(fpath_cat, fpath_cat_info):
    import pyicon as pyic
    Dmain = dict()
    Dmain['sources'] = dict()
    with open(fpath_cat, 'r') as file:
        cat_yaml = yaml.safe_load(file)["sources"]
    for run in list(cat_yaml):
        Dmain['sources'][run] = dict()
        urlpath_sim = cat_yaml[run]['args']['urlpath']
        tags = cat_yaml[run]["parameters"]["tag"]["allowed"]
        for tag in tags:
            urlpath_tag = urlpath_sim.replace('{{tag}}', tag)
            # print(urlpath_tag)
            flist = glob.glob(urlpath_tag)
            flist.sort()
            f = Dataset(flist[0], 'r')
            variables = list(f.variables)
            t_start = pyic.nctime2numpy(f['time'])[0]
            try:
                t_2nd   = pyic.nctime2numpy(f['time'])[1]
                f.close()
            except:
                f.close()
                f = Dataset(flist[1], 'r')
                t_2nd = pyic.nctime2numpy(f['time'])[0]
            f = Dataset(flist[-1], 'r')
            t_end = pyic.nctime2numpy(f['time'])[-1]
            f.close()

            t_inc = (t_2nd-t_start).astype(float)/86400.
            if t_inc==1.:
                ofreq = '1D'
            elif t_inc==0.25:
                ofreq = '3H'
            elif t_inc>27.5 and t_inc<31.5:
                ofreq = '1M'
            elif t_inc>364.5 and t_inc<366.5:
                ofreq = '1Y'
            else:
                ofreq = 'unknown'
                print(f'unknown t_inc: {t_inc}')

            Dmain['sources'][run][tag]=dict()
            Dmain['sources'][run][tag]['variables']=variables
            Dmain['sources'][run][tag]['output_freq' ] = ofreq
            Dmain['sources'][run][tag]['simulation_intervall'] = f"{str(t_start)[:10]} - {str(t_end)[:10]}"
            Dmain['sources'][run][tag]['simulation_start'] = f"{str(t_start)[:10]}"
            Dmain['sources'][run][tag]['simulation_end']   = f"{str(t_end  )[:10]}"
    # print(f'Writing {fpath_cat_info}')
    with open(fpath_cat_info, 'w') as file:
        yaml.dump(Dmain, file, default_flow_style=False)
    return

def add(catalog, run, 
        path_data='./', 
        project='MPI-M ICON',
        description='',
        contact='',
        tstr='auto',
        fname_out='auto',
       ):

    catalog = _get_main_catalog(catalog)
    path_catalog = os.path.dirname(os.path.abspath(catalog))

    path_data = os.path.abspath(path_data)
    #urlpath = f"{path_data}/{run}_{{{{tag}}}}_????????????????.nc"
    urlpath = f"{path_data}/{run}_{{{{tag}}}}_*.nc"

    dirlist = glob.glob(path_data)
    
    if tstr=='auto':
        tmp_flist = glob.glob(f'{dirlist[0]}/{run}_*_????????????????.nc')
        flist = [item for item in tmp_flist if "restart" not in item]
        tstr = flist[0].split('_')[-1].split('.nc')[0]
        print(f'flist[0] = {flist[0]}')
        print(f'Using tstr={tstr}')

    searchstr = f"{path_data}/{run}_*_{tstr}.nc"
    print(f"Looking in the following path for tags: {searchstr}")
    fnames = glob.glob(searchstr)
    fnames.sort()
    tags = [0]*len(fnames)
    for nn, fname in enumerate(fnames):
        tags[nn] = fname.split('/')[-1].split(f'{run}_')[-1].split(f'_{tstr}.nc')[0]
    filtered_tags = [tag for tag in tags if "restart" not in tag]
    tags = filtered_tags
    print(f"Found the following tags: {tags}")

    Dmain = dict()
    Dmain['sources'] = dict()
    Dmain['sources'][run] = dict()
    Dmain['sources'][run]['args'] = dict(urlpath=urlpath)
    Dmain['sources'][run]['driver'] = 'netcdf'
    Dmain['sources'][run]['parameters'] = dict()
    Dmain['sources'][run]['parameters']['tag'] = dict()
    Dmain['sources'][run]['parameters']['tag']['allowed'] = tags
    Dmain['sources'][run]['parameters']['tag']['default'] = tags[0]
    Dmain['sources'][run]['parameters']['tag']['description'] = 'file tag'
    Dmain['sources'][run]['parameters']['tag']['type'] = 'str'
    
    Dmain['sources'][run]['metadata'] = dict()
    Dmain['sources'][run]['metadata']['project'] = project
    Dmain['sources'][run]['metadata']['simulation_id'] = run
    Dmain['sources'][run]['metadata']['description'] = description
    Dmain['sources'][run]['metadata']['contact'] = contact
    #Dmain['sources'][run]['metadata']['info_cat'] = '{{CATDIR}}/

#    if verbose:
#        print('----')
#        print(Dmain)
#        print('----')

    if fname_out=='auto':
        fname_out = f"cat_{run}.yaml"

    if not os.path.exists(path_catalog):
      os.makedirs(path_catalog)

    fpath_out = path_catalog+'/'+fname_out
    print(f"Writing path_catalog file {fpath_out}")
    with open(fpath_out, 'w') as file:
        yaml.dump(Dmain, file, default_flow_style=False)

    fpath_cat_info = f'{path_catalog}/info_{fname_out}'
    simulation_info_to_yaml(fpath_out, fpath_cat_info)
    #try:
    #    fpath_cat_info = f'{path_catalog}/info_{fname_out}'
    #    simulation_info_to_yaml(fpath_out, fpath_cat_info)
    #except Exception as e:
    #    print('::: Warning: Generation of catalog with additional inofrmation failed.')
    #    print(f'{e}')

    combine_catalogs(catalog)
    return

def ls(catalog, columns='all', rows='all'):
    catalog = _get_main_catalog(catalog)
    print(f" catalog: {catalog}")

    df = _yaml_to_pandas(catalog)
    if columns!='all':
        columns = columns.split(',')
        df = df[columns]
    if rows!='all':
        rows = rows.split(',')
        for value in rows:
            ind = df['name'].str.contains(value, na=False)
            df = df[ind]

    #with open(catalog, 'r') as file:
    #    Dmain = yaml.safe_load(file)
    #for run in list(Dmain['sources']):
    #    print(f'----------')
    #    print(f'{run}: {Dmain["sources"][run]["metadata"]["description"]}')
    #    print(f'  {Dmain["sources"][run]["args"]["urlpath"]}')
    #    print(f'  {Dmain["sources"][run]["metadata"]["contact"]}')
    print(df)
    return

def query(catalog, attribute, value):                                                  
    """
    Searches and filters entries in a specified YAML catalog file based on a given attribute and value.

    This function opens the specified catalog file (in YAML format), extracts relevant information
    about each data source, and filters the entries by checking if a specific attribute contains
    the given value. The results are returned as a pandas DataFrame.

    Parameters:
    ----------
    catalog : str
        Path to the YAML catalog file (e.g., "main_catalog.yaml").
    attribute : str
        The attribute to search within each entry (e.g., "description", "contact").
    value : str
        The value to search for within the specified attribute.

    Returns:
    -------
    pd.DataFrame
        A DataFrame containing the filtered entries with the following columns:
            - 'name': The name of the catalog item.
            - 'path_data': The path to the data (from the 'urlpath' field).
            - 'description': The description of the catalog item.
            - 'contact': The contact information for the catalog item.

    Example:
    --------
    >>> query("main_catalog.yaml", "description", "climate data")

    This will search for entries in 'main_catalog.yaml' where the 'description' field contains
    "climate data" and return a DataFrame with the relevant entries.
    """

    catalog = _get_main_catalog(catalog)
    df = _yaml_to_pandas(catalog)

    #ind = df[attribute]==value
    ind = df[attribute].str.contains(value, na=False)
    df_reduced = df[ind]
    print(df_reduced)
    return df_reduced

def _yaml_to_pandas(catalog):
    catalog = _get_main_catalog(catalog)
    with open(catalog, 'r') as f:
        Dyaml = yaml.safe_load(f)['sources']
    Dout = dict()
    for item in list(Dyaml):
      Dout[item] = dict()
      Dout[item]['name'] = item
      Dout[item]['path_data'] = Dyaml[item]['args']['urlpath']
      Dout[item]['description'] = Dyaml[item]['metadata']['description']
      Dout[item]['contact'] = Dyaml[item]['metadata']['contact']

    df = pd.DataFrame(Dout).transpose()
    return df

def _get_main_catalog(catalog):
    if catalog=='main':
        catalog = os.path.expanduser("~") + '/intake_pyicon/main_catalog.yaml'
    return catalog

def make_main(catalog):
    catalog = _get_main_catalog(catalog)
    with open(catalog, 'r') as file:
        Dmain = yaml.safe_load(file)
    return

def main():
    description_main = """
pyicon's CLI for handling ICON intake catalogs.

To get help for the individual functions use:
>>> pyic_intake.py func -h
    """

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=description_main,
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available functions")

    # --- add
    parser_add = subparsers.add_parser("add", help="Adds a simulation to the yaml intake catalog.")
    parser_add.add_argument("catalog", type=str,
        help="Catalog where simulation is storred. If 'main' is given then catalog is saved under ${HOME}/intake_pyicon/main_catalog.yaml")
    parser_add.add_argument("run", type=str, 
        help="Simulation name or id.")
    parser_add.add_argument("--path_data", type=str, default='./',
        help="Path to simulation data, can contain wildcards.")
    parser_add.add_argument("--project", type=str, default='MPI-M ICON',
        help="Optional name of a project in which this simulation is performed, e.g. ICON-XPP, NextGEMS etc.")
    parser_add.add_argument("--description", type=str, default='',
        help="Some brief informative text that describes the simulation.")
    parser_add.add_argument("--contact", type=str, default='',
        help="Give a contact persion.")
    parser_add.add_argument("--tstr", type=str, default='auto',
        help="Time string that should be used to identify simulation tags. Speficy only if automatic indentification does not work.")
    parser_add.add_argument("--fname_out", type=str, default='auto',
        help="Name of simulation catalog. Default is `cat_{run}.yaml`")

    parser_add.set_defaults(func=lambda args: add(args.catalog, args.run, args.path_data,
        args.project, args.description, args.contact, args.tstr, args.fname_out))

    # --- ls
    parser_ls = subparsers.add_parser("ls", help="List simulations within a yaml intake catalog.")
    parser_ls.add_argument("catalog", type=str,
        help="Catalog to browse through. If 'main' is given then catalog is saved under ${HOME}/intake_pyicon/main_catalog.yaml")  
    parser_ls.add_argument("--columns", type=str, default='all',
        help="If not 'all' then only the comma separated list of columns is shown (do not use white spaces). Example: --columns=name,contact")
    parser_ls.add_argument("--rows", type=str, default='all',
        help="If not 'all' then only the comma separated list of rows is shown (do not use white spaces). Example: --rows=name,contact")

    parser_ls.set_defaults(func=lambda args: ls(args.catalog, args.columns, args.rows)) 

    # --- query
    parser_query = subparsers.add_parser("query", description=query.__doc__,
        formatter_class=argparse.RawTextHelpFormatter,
        help="Queries and intake catalog regarding a specified attribute and a specified value.", )
    parser_query.add_argument("catalog", type=str, 
        help="Adress of  catalog to query.")
    parser_query.add_argument("attribute", type=str,
        help="Attribute that should be looked through.")
    parser_query.add_argument("value", type=str,
        help="The value that should match the attribute.")

    parser_query.set_defaults(func=lambda args: query(args.catalog, args.attribute, args.value)) 

    # parse the arguments and 
    args = parser.parse_args()
    # call the appropriate function
    args.func(args)

    ## call the function with parsed arguments
    #generate_simulation_catalog(
    #    args.run, 
    #    path_data=args.path_data,
    #    description=args.description, 
    #    tstr=args.tstr, 
    #    fname_out=args.fname_out, 
    #    catalog_dir=args.catalog_dir,
    #)

if __name__ == "__main__":
  main()
