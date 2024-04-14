


import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import simpson
from scipy.optimize import newton

import paths
import colors
import read
import spirals
from plot_sound_speed import get_sound_speed
a = 0
b = 0
h = 0.1
cs0 = 0.1

OUTFILE = paths.figures / "spiral_shape_analytic.pdf"
plt.style.use('bmh')
PHI_PLANET = 0

H = [0.01,0.1,0.9,1.0]
LS = ['-', '--', ':']
A = [0,0.15]
B = [0,1.3]
COLOR = [colors.teal, colors.dark_orange]
NAME = ['wide', 'narrow']
NDIFF = 1

r = np.linspace(0.4,2.5,1000)

fig, ax = plt.subplots(1,1,figsize = (4,8))
fig.subplots_adjust(top=0.7,left=0.22)

for h, ls in zip(H,LS):
    for a, b, c,n in zip(A,B,COLOR,NAME):
        phi = spirals.phi_peak_analytic_shadow(r,PHI_PLANET,h,a,b)
        label = f'$h = {h}$, {n}'
        much_less = phi < -3*np.pi
        ax.plot(phi[much_less]+4*np.pi,np.log(r)[much_less],c=c,ls=ls)
        less = (phi < -np.pi) & (~much_less)
        ax.plot(phi[less]+2*np.pi,np.log(r)[less],c=c,ls=ls)
        much_more = phi > 3*np.pi
        ax.plot(phi[much_more]-4*np.pi,np.log(r)[much_more],c=c,ls=ls)
        more = (phi > np.pi) & (~much_more)
        ax.plot(phi[more]-2*np.pi,np.log(r)[more],c=c,ls=ls)
        near_planet = np.abs(phi) < 0.2
        before_planet = (phi < 0) & ~(less|much_less|more|much_more|near_planet)
        after_planet = (phi > 0) & ~(less|much_less|more|much_more|near_planet)
        ax.plot(phi[before_planet],np.log(r)[before_planet],c=c,ls=ls)
        ax.plot(phi[after_planet],np.log(r)[after_planet],c=c,ls=ls,label=label)
for h in [1.0]:
    for a, b in zip([0.0],[0.0]):
        phi = spirals.phi_peak_analytic_shadow(r,PHI_PLANET,h,a,b)
        label = 'No shadow'
        c = 'k'
        ls = '-'
        much_less = phi < -3*np.pi
        ax.plot(phi[much_less]+4*np.pi,np.log(r)[much_less],c=c,ls=ls)
        less = (phi < -np.pi) & (~much_less)
        ax.plot(phi[less]+2*np.pi,np.log(r)[less],c=c,ls=ls)
        much_more = phi > 3*np.pi
        ax.plot(phi[much_more]-4*np.pi,np.log(r)[much_more],c=c,ls=ls)
        more = (phi > np.pi) & (~much_more)
        ax.plot(phi[more]-2*np.pi,np.log(r)[more],c=c,ls=ls)
        near_planet = np.abs(phi) < 0.2
        before_planet = (phi < 0) & ~(less|much_less|more|much_more|near_planet)
        after_planet = (phi > 0) & ~(less|much_less|more|much_more|near_planet)
        ax.plot(phi[before_planet],np.log(r)[before_planet],c=c,ls=ls)
        ax.plot(phi[after_planet],np.log(r)[after_planet],c=c,ls=ls,label=label)


ax.legend(fontsize=14,loc=(0.15,1.05))
ax.set_xticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi])
ax.set_xticklabels(['$-\\pi$', '$-\\frac{\\pi}{2}$', '0', '$\\frac{\\pi}{2}$', '$\\pi$'])
ax.set_ylabel('$\\ln(r)$',fontdict={'size':14})
ax.set_xlabel('$\\phi$',fontdict={'size':14})
        
fig.savefig(OUTFILE)