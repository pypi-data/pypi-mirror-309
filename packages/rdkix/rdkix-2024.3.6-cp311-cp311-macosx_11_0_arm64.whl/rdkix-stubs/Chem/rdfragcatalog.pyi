from __future__ import annotations
import rdkix.Chem
import typing
__all__ = ['FragCatGenerator', 'FragCatParams', 'FragCatalog', 'FragFPGenerator']
class FragCatGenerator(Boost.Python.instance):
    __instance_size__: typing.ClassVar[int] = 32
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def AddFragsFromMol(self, mol: Mol, fcat: FragCatalog) -> int:
        """
            C++ signature :
                unsigned int AddFragsFromMol(RDKix::FragCatGenerator {lvalue},RDKix::ROMol,RDCatalog::HierarchCatalog<RDKix::FragCatalogEntry, RDKix::FragCatParams, int>*)
        """
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(_object*)
        """
class FragCatParams(Boost.Python.instance):
    __instance_size__: typing.ClassVar[int] = 96
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def GetFuncGroup(self, fid: int) -> rdkix.Chem.Mol:
        """
            C++ signature :
                RDKix::ROMol const* GetFuncGroup(RDKix::FragCatParams {lvalue},int)
        """
    def GetLowerFragLength(self) -> int:
        """
            C++ signature :
                unsigned int GetLowerFragLength(RDKix::FragCatParams {lvalue})
        """
    def GetNumFuncGroups(self) -> int:
        """
            C++ signature :
                unsigned int GetNumFuncGroups(RDKix::FragCatParams {lvalue})
        """
    def GetTolerance(self) -> float:
        """
            C++ signature :
                double GetTolerance(RDKix::FragCatParams {lvalue})
        """
    def GetTypeString(self) -> str:
        """
            C++ signature :
                std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> GetTypeString(RDKix::FragCatParams {lvalue})
        """
    def GetUpperFragLength(self) -> int:
        """
            C++ signature :
                unsigned int GetUpperFragLength(RDKix::FragCatParams {lvalue})
        """
    def Serialize(self) -> str:
        """
            C++ signature :
                std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> Serialize(RDKix::FragCatParams {lvalue})
        """
    def __init__(self, lLen: int, uLen: int, fgroupFilename: str, tol: float = 1e-08) -> None:
        """
            C++ signature :
                void __init__(_object*,int,int,std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> [,double=1e-08])
        """
class FragCatalog(Boost.Python.instance):
    __getstate_manages_dict__: typing.ClassVar[bool] = True
    __instance_size__: typing.ClassVar[int] = 128
    __safe_for_unpickling__: typing.ClassVar[bool] = True
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def GetBitDescription(self, idx: int) -> str:
        """
            C++ signature :
                std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> GetBitDescription(RDCatalog::HierarchCatalog<RDKix::FragCatalogEntry, RDKix::FragCatParams, int> const*,unsigned int)
        """
    def GetBitDiscrims(self, idx: int) -> typing.Sequence[double]:
        """
            C++ signature :
                std::__1::vector<double, std::__1::allocator<double>> GetBitDiscrims(RDCatalog::HierarchCatalog<RDKix::FragCatalogEntry, RDKix::FragCatParams, int> const*,unsigned int)
        """
    def GetBitEntryId(self, idx: int) -> int:
        """
            C++ signature :
                unsigned int GetBitEntryId(RDCatalog::HierarchCatalog<RDKix::FragCatalogEntry, RDKix::FragCatParams, int> const*,unsigned int)
        """
    def GetBitFuncGroupIds(self, idx: int) -> typing.Sequence[int]:
        """
            C++ signature :
                std::__1::vector<int, std::__1::allocator<int>> GetBitFuncGroupIds(RDCatalog::HierarchCatalog<RDKix::FragCatalogEntry, RDKix::FragCatParams, int> const*,unsigned int)
        """
    def GetBitOrder(self, idx: int) -> int:
        """
            C++ signature :
                unsigned int GetBitOrder(RDCatalog::HierarchCatalog<RDKix::FragCatalogEntry, RDKix::FragCatParams, int> const*,unsigned int)
        """
    def GetCatalogParams(self) -> FragCatParams:
        """
            C++ signature :
                RDKix::FragCatParams* GetCatalogParams(RDCatalog::HierarchCatalog<RDKix::FragCatalogEntry, RDKix::FragCatParams, int> {lvalue})
        """
    def GetEntryBitId(self, idx: int) -> int:
        """
            C++ signature :
                unsigned int GetEntryBitId(RDCatalog::HierarchCatalog<RDKix::FragCatalogEntry, RDKix::FragCatParams, int> const*,unsigned int)
        """
    def GetEntryDescription(self, idx: int) -> str:
        """
            C++ signature :
                std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> GetEntryDescription(RDCatalog::HierarchCatalog<RDKix::FragCatalogEntry, RDKix::FragCatParams, int> const*,unsigned int)
        """
    def GetEntryDownIds(self, idx: int) -> typing.Sequence[int]:
        """
            C++ signature :
                std::__1::vector<int, std::__1::allocator<int>> GetEntryDownIds(RDCatalog::HierarchCatalog<RDKix::FragCatalogEntry, RDKix::FragCatParams, int> const*,unsigned int)
        """
    def GetEntryFuncGroupIds(self, idx: int) -> typing.Sequence[int]:
        """
            C++ signature :
                std::__1::vector<int, std::__1::allocator<int>> GetEntryFuncGroupIds(RDCatalog::HierarchCatalog<RDKix::FragCatalogEntry, RDKix::FragCatParams, int> const*,unsigned int)
        """
    def GetEntryOrder(self, idx: int) -> int:
        """
            C++ signature :
                unsigned int GetEntryOrder(RDCatalog::HierarchCatalog<RDKix::FragCatalogEntry, RDKix::FragCatParams, int> const*,unsigned int)
        """
    def GetFPLength(self) -> int:
        """
            C++ signature :
                unsigned int GetFPLength(RDCatalog::HierarchCatalog<RDKix::FragCatalogEntry, RDKix::FragCatParams, int> {lvalue})
        """
    def GetNumEntries(self) -> int:
        """
            C++ signature :
                unsigned int GetNumEntries(RDCatalog::HierarchCatalog<RDKix::FragCatalogEntry, RDKix::FragCatParams, int> {lvalue})
        """
    def Serialize(self) -> str:
        """
            C++ signature :
                std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> Serialize(RDCatalog::HierarchCatalog<RDKix::FragCatalogEntry, RDKix::FragCatParams, int> {lvalue})
        """
    def __getinitargs__(self) -> tuple:
        """
            C++ signature :
                boost::python::tuple __getinitargs__(RDCatalog::HierarchCatalog<RDKix::FragCatalogEntry, RDKix::FragCatParams, int>)
        """
    def __getstate__(self) -> tuple:
        """
            C++ signature :
                boost::python::tuple __getstate__(boost::python::api::object)
        """
    @typing.overload
    def __init__(self, params: FragCatParams) -> None:
        """
            C++ signature :
                void __init__(_object*,RDKix::FragCatParams*)
        """
    @typing.overload
    def __init__(self, pickle: str) -> None:
        """
            C++ signature :
                void __init__(_object*,std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>)
        """
    def __setstate__(self, data: tuple) -> None:
        """
            C++ signature :
                void __setstate__(boost::python::api::object,boost::python::tuple)
        """
class FragFPGenerator(Boost.Python.instance):
    __instance_size__: typing.ClassVar[int] = 32
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def GetFPForMol(self, mol: Mol, fcat: FragCatalog) -> ExplicitBitVect:
        """
            C++ signature :
                ExplicitBitVect* GetFPForMol(RDKix::FragFPGenerator {lvalue},RDKix::ROMol,RDCatalog::HierarchCatalog<RDKix::FragCatalogEntry, RDKix::FragCatParams, int>)
        """
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(_object*)
        """
