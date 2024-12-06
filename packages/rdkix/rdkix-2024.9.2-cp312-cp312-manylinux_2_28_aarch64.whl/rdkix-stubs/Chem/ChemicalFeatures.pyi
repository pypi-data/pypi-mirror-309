from __future__ import annotations
from rdkix.Chem.rdChemicalFeatures import FreeChemicalFeature
from rdkix.Chem.rdMolChemicalFeatures import MolChemicalFeature
from rdkix.Chem.rdMolChemicalFeatures import MolChemicalFeatureFactory
__all__ = ['FreeChemicalFeature', 'MCFF_GetFeaturesForMol', 'MolChemicalFeature', 'MolChemicalFeatureFactory']
def MCFF_GetFeaturesForMol(self, mol, includeOnly = '', confId = -1):
    ...
