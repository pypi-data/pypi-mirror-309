"""
 contains code for standardization of data matrices for clustering


"""
from __future__ import annotations
from rdkix.ML.Data import Stats
__all__ = ['Stats', 'StdDev', 'methods']
def StdDev(mat):
    """
     the standard deviation classifier
    
       This uses _ML.Data.Stats.StandardizeMatrix()_ to do the work
    
      
    """
methods: list  # value = [('None', <function <lambda> at 0x0000014377906CA0>, 'No Standardization'), ('Standard Deviation', StdDev, 'Use the standard deviation')]
