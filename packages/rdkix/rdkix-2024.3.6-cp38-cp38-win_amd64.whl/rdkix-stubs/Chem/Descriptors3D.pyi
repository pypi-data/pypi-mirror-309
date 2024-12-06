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
descList: list  # value = [('PMI1', <function <lambda> at 0x0000017AC33A7E50>), ('PMI2', <function <lambda> at 0x0000017ACA0374C0>), ('PMI3', <function <lambda> at 0x0000017ACA037550>), ('NPR1', <function <lambda> at 0x0000017ACA0375E0>), ('NPR2', <function <lambda> at 0x0000017ACA037670>), ('RadiusOfGyration', <function <lambda> at 0x0000017ACA037700>), ('InertialShapeFactor', <function <lambda> at 0x0000017ACA037790>), ('Eccentricity', <function <lambda> at 0x0000017ACA037820>), ('Asphericity', <function <lambda> at 0x0000017ACA0378B0>), ('SpherocityIndex', <function <lambda> at 0x0000017ACA037940>), ('PBF', <function <lambda> at 0x0000017ACA0379D0>)]
