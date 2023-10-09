import os

from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from models.basemodel import BaseModel
from datasetbuilder import DatasetBuilder
from dicomimageloader import DicomImageLoader
from dicomimageseriesloader import DicomImageSeriesLoader
from multidicomimageseriesloader import MultiDicomImageSeriesLoader
from datasetstoragemanager import DatasetStorageManager


engine = create_engine('sqlite://', echo=False)
BaseModel.metadata.create_all(engine)

DATASET_DIR = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset')
DATASET_NAME = 'myDataset'


with Session(engine) as session:
    builder = DatasetBuilder(path=DATASET_DIR, name=DATASET_NAME)   # Build dataset from file paths
    dataset = builder.build()
    manager = DatasetStorageManager(session=session)                # Save to database
    name = manager.save(dataset)
    dataset = manager.load(name)                                    # Load back into memory
    imageLoader = DicomImageLoader(dataset)                         # Load the first image in dataset (as PyDicom object)
    image = imageLoader.load()
    imageSeriesLoader = DicomImageSeriesLoader(dataset)             # Load first scan in dataset (as file set of PyDicom objects)
    images = imageSeriesLoader.load()
    for image in images:
        pass
    multiImageSeriesLoader = MultiDicomImageSeriesLoader(dataset)
    images = multiImageSeriesLoader.load()
    for fileSetName in images.keys():
        print(fileSetName)
    manager.delete(name)