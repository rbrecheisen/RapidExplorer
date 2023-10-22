# from rapidx.app.datasetstoragemanager import DatasetStorageManager
# from rapidx.app.dataset import Dataset


# def test(session):
#     manager = DatasetStorageManager(session=session)  
#     oldName = 'myDataset'
#     newName = 'myNewDataset'
#     # Create new dataset and save it
#     dataset = Dataset(name=oldName, path='/path/to/dataset')
#     dataset = manager.save(dataset)
#     datasetId = dataset.id()
#     # Load dataset and rename it
#     dataset = manager.load(datasetId)
#     dataset.setName(newName)
#     manager.save(dataset)
#     # Load dataset again and check new name
#     dataset = manager.load(datasetId)
#     assert dataset.name() == newName
