"""
Module wvfct


Defined at pwcom.fpp lines 279-308

"""
from __future__ import print_function, absolute_import, division
import libqepy_pw
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def get_npwx():
    """
    Element npwx ftype=integer  pytype=int
    
    
    Defined at pwcom.fpp line 287
    
    """
    return libqepy_pw.f90wrap_wvfct__get__npwx()

def set_npwx(npwx):
    libqepy_pw.f90wrap_wvfct__set__npwx(npwx)

def get_nbndx():
    """
    Element nbndx ftype=integer  pytype=int
    
    
    Defined at pwcom.fpp line 289
    
    """
    return libqepy_pw.f90wrap_wvfct__get__nbndx()

def set_nbndx(nbndx):
    libqepy_pw.f90wrap_wvfct__set__nbndx(nbndx)

def get_nbnd():
    """
    Element nbnd ftype=integer  pytype=int
    
    
    Defined at pwcom.fpp line 291
    
    """
    return libqepy_pw.f90wrap_wvfct__get__nbnd()

def set_nbnd(nbnd):
    libqepy_pw.f90wrap_wvfct__set__nbnd(nbnd)

def get_nbnd_cond():
    """
    Element nbnd_cond ftype=integer  pytype=int
    
    
    Defined at pwcom.fpp line 293
    
    """
    return libqepy_pw.f90wrap_wvfct__get__nbnd_cond()

def set_nbnd_cond(nbnd_cond):
    libqepy_pw.f90wrap_wvfct__set__nbnd_cond(nbnd_cond)

def get_npw():
    """
    Element npw ftype=integer  pytype=int
    
    
    Defined at pwcom.fpp line 295
    
    """
    return libqepy_pw.f90wrap_wvfct__get__npw()

def set_npw(npw):
    libqepy_pw.f90wrap_wvfct__set__npw(npw)

def get_current_k():
    """
    Element current_k ftype=integer  pytype=int
    
    
    Defined at pwcom.fpp line 297
    
    """
    return libqepy_pw.f90wrap_wvfct__get__current_k()

def set_current_k(current_k):
    libqepy_pw.f90wrap_wvfct__set__current_k(current_k)

def get_array_et():
    """
    Element et ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 299
    
    """
    global et
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pw.f90wrap_wvfct__array__et(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        et = _arrays[array_handle]
    else:
        et = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pw.f90wrap_wvfct__array__et)
        _arrays[array_handle] = et
    return et

def set_array_et(et):
    globals()['et'][...] = et

def get_array_wg():
    """
    Element wg ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 301
    
    """
    global wg
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pw.f90wrap_wvfct__array__wg(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        wg = _arrays[array_handle]
    else:
        wg = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pw.f90wrap_wvfct__array__wg)
        _arrays[array_handle] = wg
    return wg

def set_array_wg(wg):
    globals()['wg'][...] = wg

def get_array_g2kin():
    """
    Element g2kin ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 303
    
    """
    global g2kin
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pw.f90wrap_wvfct__array__g2kin(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        g2kin = _arrays[array_handle]
    else:
        g2kin = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pw.f90wrap_wvfct__array__g2kin)
        _arrays[array_handle] = g2kin
    return g2kin

def set_array_g2kin(g2kin):
    globals()['g2kin'][...] = g2kin

def get_array_btype():
    """
    Element btype ftype=integer pytype=int
    
    
    Defined at pwcom.fpp line 305
    
    """
    global btype
    array_ndim, array_type, array_shape, array_handle = \
        libqepy_pw.f90wrap_wvfct__array__btype(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        btype = _arrays[array_handle]
    else:
        btype = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                libqepy_pw.f90wrap_wvfct__array__btype)
        _arrays[array_handle] = btype
    return btype

def set_array_btype(btype):
    globals()['btype'][...] = btype


_array_initialisers = [get_array_et, get_array_wg, get_array_g2kin, \
    get_array_btype]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "wvfct".')

for func in _dt_array_initialisers:
    func()
