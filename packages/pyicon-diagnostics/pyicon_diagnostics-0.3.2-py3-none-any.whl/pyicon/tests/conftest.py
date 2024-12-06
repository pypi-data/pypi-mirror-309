from pathlib import Path
import pytest
import xarray as xr
import pyicon as pyic


@pytest.fixture()
def lazy_raw_grid():
    path_data = Path(pyic.params["path_example_data"])
    path_data.mkdir(parents=True, exist_ok=True)
    grid_path = path_data / "icon_grid_0014_R02B04_O.nc"

    if not grid_path.exists():
        import requests

        grid_download_link = "http://icon-downloads.mpimet.mpg.de/grids/public/mpim/0014/icon_grid_0014_R02B04_O.nc"
        try:
            r = requests.get(grid_download_link, allow_redirects=True)
            with open(grid_path, "wb") as grid_file:
                grid_file.write(r.content)
        except:
            raise FileNotFoundError(
                "{grid_path} does not exist and unable to \
                download it"
            )

    ds_grid = xr.open_dataset(grid_path, chunks="auto")
    return ds_grid


@pytest.fixture()
def eager_raw_grid(lazy_raw_grid):
    ds_raw_grid = lazy_raw_grid.compute()
    return ds_raw_grid


@pytest.fixture()
def lazy_processed_tgrid(lazy_raw_grid):
    return pyic.convert_tgrid_data(lazy_raw_grid)


@pytest.fixture()
def eager_processed_tgrid(eager_raw_grid):
    return pyic.convert_tgrid_data(eager_raw_grid)


@pytest.fixture()
def lazy_examp_icon_dataset():
    path_data = Path(pyic.params["path_example_data"])
    path_data.mkdir(parents=True, exist_ok=True)
    fpath_data = path_data / "icon_example_data_r2b4.nc"

    if not fpath_data.exists():
        import requests

        #download_link = "https://swift.dkrz.de/v1/dkrz_83018ad4-3c8d-4c7d-b684-7ba0742caa1a/pyicon_test_data/icon_example_data_r2b4.nc?temp_url_sig=03fb5d20a44832c7cf736ab83c1be3936364dbf6&temp_url_expires=2026-11-24T11:53:16Z"
        download_link = "https://swift.dkrz.de/v1/dkrz_07387162e5cd4c81b1376bd7c648bb60/pyicon_example_data/example_data_r2b4/icon_example_data_r2b4.nc"
        try:
            r = requests.get(download_link, allow_redirects=True, stream=True)
            with open(fpath_data, "wb") as fobj:
                fobj.write(r.content)
        except:
            raise FileNotFoundError(
                "{fpath_data} does not exist and unable to \
                download it"
            )

    ds = xr.open_dataset(fpath_data, chunks="auto")
    return ds


@pytest.fixture()
def eager_examp_icon_dataset(lazy_examp_icon_dataset):
    return lazy_examp_icon_dataset.compute()


@pytest.fixture()
def lazy_examp_icon_dataarray(lazy_examp_icon_dataset):
    return lazy_examp_icon_dataset["to"]


@pytest.fixture()
def eager_examp_icon_dataarray(eager_examp_icon_dataset):
    return eager_examp_icon_dataset["to"]
