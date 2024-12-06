"""
 Actual implementation of the FMCS algorithm
This code should be used by importing rdkix.Chem.MCS

"""
from __future__ import annotations
from _heapq import heapify
from _heapq import heappop
from _heapq import heappush
from collections import Counter
from collections import defaultdict
from collections import namedtuple
import copy as copy
import itertools as itertools
from itertools import chain
from itertools import combinations
from rdkix import Chem
from rdkix.Chem.fmcs.fmcs import Atom
from rdkix.Chem.fmcs.fmcs import AtomSmartsNoAromaticity
from rdkix.Chem.fmcs.fmcs import Bond
from rdkix.Chem.fmcs.fmcs import CachingTargetsMatcher
from rdkix.Chem.fmcs.fmcs import CangenNode
from rdkix.Chem.fmcs.fmcs import Default
from rdkix.Chem.fmcs.fmcs import DirectedEdge
from rdkix.Chem.fmcs.fmcs import FragmentedTypedMolecule
from rdkix.Chem.fmcs.fmcs import MATCH
from rdkix.Chem.fmcs.fmcs import MCSResult
from rdkix.Chem.fmcs.fmcs import Molecule as EnumerationMolecule
from rdkix.Chem.fmcs.fmcs import OutgoingEdge
from rdkix.Chem.fmcs.fmcs import SingleBestAtoms
from rdkix.Chem.fmcs.fmcs import SingleBestAtomsCompleteRingsOnly
from rdkix.Chem.fmcs.fmcs import SingleBestBonds
from rdkix.Chem.fmcs.fmcs import SingleBestBondsCompleteRingsOnly
from rdkix.Chem.fmcs.fmcs import Subgraph
from rdkix.Chem.fmcs.fmcs import Timer
from rdkix.Chem.fmcs.fmcs import TypedFragment
from rdkix.Chem.fmcs.fmcs import TypedMolecule
from rdkix.Chem.fmcs.fmcs import Uniquer
from rdkix.Chem.fmcs.fmcs import VerboseCachingTargetsMatcher
from rdkix.Chem.fmcs.fmcs import VerboseHeapOps
from rdkix.Chem.fmcs.fmcs import all_subgraph_extensions
from rdkix.Chem.fmcs.fmcs import assign_isotopes_from_class_tag
from rdkix.Chem.fmcs.fmcs import atom_typer_any
from rdkix.Chem.fmcs.fmcs import atom_typer_elements
from rdkix.Chem.fmcs.fmcs import atom_typer_elements as default_atom_typer
from rdkix.Chem.fmcs.fmcs import atom_typer_isotopes
from rdkix.Chem.fmcs.fmcs import bond_typer_any
from rdkix.Chem.fmcs.fmcs import bond_typer_bondtypes
from rdkix.Chem.fmcs.fmcs import bond_typer_bondtypes as default_bond_typer
from rdkix.Chem.fmcs.fmcs import canon
from rdkix.Chem.fmcs.fmcs import check_completeRingsOnly
from rdkix.Chem.fmcs.fmcs import compute_mcs
from rdkix.Chem.fmcs.fmcs import convert_input_to_typed_molecules
from rdkix.Chem.fmcs.fmcs import enumerate_subgraphs
from rdkix.Chem.fmcs.fmcs import find_duplicates
from rdkix.Chem.fmcs.fmcs import find_extension_size
from rdkix.Chem.fmcs.fmcs import find_extensions
from rdkix.Chem.fmcs.fmcs import find_upper_fragment_size_limits
from rdkix.Chem.fmcs.fmcs import fmcs
from rdkix.Chem.fmcs.fmcs import fragmented_mol_to_enumeration_mols
from rdkix.Chem.fmcs.fmcs import gen_primes
from rdkix.Chem.fmcs.fmcs import generate_smarts
from rdkix.Chem.fmcs.fmcs import get_canonical_bondtype_counts
from rdkix.Chem.fmcs.fmcs import get_canonical_bondtypes
from rdkix.Chem.fmcs.fmcs import get_closure_label
from rdkix.Chem.fmcs.fmcs import get_counts
from rdkix.Chem.fmcs.fmcs import get_initial_cangen_nodes
from rdkix.Chem.fmcs.fmcs import get_isotopes
from rdkix.Chem.fmcs.fmcs import get_selected_atom_classes
from rdkix.Chem.fmcs.fmcs import get_specified_types
from rdkix.Chem.fmcs.fmcs import get_typed_fragment
from rdkix.Chem.fmcs.fmcs import get_typed_molecule
from rdkix.Chem.fmcs.fmcs import intersect_counts
from rdkix.Chem.fmcs.fmcs import main
from rdkix.Chem.fmcs.fmcs import make_arbitrary_smarts
from rdkix.Chem.fmcs.fmcs import make_canonical_smarts
from rdkix.Chem.fmcs.fmcs import make_complete_sdf
from rdkix.Chem.fmcs.fmcs import make_fragment_sdf
from rdkix.Chem.fmcs.fmcs import make_fragment_smiles
from rdkix.Chem.fmcs.fmcs import make_structure_format
from rdkix.Chem.fmcs.fmcs import nonempty_powerset
from rdkix.Chem.fmcs.fmcs import parse_num_atoms
from rdkix.Chem.fmcs.fmcs import parse_select
from rdkix.Chem.fmcs.fmcs import parse_threshold
from rdkix.Chem.fmcs.fmcs import parse_timeout
from rdkix.Chem.fmcs.fmcs import powerset
from rdkix.Chem.fmcs.fmcs import prune_maximize_atoms
from rdkix.Chem.fmcs.fmcs import prune_maximize_bonds
from rdkix.Chem.fmcs.fmcs import remove_unknown_bondtypes
from rdkix.Chem.fmcs.fmcs import rerank
from rdkix.Chem.fmcs.fmcs import restore_isotopes
from rdkix.Chem.fmcs.fmcs import save_atom_classes
from rdkix.Chem.fmcs.fmcs import save_isotopes
from rdkix.Chem.fmcs.fmcs import set_isotopes
from rdkix.Chem.fmcs.fmcs import starting_from
from rdkix.Chem.fmcs.fmcs import subgraph_to_fragment
import re as re
import sys as sys
import time as time
import weakref as weakref
__all__ = ['Atom', 'AtomSmartsNoAromaticity', 'Bond', 'CachingTargetsMatcher', 'CangenNode', 'Chem', 'Counter', 'Default', 'DirectedEdge', 'EnumerationMolecule', 'FragmentedTypedMolecule', 'MATCH', 'MCSResult', 'OutgoingEdge', 'SingleBestAtoms', 'SingleBestAtomsCompleteRingsOnly', 'SingleBestBonds', 'SingleBestBondsCompleteRingsOnly', 'Subgraph', 'Timer', 'TypedFragment', 'TypedMolecule', 'Uniquer', 'VerboseCachingTargetsMatcher', 'VerboseHeapOps', 'all_subgraph_extensions', 'assign_isotopes_from_class_tag', 'atom_typer_any', 'atom_typer_elements', 'atom_typer_isotopes', 'atom_typers', 'bond_typer_any', 'bond_typer_bondtypes', 'bond_typers', 'canon', 'chain', 'check_completeRingsOnly', 'combinations', 'compare_shortcuts', 'compute_mcs', 'convert_input_to_typed_molecules', 'copy', 'default_atom_typer', 'default_bond_typer', 'defaultdict', 'eleno', 'enumerate_subgraphs', 'find_duplicates', 'find_extension_size', 'find_extensions', 'find_upper_fragment_size_limits', 'fmcs', 'fragmented_mol_to_enumeration_mols', 'gen_primes', 'generate_smarts', 'get_canonical_bondtype_counts', 'get_canonical_bondtypes', 'get_closure_label', 'get_counts', 'get_initial_cangen_nodes', 'get_isotopes', 'get_selected_atom_classes', 'get_specified_types', 'get_typed_fragment', 'get_typed_molecule', 'heapify', 'heappop', 'heappush', 'intersect_counts', 'itertools', 'main', 'make_arbitrary_smarts', 'make_canonical_smarts', 'make_complete_sdf', 'make_fragment_sdf', 'make_fragment_smiles', 'make_structure_format', 'namedtuple', 'nonempty_powerset', 'parse_num_atoms', 'parse_select', 'parse_threshold', 'parse_timeout', 'powerset', 'prune_maximize_atoms', 'prune_maximize_bonds', 'range_pat', 're', 'remove_unknown_bondtypes', 'rerank', 'restore_isotopes', 'save_atom_classes', 'save_isotopes', 'set_isotopes', 'starting_from', 'structure_format_functions', 'subgraph_to_fragment', 'sys', 'time', 'value_pat', 'weakref']
atom_typers: dict = {'any': fmcs.atom_typer_any, 'elements': fmcs.atom_typer_elements, 'isotopes': fmcs.atom_typer_isotopes}
bond_typers: dict = {'any': fmcs.bond_typer_any, 'bondtypes': fmcs.bond_typer_bondtypes}
compare_shortcuts: dict = {'topology': ('any', 'any'), 'elements': ('elements', 'any'), 'types': ('elements', 'bondtypes')}
eleno: int = 52
range_pat: re.Pattern  # value = re.compile('(\\d+)-(\\d*)')
structure_format_functions: dict = {'fragment-smiles': fmcs.make_fragment_smiles, 'fragment-sdf': fmcs.make_fragment_sdf, 'complete-sdf': fmcs.make_complete_sdf}
value_pat: re.Pattern  # value = re.compile('(\\d+)')
