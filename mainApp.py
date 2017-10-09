'''
@author: anwar
'''
import os
import sys
from Database import Database
from Commands import Commands

def looping(commander):
    '''Enter user interactive mode, wait for user's input
    '''
    while True:
        commands = input('> ')
        if not commander.processes(commands):
            break
    print("Goodbye...")

def loadOrCreateDb(dbName):
    '''Load database from file or create a new one
    '''
    db = None
    if os.path.exists(dbName):
        db = Database.load(dbName)
    else:
        print("Creat a new database '{0}'".format(dbName))
        db = Database(dbName)
    return db

def saveDb(db, dbName = "Anwar.DB"):
    '''Save current database to local file
    '''
    db.save(dbName)

if __name__ == "__main__":
    print("""File management system V1.0 by Anwar aalruwai@stevens.edu & pcanw@live.com
User can provide database name or leave it empty for default name 'Default.db'
If database doesn't exist, new one will be created.

Loop instruction: press ENTER key after you input each line of command.
Use 'quit' to quit the program.
Use 'help' to get more information.
COMMAND arguments - input help for more information
""")
    dbfilePath = "Default.db"
#    print(sys.argv)
    if len(sys.argv) >= 2:
        dbfilePath = sys.argv[1]
    db = loadOrCreateDb(dbfilePath)
    commander = Commands(db)
    looping(commander)
    saveDb(db, dbfilePath)
