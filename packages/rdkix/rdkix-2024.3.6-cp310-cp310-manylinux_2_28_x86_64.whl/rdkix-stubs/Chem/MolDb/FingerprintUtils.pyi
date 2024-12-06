from __future__ import annotations
import pickle as pickle
from rdkix import Chem
from rdkix import DataStructs
import rdkix.DataStructs.cDataStructs
import typing
__all__ = ['BuildAtomPairFP', 'BuildAvalonFP', 'BuildMorganFP', 'BuildPharm2DFP', 'BuildRDKixFP', 'BuildSigFactory', 'BuildTorsionsFP', 'Chem', 'DataStructs', 'DepickleFP', 'LayeredOptions', 'pickle', 'similarityMethods', 'supportedSimilarityMethods']
class LayeredOptions:
    fpSize: typing.ClassVar[int] = 1024
    loadLayerFlags: typing.ClassVar[int] = 4294967295
    maxPath: typing.ClassVar[int] = 6
    minPath: typing.ClassVar[int] = 1
    nWords: typing.ClassVar[int] = 32
    searchLayerFlags: typing.ClassVar[int] = 7
    wordSize: typing.ClassVar[int] = 32
    @staticmethod
    def GetFingerprint(mol, query = True):
        ...
    @staticmethod
    def GetQueryText(mol, query = True):
        ...
    @staticmethod
    def GetWords(mol, query = True):
        ...
def BuildAtomPairFP(mol):
    ...
def BuildAvalonFP(mol, smiles = None):
    ...
def BuildMorganFP(mol):
    ...
def BuildPharm2DFP(mol):
    ...
def BuildRDKixFP(mol):
    ...
def BuildSigFactory(options = None, fdefFile = None, bins = [(2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 100)], skipFeats = ('LumpedHydrophobe', 'ZnBinder')):
    ...
def BuildTorsionsFP(mol):
    ...
def DepickleFP(pkl, similarityMethod):
    ...
similarityMethods: dict = {'RDK': rdkix.DataStructs.cDataStructs.ExplicitBitVect, 'AtomPairs': rdkix.DataStructs.cDataStructs.IntSparseIntVect, 'TopologicalTorsions': rdkix.DataStructs.cDataStructs.LongSparseIntVect, 'Pharm2D': rdkix.DataStructs.cDataStructs.SparseBitVect, 'Gobbi2D': rdkix.DataStructs.cDataStructs.SparseBitVect, 'Morgan': rdkix.DataStructs.cDataStructs.UIntSparseIntVect, 'Avalon': rdkix.DataStructs.cDataStructs.ExplicitBitVect}
supportedSimilarityMethods: list = ['RDK', 'AtomPairs', 'TopologicalTorsions', 'Pharm2D', 'Gobbi2D', 'Morgan', 'Avalon']
