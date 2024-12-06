"""
Module io_global


Defined at io_global.fpp lines 13-46

"""
from __future__ import print_function, absolute_import, division
import libqepy_modules
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def get_stdin():
    """
    Element stdin ftype=integer pytype=int
    
    
    Defined at io_global.fpp line 25
    
    """
    return libqepy_modules.f90wrap_io_global__get__stdin()

stdin = get_stdin()

def get_qestdin():
    """
    Element qestdin ftype=integer  pytype=int
    
    
    Defined at io_global.fpp line 27
    
    """
    return libqepy_modules.f90wrap_io_global__get__qestdin()

def set_qestdin(qestdin):
    libqepy_modules.f90wrap_io_global__set__qestdin(qestdin)

def get_stdout():
    """
    Element stdout ftype=integer  pytype=int
    
    
    Defined at io_global.fpp line 29
    
    """
    return libqepy_modules.f90wrap_io_global__get__stdout()

def set_stdout(stdout):
    libqepy_modules.f90wrap_io_global__set__stdout(stdout)

def get_ionode_id():
    """
    Element ionode_id ftype=integer  pytype=int
    
    
    Defined at io_global.fpp line 35
    
    """
    return libqepy_modules.f90wrap_io_global__get__ionode_id()

def set_ionode_id(ionode_id):
    libqepy_modules.f90wrap_io_global__set__ionode_id(ionode_id)

def get_ionode():
    """
    Element ionode ftype=logical pytype=bool
    
    
    Defined at io_global.fpp line 37
    
    """
    return libqepy_modules.f90wrap_io_global__get__ionode()

def set_ionode(ionode):
    libqepy_modules.f90wrap_io_global__set__ionode(ionode)

def get_meta_ionode_id():
    """
    Element meta_ionode_id ftype=integer  pytype=int
    
    
    Defined at io_global.fpp line 43
    
    """
    return libqepy_modules.f90wrap_io_global__get__meta_ionode_id()

def set_meta_ionode_id(meta_ionode_id):
    libqepy_modules.f90wrap_io_global__set__meta_ionode_id(meta_ionode_id)

def get_meta_ionode():
    """
    Element meta_ionode ftype=logical pytype=bool
    
    
    Defined at io_global.fpp line 45
    
    """
    return libqepy_modules.f90wrap_io_global__get__meta_ionode()

def set_meta_ionode(meta_ionode):
    libqepy_modules.f90wrap_io_global__set__meta_ionode(meta_ionode)


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "io_global".')

for func in _dt_array_initialisers:
    func()
