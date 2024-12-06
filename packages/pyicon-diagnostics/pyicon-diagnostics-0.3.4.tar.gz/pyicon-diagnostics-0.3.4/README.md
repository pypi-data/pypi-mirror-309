# User guide for pyicon

Pyicon is a python post-processing and visualization toolbox for ICON with a focus on ocean data. The three main features of pyicon are:

* a number of functions to facilitate the every-day script-based plotting of ICON data
* an interactive (ncview-like) plotting GUI for Jupyter notebook
* a monitoring suite for ICON ocean simulations which combines dedicated diagnostic plots of an ICON simulation on a website

Pyicon is developed within the DFG-project TRR181 - Energy Transfers in Atmosphere and Ocean.

The pyicon documentation can be found here: [documentation](https://m300602.gitlab-pages.dkrz.de/pyicon/)

Pyicon is hosted at: (https://gitlab.dkrz.de/m300602/pyicon/)

## Quick start for pyicon 

You can install pyicon via pip:

```bash
pip install pyicon-diagnostics
```

However, if you want to use the most recent development version, it is advisable to
download pyicon with git:

```bash
git clone git@gitlab.dkrz.de:m300602/pyicon.git
```

Install pyicon by:

```bash
cd pyicon
pip install -e ./
```

If you notice that some requirements were not met by the installation, you can 
also use conda to install the requirements:

```bash
conda env create -f ci/requirements_latest.yml
```

or on DKRZ's super computer Levante use

``` bash
module load python3/2023.01-gcc-11.2.0
pip install healpy
```

To update pyicon, you only need to enter the pyicon directory update the git repository via

```bash
git pull
```

## Quick start for pyicon @DWD (Confluence, only intern)
https://ninjoservices.dwd.de/wiki/display/KUQ/pyICON+for+ICON+with+NWP+physics

## Installing locally

You can also install `pyicon` locally via `pip`. However, due to dependencies of `cartopy` it is advised to install `cartopy` first via `conda`.

```bash
conda install xarray cartopy dask -c conda-forge
```

Once, `cartopy` is installed in your environment:

```bash
pip install git+https://gitlab.dkrz.de/m300602/pyicon.git
```

## Developing
When adding new functions, make sure to document them with a docstring. This should detail what the function does, the arguments and what type of objects it returns. Examples are encouraged. We use so-called "numpy" style docstrings which are then automatically rendered into the sphinx documentation. A guide to numpy style docstrings is available [here](https://numpydoc.readthedocs.io/en/latest/format.html) and they even produce some nice [examples](https://numpydoc.readthedocs.io/en/latest/example.html#example).
