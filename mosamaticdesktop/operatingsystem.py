import os
import sys


class OperatingSystem:
    @staticmethod
    def isDarwin() -> bool:
        return sys.platform.startswith('darwin')
    
    @staticmethod
    def isWindows() -> bool:
        return sys.platform.startswith('win')
    
    @staticmethod
    def homeDirectory() -> str:
        if OperatingSystem.isDarwin():
            return os.environ['HOME']
        if OperatingSystem.isWindows():
            return os.environ['USERPROFILE']
        return None