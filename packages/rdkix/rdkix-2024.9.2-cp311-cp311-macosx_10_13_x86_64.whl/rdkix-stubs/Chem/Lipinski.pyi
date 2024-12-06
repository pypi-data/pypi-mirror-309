"""
 Calculation of Lipinski parameters for molecules

"""
from __future__ import annotations
from rdkix import Chem
from rdkix.Chem import rdMolDescriptors
import rdkix.Chem.rdchem
__all__ = ['Chem', 'HAcceptorSmarts', 'HDonorSmarts', 'HeavyAtomCount', 'HeteroatomSmarts', 'NHOHSmarts', 'NOCountSmarts', 'RotatableBondSmarts', 'nm', 'rdMolDescriptors', 'txt']
def HeavyAtomCount(mol):
    """
     Number of heavy atoms a molecule.
    """
HAcceptorSmarts: rdkix.Chem.rdchem.Mol  # value = <rdkix.Chem.rdchem.Mol object>
HDonorSmarts: rdkix.Chem.rdchem.Mol  # value = <rdkix.Chem.rdchem.Mol object>
HeteroatomSmarts: rdkix.Chem.rdchem.Mol  # value = <rdkix.Chem.rdchem.Mol object>
NHOHSmarts: rdkix.Chem.rdchem.Mol  # value = <rdkix.Chem.rdchem.Mol object>
NOCountSmarts: rdkix.Chem.rdchem.Mol  # value = <rdkix.Chem.rdchem.Mol object>
RotatableBondSmarts: rdkix.Chem.rdchem.Mol  # value = <rdkix.Chem.rdchem.Mol object>
_bulkConvert: tuple = ('CalcFractionCSP3', 'CalcNumAromaticRings', 'CalcNumSaturatedRings', 'CalcNumAromaticHeterocycles', 'CalcNumAromaticCarbocycles', 'CalcNumSaturatedHeterocycles', 'CalcNumSaturatedCarbocycles', 'CalcNumAliphaticRings', 'CalcNumAliphaticHeterocycles', 'CalcNumAliphaticCarbocycles')
nm: str = 'NumAliphaticCarbocycles'
txt: str = 'CalcNumAliphaticCarbocycles'
