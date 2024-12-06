"""
Module containing classes and functions for enumerating molecules
"""
from __future__ import annotations
import rdkix.Chem
import typing
__all__ = ['Enumerate', 'EnumeratorType', 'MolEnumeratorParams']
class EnumeratorType(Boost.Python.enum):
    LinkNode: typing.ClassVar[EnumeratorType]  # value = rdkix.Chem.rdMolEnumerator.EnumeratorType.LinkNode
    PositionVariation: typing.ClassVar[EnumeratorType]  # value = rdkix.Chem.rdMolEnumerator.EnumeratorType.PositionVariation
    RepeatUnit: typing.ClassVar[EnumeratorType]  # value = rdkix.Chem.rdMolEnumerator.EnumeratorType.RepeatUnit
    __slots__: typing.ClassVar[tuple] = tuple()
    names: typing.ClassVar[dict]  # value = {'LinkNode': rdkix.Chem.rdMolEnumerator.EnumeratorType.LinkNode, 'PositionVariation': rdkix.Chem.rdMolEnumerator.EnumeratorType.PositionVariation, 'RepeatUnit': rdkix.Chem.rdMolEnumerator.EnumeratorType.RepeatUnit}
    values: typing.ClassVar[dict]  # value = {0: rdkix.Chem.rdMolEnumerator.EnumeratorType.LinkNode, 1: rdkix.Chem.rdMolEnumerator.EnumeratorType.PositionVariation, 2: rdkix.Chem.rdMolEnumerator.EnumeratorType.RepeatUnit}
class MolEnumeratorParams(Boost.Python.instance):
    """
    Molecular enumerator parameters
    """
    __instance_size__: typing.ClassVar[int] = 64
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def SetEnumerationOperator(self, typ: EnumeratorType) -> None:
        """
            set the operator to be used for enumeration
        
            C++ signature :
                void SetEnumerationOperator(RDKix::MolEnumerator::MolEnumeratorParams*,(anonymous namespace)::EnumeratorTypes)
        """
    @typing.overload
    def __init__(self) -> None:
        """
            C++ signature :
                void __init__(_object*)
        """
    @typing.overload
    def __init__(self, arg1: EnumeratorType) -> typing.Any:
        """
            C++ signature :
                void* __init__(boost::python::api::object,(anonymous namespace)::EnumeratorTypes)
        """
    @property
    def doRandom(*args, **kwargs):
        """
        do random enumeration (not yet implemented
        """
    @doRandom.setter
    def doRandom(*args, **kwargs):
        ...
    @property
    def maxToEnumerate(*args, **kwargs):
        """
        maximum number of molecules to enumerate
        """
    @maxToEnumerate.setter
    def maxToEnumerate(*args, **kwargs):
        ...
    @property
    def randomSeed(*args, **kwargs):
        """
        seed for the random enumeration (not yet implemented
        """
    @randomSeed.setter
    def randomSeed(*args, **kwargs):
        ...
    @property
    def sanitize(*args, **kwargs):
        """
        sanitize molecules after enumeration
        """
    @sanitize.setter
    def sanitize(*args, **kwargs):
        ...
@typing.overload
def Enumerate(mol: Mol, maxPerOperation: int = 0) -> rdkix.Chem.MolBundle:
    """
        do an enumeration and return a MolBundle.
          If maxPerOperation is >0 that will be used as the maximum number of molecules which 
            can be returned by any given operation.
        Limitations:
          - the current implementation does not support molecules which include both
            SRUs and LINKNODEs
          - Overlapping SRUs, i.e. where one monomer is contained within another, are
            not supported
    
        C++ signature :
            RDKix::MolBundle* Enumerate(RDKix::ROMol [,unsigned int=0])
    """
@typing.overload
def Enumerate(mol: Mol, enumParams: MolEnumeratorParams) -> rdkix.Chem.MolBundle:
    """
        do an enumeration for the supplied parameter type and return a MolBundle
        Limitations:
          - Overlapping SRUs, i.e. where one monomer is contained within another, are
            not supported
    
        C++ signature :
            RDKix::MolBundle* Enumerate(RDKix::ROMol,RDKix::MolEnumerator::MolEnumeratorParams)
    """
