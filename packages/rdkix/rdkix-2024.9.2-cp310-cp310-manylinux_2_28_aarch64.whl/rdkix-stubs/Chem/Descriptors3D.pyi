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
descList: list  # value = [('PMI1', <function <lambda> at 0xffff84e3e9e0>), ('PMI2', <function <lambda> at 0xffff78bc72e0>), ('PMI3', <function <lambda> at 0xffff78bc7370>), ('NPR1', <function <lambda> at 0xffff78bc7400>), ('NPR2', <function <lambda> at 0xffff78bc7490>), ('RadiusOfGyration', <function <lambda> at 0xffff78bc7520>), ('InertialShapeFactor', <function <lambda> at 0xffff78bc75b0>), ('Eccentricity', <function <lambda> at 0xffff78bc7640>), ('Asphericity', <function <lambda> at 0xffff78bc76d0>), ('SpherocityIndex', <function <lambda> at 0xffff78bc7760>), ('PBF', <function <lambda> at 0xffff78bc77f0>)]
