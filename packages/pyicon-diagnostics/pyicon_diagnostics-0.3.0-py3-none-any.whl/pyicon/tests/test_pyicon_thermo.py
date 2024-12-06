import numpy as np
from pyicon.pyicon_thermo import _calculate_mpiom_density, _calculate_insitu_temperature


def test_mpiom_density():
    """the test values come from A3.2 of Gill (1982), Atmospheric & Ocean
    Dynamics
    """
    assert np.allclose(_calculate_mpiom_density(0, 5, 0), 999.96675, atol=1e-5)
    assert np.allclose(_calculate_mpiom_density(35, 5, 0), 1027.67547, atol=1e-5)
    assert np.allclose(_calculate_mpiom_density(35, 25, 1000), 1062.53817, atol=1e-5)


def test_insitu_temperature():
    """the test values come from A3.5 of Gill (1982), Atmospheric & Ocean
    Dynamics
    """
    assert np.allclose(
        _calculate_insitu_temperature(25, 8.4678516, 1000), 10, atol=1e-7
    )
