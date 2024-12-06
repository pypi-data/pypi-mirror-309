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
descList: list  # value = [('PMI1', <function <lambda> at 0x10619f1f0>), ('PMI2', <function <lambda> at 0x10b9f34c0>), ('PMI3', <function <lambda> at 0x10b9f3550>), ('NPR1', <function <lambda> at 0x10b9f35e0>), ('NPR2', <function <lambda> at 0x10b9f3670>), ('RadiusOfGyration', <function <lambda> at 0x10b9f3700>), ('InertialShapeFactor', <function <lambda> at 0x10b9f3790>), ('Eccentricity', <function <lambda> at 0x10b9f3820>), ('Asphericity', <function <lambda> at 0x10b9f38b0>), ('SpherocityIndex', <function <lambda> at 0x10b9f3940>), ('PBF', <function <lambda> at 0x10b9f39d0>)]
