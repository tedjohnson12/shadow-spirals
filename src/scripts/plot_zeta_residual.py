import numpy as np
import matplotlib.pyplot as plt

import paths
import colors
import read
import spirals

OUTFILE = paths.figures / "zeta_residual.png"
plt.style.use('bmh')

INDEX = 4 * 99 + 1
PHI_PLANET = spirals.phi_planet(INDEX)
WIDTH = 0.1
NDIFF = 2

r,phi = read.get_coords(INDEX, 'none', True)
r_mid = r[:-1] + np.diff(r)/2
logr = np.log10(r)
lnr_mid = np.log(r_mid)

shadow = 'wide'
initial_density = read.get_data(0, 'none', True, 'rho').T
planet_only_density = read.get_data(INDEX, 'none', True, 'rho').T
shadow_only_density = read.get_data(INDEX, shadow, False, 'rho').T
both_density = read.get_data(INDEX, shadow, True, 'rho').T
residual_anomaly = (both_density - shadow_only_density) / initial_density * 100

phi_peak = spirals.find_peaks(r,phi,residual_anomaly, PHI_PLANET, WIDTH)
_logr_mid, _phi_peak = spirals.reconstruct(lnr_mid,phi_peak)
wide_logr, wide_dphidr = spirals.central_difference(_logr_mid,_phi_peak,NDIFF)
wide_zeta = np.arctan(np.abs(1/wide_dphidr))
wide_residual = (wide_zeta - spirals.zeta_analytic(np.exp(wide_logr)))/spirals.zeta_analytic(np.exp(wide_logr))

shadow = 'narrow'
initial_density = read.get_data(0, 'none', True, 'rho').T
planet_only_density = read.get_data(INDEX, 'none', True, 'rho').T
shadow_only_density = read.get_data(INDEX, shadow, False, 'rho').T
both_density = read.get_data(INDEX, shadow, True, 'rho').T
residual_anomaly = (both_density - shadow_only_density) / initial_density * 100

phi_peak = spirals.find_peaks(r,phi,residual_anomaly, PHI_PLANET, WIDTH)
_logr_mid, _phi_peak = spirals.reconstruct(lnr_mid,phi_peak)
narrow_logr, narrow_dphidr = spirals.central_difference(_logr_mid,_phi_peak,NDIFF)
narrow_zeta = np.arctan(np.abs(1/narrow_dphidr))
narrow_residual = (narrow_zeta - spirals.zeta_analytic(np.exp(narrow_logr)))/spirals.zeta_analytic(np.exp(narrow_logr))


fig,ax = plt.subplots(1,1,figsize=(8,3))
ax:plt.Axes
reg = np.abs(wide_logr) > 0.3
ax.plot(wide_logr[reg], wide_residual[reg], label='Wide', color=colors.teal)
reg = np.abs(narrow_logr) > 0.3
ax.plot(narrow_logr[reg], narrow_residual[reg], label='Narrow', color=colors.slate)
# ax.set_ylim(-0.03,0.03)
ax.set_xlabel('$\\ln(r)$',fontdict={'size':14})
ax.set_ylabel('$\\zeta - \\zeta_{\\rm analytic}$',fontdict={'size':14})

fig.savefig(OUTFILE)


