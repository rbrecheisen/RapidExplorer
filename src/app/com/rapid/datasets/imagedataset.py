from abc import ABC
from com.rapid.datasets.dataset import Dataset


class ImageDataset(Dataset, ABC):
    
    def __init__(self) -> None:
        super(ImageDataset, self).__init__()