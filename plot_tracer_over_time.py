import numpy as np
import xarray as xr

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import cartopy.crs as ccrs

import sg.figure_axes
import sg.grids
import sg.plot

from contextlib import contextmanager
import sys, os

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout

# Make figure
plt.rcParams.update({'font.size': 16, 'font.weight': 'bold'})
plt.figure(figsize=(6, 9))


projection = ccrs.PlateCarree()


gs1 = gridspec.GridSpec(3, 1)
gs1.update(wspace=0, hspace=0, left=0.01, right=0.99, top=0.99, bottom=0.01)

STRETCH_FACTOR = 1.0001
TARGET_LAT = 0.0
TARGET_LON = 350.0
grid = sg.grids.StretchedGrid(48, STRETCH_FACTOR, TARGET_LAT, TARGET_LON)
with suppress_stdout():
    # Load data
    da = xr.combine_nested([xr.open_dataset(path)['SpeciesConc_Rn222'] for path in [
        f'OutputDir/GCHP.SpeciesConc.20160101_0030z.nc4',
        f'OutputDir/GCHP.SpeciesConc.20160101_1230z.nc4',
        f'OutputDir/GCHP.SpeciesConc.20160102_0030z.nc4',
    ]], concat_dim='time')
    ds_wind = [xr.open_dataset(path) for path in [
        f'OutputDir/GCHP.StateMet_avg.20160101_0030z.nc4',
        f'OutputDir/GCHP.StateMet_avg.20160101_1230z.nc4',
        f'OutputDir/GCHP.StateMet_avg.20160102_0030z.nc4',
    ]]
    u_wind = xr.combine_nested([ds['Met_U'] for ds in ds_wind], concat_dim='time')
    v_wind = xr.combine_nested([ds['Met_V'] for ds in ds_wind], concat_dim='time')
for time in range(3):
    ax = plt.subplot(gs1[time],  projection=projection)
    ax.set_global()
    ax.coastlines(linewidth=0.7)
    figax = sg.figure_axes.FigureAxes(ax, projection)

    text_colors = iter(['tab:blue', 'tab:green', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:cyan'])
    for face in range(6):
        xe, ye = figax.transform_xy(grid.xe(face), grid.ye(face))
        xc, yc = figax.transform_xy(grid.xc(face), grid.yc(face))
        sg.plot.draw_major_grid_boxes(figax, xe, ye, linewidth=0.4)
        data = da.isel(time=time, nf=face, lev=18).squeeze()
        sg.plot.plot_pcolomesh(figax, xe, ye, data, vmin=0, vmax=3e-20, cmap=plt.cm.Reds)
        u = u_wind.isel(time=time, nf=face, lev=18).squeeze()
        v = v_wind.isel(time=time, nf=face, lev=18).squeeze()
        plt.quiver(xc[::2,::2], yc[::2,::2],
                   -u.values[::2,::2], -v.values[::2,::2], angles='xy', pivot='tip', width=0.0008, scale=1000)
        x_shift = 0
        y_shift = -5
        if np.any(xc < -170) and np.any(xc > 170):
            x_shift=-2

        if np.any(yc > 70):
            plt.text(
                -5, 65, f'{face+1}',
                color=next(text_colors),
                horizontalalignment='center',
                verticalalignment='center',
            )
        elif np.any(yc < -70):
            plt.text(
                -30, -60, f'{face+1}',
                color=next(text_colors),
                horizontalalignment='center',
                verticalalignment='center',
            )
        else:
            sg.plot.draw_face_number(
                figax,
                xc, yc, f'{face+1}',
                x_shift=x_shift,
                y_shift=y_shift,
                color=next(text_colors),
                horizontalalignment='center',
                verticalalignment='center',
            )

plt.savefig('figure.png', dpi=300)
