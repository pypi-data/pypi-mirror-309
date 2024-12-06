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
descList: list  # value = [('PMI1', <function <lambda> at 0x102fd6520>), ('PMI2', <function <lambda> at 0x105fd0860>), ('PMI3', <function <lambda> at 0x105fd09a0>), ('NPR1', <function <lambda> at 0x105fd0a40>), ('NPR2', <function <lambda> at 0x105fd0ae0>), ('RadiusOfGyration', <function <lambda> at 0x105fd0b80>), ('InertialShapeFactor', <function <lambda> at 0x105fd0c20>), ('Eccentricity', <function <lambda> at 0x105fd0cc0>), ('Asphericity', <function <lambda> at 0x105fd0d60>), ('SpherocityIndex', <function <lambda> at 0x105fd0e00>), ('PBF', <function <lambda> at 0x105fd0ea0>)]
