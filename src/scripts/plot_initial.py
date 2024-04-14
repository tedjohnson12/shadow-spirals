"""
plot the initial pressure.
"""

import numpy as np
import matplotlib.pyplot as plt

import paths
import read


OUTFILE = paths.figures / "initial_temperature.pdf"


INDEX = 0
VAR_NAME = 'temp'
FIG_WIDTH = 8
FIG_HEIGHT = 8/3.0
INNER_RAD = 0.05

NAMES = ['none', 'narrow', 'wide']
TITLES = ['No Shadow', 'Narrow', 'Wide']
CMAP = 'plasma'

fig:plt.Figure = plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))
gs = fig.add_gridspec(1, 31)
ax_none = fig.add_subplot(gs[0, :8], projection='polar')
ax_narrow = fig.add_subplot(gs[0, 10:18], projection='polar')
ax_wide = fig.add_subplot(gs[0, 20:28], projection='polar')
ax_cbar = fig.add_subplot(gs[0, 30])

temperatures = np.vstack([(read.get_data(INDEX, _name, False, VAR_NAME)) for _name in NAMES])
tmax = np.max(temperatures)
temperatures = temperatures / tmax
vmin = np.min(temperatures)
vmax = np.max(temperatures)
r, phi = read.get_coords(INDEX, 'none', False)

for i,(_ax, _name, _title) in enumerate(zip([ax_none, ax_narrow, ax_wide], NAMES, TITLES)):
    def r_transform(x):
        return x - np.log10(r[0]) + INNER_RAD
    log_r = r_transform(np.log10(r))
    temp = read.get_data(INDEX, _name, False, VAR_NAME) / tmax
    y_ticks = np.array([0.5,1,2,])
    _ax.set_yticks(r_transform(np.log10(y_ticks)))
    _ax.set_yticklabels(y_ticks,)
    x_ticks = np.linspace(0, 2*np.pi, 4, endpoint=False)
    _ax.set_xticks(x_ticks)
    _ax.set_xticklabels([r"$0$", r"$\frac{\pi}{2}$", r"$\pi$", r"$\frac{3\pi}{2}$"],fontdict={'size':14})
    _ax.tick_params(axis='x',pad=-0)
    im = _ax.pcolormesh(
        phi,log_r,temp.T,
        cmap=CMAP,vmax=vmax,vmin=vmin
    )
fig.colorbar(im, cax=ax_cbar, label='$T/T_0$',shrink=0.6)

fig.savefig(OUTFILE)

    