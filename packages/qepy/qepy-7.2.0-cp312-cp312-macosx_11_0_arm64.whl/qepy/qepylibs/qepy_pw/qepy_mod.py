"""
Module qepy_mod


Defined at qepy_mod.fpp lines 5-984

"""
from __future__ import print_function, absolute_import, division
import libqepy_pw
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def qepy_get_rho(rhor, gather=None):
    """
    qepy_get_rho(rhor[, gather])
    
    
    Defined at qepy_mod.fpp lines 169-188
    
    Parameters
    ----------
    rhor : float array
    gather : bool
    
    """
    libqepy_pw.f90wrap_qepy_mod__qepy_get_rho(rhor=rhor, gather=gather)

def qepy_set_rho(rhor, gather=None):
    """
    qepy_set_rho(rhor[, gather])
    
    
    Defined at qepy_mod.fpp lines 190-211
    
    Parameters
    ----------
    rhor : float array
    gather : bool
    
    """
    libqepy_pw.f90wrap_qepy_mod__qepy_set_rho(rhor=rhor, gather=gather)

def qepy_get_rho_core(rhoc, gather=None):
    """
    qepy_get_rho_core(rhoc[, gather])
    
    
    Defined at qepy_mod.fpp lines 213-227
    
    Parameters
    ----------
    rhoc : float array
    gather : bool
    
    """
    libqepy_pw.f90wrap_qepy_mod__qepy_get_rho_core(rhoc=rhoc, gather=gather)

def qepy_set_rho_core(rhoc, gather=None):
    """
    qepy_set_rho_core(rhoc[, gather])
    
    
    Defined at qepy_mod.fpp lines 229-243
    
    Parameters
    ----------
    rhoc : float array
    gather : bool
    
    """
    libqepy_pw.f90wrap_qepy_mod__qepy_set_rho_core(rhoc=rhoc, gather=gather)

def qepy_set_extpot(vin, gather=None):
    """
    qepy_set_extpot(vin[, gather])
    
    
    Defined at qepy_mod.fpp lines 245-272
    
    Parameters
    ----------
    vin : float array
    gather : bool
    
    """
    libqepy_pw.f90wrap_qepy_mod__qepy_set_extpot(vin=vin, gather=gather)

def qepy_get_grid(nr=None, gather=None):
    """
    nrw = qepy_get_grid([nr, gather])
    
    
    Defined at qepy_mod.fpp lines 274-290
    
    Parameters
    ----------
    nr : int array
    gather : bool
    
    Returns
    -------
    nrw : int array
    
    """
    nrw = libqepy_pw.f90wrap_qepy_mod__qepy_get_grid(nr=nr, gather=gather)
    return nrw

def qepy_get_grid_shape(self, gather=None):
    """
    nrw = qepy_get_grid_shape(self[, gather])
    
    
    Defined at qepy_mod.fpp lines 292-311
    
    Parameters
    ----------
    dfft : Fft_Type_Descriptor
    gather : bool
    
    Returns
    -------
    nrw : int array
    
    """
    nrw = libqepy_pw.f90wrap_qepy_mod__qepy_get_grid_shape(dfft=self._handle, \
        gather=gather)
    return nrw

def qepy_get_grid_smooth(nr=None, gather=None):
    """
    nrw = qepy_get_grid_smooth([nr, gather])
    
    
    Defined at qepy_mod.fpp lines 313-329
    
    Parameters
    ----------
    nr : int array
    gather : bool
    
    Returns
    -------
    nrw : int array
    
    """
    nrw = libqepy_pw.f90wrap_qepy_mod__qepy_get_grid_smooth(nr=nr, gather=gather)
    return nrw

def qepy_set_stdout(fname=None, uni=None, append=None):
    """
    qepy_set_stdout([fname, uni, append])
    
    
    Defined at qepy_mod.fpp lines 331-357
    
    Parameters
    ----------
    fname : str
    uni : int
    append : bool
    
    """
    libqepy_pw.f90wrap_qepy_mod__qepy_set_stdout(fname=fname, uni=uni, \
        append=append)

def qepy_write_stdout(fstr):
    """
    qepy_write_stdout(fstr)
    
    
    Defined at qepy_mod.fpp lines 359-365
    
    Parameters
    ----------
    fstr : str
    
    """
    libqepy_pw.f90wrap_qepy_mod__qepy_write_stdout(fstr=fstr)

def qepy_close_stdout(fname):
    """
    qepy_close_stdout(fname)
    
    
    Defined at qepy_mod.fpp lines 367-373
    
    Parameters
    ----------
    fname : str
    
    """
    libqepy_pw.f90wrap_qepy_mod__qepy_close_stdout(fname=fname)

def qepy_get_evc(ik, wfc=None):
    """
    qepy_get_evc(ik[, wfc])
    
    
    Defined at qepy_mod.fpp lines 375-389
    
    Parameters
    ----------
    ik : int
    wfc : complex array
    
    """
    libqepy_pw.f90wrap_qepy_mod__qepy_get_evc(ik=ik, wfc=wfc)

def qepy_get_wf(ik, ibnd, wf, gather=None):
    """
    qepy_get_wf(ik, ibnd, wf[, gather])
    
    
    Defined at qepy_mod.fpp lines 391-440
    
    Parameters
    ----------
    ik : int
    ibnd : int
    wf : complex array
    gather : bool
    
    """
    libqepy_pw.f90wrap_qepy_mod__qepy_get_wf(ik=ik, ibnd=ibnd, wf=wf, gather=gather)

def qepy_get_vkb(ik, vk, gather=None):
    """
    qepy_get_vkb(ik, vk[, gather])
    
    
    Defined at qepy_mod.fpp lines 442-495
    
    Parameters
    ----------
    ik : int
    vk : complex array
    gather : bool
    
    """
    libqepy_pw.f90wrap_qepy_mod__qepy_get_vkb(ik=ik, vk=vk, gather=gather)

def qepy_set_extforces(forces):
    """
    qepy_set_extforces(forces)
    
    
    Defined at qepy_mod.fpp lines 497-506
    
    Parameters
    ----------
    forces : float array
    
    """
    libqepy_pw.f90wrap_qepy_mod__qepy_set_extforces(forces=forces)

def qepy_calc_effective_potential(potential=None, gather=None):
    """
    qepy_calc_effective_potential([potential, gather])
    
    
    Defined at qepy_mod.fpp lines 508-536
    
    Parameters
    ----------
    potential : float array
    gather : bool
    
    """
    libqepy_pw.f90wrap_qepy_mod__qepy_calc_effective_potential(potential=potential, \
        gather=gather)

def qepy_set_effective_potential(potential, gather=None):
    """
    qepy_set_effective_potential(potential[, gather])
    
    
    Defined at qepy_mod.fpp lines 538-556
    
    Parameters
    ----------
    potential : float array
    gather : bool
    
    """
    libqepy_pw.f90wrap_qepy_mod__qepy_set_effective_potential(potential=potential, \
        gather=gather)

def qepy_calc_density(rhor=None, gather=None):
    """
    qepy_calc_density([rhor, gather])
    
    
    Defined at qepy_mod.fpp lines 558-576
    
    Parameters
    ----------
    rhor : float array
    gather : bool
    
    """
    libqepy_pw.f90wrap_qepy_mod__qepy_calc_density(rhor=rhor, gather=gather)

def qepy_diagonalize(iter=None, threshold=None):
    """
    qepy_diagonalize([iter, threshold])
    
    
    Defined at qepy_mod.fpp lines 578-596
    
    Parameters
    ----------
    iter : int
    threshold : float
    
    """
    libqepy_pw.f90wrap_qepy_mod__qepy_diagonalize(iter=iter, threshold=threshold)

def qepy_update_ions(pos, ikind=None, lattice=None):
    """
    qepy_update_ions(pos[, ikind, lattice])
    
    
    Defined at qepy_mod.fpp lines 598-688
    
    Parameters
    ----------
    pos : float array
    ikind : int
    lattice : float array
    
    -----------------------------------------------------------------------
     This is function Combined 'run_pwscf' and 'move_ions'.
    ***********************************************************************
     pos:
       ionic positions in bohr
     ikind:
       ikind = 0  all
       ikind = 1  atomic configuration dependent information
     lattice:
       lattice parameter in bohr
    ***********************************************************************
    -----------------------------------------------------------------------
    """
    libqepy_pw.f90wrap_qepy_mod__qepy_update_ions(pos=pos, ikind=ikind, \
        lattice=lattice)

def qepy_restart_from_xml():
    """
    qepy_restart_from_xml()
    
    
    Defined at qepy_mod.fpp lines 690-706
    
    
    """
    libqepy_pw.f90wrap_qepy_mod__qepy_restart_from_xml()

def qepy_sum_band(occupations=None):
    """
    qepy_sum_band([occupations])
    
    
    Defined at qepy_mod.fpp lines 708-732
    
    Parameters
    ----------
    occupations : float array
    
    """
    libqepy_pw.f90wrap_qepy_mod__qepy_sum_band(occupations=occupations)

def qepy_get_tau(tau, gather=None):
    """
    qepy_get_tau(tau[, gather])
    
    
    Defined at qepy_mod.fpp lines 734-761
    
    Parameters
    ----------
    tau : float array
    gather : bool
    
    """
    libqepy_pw.f90wrap_qepy_mod__qepy_get_tau(tau=tau, gather=gather)

def qepy_open_files(io_level=None):
    """
    qepy_open_files([io_level])
    
    
    Defined at qepy_mod.fpp lines 763-783
    
    Parameters
    ----------
    io_level : int
    
    """
    libqepy_pw.f90wrap_qepy_mod__qepy_open_files(io_level=io_level)

def qepy_set_dft(dft=None):
    """
    qepy_set_dft([dft])
    
    
    Defined at qepy_mod.fpp lines 785-825
    
    Parameters
    ----------
    dft : str
    
    """
    libqepy_pw.f90wrap_qepy_mod__qepy_set_dft(dft=dft)

def qepy_calc_kinetic_density(tau):
    """
    qepy_calc_kinetic_density(tau)
    
    
    Defined at qepy_mod.fpp lines 827-905
    
    Parameters
    ----------
    tau : float array
    
    """
    libqepy_pw.f90wrap_qepy_mod__qepy_calc_kinetic_density(tau=tau)

def qepy_calc_kinetic_density_normal(tau):
    """
    qepy_calc_kinetic_density_normal(tau)
    
    
    Defined at qepy_mod.fpp lines 907-984
    
    Parameters
    ----------
    tau : float array
    
    """
    libqepy_pw.f90wrap_qepy_mod__qepy_calc_kinetic_density_normal(tau=tau)

def _mp_gather_real(fin, fout):
    """
    _mp_gather_real(fin, fout)
    
    
    Defined at qepy_mod.fpp lines 31-43
    
    Parameters
    ----------
    fin : float array
    fout : float array
    
    """
    libqepy_pw.f90wrap_qepy_mod__mp_gather_real(fin=fin, fout=fout)

def _mp_gather_complex(fin, fout):
    """
    _mp_gather_complex(fin, fout)
    
    
    Defined at qepy_mod.fpp lines 59-71
    
    Parameters
    ----------
    fin : complex array
    fout : complex array
    
    """
    libqepy_pw.f90wrap_qepy_mod__mp_gather_complex(fin=fin, fout=fout)

def mp_gather(*args, **kwargs):
    """
    mp_gather(*args, **kwargs)
    
    
    Defined at qepy_mod.fpp lines 14-15
    
    Overloaded interface containing the following procedures:
      _mp_gather_real
      _mp_gather_complex
    
    """
    for proc in [_mp_gather_real, _mp_gather_complex]:
        try:
            return proc(*args, **kwargs)
        except TypeError:
            continue
    

def _mp_scatter_real(fin, fout):
    """
    _mp_scatter_real(fin, fout)
    
    
    Defined at qepy_mod.fpp lines 45-57
    
    Parameters
    ----------
    fin : float array
    fout : float array
    
    """
    libqepy_pw.f90wrap_qepy_mod__mp_scatter_real(fin=fin, fout=fout)

def _mp_scatter_complex(fin, fout):
    """
    _mp_scatter_complex(fin, fout)
    
    
    Defined at qepy_mod.fpp lines 73-85
    
    Parameters
    ----------
    fin : complex array
    fout : complex array
    
    """
    libqepy_pw.f90wrap_qepy_mod__mp_scatter_complex(fin=fin, fout=fout)

def mp_scatter(*args, **kwargs):
    """
    mp_scatter(*args, **kwargs)
    
    
    Defined at qepy_mod.fpp lines 18-19
    
    Overloaded interface containing the following procedures:
      _mp_scatter_real
      _mp_scatter_complex
    
    """
    for proc in [_mp_scatter_real, _mp_scatter_complex]:
        try:
            return proc(*args, **kwargs)
        except TypeError:
            continue
    

def _mp_bcast_group_real_1(data):
    """
    _mp_bcast_group_real_1(data)
    
    
    Defined at qepy_mod.fpp lines 87-98
    
    Parameters
    ----------
    data : float array
    
    """
    libqepy_pw.f90wrap_qepy_mod__mp_bcast_group_real_1(data=data)

def _mp_bcast_group_real_2(data):
    """
    _mp_bcast_group_real_2(data)
    
    
    Defined at qepy_mod.fpp lines 100-110
    
    Parameters
    ----------
    data : float array
    
    """
    libqepy_pw.f90wrap_qepy_mod__mp_bcast_group_real_2(data=data)

def mp_bcast_group(*args, **kwargs):
    """
    mp_bcast_group(*args, **kwargs)
    
    
    Defined at qepy_mod.fpp lines 22-23
    
    Overloaded interface containing the following procedures:
      _mp_bcast_group_real_1
      _mp_bcast_group_real_2
    
    """
    for proc in [_mp_bcast_group_real_1, _mp_bcast_group_real_2]:
        try:
            return proc(*args, **kwargs)
        except TypeError:
            continue
    

def _qepy_get_value_real_1(fin, fout, gather=None, scatter=None):
    """
    _qepy_get_value_real_1(fin, fout[, gather, scatter])
    
    
    Defined at qepy_mod.fpp lines 112-142
    
    Parameters
    ----------
    fin : float array
    fout : float array
    gather : bool
    scatter : bool
    
    """
    libqepy_pw.f90wrap_qepy_mod__qepy_get_value_real_1(fin=fin, fout=fout, \
        gather=gather, scatter=scatter)

def _qepy_get_value_real_2(fin, fout, gather=None, scatter=None):
    """
    _qepy_get_value_real_2(fin, fout[, gather, scatter])
    
    
    Defined at qepy_mod.fpp lines 144-167
    
    Parameters
    ----------
    fin : float array
    fout : float array
    gather : bool
    scatter : bool
    
    """
    libqepy_pw.f90wrap_qepy_mod__qepy_get_value_real_2(fin=fin, fout=fout, \
        gather=gather, scatter=scatter)

def qepy_get_value(*args, **kwargs):
    """
    qepy_get_value(*args, **kwargs)
    
    
    Defined at qepy_mod.fpp lines 26-27
    
    Overloaded interface containing the following procedures:
      _qepy_get_value_real_1
      _qepy_get_value_real_2
    
    """
    for proc in [_qepy_get_value_real_1, _qepy_get_value_real_2]:
        try:
            return proc(*args, **kwargs)
        except TypeError:
            continue
    


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "qepy_mod".')

for func in _dt_array_initialisers:
    func()
