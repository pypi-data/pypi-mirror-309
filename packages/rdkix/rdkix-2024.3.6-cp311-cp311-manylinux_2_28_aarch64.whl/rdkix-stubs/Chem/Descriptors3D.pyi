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
descList: list  # value = [('PMI1', <function <lambda> at 0xffffa764fa60>), ('PMI2', <function <lambda> at 0xffff9b322c00>), ('PMI3', <function <lambda> at 0xffff9b322d40>), ('NPR1', <function <lambda> at 0xffff9b322de0>), ('NPR2', <function <lambda> at 0xffff9b322e80>), ('RadiusOfGyration', <function <lambda> at 0xffff9b322f20>), ('InertialShapeFactor', <function <lambda> at 0xffff9b322fc0>), ('Eccentricity', <function <lambda> at 0xffff9b323060>), ('Asphericity', <function <lambda> at 0xffff9b323100>), ('SpherocityIndex', <function <lambda> at 0xffff9b3231a0>), ('PBF', <function <lambda> at 0xffff9b323240>)]
