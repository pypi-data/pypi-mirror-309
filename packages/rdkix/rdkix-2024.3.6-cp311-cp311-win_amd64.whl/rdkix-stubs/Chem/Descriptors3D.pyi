"""
 Descriptors derived from a molecule's 3D structure

"""
from __future__ import annotations
from rdkix.Chem.Descriptors import _isCallable
from rdkix.Chem import rdMolDescriptors
__all__ = ['CalcMolDescriptors3D', 'descList', 'rdMolDescriptors']
def CalcMolDescriptors3D(mol, confId = None):
    """
    
        Compute all 3D descriptors of a molecule
        
        Arguments:
        - mol: the molecule to work with
        - confId: conformer ID to work with. If not specified the default (-1) is used
        
        Return:
        
        dict
            A dictionary with decriptor names as keys and the descriptor values as values
    
        raises a ValueError 
            If the molecule does not have conformers
        
    """
def _setupDescriptors(namespace):
    ...
descList: list  # value = [('PMI1', <function <lambda> at 0x0000022821783560>), ('PMI2', <function <lambda> at 0x0000022821783BA0>), ('PMI3', <function <lambda> at 0x0000022821783CE0>), ('NPR1', <function <lambda> at 0x0000022821783D80>), ('NPR2', <function <lambda> at 0x0000022821783E20>), ('RadiusOfGyration', <function <lambda> at 0x0000022821783EC0>), ('InertialShapeFactor', <function <lambda> at 0x0000022821783F60>), ('Eccentricity', <function <lambda> at 0x00000228217EC040>), ('Asphericity', <function <lambda> at 0x00000228217EC0E0>), ('SpherocityIndex', <function <lambda> at 0x00000228217EC180>), ('PBF', <function <lambda> at 0x00000228217EC220>)]
