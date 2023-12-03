import os
import importlib

from typing import Dict, Any


class ModuleLoader:
    @staticmethod
    def loadModuleClasses(moduleDirectoryPath: str, moduleBaseClass: Any) -> Dict[str, Any]:
        classes = {}
        moduleDirectoryName = os.path.split(moduleDirectoryPath)[1]
        for root, dirs, files in os.walk(moduleDirectoryPath):
            for fileName in files:
                filePath = os.path.join(root, fileName)
                if fileName == '__init__.py':
                    taskModule = filePath.split(os.path.sep)[-2]
                    if taskModule != moduleDirectoryName:
                        spec = importlib.util.spec_from_file_location(taskModule, filePath)
                        if spec and spec.loader:
                            module = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(module)
                            for attributeName in dir(module):
                                attribute = getattr(module, attributeName)
                                if isinstance(attribute, type) and issubclass(attribute, moduleBaseClass) and attribute is not moduleBaseClass:
                                    classes[attribute.NAME] = attribute
                                    print(f'Loaded module {attribute.NAME}')
        return classes