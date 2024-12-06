from __future__ import annotations
import typing
__all__ = ['MHFPEncoder']
class MHFPEncoder(Boost.Python.instance):
    __instance_size__: typing.ClassVar[int] = 96
    @staticmethod
    def CreateShinglingFromMol(*args, **kwargs) -> ...:
        """
            Creates a shingling (a list of circular n-grams / substructures) from a RDKix Mol instance.
        
            C++ signature :
                class std::vector<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >,class std::allocator<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > > > CreateShinglingFromMol(class RDKix::MHFPFingerprints::MHFPEncoder * __ptr64,class RDKix::ROMol [,unsigned char=3 [,bool=True [,bool=False [,bool=False [,unsigned char=1]]]]])
        """
    @staticmethod
    def CreateShinglingFromSmiles(*args, **kwargs) -> ...:
        """
            Creates a shingling (a list of circular n-grams / substructures) from a SMILES string.
        
            C++ signature :
                class std::vector<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >,class std::allocator<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > > > CreateShinglingFromSmiles(class RDKix::MHFPFingerprints::MHFPEncoder * __ptr64,class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > [,unsigned char=3 [,bool=True [,bool=False [,bool=False [,unsigned char=1]]]]])
        """
    @staticmethod
    def Distance(a: _vectunsignedint, b: _vectunsignedint) -> float:
        """
            C++ signature :
                double Distance(class std::vector<unsigned int,class std::allocator<unsigned int> >,class std::vector<unsigned int,class std::allocator<unsigned int> >)
        """
    @staticmethod
    def EncodeMol(*args, **kwargs) -> ...:
        """
            Creates a MHFP vector from an RDKix Mol instance.
        
            C++ signature :
                class std::vector<unsigned int,class std::allocator<unsigned int> > EncodeMol(class RDKix::MHFPFingerprints::MHFPEncoder * __ptr64,class RDKix::ROMol [,unsigned char=3 [,bool=True [,bool=False [,bool=False [,unsigned char=1]]]]])
        """
    @staticmethod
    def EncodeMolsBulk(*args, **kwargs) -> ...:
        """
            Creates a MHFP vector from a list of RDKix Mol instances.
        
            C++ signature :
                class std::vector<class std::vector<unsigned int,class std::allocator<unsigned int> >,class std::allocator<class std::vector<unsigned int,class std::allocator<unsigned int> > > > EncodeMolsBulk(class RDKix::MHFPFingerprints::MHFPEncoder * __ptr64,class boost::python::list {lvalue} [,unsigned char=3 [,bool=True [,bool=False [,bool=False [,unsigned char=1]]]]])
        """
    @staticmethod
    def EncodeSmiles(*args, **kwargs) -> ...:
        """
            Creates a MHFP vector from a SMILES string.
        
            C++ signature :
                class std::vector<unsigned int,class std::allocator<unsigned int> > EncodeSmiles(class RDKix::MHFPFingerprints::MHFPEncoder * __ptr64,class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > [,unsigned char=3 [,bool=True [,bool=False [,bool=False [,unsigned char=1]]]]])
        """
    @staticmethod
    def EncodeSmilesBulk(*args, **kwargs) -> ...:
        """
            Creates a MHFP vector from a list of SMILES strings.
        
            C++ signature :
                class std::vector<class std::vector<unsigned int,class std::allocator<unsigned int> >,class std::allocator<class std::vector<unsigned int,class std::allocator<unsigned int> > > > EncodeSmilesBulk(class RDKix::MHFPFingerprints::MHFPEncoder * __ptr64,class boost::python::list {lvalue} [,unsigned char=3 [,bool=True [,bool=False [,bool=False [,unsigned char=1]]]]])
        """
    @staticmethod
    def FromArray(*args, **kwargs) -> ...:
        """
            Creates a MHFP vector from a list of unsigned integers.
        
            C++ signature :
                class std::vector<unsigned int,class std::allocator<unsigned int> > FromArray(class RDKix::MHFPFingerprints::MHFPEncoder * __ptr64,class boost::python::list {lvalue})
        """
    @staticmethod
    def FromStringArray(*args, **kwargs) -> ...:
        """
            Creates a MHFP vector from a list of arbitrary strings.
        
            C++ signature :
                class std::vector<unsigned int,class std::allocator<unsigned int> > FromStringArray(class RDKix::MHFPFingerprints::MHFPEncoder * __ptr64,class boost::python::list {lvalue})
        """
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def EncodeSECFPMol(self, smiles: Mol, radius: int = 3, rings: bool = True, isomeric: bool = False, kekulize: bool = False, min_radius: int = 1, length: int = 2048) -> ExplicitBitVect:
        """
            Creates a SECFP binary vector from an RDKix Mol instance.
        
            C++ signature :
                class ExplicitBitVect EncodeSECFPMol(class RDKix::MHFPFingerprints::MHFPEncoder * __ptr64,class RDKix::ROMol [,unsigned char=3 [,bool=True [,bool=False [,bool=False [,unsigned char=1 [,unsigned __int64=2048]]]]]])
        """
    def EncodeSECFPMolsBulk(self, smiles: list, radius: int = 3, rings: bool = True, isomeric: bool = False, kekulize: bool = False, min_radius: int = 1, length: int = 2048) -> typing.Any:
        """
            Creates a SECFP binary vector from a list of RDKix Mol instances.
        
            C++ signature :
                class std::vector<class ExplicitBitVect,class std::allocator<class ExplicitBitVect> > EncodeSECFPMolsBulk(class RDKix::MHFPFingerprints::MHFPEncoder * __ptr64,class boost::python::list {lvalue} [,unsigned char=3 [,bool=True [,bool=False [,bool=False [,unsigned char=1 [,unsigned __int64=2048]]]]]])
        """
    def EncodeSECFPSmiles(self, smiles: str, radius: int = 3, rings: bool = True, isomeric: bool = False, kekulize: bool = False, min_radius: int = 1, length: int = 2048) -> ExplicitBitVect:
        """
            Creates a SECFP binary vector from a SMILES string.
        
            C++ signature :
                class ExplicitBitVect EncodeSECFPSmiles(class RDKix::MHFPFingerprints::MHFPEncoder * __ptr64,class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > [,unsigned char=3 [,bool=True [,bool=False [,bool=False [,unsigned char=1 [,unsigned __int64=2048]]]]]])
        """
    def EncodeSECFPSmilesBulk(self, smiles: list, radius: int = 3, rings: bool = True, isomeric: bool = False, kekulize: bool = False, min_radius: int = 1, length: int = 2048) -> typing.Any:
        """
            Creates a SECFP binary vector from a list of SMILES strings.
        
            C++ signature :
                class std::vector<class ExplicitBitVect,class std::allocator<class ExplicitBitVect> > EncodeSECFPSmilesBulk(class RDKix::MHFPFingerprints::MHFPEncoder * __ptr64,class boost::python::list {lvalue} [,unsigned char=3 [,bool=True [,bool=False [,bool=False [,unsigned char=1 [,unsigned __int64=2048]]]]]])
        """
    def __init__(self, n_permutations: int, seed: int) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64 [,unsigned int [,unsigned int]])
        """
