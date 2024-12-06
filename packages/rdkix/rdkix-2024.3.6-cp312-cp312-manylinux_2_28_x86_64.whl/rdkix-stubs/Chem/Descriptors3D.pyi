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
descList: list  # value = [('PMI1', <function <lambda> at 0x7f44d21b2c00>), ('PMI2', <function <lambda> at 0x7f44d21b32e0>), ('PMI3', <function <lambda> at 0x7f44d21b3380>), ('NPR1', <function <lambda> at 0x7f44d21b3420>), ('NPR2', <function <lambda> at 0x7f44d21b34c0>), ('RadiusOfGyration', <function <lambda> at 0x7f44d21b3560>), ('InertialShapeFactor', <function <lambda> at 0x7f44d21b3600>), ('Eccentricity', <function <lambda> at 0x7f44d21b36a0>), ('Asphericity', <function <lambda> at 0x7f44d21b3740>), ('SpherocityIndex', <function <lambda> at 0x7f44d21b37e0>), ('PBF', <function <lambda> at 0x7f44d21b3880>)]
