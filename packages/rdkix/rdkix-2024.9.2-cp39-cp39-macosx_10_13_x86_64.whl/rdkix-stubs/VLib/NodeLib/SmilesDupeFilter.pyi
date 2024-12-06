from __future__ import annotations
from rdkix import Chem
import rdkix.VLib.Filter
from rdkix.VLib.Filter import FilterNode
__all__ = ['Chem', 'DupeFilter', 'FilterNode']
class DupeFilter(rdkix.VLib.Filter.FilterNode):
    """
     canonical-smiles based duplicate filter
    
      Assumptions:
    
        - inputs are molecules
    
    
      Sample Usage:
        >>> import os
        >>> from rdkix import RDConfig
        >>> from rdkix.VLib.NodeLib.SDSupply import SDSupplyNode
        >>> fileN = os.path.join(RDConfig.RDCodeDir,'VLib','NodeLib',                             'test_data','NCI_aids.10.sdf')
        >>> suppl = SDSupplyNode(fileN)
        >>> filt = DupeFilter()
        >>> filt.AddParent(suppl)
        >>> ms = [x for x in filt]
        >>> len(ms)
        10
        >>> ms[0].GetProp("_Name")
        '48'
        >>> ms[1].GetProp("_Name")
        '78'
        >>> filt.reset()
        >>> filt.next().GetProp("_Name")
        '48'
    
    
      
    """
    def __init__(self, **kwargs):
        ...
    def filter(self, cmpd):
        ...
    def reset(self):
        ...
def _runDoctests(verbose = None):
    ...
