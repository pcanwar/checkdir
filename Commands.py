'''
@author: anwar
'''

# legal commands include 1. Quit 2. Add a file 3. Remove a file 4. Check a file for change
# command should be in following format:
# CMD arguments
import re

class Commands:
    def __init__(self, db):
        self.DB = db
        self.commandersSwitch = {"quit":None, "help":self.printHelp, "addfile":self.addFile, "deletefile":self.deleteFile, "checkfile":self.checkFile,
                                 "adddir":self.addDir, "deletedir":self.deleteDir, "checkdir":self.checkDir,
                                 "tree": self.showTree}

    def processes(self, command):
        '''Process each command line from user input
        '''
        command = command.strip()
        arr = re.split(r'\s+', command, 1)
        commandName = arr[0]
        if not commandName in self.commandersSwitch.keys():
            print("{0} is not a valid command, please try again.".format(commandName))
            return True
        if (commandName == "quit"):
            return False
        else:
            self.doWork(commandName, arr[1:])
            return True

    def doWork(self, commandName, arguments):
        '''Do real work, i.e. add, delete, check
        '''
        f = self.commandersSwitch[commandName]
        if not commandName in ['help', 'tree'] and len(arguments) == 0:
            print("{0} must have one argument.".format(commandName))
            return
        f(arguments)

    def addFile(self, arguments):
        self.DB.addFile(arguments[0])

    def deleteFile(self, arguments):
        self.DB.deleteFile(arguments[0])

    def checkFile(self, arguments):
        self.DB.checkFile(arguments[0])

    def addDir(self, arguments):
        self.DB.addDirectory(arguments[0])

    def deleteDir(self, arguments):
        self.DB.deleteDirectory(arguments[0])

    def checkDir(self, arguments):
        self.DB.checkDirectory(arguments[0])

    def printHelp(self, arguments):
        print("""help - Print this help information
    quit - Quit this system
    tree - List the tree-like structure about database
    addfile FILENAME - Add a file to database
    deletefile FILENMAE - Delete a file from database
    checkfile FILENAME - Check a file for change
    adddir DIRNAME - Add a directory to database (i.e. all files in directory and its subdirectory, not directories themselves)
    deletedir DIRNAME - Delete a directory from database
    checkdir DIRNAME - Check a directory for change
    """)

    def showTree(self, arguments):
        self.DB.showTree()
