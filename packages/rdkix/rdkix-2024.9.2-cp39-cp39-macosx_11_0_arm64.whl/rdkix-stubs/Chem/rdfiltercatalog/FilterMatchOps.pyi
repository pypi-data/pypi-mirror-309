from __future__ import annotations
import rdkix.Chem.rdfiltercatalog
import typing
__all__ = ['And', 'Not', 'Or']
class And(rdkix.Chem.rdfiltercatalog.FilterMatcherBase):
    __instance_size__: typing.ClassVar[int] = 104
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def __init__(self, arg1: FilterMatcherBase, arg2: FilterMatcherBase) -> None:
        """
            C++ signature :
                void __init__(_object*,RDKix::FilterMatcherBase {lvalue},RDKix::FilterMatcherBase {lvalue})
        """
class Not(rdkix.Chem.rdfiltercatalog.FilterMatcherBase):
    __instance_size__: typing.ClassVar[int] = 88
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def __init__(self, arg1: FilterMatcherBase) -> None:
        """
            C++ signature :
                void __init__(_object*,RDKix::FilterMatcherBase {lvalue})
        """
class Or(rdkix.Chem.rdfiltercatalog.FilterMatcherBase):
    __instance_size__: typing.ClassVar[int] = 104
    @staticmethod
    def __reduce__(*args, **kwargs):
        ...
    def __init__(self, arg1: FilterMatcherBase, arg2: FilterMatcherBase) -> None:
        """
            C++ signature :
                void __init__(_object*,RDKix::FilterMatcherBase {lvalue},RDKix::FilterMatcherBase {lvalue})
        """
