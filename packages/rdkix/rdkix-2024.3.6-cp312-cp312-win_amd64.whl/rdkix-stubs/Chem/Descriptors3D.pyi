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
descList: list  # value = [('PMI1', <function <lambda> at 0x0000024ED2D0D440>), ('PMI2', <function <lambda> at 0x0000024ED2D0DB20>), ('PMI3', <function <lambda> at 0x0000024ED2D0DBC0>), ('NPR1', <function <lambda> at 0x0000024ED2D0DC60>), ('NPR2', <function <lambda> at 0x0000024ED2D0DD00>), ('RadiusOfGyration', <function <lambda> at 0x0000024ED2D0DDA0>), ('InertialShapeFactor', <function <lambda> at 0x0000024ED2D0DE40>), ('Eccentricity', <function <lambda> at 0x0000024ED2D0DEE0>), ('Asphericity', <function <lambda> at 0x0000024ED2D0DF80>), ('SpherocityIndex', <function <lambda> at 0x0000024ED2D0E020>), ('PBF', <function <lambda> at 0x0000024ED2D0E0C0>)]
