from __future__ import annotations
import _io
from _io import StringIO
import os as os
from rdkix import Chem
from rdkix import RDConfig
import rdkix.VLib.Filter
from rdkix.VLib import Filter
from rdkix.VLib.NodeLib import SDSupply
from rdkix.VLib.NodeLib import SmartsMolFilter
import rdkix.VLib.NodeLib.SmartsMolFilter
import rdkix.VLib.NodeLib.SmartsRemover
from rdkix.VLib.NodeLib import SmartsRemover
from rdkix.VLib.NodeLib import SmilesDupeFilter
import rdkix.VLib.NodeLib.SmilesDupeFilter
from rdkix.VLib.NodeLib import SmilesOutput
import rdkix.VLib.NodeLib.SmilesOutput
from rdkix.VLib import Supply
import rdkix.VLib.Supply
__all__ = ['Chem', 'Filter', 'RDConfig', 'SDSupply', 'SmartsMolFilter', 'SmartsRemover', 'SmilesDupeFilter', 'SmilesOutput', 'StringIO', 'Supply', 'atsFilter', 'dupeFilter', 'i', 'io', 'metals', 'mols', 'os', 'output', 'remover', 'salts', 'smaFilter', 'smis', 'supplier']
atsFilter: rdkix.VLib.Filter.FilterNode  # value = <rdkix.VLib.Filter.FilterNode object>
dupeFilter: rdkix.VLib.NodeLib.SmilesDupeFilter.DupeFilter  # value = <rdkix.VLib.NodeLib.SmilesDupeFilter.DupeFilter object>
i: int = 6
io: _io.StringIO  # value = <_io.StringIO object>
metals: str = '[#21,#22,#23,#24,#25,#26,#27,#28,#29,#39,#40,#41,#42,#43,#44,#45,#46,#47,#57,#58,#59,#60,#61,#62,#63,#64,#65,#66,#67,#68,#69,#70,#71,#72,#73,#74,#75,#76,#77,#78,#79]'
mols: list  # value = [<rdkix.Chem.rdchem.Mol object>, <rdkix.Chem.rdchem.Mol object>, <rdkix.Chem.rdchem.Mol object>, <rdkix.Chem.rdchem.Mol object>, <rdkix.Chem.rdchem.Mol object>, <rdkix.Chem.rdchem.Mol object>, <rdkix.Chem.rdchem.Mol object>]
output: rdkix.VLib.NodeLib.SmilesOutput.OutputNode  # value = <rdkix.VLib.NodeLib.SmilesOutput.OutputNode object>
remover: rdkix.VLib.NodeLib.SmartsRemover.SmartsRemover  # value = <rdkix.VLib.NodeLib.SmartsRemover.SmartsRemover object>
salts: list = ['[Cl;H1&X1,-]', '[Na+]', '[O;H2,H1&-,X0&-2]']
smaFilter: rdkix.VLib.NodeLib.SmartsMolFilter.SmartsFilter  # value = <rdkix.VLib.NodeLib.SmartsMolFilter.SmartsFilter object>
smis: list = ['CCOC', 'CCO.Cl', 'CC(=O)[O-].[Na+]', 'CC[Cu]CC', 'OCC', 'C[N+](C)(C)C.[Cl-]', '[Na+].[Cl-]']
supplier: rdkix.VLib.Supply.SupplyNode  # value = <rdkix.VLib.Supply.SupplyNode object>
