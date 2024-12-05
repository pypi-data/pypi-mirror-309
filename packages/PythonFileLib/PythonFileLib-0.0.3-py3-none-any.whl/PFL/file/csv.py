import csv
import pandas as pd
import numpy as np

try:
        from .file import *
except ImportError:
        from file import *

try:
        from .txt import txt
except ImportError:
        from txt import txt

__all__ = ['CSVError','csv']

class CSVError(Exception):
        def __init__(self,path,event):
                self.path = path
                self.event = event

class RowError(CSVError,TypeError):
        def __init__(self):
                super().__init__(f"type row must be int")
                self.event = "row"

class csv(txt):
        
        def __init__(self,path,way = AP):
                self.path = path
                self.way = way
                return txt(path,way)
        
        def read(self,out_type = 'list',newline = NEND,encoding = GBK,quotechar = '"'):
                if out_type == 'list':
                        with open(self.path,self.way, newline=newline, encoding=encoding) as csvfile:
                                return csv.reader(csvfile, quotechar=quotechar)
                elif out_type == 'dict':
                        with open('output.csv', mode='r', newline='') as file:
                                return csv.DictReader(file)
                else:
                        raise WayError(out_type)

        def readrow(self,rownumber,newline = NEND,encoding = GBK,quotechar = '"'):
                
                if type(rownumber) is int:       
                        with open(self.path,self.way, newline=newline, encoding=encoding) as csvfile:
                                reader = csv.reader(csvfile, quotechar=quotechar)
                                return reader[rownumber-1]
                else:
                        raise RowError()


DICT = 'dict'
LIST = 'list'
SERI = 'series'
SPLI = 'split'
RECO = 'record'

class pandas_csv(txt):
        def __init__(self,path,way):
                pass
