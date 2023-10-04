from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from models.basemodel import BaseModel
from datasetbuilder import DatasetBuilder
from dicomimageloader import DicomImageLoader
from dicomimageseriesloader import DicomImageSeriesLoader
from datasetstoragemanager import DatasetStorageManager


engine = create_engine('sqlite://', echo=False)
BaseModel.metadata.create_all(engine)

with Session(engine) as session:

    builder = DatasetBuilder(
        path='/Users/ralph/Desktop/downloads/dataset',
        name='myDataset',
    )
    dataset = builder.build()
    
    manager = DatasetStorageManager(session=session)
    name = manager.save(dataset)
    dataset = manager.load(name)

    imageLoader = DicomImageLoader(dataset)
    image = imageLoader.load()

    imageSeriesLoader = DicomImageSeriesLoader(dataset)
    images = imageSeriesLoader.load()
    for image in images:
        pass

    manager.delete(name)