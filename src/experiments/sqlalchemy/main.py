from typing import List
from sqlalchemy.orm import mapped_column, relationship, Session
from sqlalchemy import create_engine

from models.basemodel import BaseModel
from datasetfilepathbuilder import DatasetFilePathBuilder
from datasetstoragemanager import DatasetStorageManager


engine = create_engine('sqlite://', echo=False)
BaseModel.metadata.create_all(engine)

with Session(engine) as session:
    builder = DatasetFilePathBuilder(path='/Users/ralph/Desktop/downloads/dataset')
    dataset = builder.execute()

    manager = DatasetStorageManager(session=session)
    name = manager.save(dataset)

    dataset = manager.load(name)
    print(dataset)

    manager.delete(name)