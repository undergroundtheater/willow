willow
======

Willow is a flexible platform for managing pen and paper, LARP and by-mail role-playing games.

A windows platform is *not* recommended for this application.  It is suited for any Linux environment or other environment that supports compiling libraries for python at installation using pip.


Installation
======

Requires: Bower at the system or user level, compiler access (for encryption) and associated headers (python, etc).

$ virtualenv willow
$ cd willow
$ git clone https://github.com:undergroundtheater/willow.git -b develop app
$ cd app
$ pip install -r requirements.txt
$ bower install
$ cp willow/settings_dist.py willow/settings.py
$ python manage.py assets build
$ python run.py

