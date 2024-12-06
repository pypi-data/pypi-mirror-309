import pytest
import pyicon as pyic
import xarray as xr
import matplotlib.pyplot as plt
from .conftest import lazy_examp_icon_dataarray, eager_examp_icon_dataarray


@pytest.mark.parametrize(
    "examp_icon_dataarray", ["lazy_examp_icon_dataarray", "eager_examp_icon_dataarray"]
)
@pytest.mark.parametrize("grid_type,", ["auto", "native"])
def test_plot(examp_icon_dataarray, grid_type, request):
    examp_icon_dataarray = request.getfixturevalue(examp_icon_dataarray)
    pyic.plot(examp_icon_dataarray.isel(time=0, depth=0), grid_type=grid_type)
    return


@pytest.mark.parametrize(
    "examp_icon_dataarray", ["lazy_examp_icon_dataarray", "eager_examp_icon_dataarray"]
)
def test_plot_sec(examp_icon_dataarray, request):
    examp_icon_dataarray = request.getfixturevalue(examp_icon_dataarray)
    pyic.plot_sec(examp_icon_dataarray.isel(time=0), section="170W")
    return
