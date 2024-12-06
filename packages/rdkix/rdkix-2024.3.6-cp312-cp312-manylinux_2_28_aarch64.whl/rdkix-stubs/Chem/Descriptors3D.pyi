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
descList: list  # value = [('PMI1', <function <lambda> at 0xffffb188aca0>), ('PMI2', <function <lambda> at 0xffffb188b380>), ('PMI3', <function <lambda> at 0xffffb188b420>), ('NPR1', <function <lambda> at 0xffffb188b4c0>), ('NPR2', <function <lambda> at 0xffffb188b560>), ('RadiusOfGyration', <function <lambda> at 0xffffb188b600>), ('InertialShapeFactor', <function <lambda> at 0xffffb188b6a0>), ('Eccentricity', <function <lambda> at 0xffffb188b740>), ('Asphericity', <function <lambda> at 0xffffb188b7e0>), ('SpherocityIndex', <function <lambda> at 0xffffb188b880>), ('PBF', <function <lambda> at 0xffffb188b920>)]
