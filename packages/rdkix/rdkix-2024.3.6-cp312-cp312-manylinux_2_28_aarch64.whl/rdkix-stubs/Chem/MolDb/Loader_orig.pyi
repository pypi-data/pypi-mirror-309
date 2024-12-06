from __future__ import annotations
from rdkix import Chem
from rdkix.Chem import AllChem
from rdkix.Chem import Crippen
from rdkix.Chem import Descriptors
from rdkix.Chem import Lipinski
from rdkix.Dbase.DbConnection import DbConnect
from rdkix.Dbase import DbModule
import rdkix.RDLogger
from rdkix import RDLogger as logging
import re as re
__all__ = ['AllChem', 'Chem', 'ConvertRows', 'Crippen', 'DbConnect', 'DbModule', 'Descriptors', 'Lipinski', 'LoadDb', 'ProcessMol', 'logger', 'logging', 're']
def ConvertRows(rows, globalProps, defaultVal, skipSmiles):
    ...
def LoadDb(suppl, dbName, nameProp = '_Name', nameCol = 'compound_id', silent = False, redraw = False, errorsTo = None, keepHs = False, defaultVal = 'N/A', skipProps = False, regName = 'molecules', skipSmiles = False, maxRowsCached = -1, uniqNames = False, addComputedProps = False, lazySupplier = False, startAnew = True):
    ...
def ProcessMol(mol, typeConversions, globalProps, nDone, nameProp = '_Name', nameCol = 'compound_id', redraw = False, keepHs = False, skipProps = False, addComputedProps = False, skipSmiles = False, uniqNames = None, namesSeen = None):
    ...
logger: rdkix.RDLogger.logger  # value = <rdkix.RDLogger.logger object>
