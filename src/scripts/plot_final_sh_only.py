"""
plot the initial pressure.
"""

import numpy as np
import matplotlib.pyplot as plt

import paths
import read


OUTFILE = paths.figures / "rings_sh.png"


INDEX = 400
VAR_NAME = 'rho'
FIG_WIDTH = 4
FIG_HEIGHT = 4*2
INNER_RAD = 0.05

NAMES = ['narrow_without', 'wide_without']
SHADOWS = ['narrow','wide']
TITLES = ['No Shadow', 'Narrow', 'Wide']
CMAP = 'BrBG'

fig:plt.Figure = plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))
gs = fig.add_gridspec(21,1)
ax_narrow = fig.add_subplot(gs[:8, 0], projection='polar')
ax_wide = fig.add_subplot(gs[10:18, 0], projection='polar')

axes = [ax_narrow, ax_wide]

ax_cbar = fig.add_subplot(gs[20, 0])

densities = np.array([(read.get_data(INDEX, shadow=_shadow, planet=False, var_name=VAR_NAME)) for _shadow in SHADOWS])
initial_density = read.get_data(0, 'none', True, VAR_NAME)
densities_anomaly = (densities - initial_density) / initial_density * 100
vmin = np.min(densities_anomaly)
vmax = np.max(densities_anomaly)
max_v = max(np.abs(vmax),np.abs(vmin))
vmin = -max_v
vmax = max_v
r, phi = read.get_coords(INDEX, 'none', False)

for _ax, _shadow in zip(axes, SHADOWS):
    def r_transform(x):
        return x - np.log10(r[0]) + INNER_RAD
    log_r = r_transform(np.log10(r))
    density = read.get_data(INDEX, _shadow, False, VAR_NAME)
    density_anomaly = (density - initial_density) / initial_density * 100
    y_ticks = np.array([0.5,1,2,])
    _ax.set_yticks(r_transform(np.log10(y_ticks)))
    _ax.set_yticklabels(y_ticks,)
    x_ticks = np.linspace(0, 2*np.pi, 4, endpoint=False)
    _ax.set_xticks(x_ticks)
    _ax.set_xticklabels([r"$0$", r"$\frac{\pi}{2}$", r"$\pi$", r"$\frac{3\pi}{2}$"],fontdict={'size':14})
    _ax.tick_params(axis='x',pad=-0)
    im = _ax.pcolormesh(
        phi,log_r,density_anomaly.T,
        cmap=CMAP,vmax=vmax,vmin=vmin
    )
fig.colorbar(im, cax=ax_cbar, label='$\\Delta \\rho$ (%)',shrink=0.6,orientation='horizontal')
# fig.text(0.81,0.81,'With Planet',fontdict={'size':14})
# fig.text(0.81,0.41,'Without',fontdict={'size':14})
# fig.text(0.01,0.81,'No Shadow',fontdict={'size':14})
# fig.text(0.31,0.81,'Narrow',fontdict={'size':14})
# fig.text(0.58,0.81,'Wide',fontdict={'size':14})


fig.savefig(OUTFILE)

    