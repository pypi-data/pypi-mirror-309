from __future__ import annotations
import rdkix.Chem
import typing
__all__ = ['PatternFingerprintTautomerTarget', 'TautomerQuery', 'TautomerQueryCanSerialize']
class TautomerQuery(Boost.Python.instance):
    """
    The Tautomer Query Class.
      Creates a query that enables structure search accounting for matching of
      Tautomeric forms
    """
    __getstate_manages_dict__: typing.ClassVar[bool] = True
    __safe_for_unpickling__: typing.ClassVar[bool] = True
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def GetModifiedAtoms(self) -> UnsignedLong_Vect:
        """
            C++ signature :
                std::__1::vector<unsigned long, std::__1::allocator<unsigned long>> GetModifiedAtoms(RDKix::TautomerQuery {lvalue})
        """
    def GetModifiedBonds(self) -> UnsignedLong_Vect:
        """
            C++ signature :
                std::__1::vector<unsigned long, std::__1::allocator<unsigned long>> GetModifiedBonds(RDKix::TautomerQuery {lvalue})
        """
    @typing.overload
    def GetSubstructMatch(self, target: Mol, useChirality: bool = False, useQueryQueryMatches: bool = False) -> typing.Any:
        """
            C++ signature :
                _object* GetSubstructMatch(RDKix::TautomerQuery,RDKix::ROMol [,bool=False [,bool=False]])
        """
    @typing.overload
    def GetSubstructMatch(self, target: Mol, params: SubstructMatchParameters) -> typing.Any:
        """
            C++ signature :
                _object* GetSubstructMatch(RDKix::TautomerQuery,RDKix::ROMol,RDKix::SubstructMatchParameters)
        """
    @typing.overload
    def GetSubstructMatches(self, target: Mol, uniquify: bool = True, useChirality: bool = False, useQueryQueryMatches: bool = False, maxMatches: int = 1000) -> typing.Any:
        """
            C++ signature :
                _object* GetSubstructMatches(RDKix::TautomerQuery,RDKix::ROMol [,bool=True [,bool=False [,bool=False [,unsigned int=1000]]]])
        """
    @typing.overload
    def GetSubstructMatches(self, target: Mol, params: SubstructMatchParameters) -> typing.Any:
        """
            C++ signature :
                _object* GetSubstructMatches(RDKix::TautomerQuery,RDKix::ROMol,RDKix::SubstructMatchParameters)
        """
    @typing.overload
    def GetSubstructMatchesWithTautomers(self, target: Mol, uniquify: bool = True, useChirality: bool = False, useQueryQueryMatches: bool = False, maxMatches: int = 1000) -> typing.Any:
        """
            C++ signature :
                _object* GetSubstructMatchesWithTautomers(RDKix::TautomerQuery,RDKix::ROMol [,bool=True [,bool=False [,bool=False [,unsigned int=1000]]]])
        """
    @typing.overload
    def GetSubstructMatchesWithTautomers(self, target: Mol, params: SubstructMatchParameters) -> typing.Any:
        """
            C++ signature :
                _object* GetSubstructMatchesWithTautomers(RDKix::TautomerQuery,RDKix::ROMol,RDKix::SubstructMatchParameters)
        """
    def GetTautomers(self) -> typing.Any:
        """
            C++ signature :
                _object* GetTautomers(RDKix::TautomerQuery)
        """
    def GetTemplateMolecule(self) -> rdkix.Chem.Mol:
        """
            C++ signature :
                RDKix::ROMol GetTemplateMolecule(RDKix::TautomerQuery {lvalue})
        """
    @typing.overload
    def IsSubstructOf(self, target: Mol, recursionPossible: bool = True, useChirality: bool = False, useQueryQueryMatches: bool = False) -> bool:
        """
            C++ signature :
                bool IsSubstructOf(RDKix::TautomerQuery,RDKix::ROMol [,bool=True [,bool=False [,bool=False]]])
        """
    @typing.overload
    def IsSubstructOf(self, target: Mol, params: SubstructMatchParameters) -> bool:
        """
            C++ signature :
                bool IsSubstructOf(RDKix::TautomerQuery,RDKix::ROMol,RDKix::SubstructMatchParameters)
        """
    def PatternFingerprintTemplate(self, fingerprintSize: int = 2048) -> ExplicitBitVect:
        """
            C++ signature :
                ExplicitBitVect* PatternFingerprintTemplate(RDKix::TautomerQuery {lvalue} [,unsigned int=2048])
        """
    def ToBinary(self) -> typing.Any:
        """
            C++ signature :
                boost::python::api::object ToBinary(RDKix::TautomerQuery)
        """
    def __getinitargs__(self) -> tuple:
        """
            C++ signature :
                boost::python::tuple __getinitargs__(RDKix::TautomerQuery)
        """
    def __getstate__(self) -> tuple:
        """
            C++ signature :
                boost::python::tuple __getstate__(boost::python::api::object)
        """
    @typing.overload
    def __init__(self, arg1: Mol) -> typing.Any:
        """
            C++ signature :
                void* __init__(boost::python::api::object,RDKix::ROMol)
        """
    @typing.overload
    def __init__(self, arg1: Mol, arg2: str) -> typing.Any:
        """
            C++ signature :
                void* __init__(boost::python::api::object,RDKix::ROMol,std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>)
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
def PatternFingerprintTautomerTarget(target: Mol, fingerprintSize: int = 2048) -> ExplicitBitVect:
    """
        C++ signature :
            ExplicitBitVect* PatternFingerprintTautomerTarget(RDKix::ROMol [,unsigned int=2048])
    """
def TautomerQueryCanSerialize() -> bool:
    """
        Returns True if the TautomerQuery is serializable (requires that the RDKix was built with boost::serialization)
    
        C++ signature :
            bool TautomerQueryCanSerialize()
    """
