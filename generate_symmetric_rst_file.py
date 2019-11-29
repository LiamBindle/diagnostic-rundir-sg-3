import sys

import numpy as np
import xarray as xr

# Generate spots
def super_gaussian(x, y, A, x0, y0, sigma, P=1):
    return A* np.exp(-(((x-x0)**2/(2*sigma**2))**P + ((y-y0)**2/(2*sigma**2))**P))
spot = lambda xx, yy, x0, y0: super_gaussian(xx, yy, 5e-20, x0, y0, 1.5, P=1.5)
xx, yy = np.meshgrid(np.linspace(0, 47, 48, dtype=np.float32), np.linspace(0, 47, 48, np.float32))
zz = np.zeros_like(xx, dtype=np.float32)
zz += spot(xx, yy, 12, 12)
zz += spot(xx, yy, 12, 36)
zz += spot(xx, yy, 24, 24)
zz += spot(xx, yy, 36, 36)
zz += spot(xx, yy, 36, 12)
zz = np.broadcast_to(zz, (1, 72, 48, 48))

# Modify restart file
if len(sys.argv) != 2:
    raise ValueError("You didn't give the path to the initial C48 restart file")
ds = xr.open_dataset(sys.argv[1])
for face in range(6):
    ds.SPC_Rn222[:,:,face*48:(face+1)*48, :] = zz
    ds.SPC_Rn[:,:,face*48:(face+1)*48, :] = zz

# Zero-out everything else
ds.SPC_Be7[::] = np.zeros_like(ds.SPC_Be7.values)
ds.SPC_PASV[::] = np.zeros_like(ds.SPC_PASV)
ds.SPC_Pb[::] = np.zeros_like(ds.SPC_Pb)
ds.SPC_Pb210[::] = np.zeros_like(ds.SPC_Pb210)
ds.SPC_Pb210Strat[::] = np.zeros_like(ds.SPC_Pb210Strat)
ds.SPC_Be7Strat[::] = np.zeros_like(ds.SPC_Be7Strat)
ds.SPC_Be10[::] = np.zeros_like(ds.SPC_Be10)
ds.SPC_Be10Strat[::] = np.zeros_like(ds.SPC_Be10Strat)
ds.SPC_Passive[::] = np.zeros_like(ds.SPC_Passive)
ds.SPC_PassiveTracer[::] = np.zeros_like(ds.SPC_PassiveTracer)

# Write
ds.to_netcdf('advection_diagnostic_GEOSChem_rst.c48_TransportTracers.nc',  format='NETCDF4_CLASSIC')


