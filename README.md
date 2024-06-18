# Mosamatic Desktop
Mosamatic Desktop is a Python tool for (1) automatically annotating muscle and fat tissue in CT images taken at the 3rd lumbar vertebral level and (2) calculating surface area 
and mean radiation attenuation of the muscle and fat compartments visible at L3 level. Given a full CT scan Mosamatic Desktop is also able to automatically select the L3 slice. 
It uses Total Segmentator () for this purpose by first extracting the L3 vertebra, finding its center position in the Z-direction and looking up the DICOM image closest to that
position (by inspecting the ImagePositionPatient attribute).

# Install
Installing Mosamatic Desktop is as simple as running either InstallMosamatic.bat (Windows) or InstallMosamatic.sh (Linux/MacOS), depending on your platform.

These installation scripts will setup a virtual Python environment for installing and running Mosamatic Desktop. They will also install additional Python pacakages that allow
you to use the GPU on your system (if present). Note that the automatic slice selection task will be very slow if there is no GPU support on your system. You can check whether
you have GPU support by going to "About" > "Application Info" in the main menu of Mosamatic Desktop. If it says "GPU Enabled: True" you're good to go.

# Run
Running Mosamatic Desktop can be done by executing the Mosamatic.bat or Mosamatic.sh scripts. Both will first enable the virtual Python environment Mosamatic Desktop was 
installed in, and then run the tool itself.
