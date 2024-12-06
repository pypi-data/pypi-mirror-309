from __future__ import annotations
import rdkix.Chem
import typing
from .FilterMatchOps import *
__all__ = ['ExclusionList', 'FilterCatalog', 'FilterCatalogCanSerialize', 'FilterCatalogEntry', 'FilterCatalogEntryList', 'FilterCatalogListOfEntryList', 'FilterCatalogParams', 'FilterHierarchyMatcher', 'FilterMatch', 'FilterMatchOps', 'FilterMatcherBase', 'GetFlattenedFunctionalGroupHierarchy', 'GetFunctionalGroupHierarchy', 'IntPair', 'MolList', 'PythonFilterMatcher', 'RunFilterCatalog', 'SmartsMatcher', 'VectFilterMatch']
class ExclusionList(FilterMatcherBase):
    __instance_size__: typing.ClassVar[int] = 104
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def AddPattern(self, base: FilterMatcherBase) -> None:
        """
            Add a FilterMatcherBase that should not appear in a molecule
        
            C++ signature :
                void AddPattern(class RDKix::ExclusionList {lvalue},class RDKix::FilterMatcherBase)
        """
    def SetExclusionPatterns(self, list: typing.Any) -> None:
        """
            Set a list of FilterMatcherBases that should not appear in a molecule
        
            C++ signature :
                void SetExclusionPatterns(class RDKix::ExclusionList {lvalue},class boost::python::api::object)
        """
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64)
        """
class FilterCatalog(Boost.Python.instance):
    __getstate_manages_dict__: typing.ClassVar[bool] = True
    __instance_size__: typing.ClassVar[int] = 72
    __safe_for_unpickling__: typing.ClassVar[bool] = True
    @staticmethod
    def AddEntry(entry: FilterCatalog, updateFPLength: FilterCatalogEntry = False) -> None:
        """
            Add a FilterCatalogEntry to the catalog
        
            C++ signature :
                void AddEntry(class RDKix::FilterCatalog {lvalue} [,class RDKix::FilterCatalogEntry * __ptr64=False])
        """
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def GetEntry(self, idx: int) -> FilterCatalogEntry:
        """
            Return the FilterCatalogEntry at the specified index
        
            C++ signature :
                class boost::shared_ptr<class RDKix::FilterCatalogEntry const > GetEntry(class RDKix::FilterCatalog {lvalue},unsigned int)
        """
    def GetEntryWithIdx(self, idx: int) -> FilterCatalogEntry:
        """
            Return the FilterCatalogEntry at the specified index
        
            C++ signature :
                class boost::shared_ptr<class RDKix::FilterCatalogEntry const > GetEntryWithIdx(class RDKix::FilterCatalog {lvalue},unsigned int)
        """
    def GetFilterMatches(self, mol: Mol) -> VectFilterMatch:
        """
            Return every matching filter from all catalog entries that match mol
        
            C++ signature :
                class std::vector<struct RDKix::FilterMatch,class std::allocator<struct RDKix::FilterMatch> > GetFilterMatches(class RDKix::FilterCatalog {lvalue},class RDKix::ROMol)
        """
    def GetFirstMatch(self, mol: Mol) -> FilterCatalogEntry:
        """
            Return the first catalog entry that matches mol
        
            C++ signature :
                class boost::shared_ptr<class RDKix::FilterCatalogEntry const > GetFirstMatch(class RDKix::FilterCatalog {lvalue},class RDKix::ROMol)
        """
    def GetMatches(self, mol: Mol) -> FilterCatalogEntryList:
        """
            Return all catalog entries that match mol
        
            C++ signature :
                class std::vector<class boost::shared_ptr<class RDKix::FilterCatalogEntry const >,class std::allocator<class boost::shared_ptr<class RDKix::FilterCatalogEntry const > > > GetMatches(class RDKix::FilterCatalog {lvalue},class RDKix::ROMol)
        """
    def GetNumEntries(self) -> int:
        """
            Returns the number of entries in the catalog
        
            C++ signature :
                unsigned int GetNumEntries(class RDKix::FilterCatalog {lvalue})
        """
    def HasMatch(self, mol: Mol) -> bool:
        """
            Returns True if the catalog has an entry that matches mol
        
            C++ signature :
                bool HasMatch(class RDKix::FilterCatalog {lvalue},class RDKix::ROMol)
        """
    def RemoveEntry(self, obj: typing.Any) -> bool:
        """
            Remove the given entry from the catalog
        
            C++ signature :
                bool RemoveEntry(class RDKix::FilterCatalog {lvalue},class boost::python::api::object)
        """
    def Serialize(self) -> typing.Any:
        """
            C++ signature :
                class boost::python::api::object Serialize(class RDKix::FilterCatalog)
        """
    def __getinitargs__(self) -> tuple:
        """
            C++ signature :
                class boost::python::tuple __getinitargs__(class RDKix::FilterCatalog)
        """
    def __getstate__(self) -> tuple:
        """
            C++ signature :
                class boost::python::tuple __getstate__(class boost::python::api::object)
        """
    @typing.overload
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64)
        """
    @typing.overload
    def __init__(self, binStr: str) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64,class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >)
        """
    @typing.overload
    def __init__(self, params: FilterCatalogParams) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64,class RDKix::FilterCatalogParams)
        """
    @typing.overload
    def __init__(self, catalogs: FilterCatalogs) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64,enum RDKix::FilterCatalogParams::FilterCatalogs)
        """
    def __setstate__(self, data: tuple) -> None:
        """
            C++ signature :
                void __setstate__(class boost::python::api::object,class boost::python::tuple)
        """
class FilterCatalogEntry(Boost.Python.instance):
    """
    FilterCatalogEntry
    A filter catalog entry is an entry in a filter catalog.
    Each filter is named and is used to flag a molecule usually for some
    undesirable property.
    
    For example, a PAINS (Pan Assay INterference) catalog entry be appear as
    follows:
    
    >>> from rdkix.Chem.FilterCatalog import *
    >>> params = FilterCatalogParams()
    >>> params.AddCatalog(FilterCatalogParams.FilterCatalogs.PAINS_A)
    True
    >>> catalog = FilterCatalog(params)
    >>> mol = Chem.MolFromSmiles('O=C(Cn1cnc2c1c(=O)n(C)c(=O)n2C)N/N=C/c1c(O)ccc2c1cccc2')
    >>> entry = catalog.GetFirstMatch(mol)
    >>> print (entry.GetProp('Scope'))
    PAINS filters (family A)
    >>> print (entry.GetDescription())
    hzone_phenol_A(479)
    
    
    """
    __instance_size__: typing.ClassVar[int] = 32
    @staticmethod
    def GetPropList(*args, **kwargs) -> ...:
        """
            C++ signature :
                class std::vector<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >,class std::allocator<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > > > GetPropList(class RDKix::FilterCatalogEntry {lvalue})
        """
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def ClearProp(self, key: str) -> None:
        """
            C++ signature :
                void ClearProp(class RDKix::FilterCatalogEntry {lvalue},class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >)
        """
    def GetDescription(self) -> str:
        """
            Get the description of the catalog entry
        
            C++ signature :
                class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > GetDescription(class RDKix::FilterCatalogEntry {lvalue})
        """
    def GetFilterMatches(self, mol: Mol) -> VectFilterMatch:
        """
            Retrieve the list of filters that match the molecule
        
            C++ signature :
                class std::vector<struct RDKix::FilterMatch,class std::allocator<struct RDKix::FilterMatch> > GetFilterMatches(class RDKix::FilterCatalogEntry {lvalue},class RDKix::ROMol)
        """
    def GetProp(self, key: str) -> str:
        """
            C++ signature :
                class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > GetProp(class RDKix::FilterCatalogEntry {lvalue},class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >)
        """
    def HasFilterMatch(self, mol: Mol) -> bool:
        """
            Returns True if the catalog entry contains filters that match the molecule
        
            C++ signature :
                bool HasFilterMatch(class RDKix::FilterCatalogEntry {lvalue},class RDKix::ROMol)
        """
    def IsValid(self) -> bool:
        """
            C++ signature :
                bool IsValid(class RDKix::FilterCatalogEntry {lvalue})
        """
    def Serialize(self) -> typing.Any:
        """
            C++ signature :
                class boost::python::api::object Serialize(class RDKix::FilterCatalogEntry)
        """
    def SetDescription(self, description: str) -> None:
        """
            Set the description of the catalog entry
        
            C++ signature :
                void SetDescription(class RDKix::FilterCatalogEntry {lvalue},class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >)
        """
    def SetProp(self, key: str, val: str) -> None:
        """
            C++ signature :
                void SetProp(class RDKix::FilterCatalogEntry {lvalue},class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >,class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >)
        """
    @typing.overload
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64)
        """
    @typing.overload
    def __init__(self, name: str, matcher: FilterMatcherBase) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64,class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >,class RDKix::FilterMatcherBase {lvalue})
        """
class FilterCatalogEntryList(Boost.Python.instance):
    __instance_size__: typing.ClassVar[int] = 48
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def __contains__(self, item: typing.Any) -> bool:
        """
            C++ signature :
                bool __contains__(class std::vector<class boost::shared_ptr<class RDKix::FilterCatalogEntry const >,class std::allocator<class boost::shared_ptr<class RDKix::FilterCatalogEntry const > > > {lvalue},struct _object * __ptr64)
        """
    def __delitem__(self, item: typing.Any) -> None:
        """
            C++ signature :
                void __delitem__(class std::vector<class boost::shared_ptr<class RDKix::FilterCatalogEntry const >,class std::allocator<class boost::shared_ptr<class RDKix::FilterCatalogEntry const > > > {lvalue},struct _object * __ptr64)
        """
    def __getitem__(self, item: typing.Any) -> typing.Any:
        """
            C++ signature :
                class boost::python::api::object __getitem__(struct boost::python::back_reference<class std::vector<class boost::shared_ptr<class RDKix::FilterCatalogEntry const >,class std::allocator<class boost::shared_ptr<class RDKix::FilterCatalogEntry const > > > & __ptr64>,struct _object * __ptr64)
        """
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64)
        """
    def __iter__(self) -> typing.Any:
        """
            C++ signature :
                struct boost::python::objects::iterator_range<struct boost::python::return_value_policy<struct boost::python::return_by_value,struct boost::python::default_call_policies>,class std::_Vector_iterator<class std::_Vector_val<struct std::_Simple_types<class boost::shared_ptr<class RDKix::FilterCatalogEntry const > > > > > __iter__(struct boost::python::back_reference<class std::vector<class boost::shared_ptr<class RDKix::FilterCatalogEntry const >,class std::allocator<class boost::shared_ptr<class RDKix::FilterCatalogEntry const > > > & __ptr64>)
        """
    def __len__(self) -> int:
        """
            C++ signature :
                unsigned __int64 __len__(class std::vector<class boost::shared_ptr<class RDKix::FilterCatalogEntry const >,class std::allocator<class boost::shared_ptr<class RDKix::FilterCatalogEntry const > > > {lvalue})
        """
    def __setitem__(self, item: typing.Any, value: typing.Any) -> None:
        """
            C++ signature :
                void __setitem__(class std::vector<class boost::shared_ptr<class RDKix::FilterCatalogEntry const >,class std::allocator<class boost::shared_ptr<class RDKix::FilterCatalogEntry const > > > {lvalue},struct _object * __ptr64,struct _object * __ptr64)
        """
    def append(self, item: typing.Any) -> None:
        """
            C++ signature :
                void append(class std::vector<class boost::shared_ptr<class RDKix::FilterCatalogEntry const >,class std::allocator<class boost::shared_ptr<class RDKix::FilterCatalogEntry const > > > {lvalue},class boost::python::api::object)
        """
    def extend(self, other: typing.Any) -> None:
        """
            C++ signature :
                void extend(class std::vector<class boost::shared_ptr<class RDKix::FilterCatalogEntry const >,class std::allocator<class boost::shared_ptr<class RDKix::FilterCatalogEntry const > > > {lvalue},class boost::python::api::object)
        """
class FilterCatalogListOfEntryList(Boost.Python.instance):
    __instance_size__: typing.ClassVar[int] = 48
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def __contains__(self, item: typing.Any) -> bool:
        """
            C++ signature :
                bool __contains__(class std::vector<class std::vector<class boost::shared_ptr<class RDKix::FilterCatalogEntry const >,class std::allocator<class boost::shared_ptr<class RDKix::FilterCatalogEntry const > > >,class std::allocator<class std::vector<class boost::shared_ptr<class RDKix::FilterCatalogEntry const >,class std::allocator<class boost::shared_ptr<class RDKix::FilterCatalogEntry const > > > > > {lvalue},struct _object * __ptr64)
        """
    def __delitem__(self, item: typing.Any) -> None:
        """
            C++ signature :
                void __delitem__(class std::vector<class std::vector<class boost::shared_ptr<class RDKix::FilterCatalogEntry const >,class std::allocator<class boost::shared_ptr<class RDKix::FilterCatalogEntry const > > >,class std::allocator<class std::vector<class boost::shared_ptr<class RDKix::FilterCatalogEntry const >,class std::allocator<class boost::shared_ptr<class RDKix::FilterCatalogEntry const > > > > > {lvalue},struct _object * __ptr64)
        """
    def __getitem__(self, item: typing.Any) -> typing.Any:
        """
            C++ signature :
                class boost::python::api::object __getitem__(struct boost::python::back_reference<class std::vector<class std::vector<class boost::shared_ptr<class RDKix::FilterCatalogEntry const >,class std::allocator<class boost::shared_ptr<class RDKix::FilterCatalogEntry const > > >,class std::allocator<class std::vector<class boost::shared_ptr<class RDKix::FilterCatalogEntry const >,class std::allocator<class boost::shared_ptr<class RDKix::FilterCatalogEntry const > > > > > & __ptr64>,struct _object * __ptr64)
        """
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64)
        """
    def __iter__(self) -> typing.Any:
        """
            C++ signature :
                struct boost::python::objects::iterator_range<struct boost::python::return_internal_reference<1,struct boost::python::default_call_policies>,class std::_Vector_iterator<class std::_Vector_val<struct std::_Simple_types<class std::vector<class boost::shared_ptr<class RDKix::FilterCatalogEntry const >,class std::allocator<class boost::shared_ptr<class RDKix::FilterCatalogEntry const > > > > > > > __iter__(struct boost::python::back_reference<class std::vector<class std::vector<class boost::shared_ptr<class RDKix::FilterCatalogEntry const >,class std::allocator<class boost::shared_ptr<class RDKix::FilterCatalogEntry const > > >,class std::allocator<class std::vector<class boost::shared_ptr<class RDKix::FilterCatalogEntry const >,class std::allocator<class boost::shared_ptr<class RDKix::FilterCatalogEntry const > > > > > & __ptr64>)
        """
    def __len__(self) -> int:
        """
            C++ signature :
                unsigned __int64 __len__(class std::vector<class std::vector<class boost::shared_ptr<class RDKix::FilterCatalogEntry const >,class std::allocator<class boost::shared_ptr<class RDKix::FilterCatalogEntry const > > >,class std::allocator<class std::vector<class boost::shared_ptr<class RDKix::FilterCatalogEntry const >,class std::allocator<class boost::shared_ptr<class RDKix::FilterCatalogEntry const > > > > > {lvalue})
        """
    def __setitem__(self, item: typing.Any, value: typing.Any) -> None:
        """
            C++ signature :
                void __setitem__(class std::vector<class std::vector<class boost::shared_ptr<class RDKix::FilterCatalogEntry const >,class std::allocator<class boost::shared_ptr<class RDKix::FilterCatalogEntry const > > >,class std::allocator<class std::vector<class boost::shared_ptr<class RDKix::FilterCatalogEntry const >,class std::allocator<class boost::shared_ptr<class RDKix::FilterCatalogEntry const > > > > > {lvalue},struct _object * __ptr64,struct _object * __ptr64)
        """
    def append(self, item: typing.Any) -> None:
        """
            C++ signature :
                void append(class std::vector<class std::vector<class boost::shared_ptr<class RDKix::FilterCatalogEntry const >,class std::allocator<class boost::shared_ptr<class RDKix::FilterCatalogEntry const > > >,class std::allocator<class std::vector<class boost::shared_ptr<class RDKix::FilterCatalogEntry const >,class std::allocator<class boost::shared_ptr<class RDKix::FilterCatalogEntry const > > > > > {lvalue},class boost::python::api::object)
        """
    def extend(self, other: typing.Any) -> None:
        """
            C++ signature :
                void extend(class std::vector<class std::vector<class boost::shared_ptr<class RDKix::FilterCatalogEntry const >,class std::allocator<class boost::shared_ptr<class RDKix::FilterCatalogEntry const > > >,class std::allocator<class std::vector<class boost::shared_ptr<class RDKix::FilterCatalogEntry const >,class std::allocator<class boost::shared_ptr<class RDKix::FilterCatalogEntry const > > > > > {lvalue},class boost::python::api::object)
        """
class FilterCatalogParams(Boost.Python.instance):
    class FilterCatalogs(Boost.Python.enum):
        ALL: typing.ClassVar[FilterCatalogs]  # value = rdkix.Chem.rdfiltercatalog.FilterCatalogs.ALL
        BRENK: typing.ClassVar[FilterCatalogs]  # value = rdkix.Chem.rdfiltercatalog.FilterCatalogs.BRENK
        CHEMBL: typing.ClassVar[FilterCatalogs]  # value = rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL
        CHEMBL_BMS: typing.ClassVar[FilterCatalogs]  # value = rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL_BMS
        CHEMBL_Dundee: typing.ClassVar[FilterCatalogs]  # value = rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL_Dundee
        CHEMBL_Glaxo: typing.ClassVar[FilterCatalogs]  # value = rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL_Glaxo
        CHEMBL_Inpharmatica: typing.ClassVar[FilterCatalogs]  # value = rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL_Inpharmatica
        CHEMBL_LINT: typing.ClassVar[FilterCatalogs]  # value = rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL_LINT
        CHEMBL_MLSMR: typing.ClassVar[FilterCatalogs]  # value = rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL_MLSMR
        CHEMBL_SureChEMBL: typing.ClassVar[FilterCatalogs]  # value = rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL_SureChEMBL
        NIH: typing.ClassVar[FilterCatalogs]  # value = rdkix.Chem.rdfiltercatalog.FilterCatalogs.NIH
        PAINS: typing.ClassVar[FilterCatalogs]  # value = rdkix.Chem.rdfiltercatalog.FilterCatalogs.PAINS
        PAINS_A: typing.ClassVar[FilterCatalogs]  # value = rdkix.Chem.rdfiltercatalog.FilterCatalogs.PAINS_A
        PAINS_B: typing.ClassVar[FilterCatalogs]  # value = rdkix.Chem.rdfiltercatalog.FilterCatalogs.PAINS_B
        PAINS_C: typing.ClassVar[FilterCatalogs]  # value = rdkix.Chem.rdfiltercatalog.FilterCatalogs.PAINS_C
        ZINC: typing.ClassVar[FilterCatalogs]  # value = rdkix.Chem.rdfiltercatalog.FilterCatalogs.ZINC
        __slots__: typing.ClassVar[tuple] = tuple()
        names: typing.ClassVar[dict]  # value = {'PAINS_A': rdkix.Chem.rdfiltercatalog.FilterCatalogs.PAINS_A, 'PAINS_B': rdkix.Chem.rdfiltercatalog.FilterCatalogs.PAINS_B, 'PAINS_C': rdkix.Chem.rdfiltercatalog.FilterCatalogs.PAINS_C, 'PAINS': rdkix.Chem.rdfiltercatalog.FilterCatalogs.PAINS, 'BRENK': rdkix.Chem.rdfiltercatalog.FilterCatalogs.BRENK, 'NIH': rdkix.Chem.rdfiltercatalog.FilterCatalogs.NIH, 'ZINC': rdkix.Chem.rdfiltercatalog.FilterCatalogs.ZINC, 'CHEMBL_Glaxo': rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL_Glaxo, 'CHEMBL_Dundee': rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL_Dundee, 'CHEMBL_BMS': rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL_BMS, 'CHEMBL_SureChEMBL': rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL_SureChEMBL, 'CHEMBL_MLSMR': rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL_MLSMR, 'CHEMBL_Inpharmatica': rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL_Inpharmatica, 'CHEMBL_LINT': rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL_LINT, 'CHEMBL': rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL, 'ALL': rdkix.Chem.rdfiltercatalog.FilterCatalogs.ALL}
        values: typing.ClassVar[dict]  # value = {2: rdkix.Chem.rdfiltercatalog.FilterCatalogs.PAINS_A, 4: rdkix.Chem.rdfiltercatalog.FilterCatalogs.PAINS_B, 8: rdkix.Chem.rdfiltercatalog.FilterCatalogs.PAINS_C, 14: rdkix.Chem.rdfiltercatalog.FilterCatalogs.PAINS, 16: rdkix.Chem.rdfiltercatalog.FilterCatalogs.BRENK, 32: rdkix.Chem.rdfiltercatalog.FilterCatalogs.NIH, 64: rdkix.Chem.rdfiltercatalog.FilterCatalogs.ZINC, 128: rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL_Glaxo, 256: rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL_Dundee, 512: rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL_BMS, 1024: rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL_SureChEMBL, 2048: rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL_MLSMR, 4096: rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL_Inpharmatica, 8192: rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL_LINT, 16256: rdkix.Chem.rdfiltercatalog.FilterCatalogs.CHEMBL, 16382: rdkix.Chem.rdfiltercatalog.FilterCatalogs.ALL}
    __instance_size__: typing.ClassVar[int] = 32
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def AddCatalog(self, catalogs: FilterCatalogs) -> bool:
        """
            C++ signature :
                bool AddCatalog(class RDKix::FilterCatalogParams {lvalue},enum RDKix::FilterCatalogParams::FilterCatalogs)
        """
    @typing.overload
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64)
        """
    @typing.overload
    def __init__(self, catalogs: FilterCatalogs) -> None:
        """
            Construct from a FilterCatalogs identifier (i.e. FilterCatalogParams.PAINS)
        
            C++ signature :
                void __init__(struct _object * __ptr64,enum RDKix::FilterCatalogParams::FilterCatalogs)
        """
class FilterHierarchyMatcher(FilterMatcherBase):
    """
    Hierarchical Filter
     basic constructors: 
       FilterHierarchyMatcher( matcher )
       where can be any FilterMatcherBase (SmartsMatcher, etc)
     FilterHierarchyMatcher's have children and can form matching
      trees.  then GetFilterMatches is called, the most specific (
      i.e. lowest node in a branch) is returned.
    
     n.b. A FilterHierarchicalMatcher of functional groups is returned
      by calling GetFunctionalGroupHierarchy()
    
    >>> from rdkix.Chem import MolFromSmiles
    >>> from rdkix.Chem.FilterCatalog import *
    >>> functionalGroups = GetFunctionalGroupHierarchy()
    >>> [match.filterMatch.GetName() 
    ...     for match in functionalGroups.GetFilterMatches(
    ...         MolFromSmiles('c1ccccc1Cl'))]
    ['Halogen.Aromatic', 'Halogen.NotFluorine.Aromatic']
    
    """
    __instance_size__: typing.ClassVar[int] = 32
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def AddChild(self, hierarchy: FilterHierarchyMatcher) -> FilterHierarchyMatcher:
        """
            Add a child node to this hierarchy.
        
            C++ signature :
                class boost::shared_ptr<class RDKix::FilterHierarchyMatcher> AddChild(class RDKix::FilterHierarchyMatcher {lvalue},class RDKix::FilterHierarchyMatcher)
        """
    def SetPattern(self, matcher: FilterMatcherBase) -> None:
        """
            Set the filtermatcher pattern for this node.  An empty node is considered a root node and passes along the matches to the children.
        
            C++ signature :
                void SetPattern(class RDKix::FilterHierarchyMatcher {lvalue},class RDKix::FilterMatcherBase)
        """
    @typing.overload
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64)
        """
    @typing.overload
    def __init__(self, matcher: FilterMatcherBase) -> None:
        """
            Construct from a filtermatcher
        
            C++ signature :
                void __init__(struct _object * __ptr64,class RDKix::FilterMatcherBase)
        """
class FilterMatch(Boost.Python.instance):
    """
    Object that holds the result of running FilterMatcherBase::GetMatches
    
     - filterMatch holds the FilterMatchBase that triggered the match
     - atomParis holds the [ (query_atom_idx, target_atom_idx) ] pairs for the matches.
    
    
    Note that some matches may not have atom pairs (especially matches that use FilterMatchOps.Not
    """
    __instance_size__: typing.ClassVar[int] = 40
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def __init__(self, filter: FilterMatcherBase, atomPairs: MatchTypeVect) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64,class boost::shared_ptr<class RDKix::FilterMatcherBase>,class std::vector<struct std::pair<int,int>,class std::allocator<struct std::pair<int,int> > >)
        """
    @property
    def atomPairs(*args, **kwargs):
        ...
    @property
    def filterMatch(*args, **kwargs):
        ...
class FilterMatcherBase(Boost.Python.instance):
    """
    Base class for matching molecules to filters.
    
     A FilterMatcherBase supplies the following API 
     - IsValid() returns True if the matcher is valid for use, False otherwise
     - HasMatch(mol) returns True if the molecule matches the filter
     - GetMatches(mol) -> [FilterMatch, FilterMatch] returns all the FilterMatch data
           that matches the molecule
    
    
    print( FilterMatcherBase ) will print user-friendly information about the filter
    Note that a FilterMatcherBase can be combined from may FilterMatcherBases
    This is why GetMatches can return multiple FilterMatcherBases.
    >>> from rdkix.Chem.FilterCatalog import *
    >>> carbon_matcher = SmartsMatcher('Carbon', '[#6]', 0, 1)
    >>> oxygen_matcher = SmartsMatcher('Oxygen', '[#8]', 0, 1)
    >>> co_matcher = FilterMatchOps.Or(carbon_matcher, oxygen_matcher)
    >>> mol = Chem.MolFromSmiles('C')
    >>> matches = co_matcher.GetMatches(mol)
    >>> len(matches)
    1
    >>> print(matches[0].filterMatch)
    Carbon
    
    """
    @staticmethod
    def __init__(*args, **kwargs):
        """
        Raises an exception
        This class cannot be instantiated from Python
        """
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def GetMatches(self, mol: Mol) -> VectFilterMatch:
        """
            Returns the list of matching subfilters mol matches any filter
        
            C++ signature :
                class std::vector<struct RDKix::FilterMatch,class std::allocator<struct RDKix::FilterMatch> > GetMatches(class RDKix::FilterMatcherBase {lvalue},class RDKix::ROMol)
        """
    def GetName(self) -> str:
        """
            C++ signature :
                class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > GetName(class RDKix::FilterMatcherBase {lvalue})
        """
    def HasMatch(self, mol: Mol) -> bool:
        """
            Returns True if mol matches the filter
        
            C++ signature :
                bool HasMatch(class RDKix::FilterMatcherBase {lvalue},class RDKix::ROMol)
        """
    def IsValid(self) -> bool:
        """
            Return True if the filter matcher is valid, False otherwise
        
            C++ signature :
                bool IsValid(class RDKix::FilterMatcherBase {lvalue})
        """
    def __str__(self) -> str:
        """
            C++ signature :
                class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > __str__(class RDKix::FilterMatcherBase {lvalue})
        """
class IntPair(Boost.Python.instance):
    __instance_size__: typing.ClassVar[int] = 32
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def __getitem__(self, idx: int) -> int:
        """
            C++ signature :
                int __getitem__(struct std::pair<int,int> {lvalue},unsigned __int64)
        """
    @typing.overload
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64)
        """
    @typing.overload
    def __init__(self, query: int, target: int) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64,int,int)
        """
    @property
    def query(*args, **kwargs):
        ...
    @query.setter
    def query(*args, **kwargs):
        ...
    @property
    def target(*args, **kwargs):
        ...
    @target.setter
    def target(*args, **kwargs):
        ...
class MolList(Boost.Python.instance):
    __instance_size__: typing.ClassVar[int] = 48
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def __contains__(self, item: typing.Any) -> bool:
        """
            C++ signature :
                bool __contains__(class std::vector<class RDKix::ROMol * __ptr64,class std::allocator<class RDKix::ROMol * __ptr64> > {lvalue},struct _object * __ptr64)
        """
    def __delitem__(self, item: typing.Any) -> None:
        """
            C++ signature :
                void __delitem__(class std::vector<class RDKix::ROMol * __ptr64,class std::allocator<class RDKix::ROMol * __ptr64> > {lvalue},struct _object * __ptr64)
        """
    def __getitem__(self, item: typing.Any) -> typing.Any:
        """
            C++ signature :
                class boost::python::api::object __getitem__(struct boost::python::back_reference<class std::vector<class RDKix::ROMol * __ptr64,class std::allocator<class RDKix::ROMol * __ptr64> > & __ptr64>,struct _object * __ptr64)
        """
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64)
        """
    def __iter__(self) -> typing.Any:
        """
            C++ signature :
                struct boost::python::objects::iterator_range<struct boost::python::return_value_policy<struct boost::python::return_by_value,struct boost::python::default_call_policies>,class std::_Vector_iterator<class std::_Vector_val<struct std::_Simple_types<class RDKix::ROMol * __ptr64> > > > __iter__(struct boost::python::back_reference<class std::vector<class RDKix::ROMol * __ptr64,class std::allocator<class RDKix::ROMol * __ptr64> > & __ptr64>)
        """
    def __len__(self) -> int:
        """
            C++ signature :
                unsigned __int64 __len__(class std::vector<class RDKix::ROMol * __ptr64,class std::allocator<class RDKix::ROMol * __ptr64> > {lvalue})
        """
    def __setitem__(self, item: typing.Any, value: typing.Any) -> None:
        """
            C++ signature :
                void __setitem__(class std::vector<class RDKix::ROMol * __ptr64,class std::allocator<class RDKix::ROMol * __ptr64> > {lvalue},struct _object * __ptr64,struct _object * __ptr64)
        """
    def append(self, item: typing.Any) -> None:
        """
            C++ signature :
                void append(class std::vector<class RDKix::ROMol * __ptr64,class std::allocator<class RDKix::ROMol * __ptr64> > {lvalue},class boost::python::api::object)
        """
    def extend(self, other: typing.Any) -> None:
        """
            C++ signature :
                void extend(class std::vector<class RDKix::ROMol * __ptr64,class std::allocator<class RDKix::ROMol * __ptr64> > {lvalue},class boost::python::api::object)
        """
class PythonFilterMatcher(FilterMatcherBase):
    __instance_size__: typing.ClassVar[int] = 96
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def __init__(self, callback: typing.Any) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64,struct _object * __ptr64)
        """
class SmartsMatcher(FilterMatcherBase):
    """
    Smarts Matcher Filter
     basic constructors: 
       SmartsMatcher( name, smarts_pattern, minCount=1, maxCount=UINT_MAX )
       SmartsMatcher( name, molecule, minCount=1, maxCount=UINT_MAX )
    
      note: If the supplied smarts pattern is not valid, the IsValid() function will
       return False
    >>> from rdkix.Chem.FilterCatalog import *
    >>> minCount, maxCount = 1,2
    >>> carbon_matcher = SmartsMatcher('Carbon', '[#6]', minCount, maxCount)
    >>> print (carbon_matcher.HasMatch(Chem.MolFromSmiles('CC')))
    True
    >>> print (carbon_matcher.HasMatch(Chem.MolFromSmiles('CCC')))
    False
    >>> carbon_matcher.SetMinCount(2)
    >>> print (carbon_matcher.HasMatch(Chem.MolFromSmiles('C')))
    False
    >>> carbon_matcher.SetMaxCount(3)
    >>> print (carbon_matcher.HasMatch(Chem.MolFromSmiles('CCC')))
    True
    
    """
    __instance_size__: typing.ClassVar[int] = 104
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def GetMaxCount(self) -> int:
        """
            Get the maximum times pattern can appear for the filter to match
        
            C++ signature :
                unsigned int GetMaxCount(class RDKix::SmartsMatcher {lvalue})
        """
    def GetMinCount(self) -> int:
        """
            Get the minimum times pattern must appear for the filter to match
        
            C++ signature :
                unsigned int GetMinCount(class RDKix::SmartsMatcher {lvalue})
        """
    def GetPattern(self) -> rdkix.Chem.Mol:
        """
            C++ signature :
                class boost::shared_ptr<class RDKix::ROMol> GetPattern(class RDKix::SmartsMatcher {lvalue})
        """
    def IsValid(self) -> bool:
        """
            Returns True if the SmartsMatcher is valid
        
            C++ signature :
                bool IsValid(class RDKix::SmartsMatcher {lvalue})
        """
    def SetMaxCount(self, count: int) -> None:
        """
            Set the maximum times pattern can appear for the filter to match
        
            C++ signature :
                void SetMaxCount(class RDKix::SmartsMatcher {lvalue},unsigned int)
        """
    def SetMinCount(self, count: int) -> None:
        """
            Set the minimum times pattern must appear to match
        
            C++ signature :
                void SetMinCount(class RDKix::SmartsMatcher {lvalue},unsigned int)
        """
    @typing.overload
    def SetPattern(self, pat: Mol) -> None:
        """
            Set the pattern molecule for the SmartsMatcher
        
            C++ signature :
                void SetPattern(class RDKix::SmartsMatcher {lvalue},class RDKix::ROMol)
        """
    @typing.overload
    def SetPattern(self, pat: str) -> None:
        """
            Set the smarts pattern for the Smarts Matcher (warning: MinimumCount is not reset)
        
            C++ signature :
                void SetPattern(class RDKix::SmartsMatcher {lvalue},class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >)
        """
    @typing.overload
    def __init__(self, name: str) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64,class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >)
        """
    @typing.overload
    def __init__(self, rhs: Mol) -> None:
        """
            Construct from a molecule
        
            C++ signature :
                void __init__(struct _object * __ptr64,class RDKix::ROMol)
        """
    @typing.overload
    def __init__(self, name: str, mol: Mol, minCount: int = 1, maxCount: int = 4294967295) -> None:
        """
            Construct from a name, molecule, minimum and maximum count
        
            C++ signature :
                void __init__(struct _object * __ptr64,class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >,class RDKix::ROMol [,unsigned int=1 [,unsigned int=4294967295]])
        """
    @typing.overload
    def __init__(self, name: str, smarts: str, minCount: int = 1, maxCount: int = 4294967295) -> None:
        """
            Construct from a name,smarts pattern, minimum and maximum count
        
            C++ signature :
                void __init__(struct _object * __ptr64,class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >,class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > [,unsigned int=1 [,unsigned int=4294967295]])
        """
class VectFilterMatch(Boost.Python.instance):
    __instance_size__: typing.ClassVar[int] = 48
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def __contains__(self, item: typing.Any) -> bool:
        """
            C++ signature :
                bool __contains__(class std::vector<struct RDKix::FilterMatch,class std::allocator<struct RDKix::FilterMatch> > {lvalue},struct _object * __ptr64)
        """
    def __delitem__(self, item: typing.Any) -> None:
        """
            C++ signature :
                void __delitem__(class std::vector<struct RDKix::FilterMatch,class std::allocator<struct RDKix::FilterMatch> > {lvalue},struct _object * __ptr64)
        """
    def __getitem__(self, item: typing.Any) -> typing.Any:
        """
            C++ signature :
                class boost::python::api::object __getitem__(struct boost::python::back_reference<class std::vector<struct RDKix::FilterMatch,class std::allocator<struct RDKix::FilterMatch> > & __ptr64>,struct _object * __ptr64)
        """
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64)
        """
    def __iter__(self) -> typing.Any:
        """
            C++ signature :
                struct boost::python::objects::iterator_range<struct boost::python::return_internal_reference<1,struct boost::python::default_call_policies>,class std::_Vector_iterator<class std::_Vector_val<struct std::_Simple_types<struct RDKix::FilterMatch> > > > __iter__(struct boost::python::back_reference<class std::vector<struct RDKix::FilterMatch,class std::allocator<struct RDKix::FilterMatch> > & __ptr64>)
        """
    def __len__(self) -> int:
        """
            C++ signature :
                unsigned __int64 __len__(class std::vector<struct RDKix::FilterMatch,class std::allocator<struct RDKix::FilterMatch> > {lvalue})
        """
    def __setitem__(self, item: typing.Any, value: typing.Any) -> None:
        """
            C++ signature :
                void __setitem__(class std::vector<struct RDKix::FilterMatch,class std::allocator<struct RDKix::FilterMatch> > {lvalue},struct _object * __ptr64,struct _object * __ptr64)
        """
    def append(self, item: typing.Any) -> None:
        """
            C++ signature :
                void append(class std::vector<struct RDKix::FilterMatch,class std::allocator<struct RDKix::FilterMatch> > {lvalue},class boost::python::api::object)
        """
    def extend(self, other: typing.Any) -> None:
        """
            C++ signature :
                void extend(class std::vector<struct RDKix::FilterMatch,class std::allocator<struct RDKix::FilterMatch> > {lvalue},class boost::python::api::object)
        """
def FilterCatalogCanSerialize() -> bool:
    """
        Returns True if the FilterCatalog is serializable (requires boost serialization
    
        C++ signature :
            bool FilterCatalogCanSerialize()
    """
def GetFlattenedFunctionalGroupHierarchy(normalized: bool = False) -> dict:
    """
        Returns the flattened functional group hierarchy as a dictionary  of name:ROMOL_SPTR substructure items
    
        C++ signature :
            class boost::python::dict GetFlattenedFunctionalGroupHierarchy([ bool=False])
    """
def GetFunctionalGroupHierarchy() -> FilterCatalog:
    """
        Returns the functional group hierarchy filter catalog
    
        C++ signature :
            class RDKix::FilterCatalog GetFunctionalGroupHierarchy()
    """
def RunFilterCatalog(filterCatalog: FilterCatalog, smiles: ..., structstd: ..., classstd: ..., numThreads: int = 1) -> FilterCatalogListOfEntryList:
    """
        Run the filter catalog on the input list of smiles strings.
        Use numThreads=0 to use all available processors. Returns a vector of vectors.  For each input smiles, a vector of FilterCatalogEntry objects are returned for each matched filter.  If a molecule matches no filter, the vector will be empty. If a smiles string can't be parsed, a 'Bad smiles' entry is returned.
    
        C++ signature :
            class std::vector<class std::vector<class boost::shared_ptr<class RDKix::FilterCatalogEntry const >,class std::allocator<class boost::shared_ptr<class RDKix::FilterCatalogEntry const > > >,class std::allocator<class std::vector<class boost::shared_ptr<class RDKix::FilterCatalogEntry const >,class std::allocator<class boost::shared_ptr<class RDKix::FilterCatalogEntry const > > > > > RunFilterCatalog(class RDKix::FilterCatalog,class std::vector<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >,class std::allocator<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > > > [,int=1])
    """
