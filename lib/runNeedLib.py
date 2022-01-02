import sys
from pathlib import Path


def getCurRunPath(filePath):
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent

    elif __file__:
        return Path(filePath).parent
