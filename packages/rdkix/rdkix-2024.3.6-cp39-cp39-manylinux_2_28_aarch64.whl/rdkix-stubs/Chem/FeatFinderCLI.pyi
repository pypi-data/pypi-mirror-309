from __future__ import annotations
import argparse as argparse
import os as os
from rdkix import Chem
from rdkix.Chem import ChemicalFeatures
from rdkix import RDLogger
import rdkix.RDLogger
import re as re
__all__ = ['Chem', 'ChemicalFeatures', 'GetAtomFeatInfo', 'RDLogger', 'argparse', 'existingFile', 'initParser', 'logger', 'main', 'os', 'processArgs', 're', 'splitExpr']
def GetAtomFeatInfo(factory, mol):
    ...
def existingFile(filename):
    """
     'type' for argparse - check that filename exists 
    """
def initParser():
    """
     Initialize the parser 
    """
def main():
    """
     Main application 
    """
def processArgs(args, parser):
    ...
_splashMessage: str = '\n-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*\n  FeatFinderCLI\n  Part of the RDKix (http://www.rdkit.org)\n-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*\n'
logger: rdkix.RDLogger.logger  # value = <rdkix.RDLogger.logger object>
splitExpr: re.Pattern  # value = re.compile('[ \\t,]')
