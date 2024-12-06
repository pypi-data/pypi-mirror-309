"""
Module containing functions to generate hashes for molecules
"""
from __future__ import annotations
import typing
__all__ = ['HashFunction', 'MolHash']
class HashFunction(Boost.Python.enum):
    AnonymousGraph: typing.ClassVar[HashFunction]  # value = rdkix.Chem.rdMolHash.HashFunction.AnonymousGraph
    ArthorSubstructureOrder: typing.ClassVar[HashFunction]  # value = rdkix.Chem.rdMolHash.HashFunction.ArthorSubstructureOrder
    AtomBondCounts: typing.ClassVar[HashFunction]  # value = rdkix.Chem.rdMolHash.HashFunction.AtomBondCounts
    CanonicalSmiles: typing.ClassVar[HashFunction]  # value = rdkix.Chem.rdMolHash.HashFunction.CanonicalSmiles
    DegreeVector: typing.ClassVar[HashFunction]  # value = rdkix.Chem.rdMolHash.HashFunction.DegreeVector
    ElementGraph: typing.ClassVar[HashFunction]  # value = rdkix.Chem.rdMolHash.HashFunction.ElementGraph
    ExtendedMurcko: typing.ClassVar[HashFunction]  # value = rdkix.Chem.rdMolHash.HashFunction.ExtendedMurcko
    HetAtomProtomer: typing.ClassVar[HashFunction]  # value = rdkix.Chem.rdMolHash.HashFunction.HetAtomProtomer
    HetAtomProtomerv2: typing.ClassVar[HashFunction]  # value = rdkix.Chem.rdMolHash.HashFunction.HetAtomProtomerv2
    HetAtomTautomer: typing.ClassVar[HashFunction]  # value = rdkix.Chem.rdMolHash.HashFunction.HetAtomTautomer
    HetAtomTautomerv2: typing.ClassVar[HashFunction]  # value = rdkix.Chem.rdMolHash.HashFunction.HetAtomTautomerv2
    Mesomer: typing.ClassVar[HashFunction]  # value = rdkix.Chem.rdMolHash.HashFunction.Mesomer
    MolFormula: typing.ClassVar[HashFunction]  # value = rdkix.Chem.rdMolHash.HashFunction.MolFormula
    MurckoScaffold: typing.ClassVar[HashFunction]  # value = rdkix.Chem.rdMolHash.HashFunction.MurckoScaffold
    NetCharge: typing.ClassVar[HashFunction]  # value = rdkix.Chem.rdMolHash.HashFunction.NetCharge
    RedoxPair: typing.ClassVar[HashFunction]  # value = rdkix.Chem.rdMolHash.HashFunction.RedoxPair
    Regioisomer: typing.ClassVar[HashFunction]  # value = rdkix.Chem.rdMolHash.HashFunction.Regioisomer
    SmallWorldIndexBR: typing.ClassVar[HashFunction]  # value = rdkix.Chem.rdMolHash.HashFunction.SmallWorldIndexBR
    SmallWorldIndexBRL: typing.ClassVar[HashFunction]  # value = rdkix.Chem.rdMolHash.HashFunction.SmallWorldIndexBRL
    __slots__: typing.ClassVar[tuple] = tuple()
    names: typing.ClassVar[dict]  # value = {'AnonymousGraph': rdkix.Chem.rdMolHash.HashFunction.AnonymousGraph, 'ElementGraph': rdkix.Chem.rdMolHash.HashFunction.ElementGraph, 'CanonicalSmiles': rdkix.Chem.rdMolHash.HashFunction.CanonicalSmiles, 'MurckoScaffold': rdkix.Chem.rdMolHash.HashFunction.MurckoScaffold, 'ExtendedMurcko': rdkix.Chem.rdMolHash.HashFunction.ExtendedMurcko, 'MolFormula': rdkix.Chem.rdMolHash.HashFunction.MolFormula, 'AtomBondCounts': rdkix.Chem.rdMolHash.HashFunction.AtomBondCounts, 'DegreeVector': rdkix.Chem.rdMolHash.HashFunction.DegreeVector, 'Mesomer': rdkix.Chem.rdMolHash.HashFunction.Mesomer, 'HetAtomTautomer': rdkix.Chem.rdMolHash.HashFunction.HetAtomTautomer, 'HetAtomProtomer': rdkix.Chem.rdMolHash.HashFunction.HetAtomProtomer, 'RedoxPair': rdkix.Chem.rdMolHash.HashFunction.RedoxPair, 'Regioisomer': rdkix.Chem.rdMolHash.HashFunction.Regioisomer, 'NetCharge': rdkix.Chem.rdMolHash.HashFunction.NetCharge, 'SmallWorldIndexBR': rdkix.Chem.rdMolHash.HashFunction.SmallWorldIndexBR, 'SmallWorldIndexBRL': rdkix.Chem.rdMolHash.HashFunction.SmallWorldIndexBRL, 'ArthorSubstructureOrder': rdkix.Chem.rdMolHash.HashFunction.ArthorSubstructureOrder, 'HetAtomTautomerv2': rdkix.Chem.rdMolHash.HashFunction.HetAtomTautomerv2, 'HetAtomProtomerv2': rdkix.Chem.rdMolHash.HashFunction.HetAtomProtomerv2}
    values: typing.ClassVar[dict]  # value = {1: rdkix.Chem.rdMolHash.HashFunction.AnonymousGraph, 2: rdkix.Chem.rdMolHash.HashFunction.ElementGraph, 3: rdkix.Chem.rdMolHash.HashFunction.CanonicalSmiles, 4: rdkix.Chem.rdMolHash.HashFunction.MurckoScaffold, 5: rdkix.Chem.rdMolHash.HashFunction.ExtendedMurcko, 6: rdkix.Chem.rdMolHash.HashFunction.MolFormula, 7: rdkix.Chem.rdMolHash.HashFunction.AtomBondCounts, 8: rdkix.Chem.rdMolHash.HashFunction.DegreeVector, 9: rdkix.Chem.rdMolHash.HashFunction.Mesomer, 10: rdkix.Chem.rdMolHash.HashFunction.HetAtomTautomer, 11: rdkix.Chem.rdMolHash.HashFunction.HetAtomProtomer, 12: rdkix.Chem.rdMolHash.HashFunction.RedoxPair, 13: rdkix.Chem.rdMolHash.HashFunction.Regioisomer, 14: rdkix.Chem.rdMolHash.HashFunction.NetCharge, 15: rdkix.Chem.rdMolHash.HashFunction.SmallWorldIndexBR, 16: rdkix.Chem.rdMolHash.HashFunction.SmallWorldIndexBRL, 17: rdkix.Chem.rdMolHash.HashFunction.ArthorSubstructureOrder, 18: rdkix.Chem.rdMolHash.HashFunction.HetAtomTautomerv2, 19: rdkix.Chem.rdMolHash.HashFunction.HetAtomProtomerv2}
def MolHash(mol: Mol, func: HashFunction, useCxSmiles: bool = False, cxFlagsToSkip: int = 0) -> str:
    """
        Generate a hash for a molecule. The func argument determines which hash is generated.
    
        C++ signature :
            std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> MolHash(RDKix::ROMol,RDKix::MolHash::HashFunction [,bool=False [,unsigned int=0]])
    """
