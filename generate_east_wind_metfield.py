import sys

import xarray as xr

# Modify restart file
if len(sys.argv) != 2:
    raise ValueError("You didn't give the path to the initial C48 restart file")
ds = xr.open_dataset(sys.argv[1])

ds.U[::] = 30
ds.V[::] = 0
ds.RH[::] = 0.7
ds.DTRAIN[::] = 0
ds.OMEGA[::] = 0

# Write
ds.to_netcdf('/extra-space/uncompressed-prescribed-metfields.nc',  format='NETCDF4_CLASSIC')


