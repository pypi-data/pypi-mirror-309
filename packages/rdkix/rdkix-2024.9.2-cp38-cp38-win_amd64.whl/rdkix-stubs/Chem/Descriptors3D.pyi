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
descList: list  # value = [('PMI1', <function <lambda> at 0x000002498DE77E50>), ('PMI2', <function <lambda> at 0x0000024994AF8700>), ('PMI3', <function <lambda> at 0x0000024994AF8790>), ('NPR1', <function <lambda> at 0x0000024994AF8820>), ('NPR2', <function <lambda> at 0x0000024994AF88B0>), ('RadiusOfGyration', <function <lambda> at 0x0000024994AF8940>), ('InertialShapeFactor', <function <lambda> at 0x0000024994AF89D0>), ('Eccentricity', <function <lambda> at 0x0000024994AF8A60>), ('Asphericity', <function <lambda> at 0x0000024994AF8AF0>), ('SpherocityIndex', <function <lambda> at 0x0000024994AF8B80>), ('PBF', <function <lambda> at 0x0000024994AF8C10>)]
