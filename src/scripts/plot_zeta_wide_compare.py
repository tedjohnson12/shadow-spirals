"""
Angle
"""

import numpy as np
import matplotlib.pyplot as plt

import paths
import colors
import read
import spirals
from plot_sound_speed import get_sound_speed

OUTFILE = paths.figures / "zeta_wide_compare.png"
SHADOW = 'wide'
plt.style.use('bmh')

INDEX = 4 * 99 + 1
PHI_PLANET = spirals.phi_planet(INDEX)
WIDTH = 0.1
NDIFF = 2

r,phi = read.get_coords(INDEX, SHADOW, True)
r_mid = r[:-1] + np.diff(r)/2
logr = np.log10(r)
lnr_mid = np.log(r_mid)

initial_density = read.get_data(0, 'none', True, 'rho').T
planet_only_density = read.get_data(INDEX, 'none', True, 'rho').T
shadow_only_density = read.get_data(INDEX, SHADOW, False, 'rho').T
both_density = read.get_data(INDEX, SHADOW, True, 'rho').T
residual_anomaly = (both_density - shadow_only_density) / initial_density * 100
planet_only_anomaly = (planet_only_density - initial_density) / initial_density * 100

phi_peak = spirals.find_peaks(r,phi,residual_anomaly, PHI_PLANET, WIDTH)
_logr_mid, _phi_peak = spirals.reconstruct(lnr_mid,phi_peak)
sh_logr, sh_dphidr = spirals.central_difference(_logr_mid,_phi_peak,NDIFF)
sh_zeta = np.arctan(np.abs(1/sh_dphidr))

phi_peak = spirals.find_peaks(r,phi,planet_only_anomaly, PHI_PLANET, WIDTH)
_logr_mid, _phi_peak = spirals.reconstruct(lnr_mid,phi_peak)
pl_logr, pl_dphidr = spirals.central_difference(_logr_mid,_phi_peak,NDIFF)
pl_zeta = np.arctan(np.abs(1/pl_dphidr))

fig = plt.figure(figsize=(4,4))
ax = fig.add_subplot()

tan_zeta_analytic = np.tan(spirals.zeta_analytic(np.exp(pl_logr)))
tan_zeta_both = np.tan(sh_zeta)
cs_frac = tan_zeta_both / tan_zeta_analytic

reg = pl_logr > 0.3
cs = get_sound_speed(_phi_peak,0.9,0,0)
ax.plot(pl_logr[reg],cs_frac[reg],c=colors.light_orange,ls='--',label='zeta ratio')
reg=_logr_mid > 0.3
ax.plot(_logr_mid[reg],cs[reg],c=colors.dark_orange,ls='--',label='sound speed')
ax.set_xlabel('$\\ln(r)$',fontdict={'size':14})
ax.set_ylabel(r'$c_{\rm s}/c_{\rm s, 0}$',fontdict={'size':14})
ax.legend(fontsize=14,loc=(0.3,0.6))

# inax = ax.inset_axes([0.45,0.35,0.5,0.2],xlim=(0.4,0.9),ylim=(0.03,0.25))
# inax.scatter(sh_logr,sh_zeta,s=3,c=colors.teal,marker='o',label='Shadow')
# inax.scatter(pl_logr,pl_zeta,s=3,c=colors.dark_orange,marker='o',label='No shadow')
# inax.plot(pl_logr,spirals.zeta_analytic(np.exp(pl_logr)),c=colors.yellow,ls='--',label='Analytic')
# inax.set_xticks([])
# inax.set_yticks([])
# ax.indicate_inset_zoom(inax)

fig.subplots_adjust(left=0.2,bottom=0.15)

fig.savefig(OUTFILE)

