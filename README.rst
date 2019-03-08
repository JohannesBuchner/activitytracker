Activity Tracker
===================

Track what you are spending your time on.

* It logs the current open window title and whether the user is active every 15s.
* Reports to be done. Ultimately I want to classify in "deep work" and "slacking" and see when I am most productive.


Installation
=============

Place into ~/.config/autostart/activitytracker.desktop::

	[Desktop Entry]
	Name=Activity Tracker
	GenericName=Tracks what you spend your time on
	Exec=/home/user/Downloads/activitytracker/tracker.sh
	StartupNotify=false
	Terminal=false
	Version=1.0
	Categories=Utility;
	Type=Application
	X-GNOME-Autostart-enabled=true

Then restart.

Or start it manually with::

	$ /home/user/Downloads/activitytracker/tracker.sh

Watch the recording::

	$ tail -f ~/.local/share/activitytracker/log 

Reports
=============

* Create ~/.local/share/activitytracker/classes defining in each line:

  * Name of class
  * \t as separator
  * Regular expression for matching "title :: executable"
  
  for example::
  
	Hobby	~/Downloads/activitytracker
	Lit	JabRef
	Programming	/usr/bin/gedit
	Programming	IPython
	Programming	/usr/lib/gnome-terminal/gnome-terminal-server

  * The first matching class is assigned.

* run report.py::

	$ python report.py 
	
	day of the year
	|
	|   hour of day (four for each 15 minutes
	|   |
	v   v  
	DDD-HH Hobb Lit  Prog Rese   <-- classes
	 66-16 ====               
	 66-16 ====               
	 66-16 ===       ==       
	 66-17 ====      =        
	 66-17 ====               
	 66-17 ===       ==       
	 66-18 =    =         === 
	 66-18           ==== =   
	                 \^ 
	                 |
	                 bar shows time fraction
	                 spend on that class


License
==========

2-clause BSD



