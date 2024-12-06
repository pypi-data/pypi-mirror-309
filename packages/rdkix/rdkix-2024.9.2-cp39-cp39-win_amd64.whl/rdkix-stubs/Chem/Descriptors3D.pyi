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
descList: list  # value = [('PMI1', <function <lambda> at 0x000001FDF4378AF0>), ('PMI2', <function <lambda> at 0x000001FDFC61A3A0>), ('PMI3', <function <lambda> at 0x000001FDFC61A430>), ('NPR1', <function <lambda> at 0x000001FDFC61A4C0>), ('NPR2', <function <lambda> at 0x000001FDFC61A550>), ('RadiusOfGyration', <function <lambda> at 0x000001FDFC61A5E0>), ('InertialShapeFactor', <function <lambda> at 0x000001FDFC61A670>), ('Eccentricity', <function <lambda> at 0x000001FDFC61A700>), ('Asphericity', <function <lambda> at 0x000001FDFC61A790>), ('SpherocityIndex', <function <lambda> at 0x000001FDFC61A820>), ('PBF', <function <lambda> at 0x000001FDFC61A8B0>)]
