from typing import List
from sqlalchemy.orm import mapped_column, relationship, Session
from sqlalchemy import create_engine

from models.basemodel import BaseModel
from datasetfilepathindexer import DatasetFilePathIndexer
from datasetstoragemanager import DatasetStorageManager


engine = create_engine('sqlite://', echo=False)
BaseModel.metadata.create_all(engine)

with Session(engine) as session:
    indexer = DatasetFilePathIndexer(path='/Users/ralph/Desktop/downloads/dataset')
    dataset = indexer.load()

    manager = DatasetStorageManager()
    manager.save(dataset)