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
                class std::vector<unsigned __int64,class std::allocator<unsigned __int64> > GetModifiedAtoms(class RDKix::TautomerQuery {lvalue})
        """
    def GetModifiedBonds(self) -> UnsignedLong_Vect:
        """
            C++ signature :
                class std::vector<unsigned __int64,class std::allocator<unsigned __int64> > GetModifiedBonds(class RDKix::TautomerQuery {lvalue})
        """
    @typing.overload
    def GetSubstructMatch(self, target: Mol, useChirality: bool = False, useQueryQueryMatches: bool = False) -> typing.Any:
        """
            C++ signature :
                struct _object * __ptr64 GetSubstructMatch(class RDKix::TautomerQuery,class RDKix::ROMol [,bool=False [,bool=False]])
        """
    @typing.overload
    def GetSubstructMatch(self, target: Mol, params: SubstructMatchParameters) -> typing.Any:
        """
            C++ signature :
                struct _object * __ptr64 GetSubstructMatch(class RDKix::TautomerQuery,class RDKix::ROMol,struct RDKix::SubstructMatchParameters)
        """
    @typing.overload
    def GetSubstructMatches(self, target: Mol, uniquify: bool = True, useChirality: bool = False, useQueryQueryMatches: bool = False, maxMatches: int = 1000) -> typing.Any:
        """
            C++ signature :
                struct _object * __ptr64 GetSubstructMatches(class RDKix::TautomerQuery,class RDKix::ROMol [,bool=True [,bool=False [,bool=False [,unsigned int=1000]]]])
        """
    @typing.overload
    def GetSubstructMatches(self, target: Mol, params: SubstructMatchParameters) -> typing.Any:
        """
            C++ signature :
                struct _object * __ptr64 GetSubstructMatches(class RDKix::TautomerQuery,class RDKix::ROMol,struct RDKix::SubstructMatchParameters)
        """
    @typing.overload
    def GetSubstructMatchesWithTautomers(self, target: Mol, uniquify: bool = True, useChirality: bool = False, useQueryQueryMatches: bool = False, maxMatches: int = 1000) -> typing.Any:
        """
            C++ signature :
                struct _object * __ptr64 GetSubstructMatchesWithTautomers(class RDKix::TautomerQuery,class RDKix::ROMol [,bool=True [,bool=False [,bool=False [,unsigned int=1000]]]])
        """
    @typing.overload
    def GetSubstructMatchesWithTautomers(self, target: Mol, params: SubstructMatchParameters) -> typing.Any:
        """
            C++ signature :
                struct _object * __ptr64 GetSubstructMatchesWithTautomers(class RDKix::TautomerQuery,class RDKix::ROMol,struct RDKix::SubstructMatchParameters)
        """
    def GetTautomers(self) -> typing.Any:
        """
            C++ signature :
                struct _object * __ptr64 GetTautomers(class RDKix::TautomerQuery)
        """
    def GetTemplateMolecule(self) -> rdkix.Chem.Mol:
        """
            C++ signature :
                class RDKix::ROMol GetTemplateMolecule(class RDKix::TautomerQuery {lvalue})
        """
    @typing.overload
    def IsSubstructOf(self, target: Mol, recursionPossible: bool = True, useChirality: bool = False, useQueryQueryMatches: bool = False) -> bool:
        """
            C++ signature :
                bool IsSubstructOf(class RDKix::TautomerQuery,class RDKix::ROMol [,bool=True [,bool=False [,bool=False]]])
        """
    @typing.overload
    def IsSubstructOf(self, target: Mol, params: SubstructMatchParameters) -> bool:
        """
            C++ signature :
                bool IsSubstructOf(class RDKix::TautomerQuery,class RDKix::ROMol,struct RDKix::SubstructMatchParameters)
        """
    def PatternFingerprintTemplate(self, fingerprintSize: int = 2048) -> ExplicitBitVect:
        """
            C++ signature :
                class ExplicitBitVect * __ptr64 PatternFingerprintTemplate(class RDKix::TautomerQuery {lvalue} [,unsigned int=2048])
        """
    def ToBinary(self) -> typing.Any:
        """
            C++ signature :
                class boost::python::api::object ToBinary(class RDKix::TautomerQuery)
        """
    def __getinitargs__(self) -> tuple:
        """
            C++ signature :
                class boost::python::tuple __getinitargs__(class RDKix::TautomerQuery)
        """
    def __getstate__(self) -> tuple:
        """
            C++ signature :
                class boost::python::tuple __getstate__(class boost::python::api::object)
        """
    @typing.overload
    def __init__(self, arg1: Mol) -> typing.Any:
        """
            C++ signature :
                void * __ptr64 __init__(class boost::python::api::object,class RDKix::ROMol)
        """
    @typing.overload
    def __init__(self, arg1: Mol, arg2: str) -> typing.Any:
        """
            C++ signature :
                void * __ptr64 __init__(class boost::python::api::object,class RDKix::ROMol,class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >)
        """
    @typing.overload
    def __init__(self, pickle: str) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64,class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >)
        """
    def __setstate__(self, data: tuple) -> None:
        """
            C++ signature :
                void __setstate__(class boost::python::api::object,class boost::python::tuple)
        """
def PatternFingerprintTautomerTarget(target: Mol, fingerprintSize: int = 2048) -> ExplicitBitVect:
    """
        C++ signature :
            class ExplicitBitVect * __ptr64 PatternFingerprintTautomerTarget(class RDKix::ROMol [,unsigned int=2048])
    """
def TautomerQueryCanSerialize() -> bool:
    """
        Returns True if the TautomerQuery is serializable (requires that the RDKix was built with boost::serialization)
    
        C++ signature :
            bool TautomerQueryCanSerialize()
    """
