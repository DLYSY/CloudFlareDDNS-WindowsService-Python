from inspect import getfile,currentframe
from os import path
from sys import argv
    
    
    
def get_path():
    global logger
    if len(argv) == 1 and argv[0].endswith('.exe') and not argv[0].endswith('pythonservice.exe'):
        dirpath=path.dirname(path.realpath(argv[0]))
    else:
        dirpath = path.abspath(path.dirname(getfile(currentframe())))
    return dirpath



if __name__=="__main__":
    print(get_path())