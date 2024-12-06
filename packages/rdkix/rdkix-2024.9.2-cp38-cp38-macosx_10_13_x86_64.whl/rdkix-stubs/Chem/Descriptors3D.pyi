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
descList: list  # value = [('PMI1', <function <lambda> at 0x7f998e7a95e0>), ('PMI2', <function <lambda> at 0x7f998f7d4e50>), ('PMI3', <function <lambda> at 0x7f998f7d4ee0>), ('NPR1', <function <lambda> at 0x7f998f7d4f70>), ('NPR2', <function <lambda> at 0x7f998f7e7040>), ('RadiusOfGyration', <function <lambda> at 0x7f998f7e70d0>), ('InertialShapeFactor', <function <lambda> at 0x7f998f7e7160>), ('Eccentricity', <function <lambda> at 0x7f998f7e71f0>), ('Asphericity', <function <lambda> at 0x7f998f7e7280>), ('SpherocityIndex', <function <lambda> at 0x7f998f7e7310>), ('PBF', <function <lambda> at 0x7f998f7e73a0>)]
