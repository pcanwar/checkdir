'''
@author: anwar
'''

MOD_ADLER = 65521


def compute(fileName):
    '''Checking the integrity of a file means computing the checksum of the current
file and comparing it against the value stored in the database and reporting the
result. An error message should be generated if the file is not in the database.
The current state of the database should be saved when the Quit option is chosen.
    '''
    a = 1
    b = 0
    f = open(fileName, "rb")
    try:
        byte = f.read(1)
        while len(byte) != 0:
            a  = (a  + ord(byte) )  % MOD_ADLER
            b  = (b  + a )  % MOD_ADLER
            # Do stuff with byte.
            byte = f.read(1)
    finally:
        f.close()
    return (b << 16) | a
