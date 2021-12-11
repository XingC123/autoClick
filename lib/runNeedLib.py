import os
import sys


def getCurRunPath(filePath):
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)

    elif __file__:
        return os.path.dirname(filePath)
        # return str(filePath)
