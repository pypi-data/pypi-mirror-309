from __future__ import annotations
import os as os
import pickle as pickle
from rdkix import RDConfig
import rdkix.VLib.Supply
from rdkix.VLib.Supply import SupplyNode
import sys as sys
__all__ = ['DbPickleSupplyNode', 'GetNode', 'RDConfig', 'SupplyNode', 'os', 'pickle', 'sys']
class DbPickleSupplyNode(rdkix.VLib.Supply.SupplyNode):
    """
     Supplies pickled objects from a db result set:
    
      Sample Usage:
        >>> from rdkix.Dbase.DbConnection import DbConnect
      
      
    """
    def __init__(self, cursor, cmd, binaryCol, **kwargs):
        ...
    def next(self):
        """
        
        
            
        """
    def reset(self):
        ...
def GetNode(dbName, tableName):
    ...
def _test():
    ...
_dataSeq = None
