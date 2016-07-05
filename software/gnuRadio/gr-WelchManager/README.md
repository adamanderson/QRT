This is the current Welch module, ready to be tested on the Raspberry Pi.  It should be usable in GNURadio Companion.  MAKE SURE that scipy is the newest version, on the Raspberry pi scipy must be installed from the source (this takes a few hours).  To install:
First, edit the CmakeLists.txt file in the grc directory so that the install arguemnt directs to an existing gnuradio-companion block path.
To find the block path, open gnuradio-companion and it will be in a log file (or open it with a terminal and it will show up)
Next, use these commands to install the module (from the /gr-WelchManager directory)
$mkdir build
$cd build
$cmake ../
$make
$make test
$sudo make install
