"""
plot the initial pressure.
"""

import numpy as np
import matplotlib.pyplot as plt

import paths
import read


OUTFILE = paths.figures / "final_density.pdf"


INDEX = 400
VAR_NAME = 'rho'
FIG_WIDTH = 8
FIG_HEIGHT = 8/3.0 * 2
INNER_RAD = 0.05

NAMES = ['none', 'narrow_with', 'narrow_without', 'wide_with', 'wide_without']
SHADOWS = ['none','narrow','narrow','wide','wide']
PLANETS = [True, True, False, True, False]
TITLES = ['No Shadow', 'Narrow', 'Wide']
CMAP = 'BrBG'

fig:plt.Figure = plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))
gs = fig.add_gridspec(2,31)
ax_none = fig.add_subplot(gs[0, :8], projection='polar')
ax_narrow_with = fig.add_subplot(gs[0, 10:18], projection='polar')
ax_wide_with = fig.add_subplot(gs[0, 20:28], projection='polar')
ax_narrow_without = fig.add_subplot(gs[1, 10:18], projection='polar')
ax_wide_without = fig.add_subplot(gs[1, 20:28], projection='polar')
axes = [ax_none,ax_narrow_with,ax_narrow_without,ax_wide_with,ax_wide_without]

ax_cbar = fig.add_subplot(gs[1, 0])

densities = np.array([(read.get_data(INDEX, shadow=_shadow, planet=_planet, var_name=VAR_NAME)) for _shadow,_planet in zip(SHADOWS,PLANETS)])
initial_density = read.get_data(0, 'none', True, VAR_NAME)
densities_anomaly = (densities - initial_density) / initial_density * 100
vmin = np.min(densities_anomaly)
vmax = np.max(densities_anomaly)
max_v = max(np.abs(vmax),np.abs(vmin))
vmin = -max_v
vmax = max_v
r, phi = read.get_coords(INDEX, 'none', False)

for _ax, _shadow, _planet in zip(axes, SHADOWS, PLANETS):
    def r_transform(x):
        return x - np.log10(r[0]) + INNER_RAD
    log_r = r_transform(np.log10(r))
    density = read.get_data(INDEX, _shadow, _planet, VAR_NAME)
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
fig.colorbar(im, cax=ax_cbar, label='$\\Delta \\rho$ (%)',shrink=0.6)
fig.text(0.81,0.81,'With Planet',fontdict={'size':14})
fig.text(0.81,0.41,'Without',fontdict={'size':14})
fig.text(0.01,0.81,'No Shadow',fontdict={'size':14})
fig.text(0.31,0.81,'Narrow',fontdict={'size':14})
fig.text(0.58,0.81,'Wide',fontdict={'size':14})


fig.savefig(OUTFILE)

    