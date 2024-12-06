from __future__ import annotations
from rdkix.Chem import ChemicalFeatures
import rdkix.Chem.rdChemicalFeatures
import typing
__all__ = ['ChemicalFeatures', 'FeatMapPoint']
class FeatMapPoint(rdkix.Chem.rdChemicalFeatures.FreeChemicalFeature):
    featDirs = None
    weight: typing.ClassVar[float] = 0.0
    def GetDirMatch(self, other, useBest = True):
        """
        
            >>> from rdkix import Geometry
            >>> sfeat = ChemicalFeatures.FreeChemicalFeature('Aromatic','Foo',Geometry.Point3D(0,0,0))
            >>> fmp = FeatMapPoint()
            >>> fmp.initFromFeat(sfeat)
            >>> fmp.GetDirMatch(sfeat)
            1.0
        
            >>> sfeat.featDirs=[Geometry.Point3D(0,0,1),Geometry.Point3D(0,0,-1)]
            >>> fmp.featDirs=[Geometry.Point3D(0,0,1),Geometry.Point3D(1,0,0)]
            >>> fmp.GetDirMatch(sfeat)
            1.0
            >>> fmp.GetDirMatch(sfeat,useBest=True)
            1.0
            >>> fmp.GetDirMatch(sfeat,useBest=False)
            0.0
        
            >>> sfeat.featDirs=[Geometry.Point3D(0,0,1)]
            >>> fmp.GetDirMatch(sfeat,useBest=False)
            0.5
        
            >>> sfeat.featDirs=[Geometry.Point3D(0,0,1)]
            >>> fmp.featDirs=[Geometry.Point3D(0,0,-1)]
            >>> fmp.GetDirMatch(sfeat)
            -1.0
            >>> fmp.GetDirMatch(sfeat,useBest=False)
            -1.0
        
        
            
        """
    def GetDist2(self, other):
        """
        
            >>> from rdkix import Geometry
            >>> sfeat = ChemicalFeatures.FreeChemicalFeature('Aromatic','Foo',Geometry.Point3D(0,0,0))
            >>> fmp = FeatMapPoint()
            >>> fmp.initFromFeat(sfeat)
            >>> fmp.GetDist2(sfeat)
            0.0
            >>> sfeat.SetPos(Geometry.Point3D(2,0,0))
            >>> fmp.GetDist2(sfeat)
            4.0
            
        """
    def __init__(self, *args, **kwargs):
        ...
    def initFromFeat(self, feat):
        """
        
            >>> from rdkix import Geometry
            >>> sfeat = ChemicalFeatures.FreeChemicalFeature('Aromatic','Foo',Geometry.Point3D(0,0,0))
            >>> fmp = FeatMapPoint()
            >>> fmp.initFromFeat(sfeat)
            >>> fmp.GetFamily()==sfeat.GetFamily()
            True
            >>> fmp.GetType()==sfeat.GetType()
            True
            >>> list(fmp.GetPos())
            [0.0, 0.0, 0.0]
            >>> fmp.featDirs == []
            True
        
            >>> sfeat.featDirs = [Geometry.Point3D(1.0,0,0)]
            >>> fmp.initFromFeat(sfeat)
            >>> len(fmp.featDirs)
            1
        
            
        """
def _runDoctests(verbose = None):
    ...
