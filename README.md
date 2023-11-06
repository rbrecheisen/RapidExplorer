# RapidX - Radiological analysis and processing for imaging data eXplorer

## 1. Introduction

RapidX is an open-source data processing, analysis and visualization (PAV) tool written in PySide6.
Out of the box it is focused on PAV of medical image data in either DICOM or NIFTI format. However,
it's plugin-based design allows developers to extend RapidX with many other PAV modules that can
handle different data types. For example, you could write a PngFileImporterPlugin to load PNG images,
write PngFileEnhancementTaskPlugin that enhanced it somehow, and write a PngImageViewPlugin for 
displaying the original PNG image and its enhanced version side to side.


## 2. For users

### 2.1 Installing RapidX


## 3. For developers

### 3.1 Understanding the RapidX code base
### 3.2 Understanding RapidX plugin management
### 3.3 Writing your own plugins