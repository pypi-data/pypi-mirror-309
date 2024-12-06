from __future__ import annotations
from rdkix.Dbase import DbConnection
from rdkix.ML.Data import Quantize
__all__ = ['DbConnection', 'Quantize', 'Usage', 'runIt']
def Usage():
    ...
def runIt(namesAndTypes, dbConnect, nBounds, resCol, typesToDo = ['float']):
    ...
