# GNURadio
## Installation on Raspberry Pi
Installing GNURadio under Debian on the Raspberry Pi is as simple as:
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install gnuradio*
```

Installing rtl-sdr and osmocom_fft can by done with:
```
sudo apt-get install rtl-sdr gr-osmosdr
```

Then:
```
osmocom_fft
```
There's a chance that you may experience a "BadMatch" error when launching osmocom_fft. If so, use:
```
sudo nano /boot/config.txt
```
Move to the bottom, then add the lines
```
framebuffer_depth=32
framebuffer_ignore_alpha=1
```
Reboot the Pi and relaunch osmocom_fft.

If you get an OpenGL error with ID#1281, you may need to enable the OpenGL driver for your Pi. Use:
```
sudo raspi-config
```
Navigate to "Advanced Options", move down to "GL Driver", then enable it.




It may be desirable to get a feel for the GNURadio companion by installing the gr-tutorial package from [GitHub][1]. Installation instructions can be found on the GNURadio [site][2], but building it requires installing the following dependencies which are not mentioned there:
```
sudo apt-get install cmake libboost* libcppunit* doxygen liblog4cpp5*
```

[1]: https://github.com/gnuradio/gr-tutorial
[2]: http://gnuradio.org/redmine/projects/gnuradio/wiki/Guided_Tutorial_GRC
