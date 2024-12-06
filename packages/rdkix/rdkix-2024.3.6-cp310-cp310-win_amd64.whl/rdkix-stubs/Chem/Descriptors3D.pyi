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
descList: list  # value = [('PMI1', <function <lambda> at 0x000002474DF6E680>), ('PMI2', <function <lambda> at 0x0000024756014550>), ('PMI3', <function <lambda> at 0x00000247560145E0>), ('NPR1', <function <lambda> at 0x0000024756014670>), ('NPR2', <function <lambda> at 0x0000024756014700>), ('RadiusOfGyration', <function <lambda> at 0x0000024756014790>), ('InertialShapeFactor', <function <lambda> at 0x0000024756014820>), ('Eccentricity', <function <lambda> at 0x00000247560148B0>), ('Asphericity', <function <lambda> at 0x0000024756014940>), ('SpherocityIndex', <function <lambda> at 0x00000247560149D0>), ('PBF', <function <lambda> at 0x0000024756014A60>)]
