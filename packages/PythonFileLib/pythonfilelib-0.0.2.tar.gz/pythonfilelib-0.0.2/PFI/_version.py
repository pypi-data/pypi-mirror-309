import __future__
import io
import sys

try:
        from .file import txt
except ImportError:
        from file import txt

try:
        from .version import version
except ImportError:
        from version import version

__all__ = ['get_version',
           'from_txt_get_version']

try:
        from .exception import *
except ImportError:
        from exception import *

def get_versition():
        a = txt.txt("version.py",txt.R)
        file_txt = a.readline()
        
        if file_txt == 'N' or "N":
                del a,file_txt
                return False
        
        elif file_txt == ''' version = '0.0.2' ''' or """version = '0.0.2'""":
                del a,file_txt
                return True
        
        else:
                raise VersionError()
                sys.exit()


def from_txt_get_version():
        try:
                from .file import file
        except ImportError:
                from file import file
        file = file.file('version.py')
        file.change_extension('.txt')
        try:
                import .version
        except ImportError:
                import version
        version = version.version
        if version == '0.0.2':
                file = file.file('version.txt')
                file.change_extension('.py')
                with io.open("version.py",txt.W) as f:
                        f.write("N")
                return None
        else:
                file = file.file('version.txt')
                file.change_extension('.py')
                raise VersionTxtError()
                sys.exit()
