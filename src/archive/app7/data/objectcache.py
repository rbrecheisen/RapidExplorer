from typing import Any

from singleton import singleton
from data.file import File


@singleton
class ObjectCache:
    def __init__(self) -> None:
        self._objects = {}

    def objects(self):
        return self._objects

    def nrObjects(self) -> None:
        return len(self.objects().keys())
    
    def print(self, id: str) -> None:
        if self.has(id):
            print(f'{id}: {self.get(id)}')
        else:
            print('{}')
    
    def printAll(self) -> None:
        if self.nrObjects() == 0:
            print('{}')
        else:
            for id in self.objects().keys():
                self.print(id)

    def has(self, id: str) -> bool:
        return id in self.objects().keys()
    
    def add(self, id: str, object: Any) -> None:
        if not self.has(id):
            self.objects()[id] = object

    def remove(self, id: str) -> None:
        if id in self.objects().keys():
            del self._objects[id]

    def removeAll(self) -> None:
        self.objects().clear()
        
    def get(self, id: str) -> File:
        if self.has(id):
            return self.objects()[id]
        return None

    def clear(self) -> None:
        self.objects().clear()
