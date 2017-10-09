'''
@author: anwar
'''
from datetime import datetime
import CheckSum
from Entry import Entry
import pickle
import os

class Database:
    def __init__(self, name):
        self.name = name
        self.lastModified = self.creationTime = datetime.now()
        self.ROOT = Entry("__ROOT__", dict())

    def save (self, fileName):
        '''Save current database to local file
        '''
        print("Save Database to {0}".format(fileName))
        self.lastModified = datetime.now()
        pickle.dump(self, file=open(fileName, 'wb'))

    @staticmethod
    def load (fileName):
        '''Load database from file
        '''
        db = pickle.load(open (fileName, 'rb'))
        print("Load Database from '{0}', created on {1}, last modified on {2}".format(fileName, db.creationTime, db.lastModified))
#        print(db.ROOT)
        return db

    def addFile (self, filename):
        '''Add a file to current database
        '''
        if not os.path.exists(filename):
            print("Error: The file you want to add '{0}' doesn't exist in system. Please try again.".format(filename))
            return
        if not os.path.isfile(filename):
            print("Error: '{0}' is not a valid file path".format(filename))
            return
        (filename, fullFileName, parts) = self.getFullandLoalName(filename)

        current = self.ROOT
        for part in parts[:-1]:
            if not part in current.children: #part is the string representation of file path, e.g. /tmp/dir/test.txt, part can be tmp or dir
                current.addDir(part)
            current = current.children[part]
        current.addFile(filename, fullFileName)
        print("Add file '{0}'. [checksum:{1}]".format(fullFileName, current.children[filename].children))

    def deleteFile (self, filename):
        '''Delete a file from current database
        '''
        def showError():
            print("Error: The file you want to delete '{0}' doesn't exist in system. Please try again.".format(fullFileName))
        (filename, fullFileName, parts) = self.getFullandLoalName(filename)
        current = self.ROOT
        for part in parts[:-1]:
            if part in current.children:
                current = current.children[part]
            else:
                showError()
                return
        if not filename in current.children:    #if directories found are not correct or file not found in the last layer
            showError()
            return
        del current.children[filename]
        print("The file '{0}' was deleted.".format(fullFileName))
        while current.parent != None and len(current.children) == 0:
            print("deleting {0}".format(current.name))
            del current.parent.children[current.name]
            current = current.parent


    def checkFile (self, filename):
        '''Check file integrity
        '''
        def showError():
            print("Error: The file you want to check '{0}' doesn't exist in system. Please try again.".format(fullFileName))
        (filename, fullFileName, parts) = self.getFullandLoalName(filename)
        current = self.ROOT
        for part in parts[:-1]:
            if part in current.children:
                current = current.children[part]
            else:
                showError()
                return
        if not filename in current.children:    #if directories found are not correct or file not found in the last layer
            showError()
            return
        newchecksum = CheckSum.compute(fullFileName)
        if current.children[filename].children == newchecksum:
            print("The file integrity is good.'{0}'".format(fullFileName))
        else:
            print("Warn: The file '{0}' has been changed since last time {1}".format(fullFileName, self.lastModified))

    def addDirectory(self, dirName):
        '''Add a directory to current database'''
        if not os.path.exists(dirName):
            print("Error: The directory you want to add '{0}' doesn't exist in system. Please try again.".format(dirName))
            return
        if not os.path.isdir(dirName):
            print("Error: '{0}' is not a valid directory".format(dirName))
            return
        dirName = os.path.abspath(dirName)
        for path in os.listdir(dirName):
            subPath = os.path.join(dirName, path)
            if os.path.isfile(subPath):
                self.addFile(subPath)
                continue
            if os.path.isdir(subPath):
                self.addDirectory(subPath)
                continue
    def deleteDirectory(self, dirName):
        self.iterateDirectory(dirName, self.deleteFile, 'delete')

    def checkDirectory(self, dirName):
        self.iterateDirectory(dirName, self.checkFile, "check")

    def iterateDirectory(self, dirName, f, actionName):
        if not os.path.exists(dirName):
            print("Error: The directory you want to {1} '{0}' doesn't exist in system. Please try again.".format(dirName, actionName))
            return
        if not os.path.isdir(dirName):
            print("Error: '{0}' is not a valid directory".format(dirName))
            return
        dirName = os.path.abspath(dirName)
        for path in os.listdir(dirName):
            subPath = os.path.join(dirName, path)
            if os.path.isfile(subPath):
                f(subPath)
                continue
            if os.path.isdir(subPath):
                self.iterateDirectory(subPath, f, actionName)
                continue

    def splitPath(self, path):
        '''Split a file or directory to parts, each part is a directory except the last one may be a file
        Parts are from root to leaf
        The last path separator will be deleted
        '''
        folders = []
        if len(path) > 1 and path[-1] == os.path.sep:
            path = path[:-1]
        while True:
            path, folder = os.path.split(path)
            if folder != "":
                folders.append(folder)
            else:
                if path != "":
                    folders.append(path)
                break
        folders.reverse()
        return folders

    def getFullandLoalName(self, path):
        path = os.path.abspath(path)
        parts = self.splitPath(path)
        return (parts[-1], path, parts)

    def showTree(self):
        if len(self.ROOT.children) == 0:
            print("Empty database")
            return
        self.showTreeLoop(self.ROOT, 0)

    def showTreeLoop(self, current, level):
        for (_, ele) in current.children.items():
            if ele.isDirectory():
                print("{0}{1}".format((level*2+1) * "_", ele.name))
                self.showTreeLoop(ele, level + 1)
            else:
                print("{0}|{1} [checksum:{2}]".format(level*2*"_", ele.name, ele.children))
