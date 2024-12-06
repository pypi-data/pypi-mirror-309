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
descList: list  # value = [('PMI1', <function <lambda> at 0x7fe2c3fcf5e0>), ('PMI2', <function <lambda> at 0x7fe2c4f86c10>), ('PMI3', <function <lambda> at 0x7fe2c4f86ca0>), ('NPR1', <function <lambda> at 0x7fe2c4f86d30>), ('NPR2', <function <lambda> at 0x7fe2c4f86dc0>), ('RadiusOfGyration', <function <lambda> at 0x7fe2c4f86e50>), ('InertialShapeFactor', <function <lambda> at 0x7fe2c4f86ee0>), ('Eccentricity', <function <lambda> at 0x7fe2c4f86f70>), ('Asphericity', <function <lambda> at 0x7fe2c4f9b040>), ('SpherocityIndex', <function <lambda> at 0x7fe2c4f9b0d0>), ('PBF', <function <lambda> at 0x7fe2c4f9b160>)]
