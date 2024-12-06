"""
Module oscdft_pp_mod


Defined at oscdft_pp_mod.fpp lines 5-5

"""
from __future__ import print_function, absolute_import, division
import libqepy_pp
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "oscdft_pp_mod".')

for func in _dt_array_initialisers:
    func()
