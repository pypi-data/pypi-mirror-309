from __future__ import annotations
import logging as logging
from rdkix.Chem import rdinchi
import rdkix.RDLogger
from rdkix import RDLogger
__all__: list = ['MolToInchiAndAuxInfo', 'MolToInchi', 'MolBlockToInchiAndAuxInfo', 'MolBlockToInchi', 'MolFromInchi', 'InchiReadWriteError', 'InchiToInchiKey', 'MolToInchiKey', 'INCHI_AVAILABLE']
class InchiReadWriteError(Exception):
    pass
def InchiToInchiKey(inchi):
    """
    Return the InChI key for the given InChI string. Return None on error
    """
def MolBlockToInchi(molblock, options = '', logLevel = None, treatWarningAsError = False):
    """
    Returns the standard InChI string for a mol block
    
        Keyword arguments:
        logLevel -- the log level used for logging logs and messages from InChI
        API. set to None to diable the logging completely
        treatWarningAsError -- set to True to raise an exception in case of a
        molecule that generates warning in calling InChI API. The resultant InChI
        string and AuxInfo string as well as the error message are encoded in the
        exception.
    
        Returns:
        the standard InChI string returned by InChI API for the input molecule
        
    """
def MolBlockToInchiAndAuxInfo(molblock, options = '', logLevel = None, treatWarningAsError = False):
    """
    Returns the standard InChI string and InChI auxInfo for a mol block
    
        Keyword arguments:
        logLevel -- the log level used for logging logs and messages from InChI
        API. set to None to diable the logging completely
        treatWarningAsError -- set to True to raise an exception in case of a
        molecule that generates warning in calling InChI API. The resultant InChI
        string and AuxInfo string as well as the error message are encoded in the
        exception.
    
        Returns:
        a tuple of the standard InChI string and the auxInfo string returned by
        InChI API, in that order, for the input molecule
        
    """
def MolFromInchi(inchi, sanitize = True, removeHs = True, logLevel = None, treatWarningAsError = False):
    """
    Construct a molecule from a InChI string
    
        Keyword arguments:
        sanitize -- set to True to enable sanitization of the molecule. Default is
        True
        removeHs -- set to True to remove Hydrogens from a molecule. This only
        makes sense when sanitization is enabled
        logLevel -- the log level used for logging logs and messages from InChI
        API. set to None to diable the logging completely
        treatWarningAsError -- set to True to raise an exception in case of a
        molecule that generates warning in calling InChI API. The resultant
        molecule  and error message are part of the excpetion
    
        Returns:
        a rdkix.Chem.rdchem.Mol instance
        
    """
def MolToInchi(mol, options = '', logLevel = None, treatWarningAsError = False):
    """
    Returns the standard InChI string for a molecule
    
        Keyword arguments:
        logLevel -- the log level used for logging logs and messages from InChI
        API. set to None to diable the logging completely
        treatWarningAsError -- set to True to raise an exception in case of a
        molecule that generates warning in calling InChI API. The resultant InChI
        string and AuxInfo string as well as the error message are encoded in the
        exception.
    
        Returns:
        the standard InChI string returned by InChI API for the input molecule
        
    """
def MolToInchiAndAuxInfo(mol, options = '', logLevel = None, treatWarningAsError = False):
    """
    Returns the standard InChI string and InChI auxInfo for a molecule
    
        Keyword arguments:
        logLevel -- the log level used for logging logs and messages from InChI
        API. set to None to diable the logging completely
        treatWarningAsError -- set to True to raise an exception in case of a
        molecule that generates warning in calling InChI API. The resultant InChI
        string and AuxInfo string as well as the error message are encoded in the
        exception.
    
        Returns:
        a tuple of the standard InChI string and the auxInfo string returned by
        InChI API, in that order, for the input molecule
        
    """
def MolToInchiKey(mol, options = ''):
    """
    Returns the standard InChI key for a molecule
    
        Returns:
        the standard InChI key returned by InChI API for the input molecule
        
    """
INCHI_AVAILABLE: bool = True
logLevelToLogFunctionLookup: dict = {20: rdkix.RDLogger.logger.info, 10: rdkix.RDLogger.logger.debug, 30: rdkix.RDLogger.logger.warning, 50: rdkix.RDLogger.logger.critical, 40: rdkix.RDLogger.logger.error}
logger: rdkix.RDLogger.logger  # value = <rdkix.RDLogger.logger object>
