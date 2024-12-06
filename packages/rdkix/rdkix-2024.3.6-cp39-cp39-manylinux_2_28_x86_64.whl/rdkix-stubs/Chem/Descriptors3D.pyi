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
descList: list  # value = [('PMI1', <function <lambda> at 0x7f0ea1407a60>), ('PMI2', <function <lambda> at 0x7f0e9209f8b0>), ('PMI3', <function <lambda> at 0x7f0e9209f940>), ('NPR1', <function <lambda> at 0x7f0e9209f9d0>), ('NPR2', <function <lambda> at 0x7f0e9209fa60>), ('RadiusOfGyration', <function <lambda> at 0x7f0e9209faf0>), ('InertialShapeFactor', <function <lambda> at 0x7f0e9209fb80>), ('Eccentricity', <function <lambda> at 0x7f0e9209fc10>), ('Asphericity', <function <lambda> at 0x7f0e9209fca0>), ('SpherocityIndex', <function <lambda> at 0x7f0e9209fd30>), ('PBF', <function <lambda> at 0x7f0e9209fdc0>)]
