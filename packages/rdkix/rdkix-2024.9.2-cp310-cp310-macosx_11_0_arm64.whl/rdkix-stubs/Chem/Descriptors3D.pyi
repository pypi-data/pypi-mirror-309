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
descList: list  # value = [('PMI1', <function <lambda> at 0x104e76cb0>), ('PMI2', <function <lambda> at 0x107c525f0>), ('PMI3', <function <lambda> at 0x107c52680>), ('NPR1', <function <lambda> at 0x107c52710>), ('NPR2', <function <lambda> at 0x107c527a0>), ('RadiusOfGyration', <function <lambda> at 0x107c52830>), ('InertialShapeFactor', <function <lambda> at 0x107c528c0>), ('Eccentricity', <function <lambda> at 0x107c52950>), ('Asphericity', <function <lambda> at 0x107c529e0>), ('SpherocityIndex', <function <lambda> at 0x107c52a70>), ('PBF', <function <lambda> at 0x107c52b00>)]
