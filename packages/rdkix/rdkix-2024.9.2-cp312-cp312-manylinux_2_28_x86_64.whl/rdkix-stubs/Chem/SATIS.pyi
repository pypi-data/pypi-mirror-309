"""
  Functionality for SATIS typing atoms

"""
from __future__ import annotations
import itertools as itertools
from rdkix import Chem
import rdkix.Chem.rdchem
__all__ = ['Chem', 'SATISTypes', 'aldehydePatt', 'amidePatt', 'carboxylPatt', 'carboxylatePatt', 'esterPatt', 'itertools', 'ketonePatt', 'specialCases']
def SATISTypes(mol, neighborsToInclude = 4):
    """
     returns SATIS codes for all atoms in a molecule
    
       The SATIS definition used is from:
       J. Chem. Inf. Comput. Sci. _39_ 751-757 (1999)
    
       each SATIS code is a string consisting of _neighborsToInclude_ + 1
       2 digit numbers
    
       **Arguments**
    
         - mol: a molecule
    
         - neighborsToInclude (optional): the number of neighbors to include
           in the SATIS codes
    
       **Returns**
    
         a list of strings nAtoms long
    
      
    """
aldehydePatt: rdkix.Chem.rdchem.Mol  # value = <rdkix.Chem.rdchem.Mol object>
amidePatt: rdkix.Chem.rdchem.Mol  # value = <rdkix.Chem.rdchem.Mol object>
carboxylPatt: rdkix.Chem.rdchem.Mol  # value = <rdkix.Chem.rdchem.Mol object>
carboxylatePatt: rdkix.Chem.rdchem.Mol  # value = <rdkix.Chem.rdchem.Mol object>
esterPatt: rdkix.Chem.rdchem.Mol  # value = <rdkix.Chem.rdchem.Mol object>
ketonePatt: rdkix.Chem.rdchem.Mol  # value = <rdkix.Chem.rdchem.Mol object>
specialCases: tuple  # value = ((<rdkix.Chem.rdchem.Mol object>, 97), (<rdkix.Chem.rdchem.Mol object>, 96), (<rdkix.Chem.rdchem.Mol object>, 98), (<rdkix.Chem.rdchem.Mol object>, 95), (<rdkix.Chem.rdchem.Mol object>, 94), (<rdkix.Chem.rdchem.Mol object>, 93))
