import numpy as np
import xarray as xr


def _calculate_eos_pressure(da_depth, da_zos=0, da_stretch_c=1):
    """calculates hydrostatic pressure for the equation of state

    Parameters
    ----------
    da_depth : xr.DataArray
        depth in the water column in metres
        
    da_zos : xr.DataArray or 0, optional
        sea surface height in metres
        
    da_stretch_c : xr.DataArray or 1, optional
        stretch factor from zstar

        
    Returns
    -------
    p : xr.DataArray
        hydrostatic pressure as required by the equation of state in dBar

        
    Notes
    -----
    The pressure does not include atmospheric pressure. This is neglected by
    the equation of state used in ICON.
    """
    SItodBar = 1e-4
    rho_ref = 1025.022

    p = (da_stretch_c * da_depth + da_zos) * rho_ref * SItodBar
    return p


def _calculate_insitu_temperature(sal, t_pot, p):
    """calculates in-situ temperature from model variables and pressure.

    Parameters
    ----------
    sal : xr.DataArray
        salinity in PSU
    
    t_pot : xr.DataArray
        potential temperature (what ICON outputs) in deg C
    
    p : xr.DataArray
        pressure in dBar


    Returns
    -------
    t_insitu : xr.DataArray
        in-situ temperature in deg C
    """
    a_a1 = 3.6504e-4
    a_a2 = 8.3198e-5
    a_a3 = 5.4065e-7
    a_a4 = 4.0274e-9
    
    a_b1 = 1.7439e-5
    a_b2 = 2.9778e-7
    
    a_c1 = 8.9309e-7
    a_c2 = 3.1628e-8
    a_c3 = 2.1987e-10
    
    a_d = 4.1057e-9
    
    a_e1 = 1.6056e-10
    a_e2 = 5.0484e-12
    
    z_sref = 35e0
    
    
    qnq = -p * (-a_a3 + p * a_c3)
    qn3 = -p * a_a4
    qvs = (p * (a_b1 - a_d * p)) * (sal - z_sref) + p * (a_a1 + p * (a_c1 - a_e1 * p))
    dvs = (a_b2 * p) * (sal - z_sref) + 1 + p * (-a_a2 + p * (a_c2 - a_e2 * p))

    t   = (t_pot + qvs) / dvs
    fne = - qvs + t * (dvs + t * (qnq + t * qn3)) - t_pot
    fst = dvs + t * (2 * qnq + 3 * qn3 * t)

    t_insitu   = t - fne / fst
    return t_insitu


def _calculate_mpiom_density(sal, t_insitu, p):
    """calculates potential density

    Parameters
    ----------
    sal : xr.DataArray
        salinity in PSU
    
    t_insitu : xr.DataArray
        in-situ temperature in deg C
    
    p : xr.DataArray
        pressure in dBar


    Returns
    -------
    rho : xr.DataArray
        density in kg / m^3
    """
    r_a0=999.842594
    r_a1=6.793952e-2
    r_a2=-9.095290e-3
    r_a3=1.001685e-4
    r_a4=-1.120083e-6
    r_a5=6.536332e-9
    
    r_b0 = 8.24493e-1
    r_b1 = -4.0899e-3
    r_b2 = 7.6438e-5
    r_b3 = -8.2467e-7
    r_b4 = 5.3875e-9
    
    r_c0 = -5.72466e-3
    r_c1 = 1.0227e-4
    r_c2 = -1.6546e-6
    
    r_d0=4.8314e-4
    
    r_e1 = 148.4206
    r_e0 = 19652.21
    r_e2 = -2.327105
    r_e3 = 1.360477e-2
    r_e4 = -5.155288e-5
    
    r_f0 = 54.6746
    r_f1 = -0.603459
    r_f2 = 1.09987e-2
    r_f3 = -6.1670e-5
    
    r_g0 = 7.944e-2
    r_g1 = 1.6483e-2
    r_g2 = -5.3009e-4
      
    r_h0 = 3.239908
    r_h1 = 1.43713e-3
    r_h2 = 1.16092e-4
    r_h3 = -5.77905e-7
    
    r_ai0 = 2.2838e-3
    r_ai1 = -1.0981e-5
    r_ai2 = -1.6078e-6
    
    r_aj0 = 1.91075e-4
    
    r_ak0 = 8.50935e-5
    r_ak1 = -6.12293e-6
    r_ak2 = 5.2787e-8
    
    r_am0 = -9.9348e-7
    r_am1 = 2.0816e-8
    r_am2 = 9.1697e-10

    t = t_insitu
    s = xr.where(sal > 0.0, sal, 0.0)
    s_2 = np.square(s)
    s3h  = s * np.sqrt(s)
    
    rho = r_a0 + t * (r_a1 + t * (r_a2 + t * (r_a3 + t * (r_a4 + t * r_a5)))) \
        + s * (r_b0 + t * (r_b1 + t * (r_b2 + t * (r_b3 + t * r_b4)))) \
        + r_d0 * s_2 + s3h * (r_c0 + t * (r_c1 + r_c2 * t))

    denom = 1.0 - p / (p * (r_h0 + t * (r_h1 + t * (r_h2 + t * r_h3)) \
        + s * (r_ai0 + t * (r_ai1 + r_ai2 * t)) + r_aj0 * s3h + (r_ak0 \
        + t * (r_ak1 + t * r_ak2) \
        + s * (r_am0 + t * (r_am1 + t * r_am2))) * p) + r_e0 \
        + t * (r_e1 + t * (r_e2 + t * (r_e3 + t * r_e4))) \
        + s * (r_f0 + t * (r_f1 + t * (r_f2 + t * r_f3))) \
        + s3h * (r_g0 + t * (r_g1 + r_g2 * t)))
    rho = rho/denom

    return rho


def calculate_density(so, to, zos=0, stretch_c=1, depth=None, eos_type="mpiom"):
    """calculates density from model variables

    Parameters
    ----------
    to : xr.DataArray
        potential temperature in deg C
    
    so : xr.DataArray
        salinity in PSU
    
    zos : xr.DataArray or 0, optional
        sea surface height in metres, by default 0
    
    stretch_c : xr.DataArray or 1, optional
        zos stretch factor, by default 1
    
    depth : xr.DataArray, optional
        Array containing depth in metres at prism centres, by default taken
        from to. Depth should be increasingly positive with distance below the
        surface.
    
    eos_type : str, optional
        which equation of state to use, by default "mpiom"


    Returns
    -------
    rho : xr.DataArray
        potential density


    Raises
    ------
    TypeError
        raised when depth not provided as a kwarg and also not found as a 
        coordinate on to
    
    NotImplementedError
        raised when an unrecognised equation of state is requested

        
    Notes
    -----
    Equations of state are not necessarily linear. When this is the case, the
    time mean density can not be obtained from the the time mean temperature
    and salinity. To minimise error you should either calculate the density
    online at model run time, or use the highest temporal frequency of output
    available in your calculations.
    """    
    if depth is None:
        try:
            depth = to["depth"]
        except KeyError:
            raise TypeError(
                "depth not found in to. Please provide depth as a kwarg."
                )
    
    if eos_type == "mpiom" or eos_type == "gill":
        # Then this is mpiom equation of state
        p = _calculate_eos_pressure(depth, da_zos=zos, da_stretch_c=stretch_c)
        t_insitu = _calculate_insitu_temperature(so, to, p)
        rho = _calculate_mpiom_density(so, t_insitu, p)
        
    else:
        raise NotImplementedError("The requested eos is not implemented")
    
    return rho
        