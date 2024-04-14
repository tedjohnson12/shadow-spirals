"""
Functions to find spirals
"""
from typing import Tuple
import numpy as np
from scipy.integrate import simpson
from scipy.optimize import newton

from plot_sound_speed import get_sound_speed

SOUND_SPEED = 0.1

def find_peak(
    phi:np.ndarray,
    rho:np.ndarray,
    phi_previous:float,
    phi_previous_previous:float,
    width:float
) -> float:
    """
    Find the peak of the spiral at a single value of r
    """
    guess = phi_previous + phi_previous - phi_previous_previous
    domain = np.abs(np.cos(phi) - np.cos(guess)) < width
    domain = domain[1:] | domain[:-1]
    i = np.nanargmax(np.where(domain, rho, np.nan))
    return 0.5*(phi[i] + phi[i+1])
    

def phi_planet(index:int):
    """
    The azimuthal angle of the planet.
    """ 
    return 0.5 * np.pi * (index % 4 - 1)

def find_peaks(
    r:np.ndarray,
    phi:np.ndarray,
    rho:np.ndarray,
    phi_initial:float,
    width:float
) -> np.ndarray:
    """
    Find the peaks of the spirals.
    
    Parameters
    ----------
    r : np.ndarray
        The radial coordinates
    phi : np.ndarray
        The azimuthal coordinates
    rho : np.ndarray
        The density
    phi_planet : float
        The azimuthal angle of the planet
    width : float
        The width to search for the spiral in.
    
    Returns
    -------
    phi_peaks : np.ndarray
        The azimuthal angles of the spiral peaks
    """
    # find i_r for the planet
    i_r = np.argmin(np.abs(r-1))
    # get a starting point
    phi_at_planet = find_peak(phi,rho[i_r,:],phi_initial,phi_initial,width)
    
    # go out from the planet
    indices = np.arange(i_r+1,len(r)-1,dtype=int)
    phi_out = []
    phi_last = phi_at_planet
    phi_last_last = phi_at_planet
    for i in indices:
        _phi = find_peak(phi,rho[i,:],phi_last,phi_last_last,width)
        phi_out.append(_phi)
        phi_last_last = phi_last
        phi_last = _phi
    
    # go in from the planet
    indices = np.flip(np.arange(0,i_r,dtype=int))
    phi_in = []
    phi_last = phi_at_planet
    phi_last_last = phi_at_planet
    for i in indices:
        _phi = find_peak(phi,rho[i,:],phi_last,phi_last_last,width)
        phi_in.append(_phi)
        phi_last_last = phi_last
        phi_last = _phi
    
    # put together
    phi_peaks = np.concatenate([
        phi_in[::-1],[phi_at_planet],phi_out
    ])
    return phi_peaks

def central_difference(x,y,n:int)->Tuple[np.ndarray,np.ndarray]:
    """
    Take the derivative using central differences
    """
    dy = y[2*n:] - y[:-2*n]
    dx = x[2*n:] - x[:-2*n]
    _x = x[n:-n]
    _y = dy/dx
    assert len(_x) == len(_y), f'{len(_x)} != {len(_y)}'
    return x[n:-n], dy/dx

def zeta_analytic(_r):
    return np.arctan(1/np.abs((1 - _r**(-3/2))*_r/SOUND_SPEED))

def reconstruct(r,phi):
    """
    make things continuous
    """
    dphi = np.diff(phi)
    i_before_break = np.argwhere(dphi > np.pi)
    if len(i_before_break) == 0:
        return r, phi
    elif len(i_before_break) == 1:
        i = i_before_break[0]
        index = np.arange(len(r))
        is_before = index <=i
        _phi = np.where(is_before,phi+2*np.pi,phi)
        return r, _phi
    elif len(i_before_break) == 2:
        i,j = i_before_break
        index = np.arange(len(r))
        is_before = index <=i
        is_after = index > j
        _phi = np.where(is_before,phi+2*np.pi,phi)
        _phi = np.where(is_after,_phi - 2*np.pi,_phi)
        return r, _phi
    else:
        index = np.arange(len(r))
        _phi = phi
        for i in i_before_break:
            is_after = index > i
            _phi = np.where(is_after,_phi - 2*np.pi,_phi)
        return r, _phi
    
def eval_lhs(_phi_planet,phi_end, h, a, b, dphi= 2*np.pi / 10000):
    """
    Evaluate the LHS of the cot zeta equality
    """
    n = int(np.abs(phi_end - _phi_planet)/ dphi)
    _phi = np.linspace(_phi_planet, phi_end, n)
    __phi = _phi % np.pi
    assert np.all(__phi <= np.pi)
    assert np.all(__phi >= -np.pi)
    cs = SOUND_SPEED*get_sound_speed(__phi, h, a, b)
    try:
        return simpson(cs,_phi)
    except ValueError:
        return 0

def eval_rhs(r):
    """
    Evaluate the RHS of the cot zeta equality
    """
    return np.abs(r + 2/np.sqrt(r) - 3)

def get_best_phi(r,_phi_planet, h, a, b,guess = 1):
    def fun(phi):
        return eval_lhs(_phi_planet,phi, h, a, b) - eval_rhs(r)
    k = 1 if r < 1 else -1
    try:
        return newton(fun, guess) * k
    except RuntimeError:
        return np.nan

def phi_peak_analytic_shadow(r:np.ndarray,_phi_planet:float,h:float,a:float,b:float)->np.ndarray:
    return np.array([get_best_phi(_r,_phi_planet,h,a,b) for _r in r])
    
def zeta_analytic_shadow(r:np.ndarray,_phi_planet:float,h:float,a:float,b:float,ndiff:int)->Tuple[np.ndarray,np.ndarray]:
    _phi = phi_peak_analytic_shadow(r,_phi_planet,h,a,b)
    logr, dphidr = central_difference(np.log(r),_phi,ndiff)
    zeta = np.arctan(np.abs(1/dphidr))
    return logr, zeta