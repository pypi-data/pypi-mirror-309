import sys
import os
import io
import time
import abc
import pandas as pd
import numpy as np

try:
        from .file import *
except ImportError:
        from file import *

'''
inside model
use class txt:
        def __all__(self):
                pass
        def none(self):
                pass

all right,let's start
'''

__all__ = ['txt']

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


class txt(file):
        type = AP
        lineEND = NEND
        open_type = N

        def __init__(self,path,way = type,lineEND = lineEND,open_type = open_type):
                self.type = type
                self.lineEND = lineEND
                self.open_type = open_type
                self.path = path
                self.way = way

        def write(self,text,end = lineEND):
                text = str(text)
                with io.open(self.path,self.way) as f:
                        f.write(text+end)
                        f.close()

        def read_first_line(self):
                with io.open(self.path,self.way) as f:
                        return f.readline()

        def read_all_lines(self):
                with io.open(self.path,self.way) as f:
                        return f.readlines()

        def read_spesific_line(self,linenumber = 1,way = 'normal'):
                with io.open(self.path,self.way) as f:
                        read_line_number = int(linenumber)-1
                        if way == 'normal':
                                k = f.readlines()
                                return k[read_line_number]
                        elif way == 'end':
                                k = f.readlines()
                                str = k[read_line_number]
                                if len(str)>=2 and str[-2:] == '\n':
                                        return str[:-2]
                        else:
                                raise WayError(way)

        def read_all_txt(self):
                with io.open(self.path,self.way) as f:
                        return f.read()

        def change_txt_line(self,change,linenumber):
                linenumber = int(linenumber)-1

                
                with io.open(self.path, self.way) as file:
                        lines = file.readlines()

                
                for i, line in enumerate(lines):
                        if i == linenumber:  
                                lines[i] = str(linenumber)+self.lineEND

                
                with io.open(self.path, 'w') as file:
                        file.writelines(lines)
