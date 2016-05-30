# GNURadio
## Installation on Raspberry Pi
Installing GNURadio under Debian on the Raspberry Pi is as simple as:
```
sudo apt-get install gnuradio*
```

It may be desirable to get a feel for the GNURadio companion by installing the gr-tutorial package from [GitHub][1]. Installation instructions can be found on the GNURadio [site][2], but building it requires installing the following dependencies which are not mentioned there:
```
sudo apt-get install cmake libboost* libcppunit* doxygen liblog4cpp5*
```

[1]: https://github.com/gnuradio/gr-tutorial
[2]: http://gnuradio.org/redmine/projects/gnuradio/wiki/Guided_Tutorial_GRC
