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
descList: list  # value = [('PMI1', <function <lambda> at 0x106453f60>), ('PMI2', <function <lambda> at 0x10bdbc540>), ('PMI3', <function <lambda> at 0x10bdbc680>), ('NPR1', <function <lambda> at 0x10bdbc720>), ('NPR2', <function <lambda> at 0x10bdbc7c0>), ('RadiusOfGyration', <function <lambda> at 0x10bdbc860>), ('InertialShapeFactor', <function <lambda> at 0x10bdbc900>), ('Eccentricity', <function <lambda> at 0x10bdbc9a0>), ('Asphericity', <function <lambda> at 0x10bdbca40>), ('SpherocityIndex', <function <lambda> at 0x10bdbcae0>), ('PBF', <function <lambda> at 0x10bdbcb80>)]
