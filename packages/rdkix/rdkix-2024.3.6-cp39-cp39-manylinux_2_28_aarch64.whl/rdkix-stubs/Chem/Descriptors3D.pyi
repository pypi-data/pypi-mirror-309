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
descList: list  # value = [('PMI1', <function <lambda> at 0xffffaea8b940>), ('PMI2', <function <lambda> at 0xffffa2063790>), ('PMI3', <function <lambda> at 0xffffa2063820>), ('NPR1', <function <lambda> at 0xffffa20638b0>), ('NPR2', <function <lambda> at 0xffffa2063940>), ('RadiusOfGyration', <function <lambda> at 0xffffa20639d0>), ('InertialShapeFactor', <function <lambda> at 0xffffa2063a60>), ('Eccentricity', <function <lambda> at 0xffffa2063af0>), ('Asphericity', <function <lambda> at 0xffffa2063b80>), ('SpherocityIndex', <function <lambda> at 0xffffa2063c10>), ('PBF', <function <lambda> at 0xffffa2063ca0>)]
