import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches

import paths
import read
import colors


OUTFILE = paths.figures / "slice.pdf"


INDEX = 200
VAR_NAME = 'rho'
FIG_WIDTH = 4
FIG_HEIGHT = 4
INNER_RAD = 0.05

NAMES = ['narrow_without', 'wide_without']
SHADOWS = ['narrow','wide']
TITLES = ['Narrow', 'Wide']
CMAP = 'BrBG'
I_PHI = 256

r, phi = read.get_coords(INDEX, 'none', True)

fig = plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))

ax = fig.add_subplot(111)

for i in np.arange(100, 400, 1):
    rho_initial = read.get_data(0, 'none', True, 'rho')
    rho_narrow = read.get_data(i, 'narrow', False, 'rho')
    rho_wide = read.get_data(i, 'wide', False, 'rho')

    anomaly_narrow = (rho_narrow - rho_initial) / rho_initial * 100
    anomaly_wide = (rho_wide - rho_initial) / rho_initial * 100

    r_mid = r[:-1] + np.diff(r)/2
    ln_r = np.log(r_mid)

    ax.plot(ln_r,anomaly_narrow[I_PHI,:],lw=1,c=colors.slate,alpha=0.05)
    ax.plot(ln_r,anomaly_wide[I_PHI,:],lw=1,c=colors.teal,alpha=0.05)
ax.text(0.4,4,f'$\\phi = {phi[I_PHI]:.2f}$',fontdict={'size':14})
ax.set_xlabel('$\\ln(r)$',fontdict={'size':14})
ax.set_ylabel('$\\Delta \\rho$ (%)',fontdict={'size':14})
ax.add_patch(patches.Rectangle((0,0),np.nan,np.nan,color=colors.slate,label='Narrow'))
ax.add_patch(patches.Rectangle((0,0),np.nan,np.nan,color=colors.teal,label='Wide'))
ax.legend(fontsize=14)
fig.subplots_adjust(left=0.2,bottom=0.15)


fig.savefig(OUTFILE)
