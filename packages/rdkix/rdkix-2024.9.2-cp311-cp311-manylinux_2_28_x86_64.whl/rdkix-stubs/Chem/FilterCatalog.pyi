from __future__ import annotations
from rdkix import Chem
import rdkix.Chem.rdfiltercatalog
from rdkix.Chem.rdfiltercatalog import ExclusionList
from rdkix.Chem.rdfiltercatalog import FilterCatalog
from rdkix.Chem.rdfiltercatalog import FilterCatalogEntry
from rdkix.Chem.rdfiltercatalog import FilterCatalogEntryList
from rdkix.Chem.rdfiltercatalog import FilterCatalogListOfEntryList
from rdkix.Chem.rdfiltercatalog import FilterCatalogParams
from rdkix.Chem.rdfiltercatalog import FilterHierarchyMatcher
from rdkix.Chem.rdfiltercatalog import FilterMatch
from rdkix.Chem.rdfiltercatalog import FilterMatchOps
from rdkix.Chem.rdfiltercatalog import FilterMatcherBase
from rdkix.Chem.rdfiltercatalog import IntPair
from rdkix.Chem.rdfiltercatalog import MolList
from rdkix.Chem.rdfiltercatalog import PythonFilterMatcher
from rdkix.Chem.rdfiltercatalog import SmartsMatcher
from rdkix.Chem.rdfiltercatalog import VectFilterMatch
from rdkix import rdBase
from rdkix.rdBase import MatchTypeVect
import sys as sys
__all__ = ['Chem', 'ExclusionList', 'FilterCatalog', 'FilterCatalogEntry', 'FilterCatalogEntryList', 'FilterCatalogListOfEntryList', 'FilterCatalogParams', 'FilterHierarchyMatcher', 'FilterMatch', 'FilterMatchOps', 'FilterMatcher', 'FilterMatcherBase', 'IntPair', 'MatchTypeVect', 'MolList', 'PythonFilterMatcher', 'SmartsMatcher', 'VectFilterMatch', 'rdBase', 'sys']
class FilterMatcher(rdkix.Chem.rdfiltercatalog.PythonFilterMatcher):
    """
    FilterMatcher - This class allows creation of Python based
        filters.  Subclass this class to create a Filter useable
        in a FilterCatalogEntry
    
        Simple Example:
    
        from rdkix.Chem import rdMolDescriptors
        class MWFilter(FilterMatcher):
          def __init__(self, minMw, maxMw):
              FilterMatcher.__init__(self, "MW violation")
              self.minMw = minMw
              self.maxMw = maxMw
    
          def IsValid(self):
             return True
    
          def HasMatch(self, mol):
             mw = rdMolDescriptors.CalcExactMolWt(mol)
             return not self.minMw <= mw <= self.maxMw
        
    """
    def GetMatches(self, mol, matchVect):
        """
        Return True if the filter matches the molecule
                (By default, this calls HasMatch and does not modify matchVect)
                
                matchVect is a vector of FilterMatch's which hold the matching
                filter and the matched query_atom, mol_atom pairs if applicable.
                To append to this vector:
                v = MatchTypeVect()
                v.append(IntPair( query_atom_idx, mol_atom_idx ) )
                match = FilterMatch(self, v)
                matchVect.append( match )
                
        """
    def GetName(self):
        ...
    def HasMatch(self, mol):
        """
        Return True if the filter matches the molecule
        """
    def IsValid(self, mol):
        """
        Must override this function
        """
    def __init__(self, name = 'Unamed FilterMatcher'):
        ...
