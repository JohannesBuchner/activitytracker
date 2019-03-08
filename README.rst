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


