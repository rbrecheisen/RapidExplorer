import sys


class OperatingSystem:
    @staticmethod
    def isDarwin() -> bool:
        return sys.platform.startswith('darwin')
    
    @staticmethod
    def isWindows() -> bool:
        return sys.platform.startswith('win')