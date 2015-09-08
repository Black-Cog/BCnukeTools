
# -*- coding: utf-8 -*-

# get init : need to copy these 3 lines in your own init.py
# import sys
# sys.path.append('f:/dev/BCnukeTools/user/')
# import init
# execfile( 'f:/dev/BCnukeTools/user/init.py' )


def hammerOpen():
	import sys
	if 'launchHammer' in sys.modules:
		del sys.modules['launchHammer']
	else:
		sys.path.append('f:/software/hammer_0.0.0.1dev/')
		sys.path.append('f:/software/hammer_0.0.0.1dev/Hammer/bin')

	import launchHammer
