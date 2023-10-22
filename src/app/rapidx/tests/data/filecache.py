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
        dicomFile = DicomFile(fileModel)        # Generate a UUID here or in FileModel that we can use to lookup?
        cache = FileCache()
        cache.add(file=dicomFile, model=multiFileSetModel)

    When the application starts up and database contains a registered MultiFileSetModel with corresponding FileSetModel
    and FileModel, this data should be loaded into the tree widget. At that point there is no physical data like a 
    DICOM file in the file cache (it was emptied when the application closed). 

    When you manually import a DICOM file, you're using the DicomFileImporter or DicomFileSetImporter. It will create
    a new DicomFile that can be stored in the file cache. However, when you only have the SQL database and the file
    cache is empty, how do you reload the physical DICOM file? Use a loader instead of an importer? What do we provide
    to the loader? DicomFileLoader(fileModel=fileModel)? When you click a file in the tree widget, this should trigger
    a load action on the file (which is a DICOM file). How do you know to use a DicomFileLoader and not something else?
    Like a PngFileLoader? This should be stored in SQL as well I would say, perhaps with a flag or enum field?
    """
    def __init__(self) -> None:
        self._data = {}