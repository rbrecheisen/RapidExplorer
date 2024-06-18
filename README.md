# Mosamatic Desktop
Mosamatic Desktop is a Python tool for (1) automatically annotating muscle and fat tissue in CT images taken at the 3rd lumbar vertebral level and (2) calculating surface area 
and mean radiation attenuation of the muscle and fat compartments visible at L3 level. Given a full CT scan Mosamatic Desktop is also able to automatically select the L3 slice. 
It uses Total Segmentator () for this purpose by first extracting the L3 vertebra, finding its center position in the Z-direction and looking up the DICOM image closest to that
position (by inspecting the ImagePositionPatient attribute).

# Install
Installing Mosamatic Desktop is as simple as running <br>
<br>
<code>pip install mosamaticdesktop</code><br>
<br>
In order to use the automatic slice selection task you need a CUDA-enabled PyTorch setup. You can pre-install this PyTorch version by running<br>
<br>
<code>pip install torch==2.3.1+cu121 torchvision==0.18.1+cu121 torchaudio=2.3.1+cu121 -f https://download.pytorch.org/whl/torch_stable.html</code><br>

# Run
Running Mosamatic Desktop
