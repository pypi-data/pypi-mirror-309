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
descList: list  # value = [('PMI1', <function <lambda> at 0x104575ee0>), ('PMI2', <function <lambda> at 0x104576520>), ('PMI3', <function <lambda> at 0x1045765c0>), ('NPR1', <function <lambda> at 0x104576660>), ('NPR2', <function <lambda> at 0x104576700>), ('RadiusOfGyration', <function <lambda> at 0x1045767a0>), ('InertialShapeFactor', <function <lambda> at 0x104576840>), ('Eccentricity', <function <lambda> at 0x1045768e0>), ('Asphericity', <function <lambda> at 0x104576980>), ('SpherocityIndex', <function <lambda> at 0x104576a20>), ('PBF', <function <lambda> at 0x104576ac0>)]
