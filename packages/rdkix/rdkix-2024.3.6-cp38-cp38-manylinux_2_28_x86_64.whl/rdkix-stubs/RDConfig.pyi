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
RDCodeDir: str = '/project/build/temp.linux-x86_64-cpython-38/rdkix_install/lib/python3.8/site-packages/rdkix'
RDContribDir: str = '/project/build/temp.linux-x86_64-cpython-38/rdkix_install/share/RDKix/Contrib'
RDDataDatabase: str = '/project/build/temp.linux-x86_64-cpython-38/rdkix_install/share/RDKix/Data/RDData.sqlt'
RDDataDir: str = '/project/build/temp.linux-x86_64-cpython-38/rdkix_install/share/RDKix/Data'
RDDocsDir: str = '/project/build/temp.linux-x86_64-cpython-38/rdkix_install/share/RDKix/Docs'
RDProjDir: str = '/project/build/temp.linux-x86_64-cpython-38/rdkix_install/share/RDKix/Projects'
RDTestDatabase: str = '/project/build/temp.linux-x86_64-cpython-38/rdkix_install/share/RDKix/Data/RDTests.sqlt'
defaultDBPassword: str = 'masterkey'
defaultDBUser: str = 'sysdba'
molViewer: str = 'PYMOL'
pythonExe: str = '/opt/python/cp38-cp38/bin/python3.8'
pythonTestCommand: str = 'python'
rpcTestPort: int = 8423
usePgSQL: bool = False
useSqlLite: bool = True
