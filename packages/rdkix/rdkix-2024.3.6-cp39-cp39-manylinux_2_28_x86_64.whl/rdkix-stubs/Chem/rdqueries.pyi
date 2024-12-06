"""
Module containing RDKix functionality for querying molecules.
"""
from __future__ import annotations
import rdkix.Chem
import typing
__all__ = ['AAtomQueryAtom', 'AHAtomQueryAtom', 'AtomNumEqualsQueryAtom', 'AtomNumGreaterQueryAtom', 'AtomNumLessQueryAtom', 'ExplicitDegreeEqualsQueryAtom', 'ExplicitDegreeGreaterQueryAtom', 'ExplicitDegreeLessQueryAtom', 'ExplicitValenceEqualsQueryAtom', 'ExplicitValenceGreaterQueryAtom', 'ExplicitValenceLessQueryAtom', 'FormalChargeEqualsQueryAtom', 'FormalChargeGreaterQueryAtom', 'FormalChargeLessQueryAtom', 'HCountEqualsQueryAtom', 'HCountGreaterQueryAtom', 'HCountLessQueryAtom', 'HasBitVectPropWithValueQueryAtom', 'HasBoolPropWithValueQueryAtom', 'HasBoolPropWithValueQueryBond', 'HasChiralTagQueryAtom', 'HasDoublePropWithValueQueryAtom', 'HasDoublePropWithValueQueryBond', 'HasIntPropWithValueQueryAtom', 'HasIntPropWithValueQueryBond', 'HasPropQueryAtom', 'HasPropQueryBond', 'HasStringPropWithValueQueryAtom', 'HasStringPropWithValueQueryBond', 'HybridizationEqualsQueryAtom', 'HybridizationGreaterQueryAtom', 'HybridizationLessQueryAtom', 'InNRingsEqualsQueryAtom', 'InNRingsGreaterQueryAtom', 'InNRingsLessQueryAtom', 'IsAliphaticQueryAtom', 'IsAromaticQueryAtom', 'IsBridgeheadQueryAtom', 'IsInRingQueryAtom', 'IsUnsaturatedQueryAtom', 'IsotopeEqualsQueryAtom', 'IsotopeGreaterQueryAtom', 'IsotopeLessQueryAtom', 'MAtomQueryAtom', 'MHAtomQueryAtom', 'MassEqualsQueryAtom', 'MassGreaterQueryAtom', 'MassLessQueryAtom', 'MinRingSizeEqualsQueryAtom', 'MinRingSizeGreaterQueryAtom', 'MinRingSizeLessQueryAtom', 'MissingChiralTagQueryAtom', 'NonHydrogenDegreeEqualsQueryAtom', 'NonHydrogenDegreeGreaterQueryAtom', 'NonHydrogenDegreeLessQueryAtom', 'NumAliphaticHeteroatomNeighborsEqualsQueryAtom', 'NumAliphaticHeteroatomNeighborsGreaterQueryAtom', 'NumAliphaticHeteroatomNeighborsLessQueryAtom', 'NumHeteroatomNeighborsEqualsQueryAtom', 'NumHeteroatomNeighborsGreaterQueryAtom', 'NumHeteroatomNeighborsLessQueryAtom', 'NumRadicalElectronsEqualsQueryAtom', 'NumRadicalElectronsGreaterQueryAtom', 'NumRadicalElectronsLessQueryAtom', 'QAtomQueryAtom', 'QHAtomQueryAtom', 'ReplaceAtomWithQueryAtom', 'RingBondCountEqualsQueryAtom', 'RingBondCountGreaterQueryAtom', 'RingBondCountLessQueryAtom', 'TotalDegreeEqualsQueryAtom', 'TotalDegreeGreaterQueryAtom', 'TotalDegreeLessQueryAtom', 'TotalValenceEqualsQueryAtom', 'TotalValenceGreaterQueryAtom', 'TotalValenceLessQueryAtom', 'XAtomQueryAtom', 'XHAtomQueryAtom']
def AAtomQueryAtom(negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms when AAtom is True.
    
        C++ signature :
            RDKix::QueryAtom* AAtomQueryAtom([ bool=False])
    """
def AHAtomQueryAtom(negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms when AHAtom is True.
    
        C++ signature :
            RDKix::QueryAtom* AHAtomQueryAtom([ bool=False])
    """
def AtomNumEqualsQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where AtomNum is equal to the target value.
    
        C++ signature :
            RDKix::QueryAtom* AtomNumEqualsQueryAtom(int [,bool=False])
    """
def AtomNumGreaterQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where AtomNum is equal to the target value.
        NOTE: the direction of comparison is reversed relative to the C++ API
    
        C++ signature :
            RDKix::QueryAtom* AtomNumGreaterQueryAtom(int [,bool=False])
    """
def AtomNumLessQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where AtomNum is less than the target value.
        NOTE: the direction of comparison is reversed relative to the C++ API
    
        C++ signature :
            RDKix::QueryAtom* AtomNumLessQueryAtom(int [,bool=False])
    """
def ExplicitDegreeEqualsQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where ExplicitDegree is equal to the target value.
    
        C++ signature :
            RDKix::QueryAtom* ExplicitDegreeEqualsQueryAtom(int [,bool=False])
    """
def ExplicitDegreeGreaterQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where ExplicitDegree is equal to the target value.
        NOTE: the direction of comparison is reversed relative to the C++ API
    
        C++ signature :
            RDKix::QueryAtom* ExplicitDegreeGreaterQueryAtom(int [,bool=False])
    """
def ExplicitDegreeLessQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where ExplicitDegree is less than the target value.
        NOTE: the direction of comparison is reversed relative to the C++ API
    
        C++ signature :
            RDKix::QueryAtom* ExplicitDegreeLessQueryAtom(int [,bool=False])
    """
def ExplicitValenceEqualsQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where ExplicitValence is equal to the target value.
    
        C++ signature :
            RDKix::QueryAtom* ExplicitValenceEqualsQueryAtom(int [,bool=False])
    """
def ExplicitValenceGreaterQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where ExplicitValence is equal to the target value.
        NOTE: the direction of comparison is reversed relative to the C++ API
    
        C++ signature :
            RDKix::QueryAtom* ExplicitValenceGreaterQueryAtom(int [,bool=False])
    """
def ExplicitValenceLessQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where ExplicitValence is less than the target value.
        NOTE: the direction of comparison is reversed relative to the C++ API
    
        C++ signature :
            RDKix::QueryAtom* ExplicitValenceLessQueryAtom(int [,bool=False])
    """
def FormalChargeEqualsQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where FormalCharge is equal to the target value.
    
        C++ signature :
            RDKix::QueryAtom* FormalChargeEqualsQueryAtom(int [,bool=False])
    """
def FormalChargeGreaterQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where FormalCharge is equal to the target value.
        NOTE: the direction of comparison is reversed relative to the C++ API
    
        C++ signature :
            RDKix::QueryAtom* FormalChargeGreaterQueryAtom(int [,bool=False])
    """
def FormalChargeLessQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where FormalCharge is less than the target value.
        NOTE: the direction of comparison is reversed relative to the C++ API
    
        C++ signature :
            RDKix::QueryAtom* FormalChargeLessQueryAtom(int [,bool=False])
    """
def HCountEqualsQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where HCount is equal to the target value.
    
        C++ signature :
            RDKix::QueryAtom* HCountEqualsQueryAtom(int [,bool=False])
    """
def HCountGreaterQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where HCount is equal to the target value.
        NOTE: the direction of comparison is reversed relative to the C++ API
    
        C++ signature :
            RDKix::QueryAtom* HCountGreaterQueryAtom(int [,bool=False])
    """
def HCountLessQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where HCount is less than the target value.
        NOTE: the direction of comparison is reversed relative to the C++ API
    
        C++ signature :
            RDKix::QueryAtom* HCountLessQueryAtom(int [,bool=False])
    """
def HasBitVectPropWithValueQueryAtom(propname: str, val: ExplicitBitVect, negate: bool = False, tolerance: float = 0) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches when the property 'propname' has the specified explicit bit vector value.  The Tolerance is the allowed Tanimoto difference
    
        C++ signature :
            RDKix::QueryAtom* HasBitVectPropWithValueQueryAtom(std::string,ExplicitBitVect [,bool=False [,float=0]])
    """
def HasBoolPropWithValueQueryAtom(propname: str, val: bool, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches when the property 'propname' has the specified boolean value.
    
        C++ signature :
            RDKix::QueryAtom* HasBoolPropWithValueQueryAtom(std::string,bool [,bool=False])
    """
def HasBoolPropWithValueQueryBond(propname: str, val: bool, negate: bool = False) -> rdkix.Chem.QueryBond:
    """
        Returns a QueryBond that matches when the property 'propname' has the specified boolean value.
    
        C++ signature :
            RDKix::QueryBond* HasBoolPropWithValueQueryBond(std::string,bool [,bool=False])
    """
def HasChiralTagQueryAtom(negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms when HasChiralTag is True.
    
        C++ signature :
            RDKix::QueryAtom* HasChiralTagQueryAtom([ bool=False])
    """
def HasDoublePropWithValueQueryAtom(propname: str, val: float, negate: bool = False, tolerance: float = 0.0) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches when the property 'propname' has the specified value +- tolerance
    
        C++ signature :
            RDKix::QueryAtom* HasDoublePropWithValueQueryAtom(std::string,double [,bool=False [,double=0.0]])
    """
def HasDoublePropWithValueQueryBond(propname: str, val: float, negate: bool = False, tolerance: float = 0.0) -> rdkix.Chem.QueryBond:
    """
        Returns a QueryBond that matches when the property 'propname' has the specified value +- tolerance
    
        C++ signature :
            RDKix::QueryBond* HasDoublePropWithValueQueryBond(std::string,double [,bool=False [,double=0.0]])
    """
def HasIntPropWithValueQueryAtom(propname: str, val: int, negate: bool = False, tolerance: int = 0) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches when the property 'propname' has the specified int value.
    
        C++ signature :
            RDKix::QueryAtom* HasIntPropWithValueQueryAtom(std::string,int [,bool=False [,int=0]])
    """
def HasIntPropWithValueQueryBond(propname: str, val: int, negate: bool = False, tolerance: int = 0) -> rdkix.Chem.QueryBond:
    """
        Returns a QueryBond that matches when the property 'propname' has the specified int value.
    
        C++ signature :
            RDKix::QueryBond* HasIntPropWithValueQueryBond(std::string,int [,bool=False [,int=0]])
    """
def HasPropQueryAtom(propname: str, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches when the property 'propname' exists in the atom.
    
        C++ signature :
            RDKix::QueryAtom* HasPropQueryAtom(std::string [,bool=False])
    """
@typing.overload
def HasPropQueryBond(propname: str, negate: bool = False) -> rdkix.Chem.QueryBond:
    """
        Returns a QueryBond that matches when the property 'propname' exists in the bond.
    
        C++ signature :
            RDKix::QueryBond* HasPropQueryBond(std::string [,bool=False])
    """
@typing.overload
def HasPropQueryBond(propname: str, negate: bool = False) -> rdkix.Chem.QueryBond:
    """
        Returns a QueryBond that matches when the property 'propname' exists in the bond.
    
        C++ signature :
            RDKix::QueryBond* HasPropQueryBond(std::string [,bool=False])
    """
@typing.overload
def HasPropQueryBond(propname: str, negate: bool = False) -> rdkix.Chem.QueryBond:
    """
        Returns a QueryBond that matches when the property 'propname' exists in the bond.
    
        C++ signature :
            RDKix::QueryBond* HasPropQueryBond(std::string [,bool=False])
    """
def HasStringPropWithValueQueryAtom(propname: str, val: str, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches when the property 'propname' has the specified string value.
    
        C++ signature :
            RDKix::QueryAtom* HasStringPropWithValueQueryAtom(std::string,std::string [,bool=False])
    """
def HasStringPropWithValueQueryBond(propname: str, val: str, negate: bool = False) -> rdkix.Chem.QueryBond:
    """
        Returns a QueryBond that matches when the property 'propname' has the specified string value.
    
        C++ signature :
            RDKix::QueryBond* HasStringPropWithValueQueryBond(std::string,std::string [,bool=False])
    """
def HybridizationEqualsQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where Hybridization is equal to the target value.
    
        C++ signature :
            RDKix::QueryAtom* HybridizationEqualsQueryAtom(int [,bool=False])
    """
def HybridizationGreaterQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where Hybridization is equal to the target value.
        NOTE: the direction of comparison is reversed relative to the C++ API
    
        C++ signature :
            RDKix::QueryAtom* HybridizationGreaterQueryAtom(int [,bool=False])
    """
def HybridizationLessQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where Hybridization is less than the target value.
        NOTE: the direction of comparison is reversed relative to the C++ API
    
        C++ signature :
            RDKix::QueryAtom* HybridizationLessQueryAtom(int [,bool=False])
    """
def InNRingsEqualsQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where InNRings is equal to the target value.
    
        C++ signature :
            RDKix::QueryAtom* InNRingsEqualsQueryAtom(int [,bool=False])
    """
def InNRingsGreaterQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where InNRings is equal to the target value.
        NOTE: the direction of comparison is reversed relative to the C++ API
    
        C++ signature :
            RDKix::QueryAtom* InNRingsGreaterQueryAtom(int [,bool=False])
    """
def InNRingsLessQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where InNRings is less than the target value.
        NOTE: the direction of comparison is reversed relative to the C++ API
    
        C++ signature :
            RDKix::QueryAtom* InNRingsLessQueryAtom(int [,bool=False])
    """
def IsAliphaticQueryAtom(negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms when IsAliphatic is True.
    
        C++ signature :
            RDKix::QueryAtom* IsAliphaticQueryAtom([ bool=False])
    """
def IsAromaticQueryAtom(negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms when IsAromatic is True.
    
        C++ signature :
            RDKix::QueryAtom* IsAromaticQueryAtom([ bool=False])
    """
def IsBridgeheadQueryAtom(negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms when IsBridgehead is True.
    
        C++ signature :
            RDKix::QueryAtom* IsBridgeheadQueryAtom([ bool=False])
    """
def IsInRingQueryAtom(negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms when IsInRing is True.
    
        C++ signature :
            RDKix::QueryAtom* IsInRingQueryAtom([ bool=False])
    """
def IsUnsaturatedQueryAtom(negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms when IsUnsaturated is True.
    
        C++ signature :
            RDKix::QueryAtom* IsUnsaturatedQueryAtom([ bool=False])
    """
def IsotopeEqualsQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where Isotope is equal to the target value.
    
        C++ signature :
            RDKix::QueryAtom* IsotopeEqualsQueryAtom(int [,bool=False])
    """
def IsotopeGreaterQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where Isotope is equal to the target value.
        NOTE: the direction of comparison is reversed relative to the C++ API
    
        C++ signature :
            RDKix::QueryAtom* IsotopeGreaterQueryAtom(int [,bool=False])
    """
def IsotopeLessQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where Isotope is less than the target value.
        NOTE: the direction of comparison is reversed relative to the C++ API
    
        C++ signature :
            RDKix::QueryAtom* IsotopeLessQueryAtom(int [,bool=False])
    """
def MAtomQueryAtom(negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms when MAtom is True.
    
        C++ signature :
            RDKix::QueryAtom* MAtomQueryAtom([ bool=False])
    """
def MHAtomQueryAtom(negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms when MHAtom is True.
    
        C++ signature :
            RDKix::QueryAtom* MHAtomQueryAtom([ bool=False])
    """
def MassEqualsQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where Mass is equal to the target value.
    
        C++ signature :
            RDKix::QueryAtom* MassEqualsQueryAtom(int [,bool=False])
    """
def MassGreaterQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where Mass is equal to the target value.
        NOTE: the direction of comparison is reversed relative to the C++ API
    
        C++ signature :
            RDKix::QueryAtom* MassGreaterQueryAtom(int [,bool=False])
    """
def MassLessQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where Mass is less than the target value.
        NOTE: the direction of comparison is reversed relative to the C++ API
    
        C++ signature :
            RDKix::QueryAtom* MassLessQueryAtom(int [,bool=False])
    """
def MinRingSizeEqualsQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where MinRingSize is equal to the target value.
    
        C++ signature :
            RDKix::QueryAtom* MinRingSizeEqualsQueryAtom(int [,bool=False])
    """
def MinRingSizeGreaterQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where MinRingSize is equal to the target value.
        NOTE: the direction of comparison is reversed relative to the C++ API
    
        C++ signature :
            RDKix::QueryAtom* MinRingSizeGreaterQueryAtom(int [,bool=False])
    """
def MinRingSizeLessQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where MinRingSize is less than the target value.
        NOTE: the direction of comparison is reversed relative to the C++ API
    
        C++ signature :
            RDKix::QueryAtom* MinRingSizeLessQueryAtom(int [,bool=False])
    """
def MissingChiralTagQueryAtom(negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms when MissingChiralTag is True.
    
        C++ signature :
            RDKix::QueryAtom* MissingChiralTagQueryAtom([ bool=False])
    """
def NonHydrogenDegreeEqualsQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where NonHydrogenDegree is equal to the target value.
    
        C++ signature :
            RDKix::QueryAtom* NonHydrogenDegreeEqualsQueryAtom(int [,bool=False])
    """
def NonHydrogenDegreeGreaterQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where NonHydrogenDegree is equal to the target value.
        NOTE: the direction of comparison is reversed relative to the C++ API
    
        C++ signature :
            RDKix::QueryAtom* NonHydrogenDegreeGreaterQueryAtom(int [,bool=False])
    """
def NonHydrogenDegreeLessQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where NonHydrogenDegree is less than the target value.
        NOTE: the direction of comparison is reversed relative to the C++ API
    
        C++ signature :
            RDKix::QueryAtom* NonHydrogenDegreeLessQueryAtom(int [,bool=False])
    """
def NumAliphaticHeteroatomNeighborsEqualsQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where NumAliphaticHeteroatomNeighbors is equal to the target value.
    
        C++ signature :
            RDKix::QueryAtom* NumAliphaticHeteroatomNeighborsEqualsQueryAtom(int [,bool=False])
    """
def NumAliphaticHeteroatomNeighborsGreaterQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where NumAliphaticHeteroatomNeighbors is equal to the target value.
        NOTE: the direction of comparison is reversed relative to the C++ API
    
        C++ signature :
            RDKix::QueryAtom* NumAliphaticHeteroatomNeighborsGreaterQueryAtom(int [,bool=False])
    """
def NumAliphaticHeteroatomNeighborsLessQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where NumAliphaticHeteroatomNeighbors is less than the target value.
        NOTE: the direction of comparison is reversed relative to the C++ API
    
        C++ signature :
            RDKix::QueryAtom* NumAliphaticHeteroatomNeighborsLessQueryAtom(int [,bool=False])
    """
def NumHeteroatomNeighborsEqualsQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where NumHeteroatomNeighbors is equal to the target value.
    
        C++ signature :
            RDKix::QueryAtom* NumHeteroatomNeighborsEqualsQueryAtom(int [,bool=False])
    """
def NumHeteroatomNeighborsGreaterQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where NumHeteroatomNeighbors is equal to the target value.
        NOTE: the direction of comparison is reversed relative to the C++ API
    
        C++ signature :
            RDKix::QueryAtom* NumHeteroatomNeighborsGreaterQueryAtom(int [,bool=False])
    """
def NumHeteroatomNeighborsLessQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where NumHeteroatomNeighbors is less than the target value.
        NOTE: the direction of comparison is reversed relative to the C++ API
    
        C++ signature :
            RDKix::QueryAtom* NumHeteroatomNeighborsLessQueryAtom(int [,bool=False])
    """
def NumRadicalElectronsEqualsQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where NumRadicalElectrons is equal to the target value.
    
        C++ signature :
            RDKix::QueryAtom* NumRadicalElectronsEqualsQueryAtom(int [,bool=False])
    """
def NumRadicalElectronsGreaterQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where NumRadicalElectrons is equal to the target value.
        NOTE: the direction of comparison is reversed relative to the C++ API
    
        C++ signature :
            RDKix::QueryAtom* NumRadicalElectronsGreaterQueryAtom(int [,bool=False])
    """
def NumRadicalElectronsLessQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where NumRadicalElectrons is less than the target value.
        NOTE: the direction of comparison is reversed relative to the C++ API
    
        C++ signature :
            RDKix::QueryAtom* NumRadicalElectronsLessQueryAtom(int [,bool=False])
    """
def QAtomQueryAtom(negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms when QAtom is True.
    
        C++ signature :
            RDKix::QueryAtom* QAtomQueryAtom([ bool=False])
    """
def QHAtomQueryAtom(negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms when QHAtom is True.
    
        C++ signature :
            RDKix::QueryAtom* QHAtomQueryAtom([ bool=False])
    """
def ReplaceAtomWithQueryAtom(mol: Mol, atom: Atom) -> rdkix.Chem.Atom:
    """
        Changes the given atom in the molecule to
        a query atom and returns the atom which can then be modified, for example
        with additional query constraints added.  The new atom is otherwise a copy
        of the old.
        If the atom already has a query, nothing will be changed.
    
        C++ signature :
            RDKix::Atom* ReplaceAtomWithQueryAtom(RDKix::ROMol {lvalue},RDKix::Atom {lvalue})
    """
def RingBondCountEqualsQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where RingBondCount is equal to the target value.
    
        C++ signature :
            RDKix::QueryAtom* RingBondCountEqualsQueryAtom(int [,bool=False])
    """
def RingBondCountGreaterQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where RingBondCount is equal to the target value.
        NOTE: the direction of comparison is reversed relative to the C++ API
    
        C++ signature :
            RDKix::QueryAtom* RingBondCountGreaterQueryAtom(int [,bool=False])
    """
def RingBondCountLessQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where RingBondCount is less than the target value.
        NOTE: the direction of comparison is reversed relative to the C++ API
    
        C++ signature :
            RDKix::QueryAtom* RingBondCountLessQueryAtom(int [,bool=False])
    """
def TotalDegreeEqualsQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where TotalDegree is equal to the target value.
    
        C++ signature :
            RDKix::QueryAtom* TotalDegreeEqualsQueryAtom(int [,bool=False])
    """
def TotalDegreeGreaterQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where TotalDegree is equal to the target value.
        NOTE: the direction of comparison is reversed relative to the C++ API
    
        C++ signature :
            RDKix::QueryAtom* TotalDegreeGreaterQueryAtom(int [,bool=False])
    """
def TotalDegreeLessQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where TotalDegree is less than the target value.
        NOTE: the direction of comparison is reversed relative to the C++ API
    
        C++ signature :
            RDKix::QueryAtom* TotalDegreeLessQueryAtom(int [,bool=False])
    """
def TotalValenceEqualsQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where TotalValence is equal to the target value.
    
        C++ signature :
            RDKix::QueryAtom* TotalValenceEqualsQueryAtom(int [,bool=False])
    """
def TotalValenceGreaterQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where TotalValence is equal to the target value.
        NOTE: the direction of comparison is reversed relative to the C++ API
    
        C++ signature :
            RDKix::QueryAtom* TotalValenceGreaterQueryAtom(int [,bool=False])
    """
def TotalValenceLessQueryAtom(val: int, negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms where TotalValence is less than the target value.
        NOTE: the direction of comparison is reversed relative to the C++ API
    
        C++ signature :
            RDKix::QueryAtom* TotalValenceLessQueryAtom(int [,bool=False])
    """
def XAtomQueryAtom(negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms when XAtom is True.
    
        C++ signature :
            RDKix::QueryAtom* XAtomQueryAtom([ bool=False])
    """
def XHAtomQueryAtom(negate: bool = False) -> rdkix.Chem.QueryAtom:
    """
        Returns a QueryAtom that matches atoms when XHAtom is True.
    
        C++ signature :
            RDKix::QueryAtom* XHAtomQueryAtom([ bool=False])
    """
