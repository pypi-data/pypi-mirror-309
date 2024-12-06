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
descList: list  # value = [('PMI1', <function <lambda> at 0x10e81ac20>), ('PMI2', <function <lambda> at 0x113f5e440>), ('PMI3', <function <lambda> at 0x113f5e4d0>), ('NPR1', <function <lambda> at 0x113f5e560>), ('NPR2', <function <lambda> at 0x113f5e5f0>), ('RadiusOfGyration', <function <lambda> at 0x113f5e680>), ('InertialShapeFactor', <function <lambda> at 0x113f5e710>), ('Eccentricity', <function <lambda> at 0x113f5e7a0>), ('Asphericity', <function <lambda> at 0x113f5e830>), ('SpherocityIndex', <function <lambda> at 0x113f5e8c0>), ('PBF', <function <lambda> at 0x113f5e950>)]
