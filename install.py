
import shlex
import os
import sys
import shutil


softwareEnvironment = 'f:/software/'

FORGE_VERSION = '0.0.0.1dev'
ANVIL_VERSION = '0.0.0.1dev'

forgePath  = '%sforge_%s' %( softwareEnvironment, FORGE_VERSION )
anvilPath  = '%sanvil_%s' %( softwareEnvironment, ANVIL_VERSION )
parentPath = '/'.join( sys.path[0].replace('\\', '/').split('/')[:-1] )

envs = [ forgePath, anvilPath, parentPath ]
for env in envs:
	sys.path.append( env )

import Forge
import BCnukeTools


###############################################################################################
# Version
###############################################################################################


coalMilestoneVersion = 0 # for announcing major milestones - may contain all of the below
coalMajorVersion     = 0 # backwards-incompatible changes
coalMinorVersion     = 0 # new backwards-compatible features
coalPatchVersion     = 1 # bug fixes


###############################################################################################
# Environment
###############################################################################################


softwareName = 'BCnukeTools_%s.%s.%s.%sdev/%s' %( coalMilestoneVersion, coalMajorVersion, coalMinorVersion, coalPatchVersion, 'BCnukeTools' )
softwarePath = '%s%s/' %( softwareEnvironment, softwareName )


###############################################################################################
# Folder creation
###############################################################################################


curentPath = Forge.core.System.getPath( __file__ )
coreDir = 'core'
actionsDir = 'actions'
gizmoRendermanRenderingDir = 'gizmo/renderman/rendering'
gizmoRendermanShadingDir = 'gizmo/renderman/shading'
gizmoRendermanLightingDir = 'gizmo/renderman/lighting'
iconsDir = 'icons'
userDir = 'user'

Fsystem = Forge.core.System()

for folder in 	[
					coreDir,
					actionsDir,
					gizmoRendermanRenderingDir,
					gizmoRendermanShadingDir,
					gizmoRendermanLightingDir,
					iconsDir,
					userDir,
				]:
	Fsystem.mkdir( '%s%s' %(softwarePath, folder) )

###############################################################################################
# Moving compiles files
###############################################################################################


print '>>> Install Begin'

for folder in 	[
					curentPath,
					coreDir,
					actionsDir,
					gizmoRendermanRenderingDir,
					gizmoRendermanShadingDir,
					gizmoRendermanLightingDir,
					iconsDir,
					userDir,
				]:

	for file in os.listdir( folder ):
		currentFile = '%s/%s' %( folder, file )
		newFile = '%s%s/%s' %( softwarePath, folder, file )

		if folder == userDir or '.png' in file or '.gizmo' in file:
			shutil.copy( currentFile, newFile )
			print '>>>   "%s" is well compiled.' %( newFile )
		else:
			if '.pyc' in file:
				if folder == curentPath:
					newFile = '%s/%s' %( softwarePath, file )

				if os.path.exists( newFile ):
					os.remove( newFile )

				os.rename( currentFile, newFile )
				print '>>>   "%s" is well compiled.' %( newFile )

print '>>> Install End'
