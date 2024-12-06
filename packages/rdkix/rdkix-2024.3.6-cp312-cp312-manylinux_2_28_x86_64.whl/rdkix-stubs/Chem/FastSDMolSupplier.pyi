from __future__ import annotations
from rdkix import Chem
import rdkix.Chem.rdmolfiles
import sys as sys
import warnings as warnings
__all__ = ['Chem', 'FastSDMolSupplier', 'sys', 'warnings']
class FastSDMolSupplier(rdkix.Chem.rdmolfiles.SDMolSupplier):
    pass
__warningregistry__: dict = {'version': 4}
