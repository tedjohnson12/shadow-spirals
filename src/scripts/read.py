"""
Read from the data archive
"""

import h5py
from typing import Tuple
import tarfile
from pathlib import Path
from contextlib import contextmanager
import numpy as np

import paths

DATA_PATH = paths.data
IMIN = 0
IMAX = 400

def get_case_name(shadow:str, planet:bool)->str:
    """
    Get the string used to identify the case
    
    Parameters
    ----------
    shadow : str
        'none', 'narrow', or 'wide'
    planet : bool
        True if the planet is present
        
    Returns
    -------
    str
        The name of this simulation
    """
    if shadow == 'none':
        return 'no_shadow'
    elif shadow == 'narrow':
        if planet:
            return 'narrow_with'
        else:
            return 'narrow_without'
    elif shadow == 'wide':
        if planet:
            return 'wide_with'
        else:
            return 'wide_without'
    else:
        raise ValueError(f"Unknown shadow: {shadow}")

def get_case_tar_path(shadow:str, planet:bool)->Path:
    """
    Get the path to the tar file for this case
    
    Parameters
    ----------
    shadow : str
        'none', 'narrow', or 'wide'
    planet : bool
        True if the planet is present
        
    Returns
    -------
    Path
        The path to the tar file
    """
    name = get_case_name(shadow, planet)
    return DATA_PATH / f'{name}.tar.gz'

def get_case_path(shadow:str, planet:bool)->Path:
    """
    Get the base path for the files
    
    Parameters
    ----------
    shadow : str
        'none', 'narrow', or 'wide'
    planet : bool
        True if the planet is present
        
    Returns
    -------
    Path
        The path the files
    """
    name = get_case_name(shadow, planet)
    return DATA_PATH / f'{name}'

def get_filename(index:int,shadow:str, planet:bool)->str:
    """
    get the filename
    """
    name = get_case_name(shadow, planet)
    return f'{name}.out1.{index:05d}.athdf'

def get_path(index:int,shadow:str, planet:bool)->Path:
    """
    get the path
    """
    return get_case_path(shadow, planet) / get_filename(index, shadow, planet)

def untar(shadow:str, planet:bool):
    """
    Untar the data
    """
    tar_path = get_case_tar_path(shadow, planet)
    with tarfile.open(tar_path,mode='r:gz') as tar:
        tar.extractall(get_case_path(shadow, planet),filter='data')

@contextmanager
def read(index:int,shadow:str, planet:bool):
    """
    Read the data
    """
    if index < IMIN or index > IMAX:
        raise ValueError(f'Index out of range: {index}')
    path = get_path(index,shadow, planet)
    if not path.exists():
        print(f'Missing {path}, untaring...')
        untar(shadow, planet)
    f = h5py.File(path, 'r')
    try:
        yield f
    finally:
        f.close()

def get_coords(index:int,shadow:str, planet:bool)->Tuple[np.ndarray, np.ndarray]:
    """
    Get the coordinates
    
    Parameters
    ----------
    index : int
        The index
    shadow : str
        'none', 'narrow', or 'wide'
    planet : bool
        True if the planet is present
    
    Returns
    -------
    r : np.ndarray
        The radial coordinates
    phi : np.ndarray
        The azimuthal coordinates
    """
    with read(index, shadow, planet) as f:
        r = f['x1f'][0]
        phi = f['x2f'][0]
        return r,phi

def _get_dat(index:int,shadow:str, planet:bool,var_index:int)->np.ndarray:
    """
    Generic getter for the data
    """
    with read(index, shadow, planet) as f:
        return f['prim'][var_index,0,0,:,:]

def get_data(index:int,shadow:str, planet:bool, var_name:str)->np.ndarray:
    """
    Get a 2D dataset from the Athena++ output.
    
    Parameters
    ----------
    index : int
        The index of the snapshot to read
    shadow : str
        'none', 'narrow', or 'wide'
    planet : bool
        True if the planet is present
    var_name : str
        The name of the variable to read
    
    Returns
    -------
    np.ndarray
        The data (nrad, nphi)
    """
    mapper = {
        'rho': 0,
        'press': 1,
        'velr': 2,
        'velphi': 3,
        'velz': 4
    }
    if var_name == 'temp':
        return _get_dat(index,shadow,planet,mapper['press']) /_get_dat(index,shadow,planet,mapper['rho'])
    return _get_dat(index,shadow,planet,mapper[var_name])