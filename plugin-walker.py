# Automagic plugin load script. 
# Version 1.0.0
# Maintainer andrew.bunday
# Walks from a plugin directory root adding subdirs to the path.
# Assumes file lives in the root of the plugin directory ie.
# 
# ./plugins/
#    -> init.py
#    -> myplugin/1.1   
#    -> myplugin/1.0   
#    -> myplugin2/1.0    
#
#
# Builds a list of the plugins residing in the current directory. Assumes that plugins live in a subdir
# called ./pluginname/version/*files.
#
# Unless a version for the plugin has been set in the nuke command path we use the last version in 
# the sorted list of versions available.
#
# Currently makes the assumption that only one version of plugin will be required within a scenefile... tbc.
#
# When the plugin is added to the nuke plugin path only python scripts are added to python's sys.path
# this is an over-optimisation, but appears to be harmless.... or possibly not since J_Ops stores its python in
# a "py" dir.

import os, re
import inspect
import nuke
import logging
import sys

logging.basicConfig(level=logging.ERROR)

def addPathToPlugins( plugin_path ):
	
	for dirpath, dirnames, filenames in os.walk( plugin_path, followlinks=True ):
		logging.debug( "---" )
		logging.debug( dirpath )
		logging.debug( dirnames )
		logging.debug( filenames )
		
		if re.match(".*/python$", dirpath) : #or re.match(".*/py$", dirpath):   # this is required for us to source jops directly                      
			nuke.pluginAddPath( dirpath, addToSysPath=True )    
		else:	
			nuke.pluginAddPath( dirpath, addToSysPath=False )

		if "__init__.py" in filenames: # then this must be a python module to be added to sys.path
			logging.debug( "Python module detected %s. Adding parent to syspath %s" % (os.path.basename(dirpath), os.path.dirname(dirpath)) )
			sys.path.append( os.path.dirname(dirpath) )

location = os.path.split( inspect.getsourcefile( addPathToPlugins ) )[0]

files       = os.listdir( location )
plugins  = {}

for file in files:
	if os.path.isdir( os.path.join( location, file ) ):
		plugins[ file ] = os.path.join( location, file )

for plugin_name in plugins:
	available_versions = os.listdir( plugins[ plugin_name ] )
	available_versions.sort()
	
	plugin_version = os.getenv( plugin_name.upper() )
	
	if not plugin_version or ( plugin_version not in available_versions ) :
		plugin_version = available_versions[-1]
		
	plugin_path = os.path.join( plugins[ plugin_name ], plugin_version )

	addPathToPlugins( plugin_path )
	
	
	

