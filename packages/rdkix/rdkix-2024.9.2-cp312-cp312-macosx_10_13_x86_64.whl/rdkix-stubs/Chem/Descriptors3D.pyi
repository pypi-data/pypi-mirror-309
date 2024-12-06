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
descList: list  # value = [('PMI1', <function <lambda> at 0x108eb2340>), ('PMI2', <function <lambda> at 0x10c922660>), ('PMI3', <function <lambda> at 0x10c922700>), ('NPR1', <function <lambda> at 0x10c9227a0>), ('NPR2', <function <lambda> at 0x10c922840>), ('RadiusOfGyration', <function <lambda> at 0x10c9228e0>), ('InertialShapeFactor', <function <lambda> at 0x10c922980>), ('Eccentricity', <function <lambda> at 0x10c922a20>), ('Asphericity', <function <lambda> at 0x10c922ac0>), ('SpherocityIndex', <function <lambda> at 0x10c922b60>), ('PBF', <function <lambda> at 0x10c922c00>)]
