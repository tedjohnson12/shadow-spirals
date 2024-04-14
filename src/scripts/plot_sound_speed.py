"""
Plots to show the sound speed as a function of phi.

"""

import numpy as np
import matplotlib.pyplot as plt

import paths
import colors

OUTFILE = paths.figures / "sound_speed.pdf"

H = 0.9
N_PHI = 1000
plt.style.use('bmh')

def get_sound_speed(_phi:np.ndarray,h:float,a:float,b:float)->np.ndarray:
    """
    Get the sound speed as a function of phi.
    
    Parameters
    ----------
    phi : np.ndarray
        The azimuthal angle.
    h : float
        The sound speed reduction factor.
    a : float
        The half-width of the shadowed region.
    b : float
        The half-width of the unshadowed region.
    
    Returns
    -------
    cs : np.ndarray
        The sound speed.
    """
    shadow_region = np.abs(np.sin(_phi)) <= np.sin(a)
    unshadow_region = np.abs(np.cos(_phi)) <= np.sin(b)
    transition_region = ~(shadow_region | unshadow_region)
    cs = np.ones_like(_phi) * -1
    cs = np.where(shadow_region, h, cs)
    cs = np.where(unshadow_region, 1.0, cs)
    m = np.zeros_like(_phi)
    m = np.where(_phi>0.5*np.pi, -1.0, m)
    m = np.where(_phi<-0.5*np.pi, 1.0, m)
    l = np.pi - 2*b - 2*a
    cs = np.where(
        transition_region,
        h + 0.5*(1-h) * (1 - np.cos(2*np.pi/l * (np.abs(_phi + m*np.pi) - a))),
        cs
    )
    assert np.all(cs >= 0), 'Some sounds speed values are still negative!'
    return cs
if __name__ in '__main__':
    phi = np.linspace(-np.pi, np.pi, N_PHI)
    wide_shadow = 0.0
    wide_unshadow = 0.0
    narrow_shadow = 0.15
    narrow_unshadow = 1.32

    fig, ax = plt.subplots(1,1,figsize=(3.5,3.5))
    ax:plt.Axes

    # wide shadow
    cs_wide = get_sound_speed(phi,H, wide_shadow, wide_unshadow)
    ax.plot(phi, cs_wide, label='wide shadow', color=colors.teal)

    #narrow shadow
    cs_narrow = get_sound_speed(phi,H, narrow_shadow, narrow_unshadow)
    ax.plot(phi, cs_narrow, label='narrow shadow', color=colors.dark_orange)

    # ax.set_xlim(-np.pi, np.pi)
    ax.set_ylim(0.81, 1.09)
    x_ticks = np.linspace(-np.pi, np.pi, 5)
    ax.set_xticks(x_ticks)
    ax.set_xticklabels([r"$-\pi$", r"$-\frac{\pi}{2}$", r"$0$", r"$\frac{\pi}{2}$", r"$\pi$"])
    ax.set_xlabel(r"$\phi$", fontsize=14)
    ax.set_ylabel(r"$c_s$", fontsize=14,rotation=0,ha='right')
    ax.legend(fontsize=14)
    fig.subplots_adjust(left=0.2,bottom=0.15)

    fig.savefig(OUTFILE)