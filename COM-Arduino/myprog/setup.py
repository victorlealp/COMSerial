import cx_Freeze
import sys
import os
import matplotlib

os.environ['TCL_LIBRARY'] = "C:\\Program Files (x86)\\LOCAL_TO_PYTHON\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Program Files (x86)\\LOCAL_TO_PYTHON\\tcl\\tk8.6"




base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

executables = [cx_Freeze.Executable("main.py", base=None)]





cx_Freeze.setup(
    name = "main",
    version = "1.0",
    description = "Mão Robótica",
    executables = executables
 )
