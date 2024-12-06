import numpy as np
import pandas as pd
import xarray as xr
from pandas import DataFrame
from skyfield import almanac
from skyfield import api
import gsw
import warnings


def _check_necessary_variables(ds: xr.Dataset, vars: list):
    """
    Checks that all of a list of variables are present in a dataset

    Parameters
    ----------
    ds (xarray.Dataset): _description_
    vars (list): _description_

    Raises
    ----------
    KeyError: Raises an error if all vars not present in ds

    Original author
    ----------------
    Callum Rollo
    """
    missing_vars = set(vars).difference(set(ds.variables))
    if missing_vars:
        msg = f"Required variables {list(missing_vars)} do not exist in the supplied dataset."
        raise KeyError(msg)


def _calc_teos10_variables(ds):
    """
    Calculates TEOS 10 variables not present in the dataset
    :param ds:
    :return:
    """
    _check_necessary_variables(ds, ['DEPTH', 'LONGITUDE', 'LATITUDE', 'TEMP', 'PSAL'])
    if 'DENSITY' not in ds.variables:
        SA = gsw.SA_from_SP(ds.PSAL, ds.DEPTH, ds.LONGITUDE, ds.LATITUDE)
        CT = gsw.CT_from_t(SA, ds.TEMP, ds.DEPTH)
        ds['DENSITY'] = ('N_MEASUREMENTS', gsw.rho(SA, CT, ds.DEPTH).values)
    return ds


def construct_2dgrid(x, y, v, xi=1, yi=1):
    """
    Function to grid data
    
    Parameters
    ----------
    x: data with data for the x dimension
    y: data with data for the y dimension
    v: data with data for the z dimension
    xi: Horizontal resolution for the gridding
    yi: Vertical resolution for the gridding
                
    Returns
    -------
    grid: z data gridded in x and y space with xi and yi resolution
    XI: x data gridded in x and y space with xi and yi resolution
    YI: y data gridded in x and y space with xi and yi resolution

    Original author
    ----------------
    Bastien Queste (https://github.com/bastienqueste/gliderad2cp/blob/de0652f70f4768c228f83480fa7d1d71c00f9449/gliderad2cp/process_adcp.py#L140)
    
    """
    if np.size(xi) == 1:
        xi = np.arange(np.nanmin(x), np.nanmax(x) + xi, xi)
    if np.size(yi) == 1:
        yi = np.arange(np.nanmin(y), np.nanmax(y) + yi, yi)
    raw = pd.DataFrame({'x': x, 'y': y, 'v': v}).dropna()
    grid = np.full([np.size(xi), np.size(yi)], np.nan)
    raw['xbins'], xbin_iter = pd.cut(raw.x, xi, retbins=True, labels=False)
    raw['ybins'], ybin_iter = pd.cut(raw.y, yi, retbins=True, labels=False)
    _tmp = raw.groupby(['xbins', 'ybins'])['v'].agg('median')
    grid[_tmp.index.get_level_values(0).astype(int), _tmp.index.get_level_values(1).astype(int)] = _tmp.values
    YI, XI = np.meshgrid(yi, xi)
    return grid, XI, YI

def compute_cline(var, depth_array):
    """
    Find the depth of the maximum vertical difference for a specified variables
    
    Parameters
    ----------
    var: 2D array containing data from a selected variable gridded over time/profile/distance etc. and depth (y-axis))
    depth_array: 2D array containing pressure/depth data gridded over time/profile/distance etc. and depth (y-axis))
    
    Returns
    -------
    1D array containing the depth of the cline at each timestamp/profile/distance etc.
    Original author
    ----------------
    Chiara Monforte
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        clin = np.where(np.abs(np.diff(np.nanmean(var, axis=0))) == np.nanmax(np.abs(np.diff(np.nanmean(var, axis=0)))))
    return np.round(depth_array[0, clin[0]], 1)


def compute_sunset_sunrise(time, lat, lon):
    """
    Calculates the local sunrise/sunset of the glider location from GliderTools.

    The function uses the Skyfield package to calculate the sunrise and sunset
    times using the date, latitude and longitude. The times are returned
    rather than day or night indices, as it is more flexible for the quenching
    correction.


    Parameters
    ----------
    time: numpy.ndarray or pandas.Series
        The date & time array in a numpy.datetime64 format.
    lat: numpy.ndarray or pandas.Series
        The latitude of the glider position.
    lon: numpy.ndarray or pandas.Series
        The longitude of the glider position.

    Returns
    -------
    sunrise: numpy.ndarray
        An array of the sunrise times.
    sunset: numpy.ndarray
        An array of the sunset times.

    Original author
    ----------------
    Function from GliderTools (https://github.com/GliderToolsCommunity/GliderTools/blob/master/glidertools/optics.py)

    """

    ts = api.load.timescale()
    eph = api.load("de421.bsp")

    df = DataFrame.from_dict(dict([("time", time), ("lat", lat), ("lon", lon)]))

    # set days as index
    df = df.set_index(df.time.values.astype("datetime64[D]"))

    # groupby days and find sunrise/sunset for unique days
    grp_avg = df.groupby(df.index).mean(numeric_only=False)
    date = grp_avg.index

    time_utc = ts.utc(date.year, date.month, date.day, date.hour)
    time_utc_offset = ts.utc(
        date.year, date.month, date.day + 1, date.hour
    )  # add one day for each unique day to compute sunrise and sunset pairs

    bluffton = []
    for i in range(len(grp_avg.lat)):
        bluffton.append(api.wgs84.latlon(grp_avg.lat.iloc[i], grp_avg.lon.iloc[i]))
    bluffton = np.array(bluffton)

    sunrise = []
    sunset = []
    for n in range(len(bluffton)):

        f = almanac.sunrise_sunset(eph, bluffton[n])
        t, y = almanac.find_discrete(time_utc[n], time_utc_offset[n], f)

        if not t:
            if f(time_utc[n]):  # polar day
                sunrise.append(
                    pd.Timestamp(
                        date[n].year, date[n].month, date[n].day, 0, 1
                    ).to_datetime64()
                )
                sunset.append(
                    pd.Timestamp(
                        date[n].year, date[n].month, date[n].day, 23, 59
                    ).to_datetime64()
                )
            else:  # polar night
                sunrise.append(
                    pd.Timestamp(
                        date[n].year, date[n].month, date[n].day, 11, 59
                    ).to_datetime64()
                )
                sunset.append(
                    pd.Timestamp(
                        date[n].year, date[n].month, date[n].day, 12, 1
                    ).to_datetime64()
                )

        else:
            sr = t[y == 1]  # y=1 sunrise
            sn = t[y == 0]  # y=0 sunset

            sunup = pd.to_datetime(sr.utc_iso()).tz_localize(None)
            sundown = pd.to_datetime(sn.utc_iso()).tz_localize(None)

            # this doesn't look very efficient at the moment, but I was having issues with getting the datetime64
            # to be compatible with the above code to handle polar day and polar night

            su = pd.Timestamp(
                sunup.year[0],
                sunup.month[0],
                sunup.day[0],
                sunup.hour[0],
                sunup.minute[0],
            ).to_datetime64()

            sd = pd.Timestamp(
                sundown.year[0],
                sundown.month[0],
                sundown.day[0],
                sundown.hour[0],
                sundown.minute[0],
            ).to_datetime64()

            sunrise.append(su)
            sunset.append(sd)

    sunrise = np.array(sunrise).squeeze()
    sunset = np.array(sunset).squeeze()

    grp_avg["sunrise"] = sunrise
    grp_avg["sunset"] = sunset

    # reindex days to original dataframe as night
    df_reidx = grp_avg.reindex(df.index)
    sunrise, sunset = df_reidx[["sunrise", "sunset"]].values.T

    return sunrise, sunset

def calc_DEPTH_Z(ds):
    """
    Calculate the depth (Z position) of the glider using the gsw library to convert pressure to depth.
    
    Parameters
    ----------
    ds (xarray.Dataset): The input dataset containing 'PRES', 'LATITUDE', and 'LONGITUDE' variables.
    
    Returns
    -------
    xarray.Dataset: The dataset with an additional 'DEPTH_Z' variable.

    Original author
    ----------------
    Eleanor Frajka-Williams
    """
    _check_necessary_variables(ds, ['PRES', 'LONGITUDE', 'LATITUDE'])

    # Initialize the new variable with the same dimensions as dive_num
    ds['DEPTH_Z'] = (['N_MEASUREMENTS'], np.full(ds.dims['N_MEASUREMENTS'], np.nan))

    # Calculate depth using gsw
    depth = gsw.z_from_p(ds['PRES'], ds['LATITUDE'])
    ds['DEPTH_Z'] = depth

    # Assign the calculated depth to a new variable in the dataset
    ds['DEPTH_Z'].attrs = {
        "units": "meters",
        "positive": "up",
        "standard_name": "depth",
        "comment": "Depth calculated from pressure using gsw library, positive up.",
    }
    
    return ds
