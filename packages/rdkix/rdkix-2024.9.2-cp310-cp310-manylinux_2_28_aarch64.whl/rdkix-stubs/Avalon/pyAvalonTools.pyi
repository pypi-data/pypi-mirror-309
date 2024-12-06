"""
Module containing functionality from the Avalon toolkit.

The functions currently exposed are:
  - GetCanonSmiles()   : return the canonical smiles for a molecule
  - GetAvalonFP()      : return the Avalon fingerprint for a molecule as
                         an RDKix ExplicitBitVector
  - GetAvalonCountFP()      : return the Avalon fingerprint for a molecule as
                              an RDKix SparseIntVector
  - Generate2DCoords() : use the Avalon coordinate generator to create
                         a set of 2D coordinates for a molecule
Each function can be called with either an RDKix molecule or some
molecule data as text (e.g. a SMILES or an MDL mol block).

See the individual docstrings for more information.
"""
from __future__ import annotations
import typing
__all__ = ['CheckMolecule', 'CheckMoleculeString', 'CloseCheckMolFiles', 'Generate2DCoords', 'GetAvalonCountFP', 'GetAvalonFP', 'GetAvalonFPAsWords', 'GetCanonSmiles', 'GetCheckMolLog', 'InitializeCheckMol', 'StruChkFlag', 'StruChkResult', 'avalonSSSBits', 'avalonSimilarityBits']
class StruChkFlag(Boost.Python.enum):
    __slots__: typing.ClassVar[tuple] = tuple()
    alias_conversion_failed: typing.ClassVar[StruChkFlag]  # value = rdkix.Avalon.pyAvalonTools.StruChkFlag.alias_conversion_failed
    atom_check_failed: typing.ClassVar[StruChkFlag]  # value = rdkix.Avalon.pyAvalonTools.StruChkFlag.atom_check_failed
    atom_clash: typing.ClassVar[StruChkFlag]  # value = rdkix.Avalon.pyAvalonTools.StruChkFlag.atom_clash
    bad_molecule: typing.ClassVar[StruChkFlag]  # value = rdkix.Avalon.pyAvalonTools.StruChkFlag.bad_molecule
    dubious_stereo_removed: typing.ClassVar[StruChkFlag]  # value = rdkix.Avalon.pyAvalonTools.StruChkFlag.dubious_stereo_removed
    either_warning: typing.ClassVar[StruChkFlag]  # value = rdkix.Avalon.pyAvalonTools.StruChkFlag.either_warning
    fragments_found: typing.ClassVar[StruChkFlag]  # value = rdkix.Avalon.pyAvalonTools.StruChkFlag.fragments_found
    names: typing.ClassVar[dict]  # value = {'bad_molecule': rdkix.Avalon.pyAvalonTools.StruChkFlag.bad_molecule, 'alias_conversion_failed': rdkix.Avalon.pyAvalonTools.StruChkFlag.alias_conversion_failed, 'transformed': rdkix.Avalon.pyAvalonTools.StruChkFlag.transformed, 'fragments_found': rdkix.Avalon.pyAvalonTools.StruChkFlag.fragments_found, 'either_warning': rdkix.Avalon.pyAvalonTools.StruChkFlag.either_warning, 'stereo_error': rdkix.Avalon.pyAvalonTools.StruChkFlag.stereo_error, 'dubious_stereo_removed': rdkix.Avalon.pyAvalonTools.StruChkFlag.dubious_stereo_removed, 'atom_clash': rdkix.Avalon.pyAvalonTools.StruChkFlag.atom_clash, 'atom_check_failed': rdkix.Avalon.pyAvalonTools.StruChkFlag.atom_check_failed, 'size_check_failed': rdkix.Avalon.pyAvalonTools.StruChkFlag.size_check_failed, 'recharged': rdkix.Avalon.pyAvalonTools.StruChkFlag.recharged, 'stereo_forced_bad': rdkix.Avalon.pyAvalonTools.StruChkFlag.stereo_forced_bad, 'stereo_transformed': rdkix.Avalon.pyAvalonTools.StruChkFlag.stereo_transformed, 'template_transformed': rdkix.Avalon.pyAvalonTools.StruChkFlag.template_transformed}
    recharged: typing.ClassVar[StruChkFlag]  # value = rdkix.Avalon.pyAvalonTools.StruChkFlag.recharged
    size_check_failed: typing.ClassVar[StruChkFlag]  # value = rdkix.Avalon.pyAvalonTools.StruChkFlag.size_check_failed
    stereo_error: typing.ClassVar[StruChkFlag]  # value = rdkix.Avalon.pyAvalonTools.StruChkFlag.stereo_error
    stereo_forced_bad: typing.ClassVar[StruChkFlag]  # value = rdkix.Avalon.pyAvalonTools.StruChkFlag.stereo_forced_bad
    stereo_transformed: typing.ClassVar[StruChkFlag]  # value = rdkix.Avalon.pyAvalonTools.StruChkFlag.stereo_transformed
    template_transformed: typing.ClassVar[StruChkFlag]  # value = rdkix.Avalon.pyAvalonTools.StruChkFlag.template_transformed
    transformed: typing.ClassVar[StruChkFlag]  # value = rdkix.Avalon.pyAvalonTools.StruChkFlag.transformed
    values: typing.ClassVar[dict]  # value = {1: rdkix.Avalon.pyAvalonTools.StruChkFlag.bad_molecule, 2: rdkix.Avalon.pyAvalonTools.StruChkFlag.alias_conversion_failed, 4: rdkix.Avalon.pyAvalonTools.StruChkFlag.transformed, 8: rdkix.Avalon.pyAvalonTools.StruChkFlag.fragments_found, 16: rdkix.Avalon.pyAvalonTools.StruChkFlag.either_warning, 32: rdkix.Avalon.pyAvalonTools.StruChkFlag.stereo_error, 64: rdkix.Avalon.pyAvalonTools.StruChkFlag.dubious_stereo_removed, 128: rdkix.Avalon.pyAvalonTools.StruChkFlag.atom_clash, 256: rdkix.Avalon.pyAvalonTools.StruChkFlag.atom_check_failed, 512: rdkix.Avalon.pyAvalonTools.StruChkFlag.size_check_failed, 1024: rdkix.Avalon.pyAvalonTools.StruChkFlag.recharged, 2048: rdkix.Avalon.pyAvalonTools.StruChkFlag.stereo_forced_bad, 4096: rdkix.Avalon.pyAvalonTools.StruChkFlag.stereo_transformed, 8192: rdkix.Avalon.pyAvalonTools.StruChkFlag.template_transformed}
class StruChkResult(Boost.Python.enum):
    __slots__: typing.ClassVar[tuple] = tuple()
    bad_set: typing.ClassVar[StruChkResult]  # value = rdkix.Avalon.pyAvalonTools.StruChkResult.bad_set
    names: typing.ClassVar[dict]  # value = {'success': rdkix.Avalon.pyAvalonTools.StruChkResult.success, 'bad_set': rdkix.Avalon.pyAvalonTools.StruChkResult.bad_set, 'transformed_set': rdkix.Avalon.pyAvalonTools.StruChkResult.transformed_set}
    success: typing.ClassVar[StruChkResult]  # value = rdkix.Avalon.pyAvalonTools.StruChkResult.success
    transformed_set: typing.ClassVar[StruChkResult]  # value = rdkix.Avalon.pyAvalonTools.StruChkResult.transformed_set
    values: typing.ClassVar[dict]  # value = {0: rdkix.Avalon.pyAvalonTools.StruChkResult.success, 2979: rdkix.Avalon.pyAvalonTools.StruChkResult.bad_set, 29788: rdkix.Avalon.pyAvalonTools.StruChkResult.transformed_set}
@typing.overload
def CheckMolecule(molstring: str, isSmiles: bool) -> tuple:
    """
        check a molecule passed in as a string.
        If the isSmiles argument is true, the string should represent the SMILES encoding
        of the molecule, otherwise it should be encoded as an MDL molfile.
        The first member of the return tuple contains the bit-encoded corrections made to the molecule.
        If possible, the molecule (corrected when appropriate) is returned as the second member of 
        the return tuple. Otherwise, None is returned.
    
        C++ signature :
            boost::python::tuple CheckMolecule(std::string,bool)
    """
@typing.overload
def CheckMolecule(mol: typing.Any) -> tuple:
    """
        check a molecule passed in as an RDKix molecule.
        The first member of the return tuple contains the bit-encoded corrections made to the molecule.
        If possible, the molecule (corrected when appropriate) is returned as the second member of 
        the return tuple. Otherwise, None is returned.
    
        C++ signature :
            boost::python::tuple CheckMolecule(RDKix::ROMol {lvalue})
    """
def CheckMoleculeString(molstring: str, isSmiles: bool) -> tuple:
    """
        check a molecule passed in as a string and returns the result as a string.
        If the isSmiles argument is true, the string should represent the SMILES encoding
        of the molecule, otherwise it should be encoded as an MDL molfile.
        The first member of the return tuple contains the bit-encoded corrections made to the molecule.
        If possible, a corrected CTAB for the molecule is returned as the second member of 
        the return tuple.
    
        C++ signature :
            boost::python::tuple CheckMoleculeString(std::string,bool)
    """
def CloseCheckMolFiles() -> None:
    """
        close open files used by molecule-checking functions.
    
        C++ signature :
            void CloseCheckMolFiles()
    """
@typing.overload
def Generate2DCoords(mol: typing.Any, clearConfs: bool = True) -> int:
    """
        Generates 2d coordinates for an RDKix molecule
    
        C++ signature :
            unsigned int Generate2DCoords(RDKix::ROMol {lvalue} [,bool=True])
    """
@typing.overload
def Generate2DCoords(molData: str, isSmiles: bool) -> str:
    """
        returns an MDL mol block with 2D coordinates for some molecule data.
        If the isSmiles argument is true, the data is assumed to be SMILES, otherwise
        MDL mol data is assumed.
    
        C++ signature :
            std::string Generate2DCoords(std::string,bool)
    """
@typing.overload
def GetAvalonCountFP(mol: typing.Any, nBits: int = 512, isQuery: bool = False, bitFlags: int = 15761407) -> typing.Any:
    """
        returns the Avalon count fingerprint for an RDKix molecule
    
        C++ signature :
            RDKix::SparseIntVect<unsigned int>* GetAvalonCountFP(RDKix::ROMol [,unsigned int=512 [,bool=False [,unsigned int=15761407]]])
    """
@typing.overload
def GetAvalonCountFP(molData: str, isSmiles: bool, nBits: int = 512, isQuery: bool = False, bitFlags: int = 15761407) -> typing.Any:
    """
        returns the Avalon count fingerprint for some molecule data.
        If the isSmiles argument is true, the data is assumed to be SMILES, otherwise
        MDL mol data is assumed.
    
        C++ signature :
            RDKix::SparseIntVect<unsigned int>* GetAvalonCountFP(std::string,bool [,unsigned int=512 [,bool=False [,unsigned int=15761407]]])
    """
@typing.overload
def GetAvalonFP(mol: typing.Any, nBits: int = 512, isQuery: bool = False, resetVect: bool = False, bitFlags: int = 15761407) -> typing.Any:
    """
        returns the Avalon fingerprint for an RDKix molecule
    
        C++ signature :
            ExplicitBitVect* GetAvalonFP(RDKix::ROMol [,unsigned int=512 [,bool=False [,bool=False [,unsigned int=15761407]]]])
    """
@typing.overload
def GetAvalonFP(molData: str, isSmiles: bool, nBits: int = 512, isQuery: bool = False, resetVect: bool = False, bitFlags: int = 15761407) -> typing.Any:
    """
        returns the Avalon fingerprint for some molecule data.
        If the isSmiles argument is true, the data is assumed to be SMILES, otherwise
        MDL mol data is assumed.
    
        C++ signature :
            ExplicitBitVect* GetAvalonFP(std::string,bool [,unsigned int=512 [,bool=False [,bool=False [,unsigned int=15761407]]]])
    """
@typing.overload
def GetAvalonFPAsWords(mol: typing.Any, nBits: int = 512, isQuery: bool = False, resetVect: bool = False, bitFlags: int = 15761407) -> list:
    """
        returns the Avalon fingerprint for an RDKix molecule as a list of ints
    
        C++ signature :
            boost::python::list GetAvalonFPAsWords(RDKix::ROMol [,unsigned int=512 [,bool=False [,bool=False [,unsigned int=15761407]]]])
    """
@typing.overload
def GetAvalonFPAsWords(molData: str, isSmiles: bool, nBits: int = 512, isQuery: bool = False, resetVect: bool = False, bitFlags: int = 15761407) -> list:
    """
        returns the Avalon fingerprint for some molecule data as a list of ints.
        If the isSmiles argument is true, the data is assumed to be SMILES, otherwise
        MDL mol data is assumed.
    
        C++ signature :
            boost::python::list GetAvalonFPAsWords(std::string,bool [,unsigned int=512 [,bool=False [,bool=False [,unsigned int=15761407]]]])
    """
@typing.overload
def GetCanonSmiles(mol: typing.Any, flags: int = -1) -> str:
    """
        returns canonical smiles for an RDKix molecule
    
        C++ signature :
            std::string GetCanonSmiles(RDKix::ROMol {lvalue} [,int=-1])
    """
@typing.overload
def GetCanonSmiles(molData: str, isSmiles: bool, flags: int = -1) -> str:
    """
        Returns canonical smiles for some molecule data.
        If the isSmiles argument is true, the data is assumed to be SMILES, otherwise
        MDL mol data is assumed.
    
        C++ signature :
            std::string GetCanonSmiles(std::string,bool [,int=-1])
    """
def GetCheckMolLog() -> str:
    """
        Returns the Struchk log for the last molecules processed.
    
        C++ signature :
            std::string GetCheckMolLog()
    """
def InitializeCheckMol(options: str = '') -> int:
    """
        initializes the structure checker.
        The argument should contain option lines separated by embedded newlines.An empty string will be used if the argument is omitted.An non-zero error code is returned in case of failure.
    
        C++ signature :
            int InitializeCheckMol([ std::string=''])
    """
avalonSSSBits: int = 32767
avalonSimilarityBits: int = 15761407
