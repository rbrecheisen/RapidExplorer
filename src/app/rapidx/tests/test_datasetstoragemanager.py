from rapidx.app.datasetstoragemanager import DatasetStorageManager
from rapidx.app.dataset import Dataset


def test():
    manager = DatasetStorageManager()
    # Create new dataset and save it
    dataset = Dataset(name='myDataset', path='/path/to/dataset')
    name = manager.save(dataset)
    # Load dataset and rename it
    dataset = manager.load(name)
    dataset.setName('myNewDataset')
    name = manager.save(dataset)
    # Load dataset again and check new name
    dataset = manager.load(name)
    assert dataset.name() == 'myNewDataset'
