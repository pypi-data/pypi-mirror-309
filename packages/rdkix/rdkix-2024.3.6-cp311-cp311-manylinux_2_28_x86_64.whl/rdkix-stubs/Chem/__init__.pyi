"""
 A module for molecules and stuff

 see Chem/index.html in the doc tree for documentation

"""
from __future__ import annotations
from rdkix.Chem.inchi import InchiReadWriteError
from rdkix.Chem.inchi import InchiToInchiKey
from rdkix.Chem.inchi import MolBlockToInchi
from rdkix.Chem.inchi import MolBlockToInchiAndAuxInfo
from rdkix.Chem.inchi import MolFromInchi
from rdkix.Chem.inchi import MolToInchi
from rdkix.Chem.inchi import MolToInchiAndAuxInfo
from rdkix.Chem.inchi import MolToInchiKey
from rdkix.Chem.rdMolInterchange import JSONParseParameters
from rdkix.Chem.rdMolInterchange import JSONWriteParameters
from rdkix.Chem.rdchem import Atom
from rdkix.Chem.rdchem import AtomKekulizeException
from rdkix.Chem.rdchem import AtomMonomerInfo
from rdkix.Chem.rdchem import AtomMonomerType
from rdkix.Chem.rdchem import AtomPDBResidueInfo
from rdkix.Chem.rdchem import AtomSanitizeException
from rdkix.Chem.rdchem import AtomValenceException
from rdkix.Chem.rdchem import Bond
from rdkix.Chem.rdchem import BondDir
from rdkix.Chem.rdchem import BondStereo
from rdkix.Chem.rdchem import BondType
from rdkix.Chem.rdchem import ChiralType
from rdkix.Chem.rdchem import CompositeQueryType
from rdkix.Chem.rdchem import Conformer
from rdkix.Chem.rdchem import EditableMol
from rdkix.Chem.rdchem import FixedMolSizeMolBundle
from rdkix.Chem.rdchem import HybridizationType
from rdkix.Chem.rdchem import KekulizeException
from rdkix.Chem.rdchem import Mol
from rdkix.Chem.rdchem import MolBundle
from rdkix.Chem.rdchem import MolSanitizeException
from rdkix.Chem.rdchem import PeriodicTable
from rdkix.Chem.rdchem import PropertyPickleOptions
from rdkix.Chem.rdchem import QueryAtom
from rdkix.Chem.rdchem import QueryBond
from rdkix.Chem.rdchem import RWMol
from rdkix.Chem.rdchem import ResonanceFlags
from rdkix.Chem.rdchem import ResonanceMolSupplier
from rdkix.Chem.rdchem import ResonanceMolSupplierCallback
from rdkix.Chem.rdchem import RingInfo
from rdkix.Chem.rdchem import StereoDescriptor
from rdkix.Chem.rdchem import StereoGroup
from rdkix.Chem.rdchem import StereoGroupType
from rdkix.Chem.rdchem import StereoGroup_vect
from rdkix.Chem.rdchem import StereoInfo
from rdkix.Chem.rdchem import StereoSpecified
from rdkix.Chem.rdchem import StereoType
from rdkix.Chem.rdchem import SubstanceGroup
from rdkix.Chem.rdchem import SubstanceGroupAttach
from rdkix.Chem.rdchem import SubstanceGroupCState
from rdkix.Chem.rdchem import SubstanceGroup_VECT
from rdkix.Chem.rdchem import SubstructMatchParameters
from rdkix.Chem.rdmolfiles import CXSmilesFields
from rdkix.Chem.rdmolfiles import ForwardSDMolSupplier
from rdkix.Chem.rdmolfiles import MaeMolSupplier
from rdkix.Chem.rdmolfiles import MaeWriter
from rdkix.Chem.rdmolfiles import MolWriterParams
from rdkix.Chem.rdmolfiles import MultithreadedSDMolSupplier
from rdkix.Chem.rdmolfiles import MultithreadedSmilesMolSupplier
from rdkix.Chem.rdmolfiles import PDBWriter
from rdkix.Chem.rdmolfiles import RestoreBondDirOption
from rdkix.Chem.rdmolfiles import SDMolSupplier
from rdkix.Chem.rdmolfiles import SDWriter
from rdkix.Chem.rdmolfiles import SmartsParserParams
from rdkix.Chem.rdmolfiles import SmilesMolSupplier
from rdkix.Chem.rdmolfiles import SmilesParserParams
from rdkix.Chem.rdmolfiles import SmilesWriteParams
from rdkix.Chem.rdmolfiles import SmilesWriter
from rdkix.Chem.rdmolfiles import TDTMolSupplier
from rdkix.Chem.rdmolfiles import TDTWriter
from rdkix.Chem.rdmolops import AdjustQueryParameters
from rdkix.Chem.rdmolops import AdjustQueryWhichFlags
from rdkix.Chem.rdmolops import AromaticityModel
from rdkix.Chem.rdmolops import BondWedgingParameters
from rdkix.Chem.rdmolops import MolzipLabel
from rdkix.Chem.rdmolops import MolzipParams
from rdkix.Chem.rdmolops import RemoveHsParameters
from rdkix.Chem.rdmolops import SanitizeFlags
from rdkix.Chem.rdmolops import StereoBondThresholds
from rdkix import DataStructs
from rdkix.Geometry import rdGeometry
from rdkix import RDConfig
from rdkix import rdBase
from .inchi import *
from .rdCIPLabeler import *
from .rdCoordGen import *
from .rdMolInterchange import *
from .rdchem import *
from .rdinchi import *
from .rdmolfiles import *
from .rdmolops import *
__all__ = ['ADJUST_IGNOREALL', 'ADJUST_IGNORECHAINS', 'ADJUST_IGNOREDUMMIES', 'ADJUST_IGNOREMAPPED', 'ADJUST_IGNORENONDUMMIES', 'ADJUST_IGNORENONE', 'ADJUST_IGNORERINGS', 'ALLOW_CHARGE_SEPARATION', 'ALLOW_INCOMPLETE_OCTETS', 'AROMATICITY_CUSTOM', 'AROMATICITY_DEFAULT', 'AROMATICITY_MDL', 'AROMATICITY_RDKIX', 'AROMATICITY_SIMPLE', 'AdjustQueryParameters', 'AdjustQueryWhichFlags', 'AllProps', 'AromaticityModel', 'Atom', 'AtomKekulizeException', 'AtomMonomerInfo', 'AtomMonomerType', 'AtomPDBResidueInfo', 'AtomProps', 'AtomSanitizeException', 'AtomValenceException', 'Bond', 'BondDir', 'BondProps', 'BondStereo', 'BondType', 'BondWedgingParameters', 'CHI_ALLENE', 'CHI_OCTAHEDRAL', 'CHI_OTHER', 'CHI_SQUAREPLANAR', 'CHI_TETRAHEDRAL', 'CHI_TETRAHEDRAL_CCW', 'CHI_TETRAHEDRAL_CW', 'CHI_TRIGONALBIPYRAMIDAL', 'CHI_UNSPECIFIED', 'COMPOSITE_AND', 'COMPOSITE_OR', 'COMPOSITE_XOR', 'CXSmilesFields', 'CanonSmiles', 'ChiralType', 'CompositeQueryType', 'ComputedProps', 'Conformer', 'ConversionError', 'CoordsAsDouble', 'DataStructs', 'EditableMol', 'FindMolChiralCenters', 'FixedMolSizeMolBundle', 'ForwardSDMolSupplier', 'HybridizationType', 'INCHI_AVAILABLE', 'InchiReadWriteError', 'InchiToInchiKey', 'JSONParseParameters', 'JSONWriteParameters', 'KEKULE_ALL', 'KekulizeException', 'LayeredFingerprint_substructLayers', 'MaeMolSupplier', 'MaeWriter', 'Mol', 'MolBlockToInchi', 'MolBlockToInchiAndAuxInfo', 'MolBundle', 'MolFromInchi', 'MolProps', 'MolSanitizeException', 'MolToInchi', 'MolToInchiAndAuxInfo', 'MolToInchiKey', 'MolWriterParams', 'MolzipLabel', 'MolzipParams', 'MultithreadedSDMolSupplier', 'MultithreadedSmilesMolSupplier', 'NoConformers', 'NoProps', 'PDBWriter', 'PeriodicTable', 'PrivateProps', 'PropertyPickleOptions', 'QueryAtom', 'QueryAtomData', 'QueryBond', 'QuickSmartsMatch', 'RDConfig', 'RWMol', 'RemoveHsParameters', 'ResonanceFlags', 'ResonanceMolSupplier', 'ResonanceMolSupplierCallback', 'RestoreBondDirOption', 'RingInfo', 'SANITIZE_ADJUSTHS', 'SANITIZE_ALL', 'SANITIZE_CLEANUP', 'SANITIZE_CLEANUPATROPISOMERS', 'SANITIZE_CLEANUPCHIRALITY', 'SANITIZE_CLEANUP_ORGANOMETALLICS', 'SANITIZE_FINDRADICALS', 'SANITIZE_KEKULIZE', 'SANITIZE_NONE', 'SANITIZE_PROPERTIES', 'SANITIZE_SETAROMATICITY', 'SANITIZE_SETCONJUGATION', 'SANITIZE_SETHYBRIDIZATION', 'SANITIZE_SYMMRINGS', 'SDMolSupplier', 'SDWriter', 'STEREO_ABSOLUTE', 'STEREO_AND', 'STEREO_OR', 'SanitizeFlags', 'SmartsParserParams', 'SmilesMolSupplier', 'SmilesParserParams', 'SmilesWriteParams', 'SmilesWriter', 'StereoBondThresholds', 'StereoDescriptor', 'StereoGroup', 'StereoGroupType', 'StereoGroup_vect', 'StereoInfo', 'StereoSpecified', 'StereoType', 'SubstanceGroup', 'SubstanceGroupAttach', 'SubstanceGroupCState', 'SubstanceGroup_VECT', 'SubstructMatchParameters', 'SupplierFromFilename', 'TDTMolSupplier', 'TDTWriter', 'UNCONSTRAINED_ANIONS', 'UNCONSTRAINED_CATIONS', 'inchi', 'rdBase', 'rdCIPLabeler', 'rdCoordGen', 'rdGeometry', 'rdMolInterchange', 'rdchem', 'rdinchi', 'rdmolfiles', 'rdmolops', 'templDir']
class ConversionError(Exception):
    pass
class _GetAtomsIterator(_GetRDKixObjIterator):
    def _getRDKixItem(self, i):
        ...
    def _sizeCalc(self):
        ...
class _GetBondsIterator(_GetRDKixObjIterator):
    def _getRDKixItem(self, i):
        ...
    def _sizeCalc(self):
        ...
class _GetRDKixObjIterator:
    def __getitem__(self, i):
        ...
    def __init__(self, mol):
        ...
    def __iter__(self):
        ...
    def __len__(self):
        ...
    def __next__(self):
        ...
    def _getRDKixItem(self, i):
        ...
    def _sizeCalc(self):
        ...
def CanonSmiles(smi, useChiral = 1):
    ...
def FindMolChiralCenters(mol, force = True, includeUnassigned = False, includeCIP = True, useLegacyImplementation = None):
    """
    
        >>> from rdkix import Chem
        >>> mol = Chem.MolFromSmiles('[C@H](Cl)(F)Br')
        >>> Chem.FindMolChiralCenters(mol)
        [(0, 'R')]
        >>> mol = Chem.MolFromSmiles('[C@@H](Cl)(F)Br')
        >>> Chem.FindMolChiralCenters(mol)
        [(0, 'S')]
    
        >>> Chem.FindMolChiralCenters(Chem.MolFromSmiles('CCC'))
        []
    
        By default unassigned stereo centers are not reported:
    
        >>> mol = Chem.MolFromSmiles('C[C@H](F)C(F)(Cl)Br')
        >>> Chem.FindMolChiralCenters(mol,force=True)
        [(1, 'S')]
    
        but this can be changed:
    
        >>> Chem.FindMolChiralCenters(mol,force=True,includeUnassigned=True)
        [(1, 'S'), (3, '?')]
    
        The handling of unassigned stereocenters for dependent stereochemistry is not correct 
        using the legacy implementation:
    
        >>> Chem.FindMolChiralCenters(Chem.MolFromSmiles('C1CC(C)C(C)C(C)C1'),includeUnassigned=True)
        [(2, '?'), (6, '?')]
        >>> Chem.FindMolChiralCenters(Chem.MolFromSmiles('C1C[C@H](C)C(C)[C@H](C)C1'),includeUnassigned=True)
        [(2, 'S'), (4, '?'), (6, 'R')]
    
        But works with the new implementation:
    
        >>> Chem.FindMolChiralCenters(Chem.MolFromSmiles('C1CC(C)C(C)C(C)C1'),includeUnassigned=True, useLegacyImplementation=False)
        [(2, '?'), (4, '?'), (6, '?')]
    
        Note that the new implementation also gets the correct descriptors for para-stereochemistry:
    
        >>> Chem.FindMolChiralCenters(Chem.MolFromSmiles('C1C[C@H](C)[C@H](C)[C@H](C)C1'),useLegacyImplementation=False)
        [(2, 'S'), (4, 's'), (6, 'R')]
    
        With the new implementation, if you don't care about the CIP labels of stereocenters, you can save
        some time by disabling those:
    
        >>> Chem.FindMolChiralCenters(Chem.MolFromSmiles('C1C[C@H](C)[C@H](C)[C@H](C)C1'), includeCIP=False, useLegacyImplementation=False)
        [(2, 'Tet_CCW'), (4, 'Tet_CCW'), (6, 'Tet_CCW')]
    
      
    """
def QuickSmartsMatch(smi, sma, unique = True, display = False):
    ...
def SupplierFromFilename(fileN, delim = '', **kwargs):
    ...
def _patch():
    ...
def _test():
    ...
ADJUST_IGNOREALL: rdmolops.AdjustQueryWhichFlags  # value = rdkix.Chem.rdmolops.AdjustQueryWhichFlags.ADJUST_IGNOREALL
ADJUST_IGNORECHAINS: rdmolops.AdjustQueryWhichFlags  # value = rdkix.Chem.rdmolops.AdjustQueryWhichFlags.ADJUST_IGNORECHAINS
ADJUST_IGNOREDUMMIES: rdmolops.AdjustQueryWhichFlags  # value = rdkix.Chem.rdmolops.AdjustQueryWhichFlags.ADJUST_IGNOREDUMMIES
ADJUST_IGNOREMAPPED: rdmolops.AdjustQueryWhichFlags  # value = rdkix.Chem.rdmolops.AdjustQueryWhichFlags.ADJUST_IGNOREMAPPED
ADJUST_IGNORENONDUMMIES: rdmolops.AdjustQueryWhichFlags  # value = rdkix.Chem.rdmolops.AdjustQueryWhichFlags.ADJUST_IGNORENONDUMMIES
ADJUST_IGNORENONE: rdmolops.AdjustQueryWhichFlags  # value = rdkix.Chem.rdmolops.AdjustQueryWhichFlags.ADJUST_IGNORENONE
ADJUST_IGNORERINGS: rdmolops.AdjustQueryWhichFlags  # value = rdkix.Chem.rdmolops.AdjustQueryWhichFlags.ADJUST_IGNORERINGS
ALLOW_CHARGE_SEPARATION: rdchem.ResonanceFlags  # value = rdkix.Chem.rdchem.ResonanceFlags.ALLOW_CHARGE_SEPARATION
ALLOW_INCOMPLETE_OCTETS: rdchem.ResonanceFlags  # value = rdkix.Chem.rdchem.ResonanceFlags.ALLOW_INCOMPLETE_OCTETS
AROMATICITY_CUSTOM: rdmolops.AromaticityModel  # value = rdkix.Chem.rdmolops.AromaticityModel.AROMATICITY_CUSTOM
AROMATICITY_DEFAULT: rdmolops.AromaticityModel  # value = rdkix.Chem.rdmolops.AromaticityModel.AROMATICITY_DEFAULT
AROMATICITY_MDL: rdmolops.AromaticityModel  # value = rdkix.Chem.rdmolops.AromaticityModel.AROMATICITY_MDL
AROMATICITY_RDKIX: rdmolops.AromaticityModel  # value = rdkix.Chem.rdmolops.AromaticityModel.AROMATICITY_RDKIX
AROMATICITY_SIMPLE: rdmolops.AromaticityModel  # value = rdkix.Chem.rdmolops.AromaticityModel.AROMATICITY_SIMPLE
AllProps: rdchem.PropertyPickleOptions  # value = rdkix.Chem.rdchem.PropertyPickleOptions.AllProps
AtomProps: rdchem.PropertyPickleOptions  # value = rdkix.Chem.rdchem.PropertyPickleOptions.AtomProps
BondProps: rdchem.PropertyPickleOptions  # value = rdkix.Chem.rdchem.PropertyPickleOptions.BondProps
CHI_ALLENE: rdchem.ChiralType  # value = rdkix.Chem.rdchem.ChiralType.CHI_ALLENE
CHI_OCTAHEDRAL: rdchem.ChiralType  # value = rdkix.Chem.rdchem.ChiralType.CHI_OCTAHEDRAL
CHI_OTHER: rdchem.ChiralType  # value = rdkix.Chem.rdchem.ChiralType.CHI_OTHER
CHI_SQUAREPLANAR: rdchem.ChiralType  # value = rdkix.Chem.rdchem.ChiralType.CHI_SQUAREPLANAR
CHI_TETRAHEDRAL: rdchem.ChiralType  # value = rdkix.Chem.rdchem.ChiralType.CHI_TETRAHEDRAL
CHI_TETRAHEDRAL_CCW: rdchem.ChiralType  # value = rdkix.Chem.rdchem.ChiralType.CHI_TETRAHEDRAL_CCW
CHI_TETRAHEDRAL_CW: rdchem.ChiralType  # value = rdkix.Chem.rdchem.ChiralType.CHI_TETRAHEDRAL_CW
CHI_TRIGONALBIPYRAMIDAL: rdchem.ChiralType  # value = rdkix.Chem.rdchem.ChiralType.CHI_TRIGONALBIPYRAMIDAL
CHI_UNSPECIFIED: rdchem.ChiralType  # value = rdkix.Chem.rdchem.ChiralType.CHI_UNSPECIFIED
COMPOSITE_AND: rdchem.CompositeQueryType  # value = rdkix.Chem.rdchem.CompositeQueryType.COMPOSITE_AND
COMPOSITE_OR: rdchem.CompositeQueryType  # value = rdkix.Chem.rdchem.CompositeQueryType.COMPOSITE_OR
COMPOSITE_XOR: rdchem.CompositeQueryType  # value = rdkix.Chem.rdchem.CompositeQueryType.COMPOSITE_XOR
ComputedProps: rdchem.PropertyPickleOptions  # value = rdkix.Chem.rdchem.PropertyPickleOptions.ComputedProps
CoordsAsDouble: rdchem.PropertyPickleOptions  # value = rdkix.Chem.rdchem.PropertyPickleOptions.CoordsAsDouble
INCHI_AVAILABLE: bool = True
KEKULE_ALL: rdchem.ResonanceFlags  # value = rdkix.Chem.rdchem.ResonanceFlags.KEKULE_ALL
LayeredFingerprint_substructLayers: int = 7
MolProps: rdchem.PropertyPickleOptions  # value = rdkix.Chem.rdchem.PropertyPickleOptions.MolProps
NoConformers: rdchem.PropertyPickleOptions  # value = rdkix.Chem.rdchem.PropertyPickleOptions.NoConformers
NoProps: rdchem.PropertyPickleOptions  # value = rdkix.Chem.rdchem.PropertyPickleOptions.NoProps
PrivateProps: rdchem.PropertyPickleOptions  # value = rdkix.Chem.rdchem.PropertyPickleOptions.PrivateProps
QueryAtomData: rdchem.PropertyPickleOptions  # value = rdkix.Chem.rdchem.PropertyPickleOptions.QueryAtomData
SANITIZE_ADJUSTHS: rdmolops.SanitizeFlags  # value = rdkix.Chem.rdmolops.SanitizeFlags.SANITIZE_ADJUSTHS
SANITIZE_ALL: rdmolops.SanitizeFlags  # value = rdkix.Chem.rdmolops.SanitizeFlags.SANITIZE_ALL
SANITIZE_CLEANUP: rdmolops.SanitizeFlags  # value = rdkix.Chem.rdmolops.SanitizeFlags.SANITIZE_CLEANUP
SANITIZE_CLEANUPATROPISOMERS: rdmolops.SanitizeFlags  # value = rdkix.Chem.rdmolops.SanitizeFlags.SANITIZE_CLEANUPATROPISOMERS
SANITIZE_CLEANUPCHIRALITY: rdmolops.SanitizeFlags  # value = rdkix.Chem.rdmolops.SanitizeFlags.SANITIZE_CLEANUPCHIRALITY
SANITIZE_CLEANUP_ORGANOMETALLICS: rdmolops.SanitizeFlags  # value = rdkix.Chem.rdmolops.SanitizeFlags.SANITIZE_CLEANUP_ORGANOMETALLICS
SANITIZE_FINDRADICALS: rdmolops.SanitizeFlags  # value = rdkix.Chem.rdmolops.SanitizeFlags.SANITIZE_FINDRADICALS
SANITIZE_KEKULIZE: rdmolops.SanitizeFlags  # value = rdkix.Chem.rdmolops.SanitizeFlags.SANITIZE_KEKULIZE
SANITIZE_NONE: rdmolops.SanitizeFlags  # value = rdkix.Chem.rdmolops.SanitizeFlags.SANITIZE_NONE
SANITIZE_PROPERTIES: rdmolops.SanitizeFlags  # value = rdkix.Chem.rdmolops.SanitizeFlags.SANITIZE_PROPERTIES
SANITIZE_SETAROMATICITY: rdmolops.SanitizeFlags  # value = rdkix.Chem.rdmolops.SanitizeFlags.SANITIZE_SETAROMATICITY
SANITIZE_SETCONJUGATION: rdmolops.SanitizeFlags  # value = rdkix.Chem.rdmolops.SanitizeFlags.SANITIZE_SETCONJUGATION
SANITIZE_SETHYBRIDIZATION: rdmolops.SanitizeFlags  # value = rdkix.Chem.rdmolops.SanitizeFlags.SANITIZE_SETHYBRIDIZATION
SANITIZE_SYMMRINGS: rdmolops.SanitizeFlags  # value = rdkix.Chem.rdmolops.SanitizeFlags.SANITIZE_SYMMRINGS
STEREO_ABSOLUTE: rdchem.StereoGroupType  # value = rdkix.Chem.rdchem.StereoGroupType.STEREO_ABSOLUTE
STEREO_AND: rdchem.StereoGroupType  # value = rdkix.Chem.rdchem.StereoGroupType.STEREO_AND
STEREO_OR: rdchem.StereoGroupType  # value = rdkix.Chem.rdchem.StereoGroupType.STEREO_OR
UNCONSTRAINED_ANIONS: rdchem.ResonanceFlags  # value = rdkix.Chem.rdchem.ResonanceFlags.UNCONSTRAINED_ANIONS
UNCONSTRAINED_CATIONS: rdchem.ResonanceFlags  # value = rdkix.Chem.rdchem.ResonanceFlags.UNCONSTRAINED_CATIONS
templDir: str = '/project/build/temp.linux-x86_64-cpython-311/rdkix_install/share/RDKix/Data/'
