from rapidx.tests.singleton import singleton


@singleton
class FileCache:
    """ Do I store complete datasets in here? Like MultiFileSet objects? Or only individual
    files like DICOM files?

    Let's look at a usage scenario. I want to import a CT scan. It consists of multiple 
    DICOM files. How do I get it to be (1) registered in the database and (2) physically
    loaded in the application? 

    DicomFileImporter could be a class that handles single files. Example usage:

    importer = DicomFileImporter(path='/path/to/dicomFile')     # Instantiate importer
    QThreadPool.globalInstance().start(importer)                # Run it in the background so we can track progress
    ...
    def run(self):
        multiFileSetModel = MultiFileSetModelFactory.create()
        fileSetModel = FileSetModelFactory.create(..., multiFileSetModel=multiFileSetModel)
        fileModel = FileModelFactory.create(..., fileSetModel=fileSetModel)
        dicomFile = DicomFile(fileModel)
        cache = FileCache()
        cache.add(file=dicomFile, model=multiFileSetModel)
        

    """
    def __init__(self) -> None:
        self._data = {}