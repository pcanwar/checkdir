'''
@author: anwar
'''
from datetime import datetime
import os
import CheckSum        

class Entry:
    def __init__(self, name, childrenin, parent = None):
        self.name = name
        self.parent = parent    #Parent is also an Entry, except None for ROOT
        self.children = childrenin  #all children should also be Entry class
        
    def addDir(self, dirName):
        self.children[dirName] = Entry(dirName, dict(), self)
        
    def addFile(self, fileName, fullFileName):
        self.children[fileName] = Entry(fileName, CheckSum.compute(fullFileName), self)
        
    def isDirectory(self):
        return type(self.children) is dict
    
    def __str__(self):
        return "{0}: {1} children".format(self.name,len(self.children))