import sys
import os
import io
import abc
import pathlib
import __future__

try:
        #import pandas as pd
        import numpy as np
except ImportError or ModuleNotFoundError:
        #error = '00010'
        sys.exit()

'''
inside model
use class txt:
        def __all__(self):
                pass
        def none(self):
                pass

all right,let's start
'''

R = 'r'
RP = 'r+'
A = 'a'
AP = 'a+'
W = 'w'
WP = 'w+'
RB = 'rb'
RBP = 'rb+'
WB = 'wb'
WBP = 'wb+'

N = 'normal'
UN = 'disabled'
UR = 'unread'
UW = 'unwrite'

GBK = 'GBK'
UTF = 'UTF-8'

END = 'end'
NEND = '\n'
EEND = ' '
REND = '\r'
NREND = '\r\n'

class WayError(Exception):
        '''
        This will run if you use wrong 'way' keys.
        '''
        def __init__(self,error_code):
                super().__init__(f"{error_code} is not excepted.")
                self.error_code = error_code

class FileError(Exception):
        '''
        the father class of all the file errors.
        '''
        def __init__(self,filename,event):
                super().__init__(f"{filename} was {event}.")
                self.filename = filename
                self.event = event

class PathError(FileError,OSError):
        '''
        it would return if path has some error.
        '''
        def __init__(self,path,event):
                super().__init__(f"{path} was {event}.")
                self.path = path
                self.event = event

class PathNotFoundError(PathError):
        '''
        it would return if path has some error.
        '''
        def __init__(self,path):
                super().__init__(f"{path} not found.")
                self.path = path
                self.event = "not_found"

class PathIsFoundError(PathError):
        '''
        it would return if path has some error.
        '''
        def __init__(self,path):
                super().__init__(f"{filename} is found.")
                self.path = path
                self.event = "is_found"

class file:
        def __init__(self,path,way = R):
                self.path = path
                self.way = way
                io.open(self.path,self.way)

        def change_extension(self,new_extension):
                filename = os.path.split(self.path)[1]
                base_name = os.path.splitext(filename)[0]  
                new_filename = f"{base_name}.{new_extension}"  
                return os.rename(filename, new_filename)

        def movefile(self,newpath):
                if (os.path.exists(self.path) and os.path.exists(newpath)):
                        for a,b in os.path.split(self.path):
                                os.path.join(newpath,b)
                        del a,b                        
                else:
                        raise FileNotFoundError(f"Can not fond",oldpath,newpath)
                

        def findfile(self,file):
                filelist=[]
                if os.path.exists(self.path):
                        for f in os.listdir(self.path):
                                temp_dir = os.path.join(path, f)
                                if os.path.isfile(temp_dir) and temp_dir.endswith(file):
                                        for a,b in os.path.split(temp_dir):
                                                filelist.append(b)
                        '''
                    elif os.path.isdir(temp_dir):
                        get_file_list(temp_dir, file, filelist)
                        '''
                        return filelist
                        del a,b
                else:
                        raise FileNotFoundError(f"Can not fond",self.path)
                        pass

        def findallfile(self,file):
                filelist=[]
                if os.path.exists(self.path):
                        for f in os.listdir(self.path):
                                temp_dir = os.path.join(self.path, f)
                                if os.path.isfile(temp_dir) and temp_dir.endswith(file):
                                        for a,b in os.path.split(temp_dir):
                                                filelist.append(b)
                                        del a,b
                                elif os.path.isdir(temp_dir):
                                        get_file_list(temp_dir, file, filelist)
                                        return filelist
                                        
                                else:
                                        raise FileNotFoundError(f"Can not fond",path)
                
        def change_extension(self,new='.py'):
                file_path=Path(self.path)
                new_file_path = file_path.with_suffix(new)
         
                # 重命名文件
                return file_path.rename(new_file_path)
 




'''
class TxtPathError(FileNotFoundError):

        pass
'''
