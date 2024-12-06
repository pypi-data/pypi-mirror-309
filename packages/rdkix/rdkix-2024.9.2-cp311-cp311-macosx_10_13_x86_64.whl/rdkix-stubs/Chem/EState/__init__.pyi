"""
 A module for Kier and Hall's EState Descriptors

Unless otherwise noted, all definitions here can be found in:

  L.B. Kier and L.H. Hall _Molecular Structure Description:
  The Electrotopological State"_  Academic Press (1999)

"""
from __future__ import annotations
import numpy as numpy
from rdkix import Chem
from rdkix.Chem.EState.AtomTypes import BuildPatts
from rdkix.Chem.EState.AtomTypes import TypeAtoms
from rdkix.Chem.EState.EState import EStateIndices
from rdkix.Chem.EState.EState import GetPrincipleQuantumNumber
from rdkix.Chem.EState.EState import MaxAbsEStateIndex
from rdkix.Chem.EState.EState import MaxEStateIndex
from rdkix.Chem.EState.EState import MinAbsEStateIndex
from rdkix.Chem.EState.EState import MinEStateIndex
import sys as sys
from .AtomTypes import *
from .EState import *
__all__ = ['AtomTypes', 'BuildPatts', 'Chem', 'EState', 'EStateIndices', 'GetPrincipleQuantumNumber', 'MaxAbsEStateIndex', 'MaxEStateIndex', 'MinAbsEStateIndex', 'MinEStateIndex', 'TypeAtoms', 'esPatterns', 'numpy', 'sys']
esPatterns = None
