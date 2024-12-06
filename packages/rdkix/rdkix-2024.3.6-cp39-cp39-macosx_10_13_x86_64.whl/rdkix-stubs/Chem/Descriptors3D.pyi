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
descList: list  # value = [('PMI1', <function <lambda> at 0x10795e1f0>), ('PMI2', <function <lambda> at 0x10d013280>), ('PMI3', <function <lambda> at 0x10d013310>), ('NPR1', <function <lambda> at 0x10d0133a0>), ('NPR2', <function <lambda> at 0x10d013430>), ('RadiusOfGyration', <function <lambda> at 0x10d0134c0>), ('InertialShapeFactor', <function <lambda> at 0x10d013550>), ('Eccentricity', <function <lambda> at 0x10d0135e0>), ('Asphericity', <function <lambda> at 0x10d013670>), ('SpherocityIndex', <function <lambda> at 0x10d013700>), ('PBF', <function <lambda> at 0x10d013790>)]
