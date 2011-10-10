Nuke Plugin Walker
==================

## The Short Description


An auto discovery and loading script for The Foundry's Nuke Compositing Application. 

Supports adding of plugin paths to the nuke pluginpath, python sys.path and controlled versioning of plugins. 


## A Slightly Longer Description

This simple python snippet makes my life much easier when packaging up new plugins/gizmos for Nuke. The main inspiration for doing this came from becoming annoyed by artists adding each new plugin to their menu.py scripts in their home directories and by each plugin having this codeblock in its init.py:

    for path in nuke.pluginPath():
        if os.path.exists(path+"/myplugin/py"):
            sys.path.append(path+"/myplugin/py")
        if os.path.exists(path+"/../myplugins/py"):
            sys.path.append(path+"/py")
        if os.path.exists(path+"/../myplugin/ndk"):
            nuke.pluginAddPath(path+"/ndk")
        if os.path.exists(path+"/../myplugin/icons"):         
            nuke.pluginAddPath(path+"/icons")

This script *removes* the requirement for each plugin to feature this snippet and also provides handling for multiple versioning of plugins installed on the system. 


## Simple Usage Instructions

Your plugins should be organised in the fairly standard layout of:

    MyPlugin/<VERSION>/
        docs/
        icons/
        ndk/
        py       
        menu.py
        init.py
      
*The python directory may be called either py/python.*

The init.py file should be left empty unless you perform some initialization for your plugin here. The gumph involving lots of **os.path.exists** calls listed earlier shouldn't be put in. 

All of your plugins should live under the same plugin directory, or else you should have a copy of the plugin walker copied into each of the directories listed in your NUKE_PATH.

### Versioning

Since the walker supports versioning of your plugins you can place each major.minor release in a sub-directory under the plugin name. To ensure that Nuke auto-loads the walker script it's renamed to init.py upon installation.

Here's an example:

    ./plugins/
        -> init.py
        -> myplugin/1.1   
        -> myplugin/1.0   
        -> myplugin2/1.0    

When the walker runs it first looks under its current directory for the plugin names and versions. It will then attempt to load the one with the latest release. 

If a specific version is required then it can be set via an environment variable.

    export MYPLUGIN=1.0

The environment variable is the name of the plugin converted to uppercase.

#### Patch Versions

Personally we only allow major.minor versions of plugins to visible to the end users. This means that they never see patch versions on the system and usually we'll overwrite these with the next release.

For us the patch versions are controlled and search-able via the system package manager. ie.

    Package Name          Package Version
    nuke6.3-myplugin1.0   1.0.2-baseblack-r1
    
***    
