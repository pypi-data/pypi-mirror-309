"""""" # start delvewheel patch
def _delvewheel_patch_1_9_0():
    import ctypes
    import os
    import platform
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'rdkix.libs'))
    is_conda_cpython = platform.python_implementation() == 'CPython' and (hasattr(ctypes.pythonapi, 'Anaconda_GetVersion') or 'packaged by conda-forge' in sys.version)
    if sys.version_info[:2] >= (3, 8) and not is_conda_cpython or sys.version_info[:2] >= (3, 10):
        if os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        load_order_filepath = os.path.join(libs_dir, '.load-order-rdkix-2024.3.6')
        if os.path.isfile(load_order_filepath):
            import ctypes.wintypes
            with open(os.path.join(libs_dir, '.load-order-rdkix-2024.3.6')) as file:
                load_order = file.read().split()
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            kernel32.LoadLibraryExW.restype = ctypes.wintypes.HMODULE
            kernel32.LoadLibraryExW.argtypes = ctypes.wintypes.LPCWSTR, ctypes.wintypes.HANDLE, ctypes.wintypes.DWORD
            for lib in load_order:
                lib_path = os.path.join(os.path.join(libs_dir, lib))
                if os.path.isfile(lib_path) and not kernel32.LoadLibraryExW(lib_path, None, 8):
                    raise OSError('Error loading {}; {}'.format(lib, ctypes.FormatError(ctypes.get_last_error())))


_delvewheel_patch_1_9_0()
del _delvewheel_patch_1_9_0
# end delvewheel patch

import logging
import sys

# Need to import rdBase to properly wrap exceptions
# otherwise they will leak memory
from . import rdBase

try:
  from .rdBase import rdkixVersion as __version__
except ImportError:
  __version__ = 'Unknown'
  raise

logger = logging.getLogger("rdkix")

# if we are running in a jupyter notebook, enable the extensions
try:
  kernel_name = get_ipython().__class__.__name__
  module_name = get_ipython().__class__.__module__

  if kernel_name == 'ZMQInteractiveShell' or module_name == 'google.colab._shell':
    logger.info("Enabling RDKix %s jupyter extensions" % __version__)
    from rdkix.Chem.Draw import IPythonConsole
    rdBase.LogToPythonStderr()
except Exception:
  pass

# Do logging setup at the end, so users can suppress the
# "enabling jupyter" message at the root logger.
log_handler = logging.StreamHandler(sys.stderr)
logger.addHandler(log_handler)
logger.setLevel(logging.WARN)
logger.propagate = False

# Uncomment this to use Python logging by default:
# rdBase.LogToPythonLogger()
