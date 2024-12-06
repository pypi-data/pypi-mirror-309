"""
 Configuration for the RDKix Python code

"""
from __future__ import annotations
import os as os
import rdkix as rdkix
import sqlite3 as sqlite3
import sys as sys
__all__ = ['ObsoleteCodeError', 'RDCodeDir', 'RDContribDir', 'RDDataDatabase', 'RDDataDir', 'RDDocsDir', 'RDProjDir', 'RDTestDatabase', 'UnimplementedCodeError', 'defaultDBPassword', 'defaultDBUser', 'molViewer', 'os', 'pythonExe', 'pythonTestCommand', 'rdkix', 'rpcTestPort', 'sqlite3', 'sys', 'usePgSQL', 'useSqlLite']
class ObsoleteCodeError(Exception):
    pass
class UnimplementedCodeError(Exception):
    pass
RDCodeDir: str = 'C:/rdkix/build/temp.win-amd64-cpython-38/Release/rdkix_install/Lib/site-packages\\rdkix'
RDContribDir: str = 'C:/rdkix/build/temp.win-amd64-cpython-38/Release/rdkix_install\\share/RDKix\\Contrib'
RDDataDatabase: str = 'C:/rdkix/build/temp.win-amd64-cpython-38/Release/rdkix_install\\share/RDKix\\Data\\RDData.sqlt'
RDDataDir: str = 'C:/rdkix/build/temp.win-amd64-cpython-38/Release/rdkix_install\\share/RDKix\\Data'
RDDocsDir: str = 'C:/rdkix/build/temp.win-amd64-cpython-38/Release/rdkix_install\\share/RDKix\\Docs'
RDProjDir: str = 'C:/rdkix/build/temp.win-amd64-cpython-38/Release/rdkix_install\\share/RDKix\\Projects'
RDTestDatabase: str = 'C:/rdkix/build/temp.win-amd64-cpython-38/Release/rdkix_install\\share/RDKix\\Data\\RDTests.sqlt'
defaultDBPassword: str = 'masterkey'
defaultDBUser: str = 'sysdba'
molViewer: str = 'PYMOL'
pythonExe: str = 'C:\\Users\\runneradmin\\AppData\\Local\\Temp\\cibw-run-ad2fj8m8\\cp38-win_amd64\\build\\venv\\Scripts\\python.exe'
pythonTestCommand: str = 'python'
rpcTestPort: int = 8423
usePgSQL: bool = False
useSqlLite: bool = True
