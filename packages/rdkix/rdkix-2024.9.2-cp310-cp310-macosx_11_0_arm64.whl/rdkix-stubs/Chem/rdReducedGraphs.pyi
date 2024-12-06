"""
Module containing functions to generate and work with reduced graphs
"""
from __future__ import annotations
import rdkix.Chem
import typing
__all__ = ['GenerateErGFingerprintForReducedGraph', 'GenerateMolExtendedReducedGraph', 'GetErGFingerprint']
def GenerateErGFingerprintForReducedGraph(mol: Mol, atomTypes: typing.Any = 0, fuzzIncrement: float = 0.3, minPath: int = 1, maxPath: int = 15) -> typing.Any:
    """
        Returns the ErG fingerprint vector for a reduced graph
    
        C++ signature :
            _object* GenerateErGFingerprintForReducedGraph(RDKix::ROMol [,boost::python::api::object=0 [,double=0.3 [,int=1 [,int=15]]]])
    """
def GenerateMolExtendedReducedGraph(mol: Mol, atomTypes: typing.Any = 0) -> rdkix.Chem.Mol:
    """
        Returns the reduced graph for a molecule
    
        C++ signature :
            RDKix::ROMol* GenerateMolExtendedReducedGraph(RDKix::ROMol [,boost::python::api::object=0])
    """
def GetErGFingerprint(mol: Mol, atomTypes: typing.Any = 0, fuzzIncrement: float = 0.3, minPath: int = 1, maxPath: int = 15) -> typing.Any:
    """
        Returns the ErG fingerprint vector for a molecule
    
        C++ signature :
            _object* GetErGFingerprint(RDKix::ROMol [,boost::python::api::object=0 [,double=0.3 [,int=1 [,int=15]]]])
    """
