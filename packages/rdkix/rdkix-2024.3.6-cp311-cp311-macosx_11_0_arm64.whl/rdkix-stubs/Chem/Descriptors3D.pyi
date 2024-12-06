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
descList: list  # value = [('PMI1', <function <lambda> at 0x102be99e0>), ('PMI2', <function <lambda> at 0x105c185e0>), ('PMI3', <function <lambda> at 0x105c18720>), ('NPR1', <function <lambda> at 0x105c187c0>), ('NPR2', <function <lambda> at 0x105c18860>), ('RadiusOfGyration', <function <lambda> at 0x105c18900>), ('InertialShapeFactor', <function <lambda> at 0x105c189a0>), ('Eccentricity', <function <lambda> at 0x105c18a40>), ('Asphericity', <function <lambda> at 0x105c18ae0>), ('SpherocityIndex', <function <lambda> at 0x105c18b80>), ('PBF', <function <lambda> at 0x105c18c20>)]
