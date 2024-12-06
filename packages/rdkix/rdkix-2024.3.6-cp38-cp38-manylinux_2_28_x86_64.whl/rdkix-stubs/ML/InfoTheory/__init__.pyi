"""
 Information Theory functionality

"""
from __future__ import annotations
from rdkix.ML.InfoTheory.rdInfoTheory import BitCorrMatGenerator
from rdkix.ML.InfoTheory.rdInfoTheory import InfoBitRanker
from rdkix.ML.InfoTheory.rdInfoTheory import InfoType
from .rdInfoTheory import *
__all__ = ['BIASCHISQUARE', 'BIASENTROPY', 'BitCorrMatGenerator', 'CHISQUARE', 'ENTROPY', 'InfoBitRanker', 'InfoType', 'rdInfoTheory']
BIASCHISQUARE: rdInfoTheory.InfoType  # value = rdkix.ML.InfoTheory.rdInfoTheory.InfoType.BIASCHISQUARE
BIASENTROPY: rdInfoTheory.InfoType  # value = rdkix.ML.InfoTheory.rdInfoTheory.InfoType.BIASENTROPY
CHISQUARE: rdInfoTheory.InfoType  # value = rdkix.ML.InfoTheory.rdInfoTheory.InfoType.CHISQUARE
ENTROPY: rdInfoTheory.InfoType  # value = rdkix.ML.InfoTheory.rdInfoTheory.InfoType.ENTROPY
