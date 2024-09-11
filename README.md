# Mosamatic Desktop
Mosamatic Desktop is a Python tool for (1) automatically annotating muscle and fat tissue in CT images taken at the 3rd lumbar vertebral level and (2) calculating surface area 
and mean radiation attenuation of the muscle and fat compartments visible at L3 level. Given a full CT scan Mosamatic Desktop is also able to automatically select the L3 slice. 
It uses Total Segmentator () for this purpose by first extracting the L3 vertebra, finding its center position in the Z-direction and looking up the DICOM image closest to that
position (by inspecting the ImagePositionPatient attribute).

# Installation
Installing Mosamatic Desktop is as simple as running either InstallMosamatic.bat (Windows) or InstallMosamatic.sh (Linux/MacOS), depending on your platform.

These installation scripts will setup a virtual Python environment for installing and running Mosamatic Desktop. They will also install additional Python pacakages that allow
you to use the GPU on your system (if present). Note that the automatic slice selection task will be very slow if there is no GPU support on your system. You can check whether
you have GPU support by going to "About" > "Application Info" in the main menu of Mosamatic Desktop. If it says "GPU Enabled: True" you're good to go.

## Install Python
- Go to https://www.python.org and install the most recent Python environment (3.12 as of writing this manual). After installation, test your installation by opening a terminal window by clicking the "Start" button in your Windows task bar and searching for "Terminal". 
- In the terminal type "python --version". You should now see some information about the recently installed Python environment, particularly the installed version.

## Install Mosamatic using the InstallMosamatic.bat script
- Find the installation script "InstallMosamatic.bat" in the root directory of the source code project here on GitHub.
- Download the installation script somewhere on your system, e.g., on your Desktop.
- Double-click the installation script. This will start the installation process for Mosamatic. After the script finishes (hopefully successfully), you should see another icon on your desktop "MosamaticDesktop". This is a shortcut pointing to the executable (.exe) of the application.
- After successful installation, you can double-click the "MosamaticDesktop" icon on your desktop to start the application. After a few seconds you should see the main tool window as illustrated in the figure below.

![Mosamatic Desktop main window](MosamaticDesktop/asserts/MosamaticMainWindow.png)

# Run
Running Mosamatic Desktop can be done by executing the Mosamatic.bat or Mosamatic.sh scripts. Both will first enable the virtual Python environment Mosamatic Desktop was 
installed in, and then run the tool itself.
