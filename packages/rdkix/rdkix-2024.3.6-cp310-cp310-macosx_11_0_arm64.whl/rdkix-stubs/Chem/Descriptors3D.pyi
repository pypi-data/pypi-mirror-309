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
descList: list  # value = [('PMI1', <function <lambda> at 0x1050a2cb0>), ('PMI2', <function <lambda> at 0x107d7e3b0>), ('PMI3', <function <lambda> at 0x107d7e440>), ('NPR1', <function <lambda> at 0x107d7e4d0>), ('NPR2', <function <lambda> at 0x107d7e560>), ('RadiusOfGyration', <function <lambda> at 0x107d7e5f0>), ('InertialShapeFactor', <function <lambda> at 0x107d7e680>), ('Eccentricity', <function <lambda> at 0x107d7e710>), ('Asphericity', <function <lambda> at 0x107d7e7a0>), ('SpherocityIndex', <function <lambda> at 0x107d7e830>), ('PBF', <function <lambda> at 0x107d7e8c0>)]
