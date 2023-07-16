pypboy
======

This is a modified version of ZapWizard's Pipboy 3000 MkIV software forked from the original, with the
intent of cleaning up the code, making it run more efficiently on Raspberry Pi, and more importantly, adding Touchscreen support
such that projects running on a lower-complexity build of the Pipboy 3D Print can operate without requiring all the proper dials
and other such bells and whistles.

======

Adding radio stations is now as easy as making a folder in sounds/radio with MP3, OGG or WAV files.
Make a file name Station.py, with station_name = "Your name here" to set the menu text. The folder name used if the file is missing.
Add a number to the beginning of the folder name to set the menu position.

======

Navigation:

Clicking can be used to navigate between the five main modules, but the original controls remain, unaltered.

F1 - Stats
F2 - Inventory
F3 - Data
F4 - Map
F5 - Radio
F6 - Boot screen

1,2,3,4, etc to navigate the sub-header menu

Up/Down arrow keys to navigate the sub-menus

+/- to zoom the map

======

Supports caching and offline loading of maps.
* In settings.py set 'LOAD_CACHED_MAP = False'
* Run the application once
* In settings.py set 'LOAD_CACHED_MAP = True'
* Pypboy will now load the cached map on starting

======

## Autors
* Touch and Mouse controls, as well as Fixes and Updates by cgruhler

* Major overhaul by ZapWizard for the Functional Pip-Boy 3000 MK IV GUI

* Fixes and Updates by kingpinzs

* Fixes and Updates by amolloy

* Fixes and Updates by Goldstein

* Updates by Sabas of The Inventor's House Hackerspace

* Originally by grieve work original<br>

======

## License
MIT

======

### Enable app to startup on boot
pi@XXXX:~/Downloads/pypboy $ cat ~/launch_pipboy.sh
#!/bin/bash
cd ~/Downloads/pypboy
python ./main.py

pi@XXXX:~/Downloads/pypboy $ grep launch_pipboy /etc/lightdm/lightdm.conf
session-setup-script=/home/pi/launch_pipboy.sh
pi@XXXX:~/Downloads/pypboy $
