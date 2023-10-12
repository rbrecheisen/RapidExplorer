DATASETS

Package structure:

- data
  - loaders
    - dicomdatasetloader.py
    - dicomfileloader.py
    - dicomfilesetloader.py
    - niftifileloader.py
    - pngfileloader.py
    - textfileloader.py
  - models
    - basemodel.py
    - datasetmodel.py
    - filemodel.py
    - filesetmodel.py
  - objs
    - dataset.py
    - file.py
    - fileset.py
- images
  - icons
- widgets
  - dialogs
    - logdialog.py
  - panels
    - taskpanel.py
  - datasetdockwidget.py
  - dockwidget.py
  - taskdockwidget.py
  - viewdockwidget.py

TASKS

Tasks operate on datasets and produce datasets as output whether it be
a simple scalar value, a table or image dataset. Each task knows what
kind of dataset it supports as input and what kind of dataset it outputs.

class Task:
- input_dataset_type = DicomImageDataset
- output_dataset_type = ArrayDataset2D


VIEWS

Views display datasets.
