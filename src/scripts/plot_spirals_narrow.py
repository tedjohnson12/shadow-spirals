"""
Plot some spiral figures
"""

import numpy as np
import matplotlib.pyplot as plt

import paths
import read
import spirals

OUTFILE = paths.figures / "spirals_narrow.pdf"
SHADOW = 'narrow'
plt.style.use('bmh')

INDEX = 4 * 99 + 1
PHI_PLANET = spirals.phi_planet(INDEX)
WIDTH = 0.1
SCALE = 0.1

fig, axes = plt.subplots(1,5,figsize=(8,4),width_ratios=[1,1,1,1,0.1])

ax_shadow_only:plt.Axes = axes[0]
ax_both:plt.Axes = axes[1]
ax_residual:plt.Axes = axes[2]
ax_planet_only:plt.Axes = axes[3]
ax_cbar:plt.Axes = axes[4]

axes = [ax_shadow_only,ax_both,ax_residual,ax_planet_only]
TITLES = ['Shadow Only', 'Shadow + Planet', 'Residual', 'Planet Only']

fig.subplots_adjust(wspace=0.0,hspace=0.0,bottom=0.2)

r,phi = read.get_coords(INDEX, SHADOW, True)
r_mid = r[:-1] + np.diff(r)/2
logr = np.log10(r)
logr_mid = np.log10(r_mid)

# densities
initial_density = read.get_data(0, 'none', True, 'rho').T
planet_only_density = read.get_data(INDEX, 'none', True, 'rho').T
shadow_only_density = read.get_data(INDEX, SHADOW, False, 'rho').T
both_density = read.get_data(INDEX, SHADOW, True, 'rho').T

planet_only_anomaly = (planet_only_density - initial_density) / initial_density * 100
shadow_only_anomaly = (shadow_only_density - initial_density) / initial_density * 100
both_anomaly = (both_density - initial_density) / initial_density * 100
residual_anomaly = (both_density - shadow_only_density) / initial_density * 100

vmax = max(np.percentile(planet_only_anomaly,99),np.percentile(residual_anomaly,99))
vmin = max(np.percentile(planet_only_anomaly,1),np.percentile(residual_anomaly,1))
max_vmax = max(abs(vmax),abs(vmin))
vmax = max_vmax
vmin = -max_vmax

sh_vmax = max(np.max(shadow_only_anomaly),np.max(both_anomaly))
sh_vmin = min(np.min(shadow_only_anomaly),np.min(both_anomaly))
max_sh_vmax = max(abs(sh_vmax),abs(sh_vmin))
scale = max_vmax / max_sh_vmax

data = [shadow_only_anomaly, both_anomaly,residual_anomaly, planet_only_anomaly]
scatter = [False, False, True, True]
scale_list = [scale, scale, 1, 1]

for _ax, _title, _data, _scatter, _scale in zip(axes, TITLES, data, scatter, scale_list):
    _ax:plt.Axes
    _ax.set_title(_title,fontdict={'size':12})
    _ax.set_xticks([-np.pi,-np.pi/2,0,np.pi/2])
    _ax.set_xticklabels([r"$-\pi$", r"$-\frac{\pi}{2}$", r"$0$", r"$\frac{\pi}{2}$"],fontdict={'size':14})
    if _ax is not ax_shadow_only:
        _ax.set_yticklabels([])
    im = _ax.pcolormesh(phi,logr*np.log(10),_scale*_data,cmap='BrBG',vmin=vmin,vmax=vmax)
    phi_peak = spirals.find_peaks(r,phi,_data, PHI_PLANET, WIDTH)
    if _scatter:
        _ax.scatter(phi_peak,logr_mid*np.log(10),s=3,c='k',marker='.')
ax_shadow_only.text(-0.8*np.pi,0.52,f'Scaled by {scale:.1f}',fontdict={'size':12})
ax_shadow_only.set_ylabel('$\\ln (r)$',fontdict={'size':14})
fig.text(0.5,0.07,'$\\phi$',fontdict={'size':14})
fig.text(0.14,0.06,f'$t = {0.25 * INDEX:.2f}~P_{{orb}}$',fontdict={'size':14})
fig.text(0.79,0.06,'Narrow',fontdict={'size':14})
fig.colorbar(im, cax=ax_cbar, label='$\\Delta \\rho$ (%)',shrink=0.6)
fig.savefig(OUTFILE)


