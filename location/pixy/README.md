look at hello_pixy.cpp was the first completed program for a single camera.  (MWE-11/06/2017)

**Build Notes**

cd /CS460/location/pixy/scripts
chmod +x build_hello_pixy.sh
./build_hello_pixy.sh

run
cd ~/CS460/location/pixy/build/hello_pixy 
./hello_pixy


**git notes**

git pull


git add . # adds all files with changes to commit
git commit -m "Updated Pixy build info for new folder structure"

link
git remote add origin https://github.com/unlimiteddigits/SeniorDesign.git
git push -u origin master

git clone https://github.com/unlimiteddigits/SeniorDesign.git
git clone https://github.com/elliae01/CS460.git

-----------------------------
git rm -r  __pycache__
git commit -m "removed accidental add"
git push -u origin master





libpixyusb API Reference:

http://charmedlabs.github.io/pixy/index.html

Pixy README

This directory contains:


/doc - this directory contains a doxygen configuration file for building doxygen documentation.

/scripts - this directory contains scripts for building pixy software modules.

/src/device - this directory contains code (firmware) that runs on the Pixy
(CMUcam5) device.

/src/host - this directory contains code that runs on the host computer.
(Windows PC, Linux PC, Mac)

/src/host/hello_pixy - this directory contains an example program that uses libpixyusb for communicating with Pixy.

/src/host/libpixyusb - this directory contains the USB library for communicating with Pixy.

/src/host/arduino - this directory contains the Arduino library for communicating with Pixy.

