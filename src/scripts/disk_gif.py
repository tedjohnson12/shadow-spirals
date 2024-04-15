

import numpy as np
import matplotlib.pyplot as plt
from os import system
from tqdm.auto import tqdm

import paths
import read


OUTPATH = paths.figures / 'gif'

FIG_HEIGHT = 4
FIG_WIDTH = 4
CMAP = 'BrBG'
INNER_RAD = 1
DPI = 200

rho_initial = read.get_data(0, 'none', True, 'rho').T
r, phi = read.get_coords(0, 'none', True)

def r_transform(x):
        return x - np.log(r[0]) + INNER_RAD



def main(index:int, shadow:str, planet:bool,filename:str):
    
    fig = plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))
    gs = fig.add_gridspec(1,11)
    time = index/4.0
    
    main_ax = fig.add_subplot(gs[0, :8], projection='polar')
    cbar_ax = fig.add_subplot(gs[0, 9])
    
    rho = read.get_data(index, shadow, planet, 'rho').T
    anomaly = (rho - rho_initial) / rho_initial * 100
    
    logr = r_transform(np.log(r))
    y_ticks = np.array([0.5,1,2])
    main_ax.set_yticks(r_transform(np.log(y_ticks)))
    main_ax.set_yticklabels(y_ticks,)
    x_ticks = np.linspace(0, 2*np.pi, 4, endpoint=False)
    main_ax.set_xticks(x_ticks)
    main_ax.set_xticklabels([r"$0$", r"$\frac{\pi}{2}$", r"$\pi$", r"$\frac{3\pi}{2}$"],fontdict={'size':14})
    main_ax.tick_params(axis='x',pad=-0)

    
    im = main_ax.pcolormesh(
        phi, logr, anomaly,
        cmap = CMAP
    )
    fig.colorbar(im, cax=cbar_ax, label='$\\Delta \\rho$ (%)',shrink=0.6)
    fig.subplots_adjust(right=0.85)
    fig.text(0.06,0.11,f'$t = {time:.2f}~P_{{orb}}$',fontdict={'size':14})
    
    fig.savefig(filename,dpi=DPI)
    plt.close(fig)

if __name__ in '__main__':
    shadows = ['none','wide']
    # shadows = ['wide']
    indicies = np.arange(0,400,1)
    
    if not OUTPATH.exists():
        OUTPATH.mkdir()
    
    for shadow in shadows:
        system(f'rm {OUTPATH}/{shadow}_*.png')
        for n, index in enumerate(tqdm(indicies, desc=shadow,total=len(indicies))):
            filename = OUTPATH / f'{shadow}_{n:03}.png'
            main(index, shadow, True, filename)
    