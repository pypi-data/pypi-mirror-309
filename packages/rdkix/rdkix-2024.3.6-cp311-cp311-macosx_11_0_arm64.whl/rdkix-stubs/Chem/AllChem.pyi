"""
 Import all RDKix chemistry modules

"""
from __future__ import annotations
from collections import namedtuple
import numpy as numpy
from rdkix.Chem import CanonSmiles
from rdkix.Chem.ChemicalFeatures import MCFF_GetFeaturesForMol
from rdkix.Chem import ConversionError
from rdkix.Chem.EnumerateStereoisomers import EnumerateStereoisomers
from rdkix.Chem.EnumerateStereoisomers import StereoEnumerationOptions
from rdkix.Chem import FindMolChiralCenters
from rdkix.Chem import QuickSmartsMatch
from rdkix.Chem import SupplierFromFilename
from rdkix.Chem import inchi
from rdkix.Chem.inchi import InchiReadWriteError
from rdkix.Chem.inchi import InchiToInchiKey
from rdkix.Chem.inchi import MolBlockToInchi
from rdkix.Chem.inchi import MolBlockToInchiAndAuxInfo
from rdkix.Chem.inchi import MolFromInchi
from rdkix.Chem.inchi import MolToInchi
from rdkix.Chem.inchi import MolToInchiAndAuxInfo
from rdkix.Chem.inchi import MolToInchiKey
from rdkix.Chem import rdCIPLabeler
import rdkix.Chem.rdChemReactions
from rdkix.Chem.rdChemReactions import CartesianProductStrategy
from rdkix.Chem.rdChemReactions import ChemicalReaction
from rdkix.Chem.rdChemReactions import EnumerateLibrary
from rdkix.Chem.rdChemReactions import EnumerateLibraryBase
from rdkix.Chem.rdChemReactions import EnumerationParams
from rdkix.Chem.rdChemReactions import EnumerationStrategyBase
from rdkix.Chem.rdChemReactions import EvenSamplePairsStrategy
from rdkix.Chem.rdChemReactions import FingerprintType
from rdkix.Chem.rdChemReactions import MOL_SPTR_VECT
from rdkix.Chem.rdChemReactions import RandomSampleAllBBsStrategy
from rdkix.Chem.rdChemReactions import RandomSampleStrategy
from rdkix.Chem.rdChemReactions import ReactionFingerprintParams
from rdkix.Chem.rdChemReactions import SanitizeFlags
from rdkix.Chem.rdChemReactions import VectMolVect
from rdkix.Chem.rdChemReactions import VectSizeT
from rdkix.Chem.rdChemReactions import VectorOfStringVectors
from rdkix.Chem.rdChemicalFeatures import FreeChemicalFeature
from rdkix.Chem import rdCoordGen
from rdkix.Chem.rdDepictor import ConstrainedDepictionParams
from rdkix.Chem.rdDepictor import UsingCoordGen
import rdkix.Chem.rdDistGeom
from rdkix.Chem.rdDistGeom import EmbedFailureCauses
from rdkix.Chem.rdDistGeom import EmbedParameters
import rdkix.Chem.rdFingerprintGenerator
from rdkix.Chem.rdFingerprintGenerator import AdditionalOutput
from rdkix.Chem.rdFingerprintGenerator import AtomInvariantsGenerator
from rdkix.Chem.rdFingerprintGenerator import AtomPairFingerprintOptions
from rdkix.Chem.rdFingerprintGenerator import BondInvariantsGenerator
from rdkix.Chem.rdFingerprintGenerator import FPType
from rdkix.Chem.rdFingerprintGenerator import FingeprintGenerator32
from rdkix.Chem.rdFingerprintGenerator import FingeprintGenerator64
from rdkix.Chem.rdFingerprintGenerator import FingerprintOptions
from rdkix.Chem.rdFingerprintGenerator import MorganFingerprintOptions
from rdkix.Chem.rdFingerprintGenerator import RDKixFingerprintOptions
from rdkix.Chem.rdFingerprintGenerator import TopologicalTorsionFingerprintOptions
from rdkix.Chem.rdMolAlign import O3A
from rdkix.Chem.rdMolChemicalFeatures import MolChemicalFeature
from rdkix.Chem.rdMolChemicalFeatures import MolChemicalFeatureFactory
from rdkix.Chem.rdMolDescriptors import AtomPairsParameters
from rdkix.Chem.rdMolDescriptors import DoubleCubicLatticeVolume
from rdkix.Chem.rdMolDescriptors import NumRotatableBondsOptions
from rdkix.Chem.rdMolDescriptors import Properties
from rdkix.Chem.rdMolDescriptors import PropertyFunctor
from rdkix.Chem.rdMolDescriptors import PropertyRangeQuery
from rdkix.Chem.rdMolDescriptors import PythonPropertyFunctor
from rdkix.Chem.rdMolEnumerator import EnumeratorType
from rdkix.Chem.rdMolEnumerator import MolEnumeratorParams
from rdkix.Chem import rdMolInterchange
from rdkix.Chem.rdMolInterchange import JSONParseParameters
from rdkix.Chem.rdMolInterchange import JSONWriteParameters
from rdkix.Chem import rdchem
import rdkix.Chem.rdchem
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
from rdkix.Chem import rdinchi
from rdkix.Chem import rdmolfiles
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
import rdkix.Chem.rdmolops
from rdkix.Chem import rdmolops
from rdkix.Chem.rdmolops import AdjustQueryParameters
from rdkix.Chem.rdmolops import AdjustQueryWhichFlags
from rdkix.Chem.rdmolops import AromaticityModel
from rdkix.Chem.rdmolops import BondWedgingParameters
from rdkix.Chem.rdmolops import MolzipLabel
from rdkix.Chem.rdmolops import MolzipParams
from rdkix.Chem.rdmolops import RemoveHsParameters
from rdkix.Chem.rdmolops import StereoBondThresholds
from rdkix import DataStructs
from rdkix import ForceField
from rdkix.Geometry import rdGeometry
from rdkix import RDConfig
import rdkix.RDLogger
from rdkix import rdBase
import sys as sys
import warnings as warnings
__all__ = ['ADJUST_IGNOREALL', 'ADJUST_IGNORECHAINS', 'ADJUST_IGNOREDUMMIES', 'ADJUST_IGNOREMAPPED', 'ADJUST_IGNORENONDUMMIES', 'ADJUST_IGNORENONE', 'ADJUST_IGNORERINGS', 'ALLOW_CHARGE_SEPARATION', 'ALLOW_INCOMPLETE_OCTETS', 'AROMATICITY_CUSTOM', 'AROMATICITY_DEFAULT', 'AROMATICITY_MDL', 'AROMATICITY_RDKIX', 'AROMATICITY_SIMPLE', 'AdditionalOutput', 'AdjustQueryParameters', 'AdjustQueryWhichFlags', 'AllProps', 'AromaticityModel', 'AssignBondOrdersFromTemplate', 'Atom', 'AtomInvariantsGenerator', 'AtomKekulizeException', 'AtomMonomerInfo', 'AtomMonomerType', 'AtomPDBResidueInfo', 'AtomPairFP', 'AtomPairFingerprintOptions', 'AtomPairsParameters', 'AtomProps', 'AtomSanitizeException', 'AtomValenceException', 'BAD_DOUBLE_BOND_STEREO', 'Bond', 'BondDir', 'BondInvariantsGenerator', 'BondProps', 'BondStereo', 'BondType', 'BondWedgingParameters', 'CHECK_CHIRAL_CENTERS', 'CHECK_CHIRAL_CENTERS2', 'CHECK_TETRAHEDRAL_CENTERS', 'CHI_ALLENE', 'CHI_OCTAHEDRAL', 'CHI_OTHER', 'CHI_SQUAREPLANAR', 'CHI_TETRAHEDRAL', 'CHI_TETRAHEDRAL_CCW', 'CHI_TETRAHEDRAL_CW', 'CHI_TRIGONALBIPYRAMIDAL', 'CHI_UNSPECIFIED', 'COMPOSITE_AND', 'COMPOSITE_OR', 'COMPOSITE_XOR', 'CXSmilesFields', 'CanonSmiles', 'CartesianProductStrategy', 'ChemicalReaction', 'ChiralType', 'CompositeQueryType', 'ComputeMolShape', 'ComputeMolVolume', 'ComputedProps', 'Conformer', 'ConstrainedDepictionParams', 'ConstrainedEmbed', 'ConversionError', 'CoordsAsDouble', 'DataStructs', 'DoubleCubicLatticeVolume', 'ETK_MINIMIZATION', 'EditableMol', 'EmbedFailureCauses', 'EmbedParameters', 'EnumerateLibrary', 'EnumerateLibraryBase', 'EnumerateLibraryFromReaction', 'EnumerateStereoisomers', 'EnumerationParams', 'EnumerationStrategyBase', 'EnumeratorType', 'EvenSamplePairsStrategy', 'FINAL_CENTER_IN_VOLUME', 'FINAL_CHIRAL_BOUNDS', 'FIRST_MINIMIZATION', 'FPType', 'FindMolChiralCenters', 'FingeprintGenerator32', 'FingeprintGenerator64', 'FingerprintOptions', 'FingerprintType', 'FixedMolSizeMolBundle', 'ForceField', 'ForwardSDMolSupplier', 'FreeChemicalFeature', 'GetConformerRMS', 'GetConformerRMSMatrix', 'HybridizationType', 'INCHI_AVAILABLE', 'INITIAL_COORDS', 'InchiReadWriteError', 'InchiToInchiKey', 'JSONParseParameters', 'JSONWriteParameters', 'KEKULE_ALL', 'KekulizeException', 'LINEAR_DOUBLE_BOND', 'LayeredFingerprint_substructLayers', 'MCFF_GetFeaturesForMol', 'MINIMIZE_FOURTH_DIMENSION', 'MOL_SPTR_VECT', 'MaeMolSupplier', 'MaeWriter', 'Mol', 'MolBlockToInchi', 'MolBlockToInchiAndAuxInfo', 'MolBundle', 'MolChemicalFeature', 'MolChemicalFeatureFactory', 'MolEnumeratorParams', 'MolFromInchi', 'MolProps', 'MolSanitizeException', 'MolToInchi', 'MolToInchiAndAuxInfo', 'MolToInchiKey', 'MolWriterParams', 'MolzipLabel', 'MolzipParams', 'MorganFP', 'MorganFingerprintOptions', 'MultithreadedSDMolSupplier', 'MultithreadedSmilesMolSupplier', 'NoConformers', 'NoProps', 'NumRotatableBondsOptions', 'O3A', 'PDBWriter', 'PeriodicTable', 'PrivateProps', 'Properties', 'PropertyFunctor', 'PropertyPickleOptions', 'PropertyRangeQuery', 'PythonPropertyFunctor', 'QueryAtom', 'QueryAtomData', 'QueryBond', 'QuickSmartsMatch', 'RDConfig', 'RDKixFP', 'RDKixFingerprintOptions', 'RWMol', 'RandomSampleAllBBsStrategy', 'RandomSampleStrategy', 'ReactionFingerprintParams', 'RemoveHsParameters', 'ResonanceFlags', 'ResonanceMolSupplier', 'ResonanceMolSupplierCallback', 'RestoreBondDirOption', 'RingInfo', 'SANITIZE_ADJUSTHS', 'SANITIZE_ADJUST_REACTANTS', 'SANITIZE_ALL', 'SANITIZE_ATOM_MAPS', 'SANITIZE_CLEANUP', 'SANITIZE_CLEANUPATROPISOMERS', 'SANITIZE_CLEANUPCHIRALITY', 'SANITIZE_CLEANUP_ORGANOMETALLICS', 'SANITIZE_FINDRADICALS', 'SANITIZE_KEKULIZE', 'SANITIZE_MERGEHS', 'SANITIZE_NONE', 'SANITIZE_PROPERTIES', 'SANITIZE_RGROUP_NAMES', 'SANITIZE_SETAROMATICITY', 'SANITIZE_SETCONJUGATION', 'SANITIZE_SETHYBRIDIZATION', 'SANITIZE_SYMMRINGS', 'SDMolSupplier', 'SDWriter', 'STEREO_ABSOLUTE', 'STEREO_AND', 'STEREO_OR', 'SanitizeFlags', 'SmartsParserParams', 'SmilesMolSupplier', 'SmilesParserParams', 'SmilesWriteParams', 'SmilesWriter', 'StereoBondThresholds', 'StereoDescriptor', 'StereoEnumerationOptions', 'StereoGroup', 'StereoGroupType', 'StereoGroup_vect', 'StereoInfo', 'StereoSpecified', 'StereoType', 'SubstanceGroup', 'SubstanceGroupAttach', 'SubstanceGroupCState', 'SubstanceGroup_VECT', 'SubstructMatchParameters', 'SupplierFromFilename', 'TDTMolSupplier', 'TDTWriter', 'TopologicalTorsionFP', 'TopologicalTorsionFingerprintOptions', 'TransformMol', 'UNCONSTRAINED_ANIONS', 'UNCONSTRAINED_CATIONS', 'UsingCoordGen', 'VectMolVect', 'VectSizeT', 'VectorOfStringVectors', 'inchi', 'logger', 'namedtuple', 'numpy', 'rdBase', 'rdCIPLabeler', 'rdCoordGen', 'rdGeometry', 'rdMolInterchange', 'rdchem', 'rdinchi', 'rdmolfiles', 'rdmolops', 'sys', 'templDir', 'warnings']
def AssignBondOrdersFromTemplate(refmol, mol):
    """
     assigns bond orders to a molecule based on the
        bond orders in a template molecule
    
        Arguments
          - refmol: the template molecule
          - mol: the molecule to assign bond orders to
    
        An example, start by generating a template from a SMILES
        and read in the PDB structure of the molecule
    
        >>> import os
        >>> from rdkix.Chem import AllChem
        >>> template = AllChem.MolFromSmiles("CN1C(=NC(C1=O)(c2ccccc2)c3ccccc3)N")
        >>> mol = AllChem.MolFromPDBFile(os.path.join(RDConfig.RDCodeDir, 'Chem', 'test_data', '4DJU_lig.pdb'))
        >>> len([1 for b in template.GetBonds() if b.GetBondTypeAsDouble() == 1.0])
        8
        >>> len([1 for b in mol.GetBonds() if b.GetBondTypeAsDouble() == 1.0])
        22
    
        Now assign the bond orders based on the template molecule
    
        >>> newMol = AllChem.AssignBondOrdersFromTemplate(template, mol)
        >>> len([1 for b in newMol.GetBonds() if b.GetBondTypeAsDouble() == 1.0])
        8
    
        Note that the template molecule should have no explicit hydrogens
        else the algorithm will fail.
    
        It also works if there are different formal charges (this was github issue 235):
    
        >>> template=AllChem.MolFromSmiles('CN(C)C(=O)Cc1ccc2c(c1)NC(=O)c3ccc(cc3N2)c4ccc(c(c4)OC)[N+](=O)[O-]')
        >>> mol = AllChem.MolFromMolFile(os.path.join(RDConfig.RDCodeDir, 'Chem', 'test_data', '4FTR_lig.mol'))
        >>> AllChem.MolToSmiles(mol)
        'COC1CC(C2CCC3C(O)NC4CC(CC(O)N(C)C)CCC4NC3C2)CCC1N(O)O'
        >>> newMol = AllChem.AssignBondOrdersFromTemplate(template, mol)
        >>> AllChem.MolToSmiles(newMol)
        'COc1cc(-c2ccc3c(c2)Nc2ccc(CC(=O)N(C)C)cc2NC3=O)ccc1[N+](=O)[O-]'
    
        
    """
def ComputeMolShape(mol, confId = -1, boxDim = (20, 20, 20), spacing = 0.5, **kwargs):
    """
     returns a grid representation of the molecule's shape
        
    """
def ComputeMolVolume(mol, confId = -1, gridSpacing = 0.2, boxMargin = 2.0):
    """
     Calculates the volume of a particular conformer of a molecule
        based on a grid-encoding of the molecular shape.
    
        A bit of demo as well as a test of github #1883:
    
        >>> from rdkix import Chem
        >>> from rdkix.Chem import AllChem
        >>> mol = Chem.AddHs(Chem.MolFromSmiles('C'))
        >>> AllChem.EmbedMolecule(mol)
        0
        >>> ComputeMolVolume(mol)
        28...
        >>> mol = Chem.AddHs(Chem.MolFromSmiles('O'))
        >>> AllChem.EmbedMolecule(mol)
        0
        >>> ComputeMolVolume(mol)
        20...
    
        
    """
def ConstrainedEmbed(mol, core, useTethers = True, coreConfId = -1, randomseed = 2342, getForceField = ..., **kwargs):
    """
     generates an embedding of a molecule where part of the molecule
        is constrained to have particular coordinates
    
        Arguments
          - mol: the molecule to embed
          - core: the molecule to use as a source of constraints
          - useTethers: (optional) if True, the final conformation will be
              optimized subject to a series of extra forces that pull the
              matching atoms to the positions of the core atoms. Otherwise
              simple distance constraints based on the core atoms will be
              used in the optimization.
          - coreConfId: (optional) id of the core conformation to use
          - randomSeed: (optional) seed for the random number generator
    
    
        An example, start by generating a template with a 3D structure:
    
        >>> from rdkix.Chem import AllChem
        >>> template = AllChem.MolFromSmiles("c1nn(Cc2ccccc2)cc1")
        >>> AllChem.EmbedMolecule(template)
        0
        >>> AllChem.UFFOptimizeMolecule(template)
        0
    
        Here's a molecule:
    
        >>> mol = AllChem.MolFromSmiles("c1nn(Cc2ccccc2)cc1-c3ccccc3")
    
        Now do the constrained embedding
      
        >>> mol = AllChem.ConstrainedEmbed(mol, template)
    
        Demonstrate that the positions are nearly the same with template:
    
        >>> import math
        >>> molp = mol.GetConformer().GetAtomPosition(0)
        >>> templatep = template.GetConformer().GetAtomPosition(0)
        >>> all(math.isclose(v, 0.0, abs_tol=0.01) for v in molp-templatep)
        True
        >>> molp = mol.GetConformer().GetAtomPosition(1)
        >>> templatep = template.GetConformer().GetAtomPosition(1)
        >>> all(math.isclose(v, 0.0, abs_tol=0.01) for v in molp-templatep)
        True
    
        
    """
def EnumerateLibraryFromReaction(reaction, sidechainSets, returnReactants = False):
    """
     Returns a generator for the virtual library defined by
        a reaction and a sequence of sidechain sets
    
        >>> from rdkix import Chem
        >>> from rdkix.Chem import AllChem
        >>> s1=[Chem.MolFromSmiles(x) for x in ('NC','NCC')]
        >>> s2=[Chem.MolFromSmiles(x) for x in ('OC=O','OC(=O)C')]
        >>> rxn = AllChem.ReactionFromSmarts('[O:2]=[C:1][OH].[N:3]>>[O:2]=[C:1][N:3]')
        >>> r = AllChem.EnumerateLibraryFromReaction(rxn,[s2,s1])
        >>> [Chem.MolToSmiles(x[0]) for x in list(r)]
        ['CNC=O', 'CCNC=O', 'CNC(C)=O', 'CCNC(C)=O']
    
        Note that this is all done in a lazy manner, so "infinitely" large libraries can
        be done without worrying about running out of memory. Your patience will run out first:
    
        Define a set of 10000 amines:
    
        >>> amines = (Chem.MolFromSmiles('N'+'C'*x) for x in range(10000))
    
        ... a set of 10000 acids
    
        >>> acids = (Chem.MolFromSmiles('OC(=O)'+'C'*x) for x in range(10000))
    
        ... now the virtual library (1e8 compounds in principle):
    
        >>> r = AllChem.EnumerateLibraryFromReaction(rxn,[acids,amines])
    
        ... look at the first 4 compounds:
    
        >>> [Chem.MolToSmiles(next(r)[0]) for x in range(4)]
        ['NC=O', 'CNC=O', 'CCNC=O', 'CCCNC=O']
    
    
        
    """
def GetConformerRMS(mol, confId1, confId2, atomIds = None, prealigned = False):
    """
     Returns the RMS between two conformations.
        By default, the conformers will be aligned to the first conformer
        before the RMS calculation and, as a side-effect, the second will be left
        in the aligned state.
    
        Arguments:
          - mol:        the molecule
          - confId1:    the id of the first conformer
          - confId2:    the id of the second conformer
          - atomIds:    (optional) list of atom ids to use a points for
                        alingment - defaults to all atoms
          - prealigned: (optional) by default the conformers are assumed
                        be unaligned and the second conformer be aligned
                        to the first
    
        
    """
def GetConformerRMSMatrix(mol, atomIds = None, prealigned = False):
    """
     Returns the RMS matrix of the conformers of a molecule.
        As a side-effect, the conformers will be aligned to the first
        conformer (i.e. the reference) and will left in the aligned state.
    
        Arguments:
          - mol:     the molecule
          - atomIds: (optional) list of atom ids to use a points for
                     alingment - defaults to all atoms
          - prealigned: (optional) by default the conformers are assumed
                        be unaligned and will therefore be aligned to the
                        first conformer
    
        Note that the returned RMS matrix is symmetrical, i.e. it is the
        lower half of the matrix, e.g. for 5 conformers::
    
          rmsmatrix = [ a,
                        b, c,
                        d, e, f,
                        g, h, i, j]
    
        where a is the RMS between conformers 0 and 1, b is the RMS between
        conformers 0 and 2, etc.
        This way it can be directly used as distance matrix in e.g. Butina
        clustering.
    
        
    """
def TransformMol(mol, tform, confId = -1, keepConfs = False):
    """
      Applies the transformation (usually a 4x4 double matrix) to a molecule
        if keepConfs is False then all but that conformer are removed
        
    """
def _runDoctests(verbose = None):
    ...
ADJUST_IGNOREALL: rdkix.Chem.rdmolops.AdjustQueryWhichFlags  # value = rdkix.Chem.rdmolops.AdjustQueryWhichFlags.ADJUST_IGNOREALL
ADJUST_IGNORECHAINS: rdkix.Chem.rdmolops.AdjustQueryWhichFlags  # value = rdkix.Chem.rdmolops.AdjustQueryWhichFlags.ADJUST_IGNORECHAINS
ADJUST_IGNOREDUMMIES: rdkix.Chem.rdmolops.AdjustQueryWhichFlags  # value = rdkix.Chem.rdmolops.AdjustQueryWhichFlags.ADJUST_IGNOREDUMMIES
ADJUST_IGNOREMAPPED: rdkix.Chem.rdmolops.AdjustQueryWhichFlags  # value = rdkix.Chem.rdmolops.AdjustQueryWhichFlags.ADJUST_IGNOREMAPPED
ADJUST_IGNORENONDUMMIES: rdkix.Chem.rdmolops.AdjustQueryWhichFlags  # value = rdkix.Chem.rdmolops.AdjustQueryWhichFlags.ADJUST_IGNORENONDUMMIES
ADJUST_IGNORENONE: rdkix.Chem.rdmolops.AdjustQueryWhichFlags  # value = rdkix.Chem.rdmolops.AdjustQueryWhichFlags.ADJUST_IGNORENONE
ADJUST_IGNORERINGS: rdkix.Chem.rdmolops.AdjustQueryWhichFlags  # value = rdkix.Chem.rdmolops.AdjustQueryWhichFlags.ADJUST_IGNORERINGS
ALLOW_CHARGE_SEPARATION: rdkix.Chem.rdchem.ResonanceFlags  # value = rdkix.Chem.rdchem.ResonanceFlags.ALLOW_CHARGE_SEPARATION
ALLOW_INCOMPLETE_OCTETS: rdkix.Chem.rdchem.ResonanceFlags  # value = rdkix.Chem.rdchem.ResonanceFlags.ALLOW_INCOMPLETE_OCTETS
AROMATICITY_CUSTOM: rdkix.Chem.rdmolops.AromaticityModel  # value = rdkix.Chem.rdmolops.AromaticityModel.AROMATICITY_CUSTOM
AROMATICITY_DEFAULT: rdkix.Chem.rdmolops.AromaticityModel  # value = rdkix.Chem.rdmolops.AromaticityModel.AROMATICITY_DEFAULT
AROMATICITY_MDL: rdkix.Chem.rdmolops.AromaticityModel  # value = rdkix.Chem.rdmolops.AromaticityModel.AROMATICITY_MDL
AROMATICITY_RDKIX: rdkix.Chem.rdmolops.AromaticityModel  # value = rdkix.Chem.rdmolops.AromaticityModel.AROMATICITY_RDKIX
AROMATICITY_SIMPLE: rdkix.Chem.rdmolops.AromaticityModel  # value = rdkix.Chem.rdmolops.AromaticityModel.AROMATICITY_SIMPLE
AllProps: rdkix.Chem.rdchem.PropertyPickleOptions  # value = rdkix.Chem.rdchem.PropertyPickleOptions.AllProps
AtomPairFP: rdkix.Chem.rdFingerprintGenerator.FPType  # value = rdkix.Chem.rdFingerprintGenerator.FPType.AtomPairFP
AtomProps: rdkix.Chem.rdchem.PropertyPickleOptions  # value = rdkix.Chem.rdchem.PropertyPickleOptions.AtomProps
BAD_DOUBLE_BOND_STEREO: rdkix.Chem.rdDistGeom.EmbedFailureCauses  # value = rdkix.Chem.rdDistGeom.EmbedFailureCauses.BAD_DOUBLE_BOND_STEREO
BondProps: rdkix.Chem.rdchem.PropertyPickleOptions  # value = rdkix.Chem.rdchem.PropertyPickleOptions.BondProps
CHECK_CHIRAL_CENTERS: rdkix.Chem.rdDistGeom.EmbedFailureCauses  # value = rdkix.Chem.rdDistGeom.EmbedFailureCauses.CHECK_CHIRAL_CENTERS
CHECK_CHIRAL_CENTERS2: rdkix.Chem.rdDistGeom.EmbedFailureCauses  # value = rdkix.Chem.rdDistGeom.EmbedFailureCauses.CHECK_CHIRAL_CENTERS2
CHECK_TETRAHEDRAL_CENTERS: rdkix.Chem.rdDistGeom.EmbedFailureCauses  # value = rdkix.Chem.rdDistGeom.EmbedFailureCauses.CHECK_TETRAHEDRAL_CENTERS
CHI_ALLENE: rdkix.Chem.rdchem.ChiralType  # value = rdkix.Chem.rdchem.ChiralType.CHI_ALLENE
CHI_OCTAHEDRAL: rdkix.Chem.rdchem.ChiralType  # value = rdkix.Chem.rdchem.ChiralType.CHI_OCTAHEDRAL
CHI_OTHER: rdkix.Chem.rdchem.ChiralType  # value = rdkix.Chem.rdchem.ChiralType.CHI_OTHER
CHI_SQUAREPLANAR: rdkix.Chem.rdchem.ChiralType  # value = rdkix.Chem.rdchem.ChiralType.CHI_SQUAREPLANAR
CHI_TETRAHEDRAL: rdkix.Chem.rdchem.ChiralType  # value = rdkix.Chem.rdchem.ChiralType.CHI_TETRAHEDRAL
CHI_TETRAHEDRAL_CCW: rdkix.Chem.rdchem.ChiralType  # value = rdkix.Chem.rdchem.ChiralType.CHI_TETRAHEDRAL_CCW
CHI_TETRAHEDRAL_CW: rdkix.Chem.rdchem.ChiralType  # value = rdkix.Chem.rdchem.ChiralType.CHI_TETRAHEDRAL_CW
CHI_TRIGONALBIPYRAMIDAL: rdkix.Chem.rdchem.ChiralType  # value = rdkix.Chem.rdchem.ChiralType.CHI_TRIGONALBIPYRAMIDAL
CHI_UNSPECIFIED: rdkix.Chem.rdchem.ChiralType  # value = rdkix.Chem.rdchem.ChiralType.CHI_UNSPECIFIED
COMPOSITE_AND: rdkix.Chem.rdchem.CompositeQueryType  # value = rdkix.Chem.rdchem.CompositeQueryType.COMPOSITE_AND
COMPOSITE_OR: rdkix.Chem.rdchem.CompositeQueryType  # value = rdkix.Chem.rdchem.CompositeQueryType.COMPOSITE_OR
COMPOSITE_XOR: rdkix.Chem.rdchem.CompositeQueryType  # value = rdkix.Chem.rdchem.CompositeQueryType.COMPOSITE_XOR
ComputedProps: rdkix.Chem.rdchem.PropertyPickleOptions  # value = rdkix.Chem.rdchem.PropertyPickleOptions.ComputedProps
CoordsAsDouble: rdkix.Chem.rdchem.PropertyPickleOptions  # value = rdkix.Chem.rdchem.PropertyPickleOptions.CoordsAsDouble
ETK_MINIMIZATION: rdkix.Chem.rdDistGeom.EmbedFailureCauses  # value = rdkix.Chem.rdDistGeom.EmbedFailureCauses.ETK_MINIMIZATION
FINAL_CENTER_IN_VOLUME: rdkix.Chem.rdDistGeom.EmbedFailureCauses  # value = rdkix.Chem.rdDistGeom.EmbedFailureCauses.FINAL_CENTER_IN_VOLUME
FINAL_CHIRAL_BOUNDS: rdkix.Chem.rdDistGeom.EmbedFailureCauses  # value = rdkix.Chem.rdDistGeom.EmbedFailureCauses.FINAL_CHIRAL_BOUNDS
FIRST_MINIMIZATION: rdkix.Chem.rdDistGeom.EmbedFailureCauses  # value = rdkix.Chem.rdDistGeom.EmbedFailureCauses.FIRST_MINIMIZATION
INCHI_AVAILABLE: bool = True
INITIAL_COORDS: rdkix.Chem.rdDistGeom.EmbedFailureCauses  # value = rdkix.Chem.rdDistGeom.EmbedFailureCauses.INITIAL_COORDS
KEKULE_ALL: rdkix.Chem.rdchem.ResonanceFlags  # value = rdkix.Chem.rdchem.ResonanceFlags.KEKULE_ALL
LINEAR_DOUBLE_BOND: rdkix.Chem.rdDistGeom.EmbedFailureCauses  # value = rdkix.Chem.rdDistGeom.EmbedFailureCauses.LINEAR_DOUBLE_BOND
LayeredFingerprint_substructLayers: int = 7
MINIMIZE_FOURTH_DIMENSION: rdkix.Chem.rdDistGeom.EmbedFailureCauses  # value = rdkix.Chem.rdDistGeom.EmbedFailureCauses.MINIMIZE_FOURTH_DIMENSION
MolProps: rdkix.Chem.rdchem.PropertyPickleOptions  # value = rdkix.Chem.rdchem.PropertyPickleOptions.MolProps
MorganFP: rdkix.Chem.rdFingerprintGenerator.FPType  # value = rdkix.Chem.rdFingerprintGenerator.FPType.MorganFP
NoConformers: rdkix.Chem.rdchem.PropertyPickleOptions  # value = rdkix.Chem.rdchem.PropertyPickleOptions.NoConformers
NoProps: rdkix.Chem.rdchem.PropertyPickleOptions  # value = rdkix.Chem.rdchem.PropertyPickleOptions.NoProps
PrivateProps: rdkix.Chem.rdchem.PropertyPickleOptions  # value = rdkix.Chem.rdchem.PropertyPickleOptions.PrivateProps
QueryAtomData: rdkix.Chem.rdchem.PropertyPickleOptions  # value = rdkix.Chem.rdchem.PropertyPickleOptions.QueryAtomData
RDKixFP: rdkix.Chem.rdFingerprintGenerator.FPType  # value = rdkix.Chem.rdFingerprintGenerator.FPType.RDKixFP
SANITIZE_ADJUSTHS: rdkix.Chem.rdmolops.SanitizeFlags  # value = rdkix.Chem.rdmolops.SanitizeFlags.SANITIZE_ADJUSTHS
SANITIZE_ADJUST_REACTANTS: rdkix.Chem.rdChemReactions.SanitizeFlags  # value = rdkix.Chem.rdChemReactions.SanitizeFlags.SANITIZE_ADJUST_REACTANTS
SANITIZE_ALL: rdkix.Chem.rdChemReactions.SanitizeFlags  # value = rdkix.Chem.rdChemReactions.SanitizeFlags.SANITIZE_ALL
SANITIZE_ATOM_MAPS: rdkix.Chem.rdChemReactions.SanitizeFlags  # value = rdkix.Chem.rdChemReactions.SanitizeFlags.SANITIZE_ATOM_MAPS
SANITIZE_CLEANUP: rdkix.Chem.rdmolops.SanitizeFlags  # value = rdkix.Chem.rdmolops.SanitizeFlags.SANITIZE_CLEANUP
SANITIZE_CLEANUPATROPISOMERS: rdkix.Chem.rdmolops.SanitizeFlags  # value = rdkix.Chem.rdmolops.SanitizeFlags.SANITIZE_CLEANUPATROPISOMERS
SANITIZE_CLEANUPCHIRALITY: rdkix.Chem.rdmolops.SanitizeFlags  # value = rdkix.Chem.rdmolops.SanitizeFlags.SANITIZE_CLEANUPCHIRALITY
SANITIZE_CLEANUP_ORGANOMETALLICS: rdkix.Chem.rdmolops.SanitizeFlags  # value = rdkix.Chem.rdmolops.SanitizeFlags.SANITIZE_CLEANUP_ORGANOMETALLICS
SANITIZE_FINDRADICALS: rdkix.Chem.rdmolops.SanitizeFlags  # value = rdkix.Chem.rdmolops.SanitizeFlags.SANITIZE_FINDRADICALS
SANITIZE_KEKULIZE: rdkix.Chem.rdmolops.SanitizeFlags  # value = rdkix.Chem.rdmolops.SanitizeFlags.SANITIZE_KEKULIZE
SANITIZE_MERGEHS: rdkix.Chem.rdChemReactions.SanitizeFlags  # value = rdkix.Chem.rdChemReactions.SanitizeFlags.SANITIZE_MERGEHS
SANITIZE_NONE: rdkix.Chem.rdChemReactions.SanitizeFlags  # value = rdkix.Chem.rdChemReactions.SanitizeFlags.SANITIZE_NONE
SANITIZE_PROPERTIES: rdkix.Chem.rdmolops.SanitizeFlags  # value = rdkix.Chem.rdmolops.SanitizeFlags.SANITIZE_PROPERTIES
SANITIZE_RGROUP_NAMES: rdkix.Chem.rdChemReactions.SanitizeFlags  # value = rdkix.Chem.rdChemReactions.SanitizeFlags.SANITIZE_RGROUP_NAMES
SANITIZE_SETAROMATICITY: rdkix.Chem.rdmolops.SanitizeFlags  # value = rdkix.Chem.rdmolops.SanitizeFlags.SANITIZE_SETAROMATICITY
SANITIZE_SETCONJUGATION: rdkix.Chem.rdmolops.SanitizeFlags  # value = rdkix.Chem.rdmolops.SanitizeFlags.SANITIZE_SETCONJUGATION
SANITIZE_SETHYBRIDIZATION: rdkix.Chem.rdmolops.SanitizeFlags  # value = rdkix.Chem.rdmolops.SanitizeFlags.SANITIZE_SETHYBRIDIZATION
SANITIZE_SYMMRINGS: rdkix.Chem.rdmolops.SanitizeFlags  # value = rdkix.Chem.rdmolops.SanitizeFlags.SANITIZE_SYMMRINGS
STEREO_ABSOLUTE: rdkix.Chem.rdchem.StereoGroupType  # value = rdkix.Chem.rdchem.StereoGroupType.STEREO_ABSOLUTE
STEREO_AND: rdkix.Chem.rdchem.StereoGroupType  # value = rdkix.Chem.rdchem.StereoGroupType.STEREO_AND
STEREO_OR: rdkix.Chem.rdchem.StereoGroupType  # value = rdkix.Chem.rdchem.StereoGroupType.STEREO_OR
TopologicalTorsionFP: rdkix.Chem.rdFingerprintGenerator.FPType  # value = rdkix.Chem.rdFingerprintGenerator.FPType.TopologicalTorsionFP
UNCONSTRAINED_ANIONS: rdkix.Chem.rdchem.ResonanceFlags  # value = rdkix.Chem.rdchem.ResonanceFlags.UNCONSTRAINED_ANIONS
UNCONSTRAINED_CATIONS: rdkix.Chem.rdchem.ResonanceFlags  # value = rdkix.Chem.rdchem.ResonanceFlags.UNCONSTRAINED_CATIONS
logger: rdkix.RDLogger.logger  # value = <rdkix.RDLogger.logger object>
templDir: str = '/Users/runner/work/rdkix-pypi/rdkix-pypi/build/temp.macosx-11.0-arm64-cpython-311/rdkix_install/share/RDKix/Data/'
