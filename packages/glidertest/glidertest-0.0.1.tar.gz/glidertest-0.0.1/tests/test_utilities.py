import pytest
from glidertest import fetchers, utilities
import matplotlib
matplotlib.use('agg')  # use agg backend to prevent creating plot windows during tests

def test_utilitiesmix():
    ds = fetchers.load_sample_dataset()
    utilities._check_necessary_variables(ds, ['PROFILE_NUMBER', 'DEPTH', 'TEMP', 'PSAL', 'LATITUDE', 'LONGITUDE'])
    ds = utilities._calc_teos10_variables(ds)
    p = 1
    z = 1
    tempG, profG, depthG = utilities.construct_2dgrid(ds.PROFILE_NUMBER, ds.DEPTH, ds.TEMP, p, z)
    denG, profG, depthG = utilities.construct_2dgrid(ds.PROFILE_NUMBER, ds.DEPTH, ds.DENSITY, p, z)

    halo = utilities.compute_cline(denG, depthG)


def test_sunset_sunrise():
    ds = fetchers.load_sample_dataset()
    sunrise, sunset = utilities.compute_sunset_sunrise(ds.TIME, ds.LATITUDE, ds.LONGITUDE)


def test_depth_z():
    ds = fetchers.load_sample_dataset()
    assert 'DEPTH_Z' not in ds.variables
    ds = utilities.calc_DEPTH_Z(ds)
    assert 'DEPTH_Z' in ds.variables
    assert ds.DEPTH_Z.min() < -50
