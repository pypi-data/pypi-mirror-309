"""
Module containing tools for normalizing molecules defined by SMARTS patterns
"""
from __future__ import annotations
import rdkix.Chem
import typing
__all__ = ['AllowedAtomsValidation', 'CHARGE_CORRECTIONS', 'CanonicalTautomer', 'ChargeCorrection', 'ChargeParent', 'ChargeParentInPlace', 'Cleanup', 'CleanupInPlace', 'CleanupParameters', 'DisallowedAtomsValidation', 'DisallowedRadicalValidation', 'DisconnectOrganometallics', 'DisconnectOrganometallicsInPlace', 'FeaturesValidation', 'FragmentParent', 'FragmentParentInPlace', 'FragmentRemover', 'FragmentRemoverFromData', 'FragmentValidation', 'GetV1TautomerEnumerator', 'Is2DValidation', 'IsotopeParent', 'IsotopeParentInPlace', 'IsotopeValidation', 'LargestFragmentChooser', 'Layout2DValidation', 'MOL_SPTR_VECT', 'MetalDisconnector', 'MetalDisconnectorOptions', 'MolVSValidation', 'NeutralValidation', 'NoAtomValidation', 'Normalize', 'NormalizeInPlace', 'Normalizer', 'NormalizerFromData', 'NormalizerFromParams', 'Pipeline', 'PipelineLog', 'PipelineLogEntry', 'PipelineOptions', 'PipelineResult', 'PipelineStage', 'PipelineStatus', 'RDKixValidation', 'Reionize', 'ReionizeInPlace', 'Reionizer', 'ReionizerFromData', 'RemoveFragments', 'RemoveFragmentsInPlace', 'SmilesTautomerMap', 'StandardizeSmiles', 'StereoParent', 'StereoParentInPlace', 'StereoValidation', 'SuperParent', 'SuperParentInPlace', 'Tautomer', 'TautomerEnumerator', 'TautomerEnumeratorCallback', 'TautomerEnumeratorResult', 'TautomerEnumeratorStatus', 'TautomerParent', 'TautomerParentInPlace', 'Uncharger', 'UpdateParamsFromJSON', 'ValidateSmiles', 'ValidationMethod', 'map_indexing_suite_SmilesTautomerMap_entry']
class AllowedAtomsValidation(ValidationMethod):
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def __init__(self, arg1: typing.Any) -> typing.Any:
        """
            C++ signature :
                void * __ptr64 __init__(class boost::python::api::object,class boost::python::api::object)
        """
class ChargeCorrection(Boost.Python.instance):
    __instance_size__: typing.ClassVar[int] = 96
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def __init__(self, name: str, smarts: str, charge: int) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64,class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >,class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >,int)
        """
    @property
    def Charge(*args, **kwargs):
        ...
    @Charge.setter
    def Charge(*args, **kwargs):
        ...
    @property
    def Name(*args, **kwargs):
        ...
    @Name.setter
    def Name(*args, **kwargs):
        ...
    @property
    def Smarts(*args, **kwargs):
        ...
    @Smarts.setter
    def Smarts(*args, **kwargs):
        ...
class CleanupParameters(Boost.Python.instance):
    """
    Parameters controlling molecular standardization
    """
    __instance_size__: typing.ClassVar[int] = 312
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64)
        """
    @property
    def acidbaseFile(*args, **kwargs):
        """
        file containing the acid and base definitions
        """
    @acidbaseFile.setter
    def acidbaseFile(*args, **kwargs):
        ...
    @property
    def doCanonical(*args, **kwargs):
        """
        apply atom-order dependent normalizations (like uncharging) in a canonical order
        """
    @doCanonical.setter
    def doCanonical(*args, **kwargs):
        ...
    @property
    def fragmentFile(*args, **kwargs):
        """
        file containing the acid and base definitions
        """
    @fragmentFile.setter
    def fragmentFile(*args, **kwargs):
        ...
    @property
    def largestFragmentChooserCountHeavyAtomsOnly(*args, **kwargs):
        """
        whether LargestFragmentChooser should only count heavy atoms (defaults to False)
        """
    @largestFragmentChooserCountHeavyAtomsOnly.setter
    def largestFragmentChooserCountHeavyAtomsOnly(*args, **kwargs):
        ...
    @property
    def largestFragmentChooserUseAtomCount(*args, **kwargs):
        """
        Whether LargestFragmentChooser should use atom count as main criterion before MW (defaults to True)
        """
    @largestFragmentChooserUseAtomCount.setter
    def largestFragmentChooserUseAtomCount(*args, **kwargs):
        ...
    @property
    def maxRestarts(*args, **kwargs):
        """
        maximum number of restarts
        """
    @maxRestarts.setter
    def maxRestarts(*args, **kwargs):
        ...
    @property
    def maxTautomers(*args, **kwargs):
        """
        maximum number of tautomers to generate (defaults to 1000)
        """
    @maxTautomers.setter
    def maxTautomers(*args, **kwargs):
        ...
    @property
    def maxTransforms(*args, **kwargs):
        """
        maximum number of transforms to apply during tautomer enumeration (defaults to 1000)
        """
    @maxTransforms.setter
    def maxTransforms(*args, **kwargs):
        ...
    @property
    def normalizationsFile(*args, **kwargs):
        """
        file containing the normalization transformations
        """
    @normalizationsFile.setter
    def normalizationsFile(*args, **kwargs):
        ...
    @property
    def preferOrganic(*args, **kwargs):
        """
        prefer organic fragments to inorganic ones when deciding what to keep
        """
    @preferOrganic.setter
    def preferOrganic(*args, **kwargs):
        ...
    @property
    def tautomerReassignStereo(*args, **kwargs):
        """
        call AssignStereochemistry on all generated tautomers (defaults to True)
        """
    @tautomerReassignStereo.setter
    def tautomerReassignStereo(*args, **kwargs):
        ...
    @property
    def tautomerRemoveBondStereo(*args, **kwargs):
        """
        remove stereochemistry from double bonds involved in tautomerism (defaults to True)
        """
    @tautomerRemoveBondStereo.setter
    def tautomerRemoveBondStereo(*args, **kwargs):
        ...
    @property
    def tautomerRemoveIsotopicHs(*args, **kwargs):
        """
        remove isotopic Hs from centers involved in tautomerism (defaults to True)
        """
    @tautomerRemoveIsotopicHs.setter
    def tautomerRemoveIsotopicHs(*args, **kwargs):
        ...
    @property
    def tautomerRemoveSp3Stereo(*args, **kwargs):
        """
        remove stereochemistry from sp3 centers involved in tautomerism (defaults to True)
        """
    @tautomerRemoveSp3Stereo.setter
    def tautomerRemoveSp3Stereo(*args, **kwargs):
        ...
    @property
    def tautomerTransformsFile(*args, **kwargs):
        """
        file containing the tautomer transformations
        """
    @tautomerTransformsFile.setter
    def tautomerTransformsFile(*args, **kwargs):
        ...
class DisallowedAtomsValidation(ValidationMethod):
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def __init__(self, arg1: typing.Any) -> typing.Any:
        """
            C++ signature :
                void * __ptr64 __init__(class boost::python::api::object,class boost::python::api::object)
        """
class DisallowedRadicalValidation(ValidationMethod):
    __instance_size__: typing.ClassVar[int] = 32
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64)
        """
class FeaturesValidation(ValidationMethod):
    __instance_size__: typing.ClassVar[int] = 40
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64)
        """
    @typing.overload
    def __init__(self, allowEnhancedStereo: bool = False, allowAromaticBondType: bool = False, allowDativeBondType: bool = False, allowQueries: bool = False, allowDummmies: bool = False, allowAtomAliases: bool = False) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64 [,bool=False [,bool=False [,bool=False [,bool=False [,bool=False [,bool=False]]]]]])
        """
    @property
    def allowAromaticBondType(*args, **kwargs):
        ...
    @allowAromaticBondType.setter
    def allowAromaticBondType(*args, **kwargs):
        ...
    @property
    def allowAtomAliases(*args, **kwargs):
        ...
    @allowAtomAliases.setter
    def allowAtomAliases(*args, **kwargs):
        ...
    @property
    def allowDativeBondType(*args, **kwargs):
        ...
    @allowDativeBondType.setter
    def allowDativeBondType(*args, **kwargs):
        ...
    @property
    def allowDummies(*args, **kwargs):
        ...
    @allowDummies.setter
    def allowDummies(*args, **kwargs):
        ...
    @property
    def allowEnhancedStereo(*args, **kwargs):
        ...
    @allowEnhancedStereo.setter
    def allowEnhancedStereo(*args, **kwargs):
        ...
    @property
    def allowQueries(*args, **kwargs):
        ...
    @allowQueries.setter
    def allowQueries(*args, **kwargs):
        ...
class FragmentRemover(Boost.Python.instance):
    __instance_size__: typing.ClassVar[int] = 40
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64)
        """
    @typing.overload
    def __init__(self, fragmentFilename: str = '', leave_last: bool = True, skip_if_all_match: bool = False) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64 [,class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >='' [,bool=True [,bool=False]]])
        """
    def remove(self, mol: Mol) -> rdkix.Chem.Mol:
        """
            C++ signature :
                class RDKix::ROMol * __ptr64 remove(class RDKix::MolStandardize::FragmentRemover {lvalue},class RDKix::ROMol)
        """
    def removeInPlace(self, mol: Mol) -> None:
        """
            modifies the molecule in place
        
            C++ signature :
                void removeInPlace(class RDKix::MolStandardize::FragmentRemover {lvalue},class RDKix::ROMol {lvalue})
        """
class FragmentValidation(ValidationMethod):
    __instance_size__: typing.ClassVar[int] = 32
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64)
        """
class Is2DValidation(ValidationMethod):
    __instance_size__: typing.ClassVar[int] = 40
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64)
        """
    @typing.overload
    def __init__(self, threshold: float = 0.001) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64 [,double=0.001])
        """
    @property
    def threshold(*args, **kwargs):
        ...
    @threshold.setter
    def threshold(*args, **kwargs):
        ...
class IsotopeValidation(ValidationMethod):
    __instance_size__: typing.ClassVar[int] = 40
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64)
        """
    @typing.overload
    def __init__(self, strict: bool = False) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64 [,bool=False])
        """
    @property
    def strict(*args, **kwargs):
        ...
    @strict.setter
    def strict(*args, **kwargs):
        ...
class LargestFragmentChooser(Boost.Python.instance):
    __instance_size__: typing.ClassVar[int] = 32
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, preferOrganic: bool = False) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64 [,bool=False])
        """
    @typing.overload
    def __init__(self, params: CleanupParameters) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64,struct RDKix::MolStandardize::CleanupParameters)
        """
    def choose(self, mol: Mol) -> rdkix.Chem.Mol:
        """
            C++ signature :
                class RDKix::ROMol * __ptr64 choose(class RDKix::MolStandardize::LargestFragmentChooser {lvalue},class RDKix::ROMol)
        """
    def chooseInPlace(self, mol: Mol) -> None:
        """
            C++ signature :
                void chooseInPlace(class RDKix::MolStandardize::LargestFragmentChooser {lvalue},class RDKix::ROMol {lvalue})
        """
class Layout2DValidation(ValidationMethod):
    __instance_size__: typing.ClassVar[int] = 64
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64)
        """
    @typing.overload
    def __init__(self, clashLimit: float = 0.15, bondLengthLimit: float = 25.0, allowLongBondsInRings: bool = True, allowAtomBondClashExemption: bool = True, minMedianBondLength: float = False) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64 [,double=0.15 [,double=25.0 [,bool=True [,bool=True [,double=False]]]]])
        """
    @property
    def allowAtomBondClashExemption(*args, **kwargs):
        ...
    @allowAtomBondClashExemption.setter
    def allowAtomBondClashExemption(*args, **kwargs):
        ...
    @property
    def allowLongBondsInRings(*args, **kwargs):
        ...
    @allowLongBondsInRings.setter
    def allowLongBondsInRings(*args, **kwargs):
        ...
    @property
    def bondLengthLimit(*args, **kwargs):
        ...
    @bondLengthLimit.setter
    def bondLengthLimit(*args, **kwargs):
        ...
    @property
    def clashLimit(*args, **kwargs):
        ...
    @clashLimit.setter
    def clashLimit(*args, **kwargs):
        ...
    @property
    def minMedianBondLength(*args, **kwargs):
        ...
    @minMedianBondLength.setter
    def minMedianBondLength(*args, **kwargs):
        ...
class MOL_SPTR_VECT(Boost.Python.instance):
    __instance_size__: typing.ClassVar[int] = 48
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def __contains__(self, item: typing.Any) -> bool:
        """
            C++ signature :
                bool __contains__(class std::vector<class boost::shared_ptr<class RDKix::ROMol>,class std::allocator<class boost::shared_ptr<class RDKix::ROMol> > > {lvalue},struct _object * __ptr64)
        """
    def __delitem__(self, item: typing.Any) -> None:
        """
            C++ signature :
                void __delitem__(class std::vector<class boost::shared_ptr<class RDKix::ROMol>,class std::allocator<class boost::shared_ptr<class RDKix::ROMol> > > {lvalue},struct _object * __ptr64)
        """
    def __getitem__(self, item: typing.Any) -> typing.Any:
        """
            C++ signature :
                class boost::python::api::object __getitem__(struct boost::python::back_reference<class std::vector<class boost::shared_ptr<class RDKix::ROMol>,class std::allocator<class boost::shared_ptr<class RDKix::ROMol> > > & __ptr64>,struct _object * __ptr64)
        """
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64)
        """
    def __iter__(self) -> typing.Any:
        """
            C++ signature :
                struct boost::python::objects::iterator_range<struct boost::python::return_value_policy<struct boost::python::return_by_value,struct boost::python::default_call_policies>,class std::_Vector_iterator<class std::_Vector_val<struct std::_Simple_types<class boost::shared_ptr<class RDKix::ROMol> > > > > __iter__(struct boost::python::back_reference<class std::vector<class boost::shared_ptr<class RDKix::ROMol>,class std::allocator<class boost::shared_ptr<class RDKix::ROMol> > > & __ptr64>)
        """
    def __len__(self) -> int:
        """
            C++ signature :
                unsigned __int64 __len__(class std::vector<class boost::shared_ptr<class RDKix::ROMol>,class std::allocator<class boost::shared_ptr<class RDKix::ROMol> > > {lvalue})
        """
    def __setitem__(self, item: typing.Any, value: typing.Any) -> None:
        """
            C++ signature :
                void __setitem__(class std::vector<class boost::shared_ptr<class RDKix::ROMol>,class std::allocator<class boost::shared_ptr<class RDKix::ROMol> > > {lvalue},struct _object * __ptr64,struct _object * __ptr64)
        """
    def append(self, item: typing.Any) -> None:
        """
            C++ signature :
                void append(class std::vector<class boost::shared_ptr<class RDKix::ROMol>,class std::allocator<class boost::shared_ptr<class RDKix::ROMol> > > {lvalue},class boost::python::api::object)
        """
    def extend(self, other: typing.Any) -> None:
        """
            C++ signature :
                void extend(class std::vector<class boost::shared_ptr<class RDKix::ROMol>,class std::allocator<class boost::shared_ptr<class RDKix::ROMol> > > {lvalue},class boost::python::api::object)
        """
class MetalDisconnector(Boost.Python.instance):
    """
    a class to disconnect metals that are defined as covalently bonded to non-metals
    """
    __instance_size__: typing.ClassVar[int] = 32
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def Disconnect(self, mol: Mol) -> rdkix.Chem.Mol:
        """
            performs the disconnection
        
            C++ signature :
                class RDKix::ROMol * __ptr64 Disconnect(class `anonymous namespace'::MetalDisconnectorWrap {lvalue},class RDKix::ROMol)
        """
    def DisconnectInPlace(self, mol: Mol) -> None:
        """
            performs the disconnection, modifies the input molecule
        
            C++ signature :
                void DisconnectInPlace(class `anonymous namespace'::MetalDisconnectorWrap {lvalue},class RDKix::ROMol {lvalue})
        """
    def SetMetalNof(self, mol: Mol) -> None:
        """
            Set the query molecule defining the metals to disconnect if attached to Nitrogen, Oxygen or Fluorine.
        
            C++ signature :
                void SetMetalNof(class `anonymous namespace'::MetalDisconnectorWrap {lvalue},class RDKix::ROMol)
        """
    def SetMetalNon(self, mol: Mol) -> None:
        """
            Set the query molecule defining the metals to disconnect from other inorganic elements.
        
            C++ signature :
                void SetMetalNon(class `anonymous namespace'::MetalDisconnectorWrap {lvalue},class RDKix::ROMol)
        """
    def __init__(self, options: typing.Any = None) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64 [,class boost::python::api::object=None])
        """
    @property
    def MetalNof(*args, **kwargs):
        """
        SMARTS defining the metals to disconnect if attached to Nitrogen, Oxygen or Fluorine
        """
    @property
    def MetalNon(*args, **kwargs):
        """
        SMARTS defining the metals to disconnect other inorganic elements
        """
class MetalDisconnectorOptions(Boost.Python.instance):
    """
    Metal Disconnector Options
    """
    __instance_size__: typing.ClassVar[int] = 32
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64)
        """
    @property
    def adjustCharges(*args, **kwargs):
        """
        Whether to adjust charges on ligand atoms.  Default true.
        """
    @adjustCharges.setter
    def adjustCharges(*args, **kwargs):
        ...
    @property
    def removeHapticDummies(*args, **kwargs):
        """
        Whether to remove the dummy atoms representing haptic bonds.  Such dummies are bonded to the metal with a bond that has the MolFileBondEndPts prop set.  Default false.
        """
    @removeHapticDummies.setter
    def removeHapticDummies(*args, **kwargs):
        ...
    @property
    def splitAromaticC(*args, **kwargs):
        """
        Whether to split metal-aromatic C bonds.  Default false.
        """
    @splitAromaticC.setter
    def splitAromaticC(*args, **kwargs):
        ...
    @property
    def splitGrignards(*args, **kwargs):
        """
        Whether to split Grignard-type complexes. Default false.
        """
    @splitGrignards.setter
    def splitGrignards(*args, **kwargs):
        ...
class MolVSValidation(ValidationMethod):
    __instance_size__: typing.ClassVar[int] = 56
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64)
        """
    @typing.overload
    def __init__(self, arg1: typing.Any) -> typing.Any:
        """
            C++ signature :
                void * __ptr64 __init__(class boost::python::api::object,class boost::python::api::object)
        """
class NeutralValidation(ValidationMethod):
    __instance_size__: typing.ClassVar[int] = 32
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64)
        """
class NoAtomValidation(ValidationMethod):
    __instance_size__: typing.ClassVar[int] = 32
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64)
        """
class Normalizer(Boost.Python.instance):
    __instance_size__: typing.ClassVar[int] = 40
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64)
        """
    @typing.overload
    def __init__(self, normalizeFilename: str, maxRestarts: int) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64,class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >,unsigned int)
        """
    def normalize(self, mol: Mol) -> rdkix.Chem.Mol:
        """
            C++ signature :
                class RDKix::ROMol * __ptr64 normalize(class RDKix::MolStandardize::Normalizer {lvalue},class RDKix::ROMol)
        """
    def normalizeInPlace(self, mol: Mol) -> None:
        """
            modifies the input molecule
        
            C++ signature :
                void normalizeInPlace(class RDKix::MolStandardize::Normalizer {lvalue},class RDKix::ROMol {lvalue})
        """
class Pipeline(Boost.Python.instance):
    __instance_size__: typing.ClassVar[int] = 264
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    @staticmethod
    def run(arg1: Pipeline, arg2: str) -> PipelineResult:
        """
            C++ signature :
                struct RDKix::MolStandardize::PipelineResult run(class RDKix::MolStandardize::Pipeline {lvalue},class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >)
        """
    @typing.overload
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64)
        """
    @typing.overload
    def __init__(self, arg1: PipelineOptions) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64,struct RDKix::MolStandardize::PipelineOptions)
        """
class PipelineLog(Boost.Python.instance):
    @staticmethod
    def __init__(*args, **kwargs):
        """
        Raises an exception
        This class cannot be instantiated from Python
        """
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def __contains__(self, item: typing.Any) -> bool:
        """
            C++ signature :
                bool __contains__(class std::vector<struct RDKix::MolStandardize::PipelineLogEntry,class std::allocator<struct RDKix::MolStandardize::PipelineLogEntry> > {lvalue},struct _object * __ptr64)
        """
    def __delitem__(self, item: typing.Any) -> None:
        """
            C++ signature :
                void __delitem__(class std::vector<struct RDKix::MolStandardize::PipelineLogEntry,class std::allocator<struct RDKix::MolStandardize::PipelineLogEntry> > {lvalue},struct _object * __ptr64)
        """
    def __getitem__(self, item: typing.Any) -> typing.Any:
        """
            C++ signature :
                class boost::python::api::object __getitem__(struct boost::python::back_reference<class std::vector<struct RDKix::MolStandardize::PipelineLogEntry,class std::allocator<struct RDKix::MolStandardize::PipelineLogEntry> > & __ptr64>,struct _object * __ptr64)
        """
    def __iter__(self) -> typing.Any:
        """
            C++ signature :
                struct boost::python::objects::iterator_range<struct boost::python::return_internal_reference<1,struct boost::python::default_call_policies>,class std::_Vector_iterator<class std::_Vector_val<struct std::_Simple_types<struct RDKix::MolStandardize::PipelineLogEntry> > > > __iter__(struct boost::python::back_reference<class std::vector<struct RDKix::MolStandardize::PipelineLogEntry,class std::allocator<struct RDKix::MolStandardize::PipelineLogEntry> > & __ptr64>)
        """
    def __len__(self) -> int:
        """
            C++ signature :
                unsigned __int64 __len__(class std::vector<struct RDKix::MolStandardize::PipelineLogEntry,class std::allocator<struct RDKix::MolStandardize::PipelineLogEntry> > {lvalue})
        """
    def __setitem__(self, item: typing.Any, value: typing.Any) -> None:
        """
            C++ signature :
                void __setitem__(class std::vector<struct RDKix::MolStandardize::PipelineLogEntry,class std::allocator<struct RDKix::MolStandardize::PipelineLogEntry> > {lvalue},struct _object * __ptr64,struct _object * __ptr64)
        """
    def append(self, item: typing.Any) -> None:
        """
            C++ signature :
                void append(class std::vector<struct RDKix::MolStandardize::PipelineLogEntry,class std::allocator<struct RDKix::MolStandardize::PipelineLogEntry> > {lvalue},class boost::python::api::object)
        """
    def extend(self, other: typing.Any) -> None:
        """
            C++ signature :
                void extend(class std::vector<struct RDKix::MolStandardize::PipelineLogEntry,class std::allocator<struct RDKix::MolStandardize::PipelineLogEntry> > {lvalue},class boost::python::api::object)
        """
class PipelineLogEntry(Boost.Python.instance):
    @staticmethod
    def __init__(*args, **kwargs):
        """
        Raises an exception
        This class cannot be instantiated from Python
        """
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    @property
    def detail(*args, **kwargs):
        ...
    @property
    def status(*args, **kwargs):
        ...
class PipelineOptions(Boost.Python.instance):
    __instance_size__: typing.ClassVar[int] = 192
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64)
        """
    @property
    def allowAromaticBondType(*args, **kwargs):
        ...
    @allowAromaticBondType.setter
    def allowAromaticBondType(*args, **kwargs):
        ...
    @property
    def allowAtomBondClashExemption(*args, **kwargs):
        ...
    @allowAtomBondClashExemption.setter
    def allowAtomBondClashExemption(*args, **kwargs):
        ...
    @property
    def allowDativeBondType(*args, **kwargs):
        ...
    @allowDativeBondType.setter
    def allowDativeBondType(*args, **kwargs):
        ...
    @property
    def allowEmptyMolecules(*args, **kwargs):
        ...
    @allowEmptyMolecules.setter
    def allowEmptyMolecules(*args, **kwargs):
        ...
    @property
    def allowEnhancedStereo(*args, **kwargs):
        ...
    @allowEnhancedStereo.setter
    def allowEnhancedStereo(*args, **kwargs):
        ...
    @property
    def allowLongBondsInRings(*args, **kwargs):
        ...
    @allowLongBondsInRings.setter
    def allowLongBondsInRings(*args, **kwargs):
        ...
    @property
    def atomClashLimit(*args, **kwargs):
        ...
    @atomClashLimit.setter
    def atomClashLimit(*args, **kwargs):
        ...
    @property
    def bondLengthLimit(*args, **kwargs):
        ...
    @bondLengthLimit.setter
    def bondLengthLimit(*args, **kwargs):
        ...
    @property
    def is2DZeroThreshold(*args, **kwargs):
        ...
    @is2DZeroThreshold.setter
    def is2DZeroThreshold(*args, **kwargs):
        ...
    @property
    def metalNof(*args, **kwargs):
        ...
    @metalNof.setter
    def metalNof(*args, **kwargs):
        ...
    @property
    def metalNon(*args, **kwargs):
        ...
    @metalNon.setter
    def metalNon(*args, **kwargs):
        ...
    @property
    def minMedianBondLength(*args, **kwargs):
        ...
    @minMedianBondLength.setter
    def minMedianBondLength(*args, **kwargs):
        ...
    @property
    def normalizerData(*args, **kwargs):
        ...
    @normalizerData.setter
    def normalizerData(*args, **kwargs):
        ...
    @property
    def normalizerMaxRestarts(*args, **kwargs):
        ...
    @normalizerMaxRestarts.setter
    def normalizerMaxRestarts(*args, **kwargs):
        ...
    @property
    def outputV2000(*args, **kwargs):
        ...
    @outputV2000.setter
    def outputV2000(*args, **kwargs):
        ...
    @property
    def reportAllFailures(*args, **kwargs):
        ...
    @reportAllFailures.setter
    def reportAllFailures(*args, **kwargs):
        ...
    @property
    def scaledMedianBondLength(*args, **kwargs):
        ...
    @scaledMedianBondLength.setter
    def scaledMedianBondLength(*args, **kwargs):
        ...
    @property
    def strictParsing(*args, **kwargs):
        ...
    @strictParsing.setter
    def strictParsing(*args, **kwargs):
        ...
class PipelineResult(Boost.Python.instance):
    @staticmethod
    def __init__(*args, **kwargs):
        """
        Raises an exception
        This class cannot be instantiated from Python
        """
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    @property
    def inputMolData(*args, **kwargs):
        ...
    @property
    def log(*args, **kwargs):
        ...
    @property
    def outputMolData(*args, **kwargs):
        ...
    @property
    def parentMolData(*args, **kwargs):
        ...
    @property
    def stage(*args, **kwargs):
        ...
    @property
    def status(*args, **kwargs):
        ...
class PipelineStage(Boost.Python.enum):
    COMPLETED: typing.ClassVar[PipelineStage]  # value = rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStage.COMPLETED
    PARSING_INPUT: typing.ClassVar[PipelineStage]  # value = rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStage.PARSING_INPUT
    PREPARE_FOR_STANDARDIZATION: typing.ClassVar[PipelineStage]  # value = rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStage.PREPARE_FOR_STANDARDIZATION
    PREPARE_FOR_VALIDATION: typing.ClassVar[PipelineStage]  # value = rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStage.PREPARE_FOR_VALIDATION
    SERIALIZING_OUTPUT: typing.ClassVar[PipelineStage]  # value = rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStage.SERIALIZING_OUTPUT
    STANDARDIZATION: typing.ClassVar[PipelineStage]  # value = rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStage.STANDARDIZATION
    VALIDATION: typing.ClassVar[PipelineStage]  # value = rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStage.VALIDATION
    __slots__: typing.ClassVar[tuple] = tuple()
    names: typing.ClassVar[dict]  # value = {'PARSING_INPUT': rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStage.PARSING_INPUT, 'PREPARE_FOR_VALIDATION': rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStage.PREPARE_FOR_VALIDATION, 'VALIDATION': rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStage.VALIDATION, 'PREPARE_FOR_STANDARDIZATION': rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStage.PREPARE_FOR_STANDARDIZATION, 'STANDARDIZATION': rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStage.STANDARDIZATION, 'SERIALIZING_OUTPUT': rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStage.SERIALIZING_OUTPUT, 'COMPLETED': rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStage.COMPLETED}
    values: typing.ClassVar[dict]  # value = {1: rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStage.PARSING_INPUT, 2: rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStage.PREPARE_FOR_VALIDATION, 3: rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStage.VALIDATION, 4: rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStage.PREPARE_FOR_STANDARDIZATION, 5: rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStage.STANDARDIZATION, 9: rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStage.SERIALIZING_OUTPUT, 10: rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStage.COMPLETED}
class PipelineStatus(Boost.Python.enum):
    BASIC_VALIDATION_ERROR: typing.ClassVar[PipelineStatus]  # value = rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.BASIC_VALIDATION_ERROR
    CHARGE_STANDARDIZATION_ERROR: typing.ClassVar[PipelineStatus]  # value = rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.CHARGE_STANDARDIZATION_ERROR
    FEATURES_VALIDATION_ERROR: typing.ClassVar[PipelineStatus]  # value = rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.FEATURES_VALIDATION_ERROR
    FRAGMENTS_REMOVED: typing.ClassVar[PipelineStatus]  # value = rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.FRAGMENTS_REMOVED
    FRAGMENT_STANDARDIZATION_ERROR: typing.ClassVar[PipelineStatus]  # value = rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.FRAGMENT_STANDARDIZATION_ERROR
    INPUT_ERROR: typing.ClassVar[PipelineStatus]  # value = rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.INPUT_ERROR
    IS2D_VALIDATION_ERROR: typing.ClassVar[PipelineStatus]  # value = rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.IS2D_VALIDATION_ERROR
    LAYOUT2D_VALIDATION_ERROR: typing.ClassVar[PipelineStatus]  # value = rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.LAYOUT2D_VALIDATION_ERROR
    METALS_DISCONNECTED: typing.ClassVar[PipelineStatus]  # value = rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.METALS_DISCONNECTED
    METAL_STANDARDIZATION_ERROR: typing.ClassVar[PipelineStatus]  # value = rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.METAL_STANDARDIZATION_ERROR
    NORMALIZATION_APPLIED: typing.ClassVar[PipelineStatus]  # value = rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.NORMALIZATION_APPLIED
    NORMALIZER_STANDARDIZATION_ERROR: typing.ClassVar[PipelineStatus]  # value = rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.NORMALIZER_STANDARDIZATION_ERROR
    NO_EVENT: typing.ClassVar[PipelineStatus]  # value = rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.NO_EVENT
    OUTPUT_ERROR: typing.ClassVar[PipelineStatus]  # value = rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.OUTPUT_ERROR
    PIPELINE_ERROR: typing.ClassVar[PipelineStatus]  # value = rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.PIPELINE_ERROR
    PREPARE_FOR_STANDARDIZATION_ERROR: typing.ClassVar[PipelineStatus]  # value = rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.PREPARE_FOR_STANDARDIZATION_ERROR
    PREPARE_FOR_VALIDATION_ERROR: typing.ClassVar[PipelineStatus]  # value = rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.PREPARE_FOR_VALIDATION_ERROR
    PROTONATION_CHANGED: typing.ClassVar[PipelineStatus]  # value = rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.PROTONATION_CHANGED
    STANDARDIZATION_ERROR: typing.ClassVar[PipelineStatus]  # value = rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.STANDARDIZATION_ERROR
    STEREO_VALIDATION_ERROR: typing.ClassVar[PipelineStatus]  # value = rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.STEREO_VALIDATION_ERROR
    STRUCTURE_MODIFICATION: typing.ClassVar[PipelineStatus]  # value = rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.STRUCTURE_MODIFICATION
    VALIDATION_ERROR: typing.ClassVar[PipelineStatus]  # value = rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.VALIDATION_ERROR
    __slots__: typing.ClassVar[tuple] = tuple()
    names: typing.ClassVar[dict]  # value = {'NO_EVENT': rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.NO_EVENT, 'INPUT_ERROR': rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.INPUT_ERROR, 'PREPARE_FOR_VALIDATION_ERROR': rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.PREPARE_FOR_VALIDATION_ERROR, 'FEATURES_VALIDATION_ERROR': rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.FEATURES_VALIDATION_ERROR, 'BASIC_VALIDATION_ERROR': rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.BASIC_VALIDATION_ERROR, 'IS2D_VALIDATION_ERROR': rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.IS2D_VALIDATION_ERROR, 'LAYOUT2D_VALIDATION_ERROR': rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.LAYOUT2D_VALIDATION_ERROR, 'STEREO_VALIDATION_ERROR': rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.STEREO_VALIDATION_ERROR, 'VALIDATION_ERROR': rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.VALIDATION_ERROR, 'PREPARE_FOR_STANDARDIZATION_ERROR': rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.PREPARE_FOR_STANDARDIZATION_ERROR, 'METAL_STANDARDIZATION_ERROR': rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.METAL_STANDARDIZATION_ERROR, 'NORMALIZER_STANDARDIZATION_ERROR': rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.NORMALIZER_STANDARDIZATION_ERROR, 'FRAGMENT_STANDARDIZATION_ERROR': rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.FRAGMENT_STANDARDIZATION_ERROR, 'CHARGE_STANDARDIZATION_ERROR': rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.CHARGE_STANDARDIZATION_ERROR, 'STANDARDIZATION_ERROR': rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.STANDARDIZATION_ERROR, 'OUTPUT_ERROR': rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.OUTPUT_ERROR, 'PIPELINE_ERROR': rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.PIPELINE_ERROR, 'METALS_DISCONNECTED': rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.METALS_DISCONNECTED, 'NORMALIZATION_APPLIED': rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.NORMALIZATION_APPLIED, 'FRAGMENTS_REMOVED': rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.FRAGMENTS_REMOVED, 'PROTONATION_CHANGED': rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.PROTONATION_CHANGED, 'STRUCTURE_MODIFICATION': rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.STRUCTURE_MODIFICATION}
    values: typing.ClassVar[dict]  # value = {0: rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.NO_EVENT, 1: rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.INPUT_ERROR, 2: rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.PREPARE_FOR_VALIDATION_ERROR, 4: rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.FEATURES_VALIDATION_ERROR, 8: rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.BASIC_VALIDATION_ERROR, 16: rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.IS2D_VALIDATION_ERROR, 32: rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.LAYOUT2D_VALIDATION_ERROR, 64: rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.STEREO_VALIDATION_ERROR, 124: rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.VALIDATION_ERROR, 128: rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.PREPARE_FOR_STANDARDIZATION_ERROR, 256: rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.METAL_STANDARDIZATION_ERROR, 512: rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.NORMALIZER_STANDARDIZATION_ERROR, 1024: rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.FRAGMENT_STANDARDIZATION_ERROR, 2048: rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.CHARGE_STANDARDIZATION_ERROR, 3840: rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.STANDARDIZATION_ERROR, 4096: rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.OUTPUT_ERROR, 8191: rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.PIPELINE_ERROR, 8388608: rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.METALS_DISCONNECTED, 16777216: rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.NORMALIZATION_APPLIED, 33554432: rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.FRAGMENTS_REMOVED, 67108864: rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.PROTONATION_CHANGED, 125829120: rdkix.Chem.MolStandardize.rdMolStandardize.PipelineStatus.STRUCTURE_MODIFICATION}
class RDKixValidation(ValidationMethod):
    __instance_size__: typing.ClassVar[int] = 40
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64)
        """
    @typing.overload
    def __init__(self, allowEmptyMolecules: bool = False) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64 [,bool=False])
        """
    @property
    def allowEmptyMolecules(*args, **kwargs):
        ...
    @allowEmptyMolecules.setter
    def allowEmptyMolecules(*args, **kwargs):
        ...
class Reionizer(Boost.Python.instance):
    __instance_size__: typing.ClassVar[int] = 56
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64)
        """
    @typing.overload
    def __init__(self, acidbaseFile: str) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64,class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >)
        """
    @typing.overload
    def __init__(self, acidbaseFile: str, ccs: typing.Any) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64,class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >,class std::vector<struct RDKix::MolStandardize::ChargeCorrection,class std::allocator<struct RDKix::MolStandardize::ChargeCorrection> >)
        """
    def reionize(self, mol: Mol) -> rdkix.Chem.Mol:
        """
            C++ signature :
                class RDKix::ROMol * __ptr64 reionize(class RDKix::MolStandardize::Reionizer {lvalue},class RDKix::ROMol)
        """
    def reionizeInPlace(self, mol: Mol) -> None:
        """
            modifies the input molecule
        
            C++ signature :
                void reionizeInPlace(class RDKix::MolStandardize::Reionizer {lvalue},class RDKix::ROMol {lvalue})
        """
class SmilesTautomerMap(Boost.Python.instance):
    """
    maps SMILES strings to the respective Tautomer objects
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
    def __contains__(self, item: typing.Any) -> bool:
        """
            C++ signature :
                bool __contains__(class std::map<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >,class RDKix::MolStandardize::Tautomer,struct std::less<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > >,class std::allocator<struct std::pair<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > const ,class RDKix::MolStandardize::Tautomer> > > {lvalue},struct _object * __ptr64)
        """
    def __delitem__(self, item: typing.Any) -> None:
        """
            C++ signature :
                void __delitem__(class std::map<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >,class RDKix::MolStandardize::Tautomer,struct std::less<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > >,class std::allocator<struct std::pair<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > const ,class RDKix::MolStandardize::Tautomer> > > {lvalue},struct _object * __ptr64)
        """
    def __getitem__(self, item: typing.Any) -> typing.Any:
        """
            C++ signature :
                class boost::python::api::object __getitem__(struct boost::python::back_reference<class std::map<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >,class RDKix::MolStandardize::Tautomer,struct std::less<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > >,class std::allocator<struct std::pair<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > const ,class RDKix::MolStandardize::Tautomer> > > & __ptr64>,struct _object * __ptr64)
        """
    def __iter__(self) -> typing.Any:
        """
            C++ signature :
                struct boost::python::objects::iterator_range<struct boost::python::return_value_policy<struct boost::python::return_by_value,struct boost::python::default_call_policies>,class std::_Tree_iterator<class std::_Tree_val<struct std::_Tree_simple_types<struct std::pair<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > const ,class RDKix::MolStandardize::Tautomer> > > > > __iter__(struct boost::python::back_reference<class std::map<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >,class RDKix::MolStandardize::Tautomer,struct std::less<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > >,class std::allocator<struct std::pair<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > const ,class RDKix::MolStandardize::Tautomer> > > & __ptr64>)
        """
    def __len__(self) -> int:
        """
            C++ signature :
                unsigned __int64 __len__(class std::map<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >,class RDKix::MolStandardize::Tautomer,struct std::less<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > >,class std::allocator<struct std::pair<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > const ,class RDKix::MolStandardize::Tautomer> > > {lvalue})
        """
    def __setitem__(self, item: typing.Any, value: typing.Any) -> None:
        """
            C++ signature :
                void __setitem__(class std::map<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >,class RDKix::MolStandardize::Tautomer,struct std::less<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > >,class std::allocator<struct std::pair<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > const ,class RDKix::MolStandardize::Tautomer> > > {lvalue},struct _object * __ptr64,struct _object * __ptr64)
        """
    def items(self) -> tuple:
        """
            C++ signature :
                class boost::python::tuple items(class std::map<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >,class RDKix::MolStandardize::Tautomer,struct std::less<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > >,class std::allocator<struct std::pair<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > const ,class RDKix::MolStandardize::Tautomer> > >)
        """
    def keys(self) -> tuple:
        """
            C++ signature :
                class boost::python::tuple keys(class std::map<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >,class RDKix::MolStandardize::Tautomer,struct std::less<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > >,class std::allocator<struct std::pair<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > const ,class RDKix::MolStandardize::Tautomer> > >)
        """
    def values(self) -> tuple:
        """
            C++ signature :
                class boost::python::tuple values(class std::map<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >,class RDKix::MolStandardize::Tautomer,struct std::less<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > >,class std::allocator<struct std::pair<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > const ,class RDKix::MolStandardize::Tautomer> > >)
        """
class StereoValidation(ValidationMethod):
    __instance_size__: typing.ClassVar[int] = 32
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64)
        """
class Tautomer(Boost.Python.instance):
    """
    used to hold the aromatic and kekulized versions of each tautomer
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
    @property
    def kekulized(*args, **kwargs):
        """
        kekulized version of the tautomer
        """
    @property
    def tautomer(*args, **kwargs):
        """
        aromatic version of the tautomer
        """
class TautomerEnumerator(Boost.Python.instance):
    tautomerScoreVersion: typing.ClassVar[str] = '1.0.0'
    @staticmethod
    def ScoreTautomer(mol: Mol) -> int:
        """
            returns the score for a tautomer using the default scoring scheme.
        
            C++ signature :
                int ScoreTautomer(class RDKix::ROMol)
        """
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    @typing.overload
    def Canonicalize(self, mol: Mol) -> rdkix.Chem.Mol:
        """
            Returns the canonical tautomer for a molecule.
            
              The default scoring scheme is inspired by the publication:
              M. Sitzmann et al., “Tautomerism in Large Databases.”, JCAMD 24:521 (2010)
              https://doi.org/10.1007/s10822-010-9346-4
            
              Note that the canonical tautomer is very likely not the most stable tautomer
              for any given conditions. The default scoring rules are designed to produce
              "reasonable" tautomers, but the primary concern is that the results are
              canonical: you always get the same canonical tautomer for a molecule
              regardless of what the input tautomer or atom ordering were.
        
            C++ signature :
                class RDKix::ROMol * __ptr64 Canonicalize(class RDKix::MolStandardize::TautomerEnumerator,class RDKix::ROMol)
        """
    @typing.overload
    def Canonicalize(self, mol: Mol, scoreFunc: typing.Any) -> rdkix.Chem.Mol:
        """
            picks the canonical tautomer from an iterable of molecules using a custom scoring function
        
            C++ signature :
                class RDKix::ROMol * __ptr64 Canonicalize(class RDKix::MolStandardize::TautomerEnumerator,class RDKix::ROMol,class boost::python::api::object)
        """
    def Enumerate(self, mol: Mol) -> TautomerEnumeratorResult:
        """
            Generates the tautomers for a molecule.
                         
              The enumeration rules are inspired by the publication:
              M. Sitzmann et al., “Tautomerism in Large Databases.”, JCAMD 24:521 (2010)
              https://doi.org/10.1007/s10822-010-9346-4
              
              Note: the definitions used here are that the atoms modified during
              tautomerization are the atoms at the beginning and end of each tautomer
              transform (the H "donor" and H "acceptor" in the transform) and the bonds
              modified during transformation are any bonds whose order is changed during
              the tautomer transform (these are the bonds between the "donor" and the
              "acceptor").
        
            C++ signature :
                class `anonymous namespace'::PyTautomerEnumeratorResult * __ptr64 Enumerate(class RDKix::MolStandardize::TautomerEnumerator,class RDKix::ROMol)
        """
    def GetCallback(self) -> typing.Any:
        """
            Get the TautomerEnumeratorCallback subclass instance,
            or None if none was set.
        
            C++ signature :
                class boost::python::api::object GetCallback(class RDKix::MolStandardize::TautomerEnumerator)
        """
    def GetMaxTautomers(self) -> int:
        """
            returns the maximum number of tautomers to be generated.
        
            C++ signature :
                unsigned int GetMaxTautomers(class RDKix::MolStandardize::TautomerEnumerator {lvalue})
        """
    def GetMaxTransforms(self) -> int:
        """
            returns the maximum number of transformations to be applied.
        
            C++ signature :
                unsigned int GetMaxTransforms(class RDKix::MolStandardize::TautomerEnumerator {lvalue})
        """
    def GetReassignStereo(self) -> bool:
        """
            returns whether AssignStereochemistry will be called on each tautomer generated by the Enumerate() method.
        
            C++ signature :
                bool GetReassignStereo(class RDKix::MolStandardize::TautomerEnumerator {lvalue})
        """
    def GetRemoveBondStereo(self) -> bool:
        """
            returns whether stereochemistry information will be removed from double bonds involved in tautomerism.
        
            C++ signature :
                bool GetRemoveBondStereo(class RDKix::MolStandardize::TautomerEnumerator {lvalue})
        """
    def GetRemoveSp3Stereo(self) -> bool:
        """
            returns whether stereochemistry information will be removed from sp3 atoms involved in tautomerism.
        
            C++ signature :
                bool GetRemoveSp3Stereo(class RDKix::MolStandardize::TautomerEnumerator {lvalue})
        """
    @typing.overload
    def PickCanonical(self, iterable: typing.Any) -> rdkix.Chem.Mol:
        """
            picks the canonical tautomer from an iterable of molecules
        
            C++ signature :
                class RDKix::ROMol * __ptr64 PickCanonical(class RDKix::MolStandardize::TautomerEnumerator,class boost::python::api::object)
        """
    @typing.overload
    def PickCanonical(self, iterable: typing.Any, scoreFunc: typing.Any) -> rdkix.Chem.Mol:
        """
            returns the canonical tautomer for a molecule using a custom scoring function
        
            C++ signature :
                class RDKix::ROMol * __ptr64 PickCanonical(class RDKix::MolStandardize::TautomerEnumerator,class boost::python::api::object,class boost::python::api::object)
        """
    def SetCallback(self, callback: typing.Any) -> None:
        """
            Pass an instance of a class derived from
            TautomerEnumeratorCallback, which must implement the
            __call__() method.
        
            C++ signature :
                void SetCallback(class RDKix::MolStandardize::TautomerEnumerator {lvalue},struct _object * __ptr64)
        """
    def SetMaxTautomers(self, maxTautomers: int) -> None:
        """
            set the maximum number of tautomers to be generated.
        
            C++ signature :
                void SetMaxTautomers(class RDKix::MolStandardize::TautomerEnumerator {lvalue},unsigned int)
        """
    def SetMaxTransforms(self, maxTransforms: int) -> None:
        """
            set the maximum number of transformations to be applied. This limit is usually hit earlier than the maxTautomers limit and leads to a more linear scaling of CPU time with increasing number of tautomeric centers (see Sitzmann et al.).
        
            C++ signature :
                void SetMaxTransforms(class RDKix::MolStandardize::TautomerEnumerator {lvalue},unsigned int)
        """
    def SetReassignStereo(self, reassignStereo: bool) -> None:
        """
            set to True if you wish AssignStereochemistry to be called on each tautomer generated by the Enumerate() method. This defaults to True.
        
            C++ signature :
                void SetReassignStereo(class RDKix::MolStandardize::TautomerEnumerator {lvalue},bool)
        """
    def SetRemoveBondStereo(self, removeBondStereo: bool) -> None:
        """
            set to True if you wish stereochemistry information to be removed from double bonds involved in tautomerism. This means that enols will lose their E/Z stereochemistry after going through tautomer enumeration because of the keto-enolic tautomerism. This defaults to True in the RDKix and also in the workflow described by Sitzmann et al.
        
            C++ signature :
                void SetRemoveBondStereo(class RDKix::MolStandardize::TautomerEnumerator {lvalue},bool)
        """
    def SetRemoveSp3Stereo(self, removeSp3Stereo: bool) -> None:
        """
            set to True if you wish stereochemistry information to be removed from sp3 atoms involved in tautomerism. This means that S-aminoacids will lose their stereochemistry after going through tautomer enumeration because of the amido-imidol tautomerism. This defaults to True in RDKix, and to False in the workflow described by Sitzmann et al.
        
            C++ signature :
                void SetRemoveSp3Stereo(class RDKix::MolStandardize::TautomerEnumerator {lvalue},bool)
        """
    @typing.overload
    def __init__(self) -> typing.Any:
        """
            C++ signature :
                void * __ptr64 __init__(class boost::python::api::object)
        """
    @typing.overload
    def __init__(self, arg1: CleanupParameters) -> typing.Any:
        """
            C++ signature :
                void * __ptr64 __init__(class boost::python::api::object,struct RDKix::MolStandardize::CleanupParameters)
        """
    @typing.overload
    def __init__(self, arg1: TautomerEnumerator) -> typing.Any:
        """
            C++ signature :
                void * __ptr64 __init__(class boost::python::api::object,class RDKix::MolStandardize::TautomerEnumerator)
        """
class TautomerEnumeratorCallback(Boost.Python.instance):
    """
    Create a derived class from this abstract base class and
        implement the __call__() method.
        The __call__() method is called in the innermost loop of the
        algorithm, and provides a mechanism to monitor or stop
        its progress.
    
        To have your callback called, pass an instance of your
        derived class to TautomerEnumerator.SetCallback()
    """
    __instance_size__: typing.ClassVar[int] = 56
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    @typing.overload
    def __call__(self, mol: Mol, res: typing.Any) -> bool:
        """
            This must be implemented in the derived class. Return True if the tautomer enumeration should continue; False if the tautomer enumeration should stop.
            
        
            C++ signature :
                bool __call__(class `anonymous namespace'::PyTautomerEnumeratorCallback {lvalue},class RDKix::ROMol,class RDKix::MolStandardize::TautomerEnumeratorResult)
        """
    @typing.overload
    def __call__(self, arg1: Mol, arg2: typing.Any) -> None:
        """
            C++ signature :
                void __call__(class `anonymous namespace'::PyTautomerEnumeratorCallback {lvalue},class RDKix::ROMol,class RDKix::MolStandardize::TautomerEnumeratorResult)
        """
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64)
        """
class TautomerEnumeratorResult(Boost.Python.instance):
    """
    used to return tautomer enumeration results
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
    def __call__(self) -> MOL_SPTR_VECT:
        """
            tautomers generated by the enumerator
        
            C++ signature :
                class std::vector<class boost::shared_ptr<class RDKix::ROMol>,class std::allocator<class boost::shared_ptr<class RDKix::ROMol> > > const * __ptr64 __call__(class `anonymous namespace'::PyTautomerEnumeratorResult {lvalue})
        """
    def __getitem__(self, pos: int) -> rdkix.Chem.Mol:
        """
            C++ signature :
                class RDKix::ROMol * __ptr64 __getitem__(class `anonymous namespace'::PyTautomerEnumeratorResult {lvalue},int)
        """
    def __iter__(self) -> typing.Any:
        """
            C++ signature :
                struct boost::python::objects::iterator_range<struct boost::python::return_value_policy<struct boost::python::return_by_value,struct boost::python::default_call_policies>,class RDKix::MolStandardize::TautomerEnumeratorResult::const_iterator> __iter__(struct boost::python::back_reference<class `anonymous namespace'::PyTautomerEnumeratorResult & __ptr64>)
        """
    def __len__(self) -> int:
        """
            C++ signature :
                int __len__(class `anonymous namespace'::PyTautomerEnumeratorResult {lvalue})
        """
    @property
    def modifiedAtoms(*args, **kwargs):
        """
        tuple of atom indices modified by the transforms
        """
    @property
    def modifiedBonds(*args, **kwargs):
        """
        tuple of bond indices modified by the transforms
        """
    @property
    def smiles(*args, **kwargs):
        """
        SMILES of tautomers generated by the enumerator
        """
    @property
    def smilesTautomerMap(*args, **kwargs):
        """
        dictionary mapping SMILES strings to the respective Tautomer objects
        """
    @property
    def status(*args, **kwargs):
        """
        whether the enumeration completed or not; see TautomerEnumeratorStatus for possible values
        """
    @property
    def tautomers(*args, **kwargs):
        """
        tautomers generated by the enumerator
        """
class TautomerEnumeratorStatus(Boost.Python.enum):
    Canceled: typing.ClassVar[TautomerEnumeratorStatus]  # value = rdkix.Chem.MolStandardize.rdMolStandardize.TautomerEnumeratorStatus.Canceled
    Completed: typing.ClassVar[TautomerEnumeratorStatus]  # value = rdkix.Chem.MolStandardize.rdMolStandardize.TautomerEnumeratorStatus.Completed
    MaxTautomersReached: typing.ClassVar[TautomerEnumeratorStatus]  # value = rdkix.Chem.MolStandardize.rdMolStandardize.TautomerEnumeratorStatus.MaxTautomersReached
    MaxTransformsReached: typing.ClassVar[TautomerEnumeratorStatus]  # value = rdkix.Chem.MolStandardize.rdMolStandardize.TautomerEnumeratorStatus.MaxTransformsReached
    __slots__: typing.ClassVar[tuple] = tuple()
    names: typing.ClassVar[dict]  # value = {'Completed': rdkix.Chem.MolStandardize.rdMolStandardize.TautomerEnumeratorStatus.Completed, 'MaxTautomersReached': rdkix.Chem.MolStandardize.rdMolStandardize.TautomerEnumeratorStatus.MaxTautomersReached, 'MaxTransformsReached': rdkix.Chem.MolStandardize.rdMolStandardize.TautomerEnumeratorStatus.MaxTransformsReached, 'Canceled': rdkix.Chem.MolStandardize.rdMolStandardize.TautomerEnumeratorStatus.Canceled}
    values: typing.ClassVar[dict]  # value = {0: rdkix.Chem.MolStandardize.rdMolStandardize.TautomerEnumeratorStatus.Completed, 1: rdkix.Chem.MolStandardize.rdMolStandardize.TautomerEnumeratorStatus.MaxTautomersReached, 2: rdkix.Chem.MolStandardize.rdMolStandardize.TautomerEnumeratorStatus.MaxTransformsReached, 3: rdkix.Chem.MolStandardize.rdMolStandardize.TautomerEnumeratorStatus.Canceled}
class Uncharger(Boost.Python.instance):
    __instance_size__: typing.ClassVar[int] = 96
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def __init__(self, canonicalOrder: bool = True, force: bool = False, protonationOnly: bool = False) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64 [,bool=True [,bool=False [,bool=False]]])
        """
    def uncharge(self, mol: Mol) -> rdkix.Chem.Mol:
        """
            C++ signature :
                class RDKix::ROMol * __ptr64 uncharge(class RDKix::MolStandardize::Uncharger {lvalue},class RDKix::ROMol)
        """
    def unchargeInPlace(self, mol: Mol) -> None:
        """
            modifies the input molecule
        
            C++ signature :
                void unchargeInPlace(class RDKix::MolStandardize::Uncharger {lvalue},class RDKix::ROMol {lvalue})
        """
class ValidationMethod(Boost.Python.instance):
    __instance_size__: typing.ClassVar[int] = 40
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64)
        """
    def validate(self, mol: Mol, reportAllFailures: bool = False) -> list:
        """
            C++ signature :
                class boost::python::list validate(class RDKix::MolStandardize::ValidationMethod,class RDKix::ROMol [,bool=False])
        """
class map_indexing_suite_SmilesTautomerMap_entry(Boost.Python.instance):
    __instance_size__: typing.ClassVar[int] = 112
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    @staticmethod
    def __repr__(arg1: map_indexing_suite_SmilesTautomerMap_entry) -> typing.Any:
        """
            C++ signature :
                class boost::python::api::object __repr__(struct std::pair<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > const ,class RDKix::MolStandardize::Tautomer>)
        """
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(struct _object * __ptr64)
        """
    def data(self) -> Tautomer:
        """
            C++ signature :
                class RDKix::MolStandardize::Tautomer data(struct std::pair<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > const ,class RDKix::MolStandardize::Tautomer> {lvalue})
        """
    def key(self) -> str:
        """
            C++ signature :
                class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > key(struct std::pair<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > const ,class RDKix::MolStandardize::Tautomer> {lvalue})
        """
def CHARGE_CORRECTIONS() -> typing.Any:
    """
        C++ signature :
            class std::vector<struct RDKix::MolStandardize::ChargeCorrection,class std::allocator<struct RDKix::MolStandardize::ChargeCorrection> > CHARGE_CORRECTIONS()
    """
def CanonicalTautomer(mol: Mol, params: typing.Any = None) -> rdkix.Chem.Mol:
    """
        Returns the canonical tautomer for the molecule
    
        C++ signature :
            class RDKix::ROMol * __ptr64 CanonicalTautomer(class RDKix::ROMol const * __ptr64 [,class boost::python::api::object=None])
    """
def ChargeParent(mol: Mol, params: typing.Any = None, skipStandardize: bool = False) -> rdkix.Chem.Mol:
    """
        Returns the uncharged version of the largest fragment
    
        C++ signature :
            class RDKix::ROMol * __ptr64 ChargeParent(class RDKix::ROMol const * __ptr64 [,class boost::python::api::object=None [,bool=False]])
    """
@typing.overload
def ChargeParentInPlace(mol: Mol, params: typing.Any = None, skipStandardize: bool = False) -> None:
    """
        Generates the charge parent in place
    
        C++ signature :
            void ChargeParentInPlace(class RDKix::ROMol * __ptr64 [,class boost::python::api::object=None [,bool=False]])
    """
@typing.overload
def ChargeParentInPlace(mols: typing.Any, numThreads: int, params: typing.Any = None, skipStandardize: bool = False) -> None:
    """
        Generates the chargeparent in place for multiple molecules
    
        C++ signature :
            void ChargeParentInPlace(class boost::python::api::object,int [,class boost::python::api::object=None [,bool=False]])
    """
def Cleanup(mol: Mol, params: typing.Any = None) -> rdkix.Chem.Mol:
    """
        Standardizes a molecule
    
        C++ signature :
            class RDKix::ROMol * __ptr64 Cleanup(class RDKix::ROMol const * __ptr64 [,class boost::python::api::object=None])
    """
@typing.overload
def CleanupInPlace(mol: Mol, params: typing.Any = None) -> None:
    """
        Standardizes a molecule in place
    
        C++ signature :
            void CleanupInPlace(class RDKix::ROMol * __ptr64 [,class boost::python::api::object=None])
    """
@typing.overload
def CleanupInPlace(mols: typing.Any, numThreads: int, params: typing.Any = None) -> None:
    """
        Standardizes multiple molecules in place
    
        C++ signature :
            void CleanupInPlace(class boost::python::api::object,int [,class boost::python::api::object=None])
    """
def DisconnectOrganometallics(mol: Mol, params: typing.Any = None) -> rdkix.Chem.Mol:
    """
        Returns the molecule disconnected using the organometallics rules.
    
        C++ signature :
            class RDKix::ROMol * __ptr64 DisconnectOrganometallics(class RDKix::ROMol {lvalue} [,class boost::python::api::object=None])
    """
def DisconnectOrganometallicsInPlace(mol: Mol, params: typing.Any = None) -> None:
    """
        Disconnects the molecule using the organometallics rules, modifies the input molecule
    
        C++ signature :
            void DisconnectOrganometallicsInPlace(class RDKix::ROMol * __ptr64 [,class boost::python::api::object=None])
    """
def FragmentParent(mol: Mol, params: typing.Any = None, skipStandardize: bool = False) -> rdkix.Chem.Mol:
    """
        Returns the largest fragment after doing a cleanup
    
        C++ signature :
            class RDKix::ROMol * __ptr64 FragmentParent(class RDKix::ROMol const * __ptr64 [,class boost::python::api::object=None [,bool=False]])
    """
@typing.overload
def FragmentParentInPlace(mol: Mol, params: typing.Any = None, skipStandardize: bool = False) -> None:
    """
        Generates the largest fragment in place
    
        C++ signature :
            void FragmentParentInPlace(class RDKix::ROMol * __ptr64 [,class boost::python::api::object=None [,bool=False]])
    """
@typing.overload
def FragmentParentInPlace(mols: typing.Any, numThreads: int, params: typing.Any = None, skipStandardize: bool = False) -> None:
    """
        Generates the largest fragment in place for multiple molecules
    
        C++ signature :
            void FragmentParentInPlace(class boost::python::api::object,int [,class boost::python::api::object=None [,bool=False]])
    """
def FragmentRemoverFromData(fragmentData: str, leave_last: bool = True, skip_if_all_match: bool = False) -> FragmentRemover:
    """
        creates a FragmentRemover from a string containing parameter data
    
        C++ signature :
            class RDKix::MolStandardize::FragmentRemover * __ptr64 FragmentRemoverFromData(class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > [,bool=True [,bool=False]])
    """
def GetV1TautomerEnumerator() -> TautomerEnumerator:
    """
        return a TautomerEnumerator using v1 of the enumeration rules
    
        C++ signature :
            class RDKix::MolStandardize::TautomerEnumerator * __ptr64 GetV1TautomerEnumerator()
    """
def IsotopeParent(mol: Mol, params: typing.Any = None, skipStandardize: bool = False) -> rdkix.Chem.Mol:
    """
        removes all isotopes specifications from the given molecule
    
        C++ signature :
            class RDKix::ROMol * __ptr64 IsotopeParent(class RDKix::ROMol const * __ptr64 [,class boost::python::api::object=None [,bool=False]])
    """
@typing.overload
def IsotopeParentInPlace(mol: Mol, params: typing.Any = None, skipStandardize: bool = False) -> None:
    """
        Generates the isotope parent in place
    
        C++ signature :
            void IsotopeParentInPlace(class RDKix::ROMol * __ptr64 [,class boost::python::api::object=None [,bool=False]])
    """
@typing.overload
def IsotopeParentInPlace(mols: typing.Any, numThreads: int, params: typing.Any = None, skipStandardize: bool = False) -> None:
    """
        Generates the isotope parent in place for multiple molecules
    
        C++ signature :
            void IsotopeParentInPlace(class boost::python::api::object,int [,class boost::python::api::object=None [,bool=False]])
    """
def Normalize(mol: Mol, params: typing.Any = None) -> rdkix.Chem.Mol:
    """
        Applies a series of standard transformations to correct functional groups and recombine charges
    
        C++ signature :
            class RDKix::ROMol * __ptr64 Normalize(class RDKix::ROMol const * __ptr64 [,class boost::python::api::object=None])
    """
@typing.overload
def NormalizeInPlace(mol: Mol, params: typing.Any = None) -> None:
    """
        Applies a series of standard transformations to correct functional groups and recombine charges, modifies the input molecule
    
        C++ signature :
            void NormalizeInPlace(class RDKix::ROMol * __ptr64 [,class boost::python::api::object=None])
    """
@typing.overload
def NormalizeInPlace(mols: typing.Any, numThreads: int, params: typing.Any = None) -> None:
    """
        Normalizes multiple molecules in place
    
        C++ signature :
            void NormalizeInPlace(class boost::python::api::object,int [,class boost::python::api::object=None])
    """
def NormalizerFromData(paramData: str, params: CleanupParameters) -> Normalizer:
    """
        creates a Normalizer from a string containing normalization SMARTS
    
        C++ signature :
            class RDKix::MolStandardize::Normalizer * __ptr64 NormalizerFromData(class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >,struct RDKix::MolStandardize::CleanupParameters)
    """
def NormalizerFromParams(params: CleanupParameters) -> Normalizer:
    """
        creates a Normalizer from CleanupParameters
    
        C++ signature :
            class RDKix::MolStandardize::Normalizer * __ptr64 NormalizerFromParams(struct RDKix::MolStandardize::CleanupParameters)
    """
def Reionize(mol: Mol, params: typing.Any = None) -> rdkix.Chem.Mol:
    """
        Ensures the strongest acid groups are charged first
    
        C++ signature :
            class RDKix::ROMol * __ptr64 Reionize(class RDKix::ROMol const * __ptr64 [,class boost::python::api::object=None])
    """
@typing.overload
def ReionizeInPlace(mol: Mol, params: typing.Any = None) -> None:
    """
        Ensures the strongest acid groups are charged first, modifies the input molecule
    
        C++ signature :
            void ReionizeInPlace(class RDKix::ROMol * __ptr64 [,class boost::python::api::object=None])
    """
@typing.overload
def ReionizeInPlace(mols: typing.Any, numThreads: int, params: typing.Any = None) -> None:
    """
        Reionizes multiple molecules in place
    
        C++ signature :
            void ReionizeInPlace(class boost::python::api::object,int [,class boost::python::api::object=None])
    """
def ReionizerFromData(paramData: str, chargeCorrections: typing.Any = []) -> Reionizer:
    """
        creates a reionizer from a string containing parameter data and a list of charge corrections
    
        C++ signature :
            class RDKix::MolStandardize::Reionizer * __ptr64 ReionizerFromData(class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > [,class boost::python::api::object=[]])
    """
def RemoveFragments(mol: Mol, params: typing.Any = None) -> rdkix.Chem.Mol:
    """
        Removes fragments from the molecule
    
        C++ signature :
            class RDKix::ROMol * __ptr64 RemoveFragments(class RDKix::ROMol const * __ptr64 [,class boost::python::api::object=None])
    """
@typing.overload
def RemoveFragmentsInPlace(mol: Mol, params: typing.Any = None) -> None:
    """
        Removes fragments from the molecule, modifies the input molecule
    
        C++ signature :
            void RemoveFragmentsInPlace(class RDKix::ROMol * __ptr64 [,class boost::python::api::object=None])
    """
@typing.overload
def RemoveFragmentsInPlace(mols: typing.Any, numThreads: int, params: typing.Any = None) -> None:
    """
        Removes fragments from multiple molecules in place
    
        C++ signature :
            void RemoveFragmentsInPlace(class boost::python::api::object,int [,class boost::python::api::object=None])
    """
def StandardizeSmiles(smiles: str) -> str:
    """
        Convenience function for standardizing a SMILES
    
        C++ signature :
            class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > StandardizeSmiles(class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >)
    """
def StereoParent(mol: Mol, params: typing.Any = None, skipStandardize: bool = False) -> rdkix.Chem.Mol:
    """
        Generates the largest fragment in place for multiple molecules
    
        C++ signature :
            class RDKix::ROMol * __ptr64 StereoParent(class RDKix::ROMol const * __ptr64 [,class boost::python::api::object=None [,bool=False]])
    """
@typing.overload
def StereoParentInPlace(mol: Mol, params: typing.Any = None, skipStandardize: bool = False) -> None:
    """
        Generates the stereo parent in place
    
        C++ signature :
            void StereoParentInPlace(class RDKix::ROMol * __ptr64 [,class boost::python::api::object=None [,bool=False]])
    """
@typing.overload
def StereoParentInPlace(mols: typing.Any, numThreads: int, params: typing.Any = None, skipStandardize: bool = False) -> None:
    """
        Generates the stereo parent in place for multiple molecules
    
        C++ signature :
            void StereoParentInPlace(class boost::python::api::object,int [,class boost::python::api::object=None [,bool=False]])
    """
def SuperParent(mol: Mol, params: typing.Any = None, skipStandardize: bool = False) -> rdkix.Chem.Mol:
    """
        Returns the super parent. The super parent is the fragment, charge, isotope, stereo, and tautomer parent of the molecule.
    
        C++ signature :
            class RDKix::ROMol * __ptr64 SuperParent(class RDKix::ROMol const * __ptr64 [,class boost::python::api::object=None [,bool=False]])
    """
@typing.overload
def SuperParentInPlace(mol: Mol, params: typing.Any = None, skipStandardize: bool = False) -> None:
    """
        Generates the super parent in place
    
        C++ signature :
            void SuperParentInPlace(class RDKix::ROMol * __ptr64 [,class boost::python::api::object=None [,bool=False]])
    """
@typing.overload
def SuperParentInPlace(mols: typing.Any, numThreads: int, params: typing.Any = None, skipStandardize: bool = False) -> None:
    """
        Generates the super parent in place for multiple molecules
    
        C++ signature :
            void SuperParentInPlace(class boost::python::api::object,int [,class boost::python::api::object=None [,bool=False]])
    """
def TautomerParent(mol: Mol, params: typing.Any = None, skipStandardize: bool = False) -> rdkix.Chem.Mol:
    """
        Returns the tautomer parent of a given molecule. The fragment parent is the standardized canonical tautomer of the molecule
    
        C++ signature :
            class RDKix::ROMol * __ptr64 TautomerParent(class RDKix::ROMol const * __ptr64 [,class boost::python::api::object=None [,bool=False]])
    """
@typing.overload
def TautomerParentInPlace(mol: Mol, params: typing.Any = None, skipStandardize: bool = False) -> None:
    """
        Generates the tautomer parent in place
    
        C++ signature :
            void TautomerParentInPlace(class RDKix::ROMol * __ptr64 [,class boost::python::api::object=None [,bool=False]])
    """
@typing.overload
def TautomerParentInPlace(mols: typing.Any, numThreads: int, params: typing.Any = None, skipStandardize: bool = False) -> None:
    """
        Generates the tautomer parent in place for multiple molecules
    
        C++ signature :
            void TautomerParentInPlace(class boost::python::api::object,int [,class boost::python::api::object=None [,bool=False]])
    """
def UpdateParamsFromJSON(params: CleanupParameters, json: str) -> None:
    """
        updates the cleanup parameters from the provided JSON string
    
        C++ signature :
            void UpdateParamsFromJSON(struct RDKix::MolStandardize::CleanupParameters {lvalue},class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >)
    """
def ValidateSmiles(mol: str) -> list:
    """
        C++ signature :
            class boost::python::list ValidateSmiles(class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >)
    """
