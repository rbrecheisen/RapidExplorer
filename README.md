# RapidX - Radiological analysis and processing for imaging data eXplorer

## 1. Introduction

RapidExplorer is an open-source data processing, analysis and visualization (PAV) tool written in PySide6.
Out of the box it is focused on PAV of medical image data in either DICOM or NIFTI format. However,
it's plugin-based design allows developers to extend RapidExplorer with many other PAV modules that can
handle different data types. For example, you could write a PngFileImporterPlugin to load PNG images,
write PngFileEnhancementTaskPlugin that enhanced it somehow, and write a PngImageViewPlugin for 
displaying the original PNG image and its enhanced version side to side.


## 2. For users

### 2.1 Installing RapidExplorer


## 3. For developers

### 3.1 General remarks
RapidExplorer is written with a certain style similar to Java. I'm not sure why I did this but somehow it
feels uncomfortable to have PySide's camel case mixed with Python's snake case. I decided to write
everything in camel case. Also, I stuck to the one class per file approach as well and I have to 
say it makes my code much more understandable. Typical Python module files often contain so much
code that it can be hard to navigate a code base without additional tools. It is much more verbose
of course, like Java is, but that verbosity somehow makes the code based feel more stable and
scalable. I'm going to stick to this way of programming for the moment. Of course, when you write
your own plugins, please feel free to return to snake case and writing dozens of clases in a single
file. If you enjoy keeping everything in your head while working on thousands of lines of code, be 
my guest.

As a second remark, I decided to adapt an "almost" TDD approach when building RapidExplorer. It's not
very strict though. I didn't start with a failing test as the first line of code I wrote. I first
created a sort of minimal skeleton with a PySide6 main window that showed nothing. But after that,
I did try to grow my code using tests like suggested in [REF]. Especially the more complicated
classes that have no UI associated with them are pretty well tested. I will explain where the
tests are in this project and how to run them.

### 3.2 Understanding the RapidExplorer source and test code bases
### 3.3 Understanding RapidX plugin management
### 3.4 Writing your own plugins