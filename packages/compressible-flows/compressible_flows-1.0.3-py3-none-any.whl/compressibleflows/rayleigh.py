from __future__ import absolute_import
from typing import Union
import numpy.typing as npt 

def P2_P1(M1:Union[npt.NDArray,float], M2:Union[npt.NDArray,float], gamma=1.4) -> Union[npt.NDArray,float]:
    """Returns P2/P1 ratio for Rayleigh Flow

    Args:
        M1 (Union[npt.NDArray,float]): Mach 1 
        M2 (Union[npt.NDArray,float]): Mach 2 
        gamma (float, optional): ratio of specific heats. Defaults to 1.4.

    Returns:
        Union[npt.NDArray,float]: Returns P2_P2 Ratio 
    """
    return ((1 + gamma*M1**2) / (1 + gamma*M2**2))

def T2_T1(M1:Union[npt.NDArray,float], M2:Union[npt.NDArray,float], gamma=1.4) ->Union[npt.NDArray,float]:
    '''Return T2/T1 for Rayleigh flow'''
    return (
        ((1 + gamma*M1**2) / (1 + gamma*M2**2))**2 *
        (M2**2 / M1**2)
        )
            
def rho2_rho1(M1:Union[npt.NDArray,float], M2:Union[npt.NDArray,float], gamma=1.4) -> Union[npt.NDArray,float]:
    '''Return rho2/rho1 for Rayleigh flow'''
    return (
        ((1 + gamma*M2**2) / (1 + gamma*M1**2)) *
        (M1**2 / M2**2)
        )
            
def T02_T01(M1:Union[npt.NDArray,float], M2:Union[npt.NDArray,float], gamma=1.4) -> Union[npt.NDArray,float]:
    '''Return Tt2/Tt1 for Rayleigh flow'''
    return (
        ((1 + gamma*M1**2) / (1 + gamma*M2**2))**2 * 
            (M2 / M1)**2 * (
            (1 + 0.5*(gamma-1)*M2**2) /
            (1 + 0.5*(gamma-1)*M1**2)
            )
        )

def P02_P01(M1:Union[npt.NDArray,float], M2:Union[npt.NDArray,float], gamma=1.4) -> Union[npt.NDArray,float]:
    '''Return pt2/pt1 for Rayleigh flow'''
    return (
        ((1 + gamma*M1**2) / (1 + gamma*M2**2)) * (
            (1 + 0.5*(gamma-1)*M2**2) /
            (1 + 0.5*(gamma-1)*M1**2)
            )**(gamma / (gamma - 1))
        )

def P_P_sonic(mach, gamma=1.4):
    '''Return p/p* for Rayleigh flow'''
    return ((1 + gamma) / (1 + gamma*mach**2))

def T_T_sonic(mach, gamma=1.4):
    '''Return T/T* for Rayleigh flow'''
    return (
        mach**2 * (1 + gamma)**2 / 
        (1 + gamma*mach**2)**2
        )
            
def rho_rho_sonic(mach, gamma=1.4):
    '''Return rho/rho* for Rayleigh flow'''
    return ((1 + gamma*mach**2) / ((1 + gamma) * mach**2))
            
def T0_T0_sonic(mach, gamma=1.4):
    '''Return Tt/Tt* for Rayleigh flow'''
    return (
        2*(1 + gamma)*mach**2 * 
        (1 + 0.5*(gamma - 1)*mach**2) / (1 + gamma*mach**2)**2
        )

def P0_P0_sonic(mach, gamma=1.4):
    '''Return pt/pt* for Rayleigh flow'''
    return (
        (1 + gamma) * (
            (1 + 0.5*(gamma-1)*mach**2) / (0.5*(gamma+1))
            )**(gamma / (gamma - 1)) /
            (1 + gamma*mach**2)
        )