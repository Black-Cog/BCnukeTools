
# -*- coding: utf-8 -*-

# get menu : need to copy these 3 lines in your own menu.py
# import sys
# sys.path.append('f:/dev/BCnukeTools/user/')
# import menu
# execfile( 'f:/dev/BCnukeTools/user/menu.py' )

############
# menu
############
nuke.menu('Nuke').addMenu('Hammer')
nuke.menu('Nuke').addCommand('Hammer/Open', hammerOpen)


############
# hotkey
############
nuke.menu( 'Nodes' ).addCommand( 'Color/Exposure', "nuke.createNode( 'EXPTool' )", 'ctrl+e')



############
# Default node value
############
nuke.knobDefault( 'EXPTool.mode', '0' )
nuke.knobDefault( 'Roto.output', 'rgba' )


############
# Load Gizmo
############
gizmoPath = getBCnukeToolPath() + 'gizmo/'
iconsPath = getBCnukeToolPath() + 'icons/'

### PRMAN
prmanMenu = nuke.menu("Nodes").addMenu( "Renderman", icon='%srman_general.png' %(iconsPath) )

# prman shading
shadingMenu = prmanMenu.addMenu( "Shading", icon='%srender_generalPurpose.png' %(iconsPath) )
shadingMenu.addCommand(
                            "PxrDisney",
                            "nuke.createNode('%srenderman/shading/PxrDisney.gizmo')" %(gizmoPath),
                            icon='%srender_PxrDisney.png' %(iconsPath),
                        )
shadingMenu.addCommand(
                            "PxrConstant",
                            "nuke.createNode('%srenderman/shading/PxrConstant.gizmo')" %(gizmoPath),
                            icon='%srender_PxrConstant.png' %(iconsPath),
                        )
shadingMenu.addCommand(
                            "PxrLMDiffuse",
                            "nuke.createNode('%srenderman/shading/PxrLMDiffuse.gizmo')" %(gizmoPath),
                            icon='%srender_PxrLMDiffuse.png' %(iconsPath),
                        )
shadingMenu.addCommand(
                            "PxrLMGlass",
                            "nuke.createNode('%srenderman/shading/PxrLMGlass.gizmo')" %(gizmoPath),
                            icon='%srender_PxrLMGlass.png' %(iconsPath),
                        )
shadingMenu.addCommand(
                            "PxrLMMetal",
                            "nuke.createNode('%srenderman/shading/PxrLMMetal.gizmo')" %(gizmoPath),
                            icon='%srender_PxrLMMetal.png' %(iconsPath),
                        )
shadingMenu.addCommand(
                            "PxrLMPlastic",
                            "nuke.createNode('%srenderman/shading/PxrLMPlastic.gizmo')" %(gizmoPath),
                            icon='%srender_PxrLMPlastic.png' %(iconsPath),
                        )
shadingMenu.addCommand(
                            "PxrLMSubsurface",
                            "nuke.createNode('%srenderman/shading/PxrLMSubsurface.gizmo')" %(gizmoPath),
                            icon='%srender_PxrLMSubsurface.png' %(iconsPath),
                        )
shadingMenu.addCommand(
                            "PxrMarschnerHair",
                            "nuke.createNode('%srenderman/shading/PxrMarschnerHair.gizmo')" %(gizmoPath),
                            icon='%srender_PxrMarschnerHair.png' %(iconsPath),
                        )
shadingMenu.addCommand(
                            "PxrVolume",
                            "nuke.createNode('%srenderman/shading/PxrVolume.gizmo')" %(gizmoPath),
                            icon='%srender_PxrVolume.png' %(iconsPath),
                        )

# prman lighting
lightingMenu = prmanMenu.addMenu( "Lighting", icon='%srender_RenderManLight.png' %(iconsPath) )
lightingMenu.addCommand(
                            "AreaLight",
                            "nuke.createNode('%srenderman/lighting/AreaLight.gizmo')" %(gizmoPath),
                            icon='%srender_RMSAreaLight.png' %(iconsPath),
                        )
lightingMenu.addCommand(
                            "DistantLight",
                            "nuke.createNode('%srenderman/lighting/DistantLight.gizmo')" %(gizmoPath),
                            icon='%srender_RenderManLight.png' %(iconsPath),
                        )
lightingMenu.addCommand(
                            "SpotLight",
                            "nuke.createNode('%srenderman/lighting/SpotLight.gizmo')" %(gizmoPath),
                            icon='%srender_RenderManLight.png' %(iconsPath),
                        )
lightingMenu.addCommand(
                            "EnvironnementLight",
                            "nuke.createNode('%srenderman/lighting/EnvironnementLight.gizmo')" %(gizmoPath),
                            icon='%srender_RMSEnvLight.png' %(iconsPath),
                        )

# prman rendering
renderingMenu = prmanMenu.addMenu( "Rendering", icon='%srman_render.png' %(iconsPath) )
renderingMenu.addCommand(
                            "ReadRib",
                            "nuke.createNode('%srenderman/rendering/ReadRib.gizmo')" %(gizmoPath),
                            icon='%srman_ribbox.png' %(iconsPath),
                        )
renderingMenu.addCommand(
                            "Preview",
                            "nuke.createNode('%srenderman/rendering/Preview.gizmo')" %(gizmoPath),
                            icon='%srman_preview.png' %(iconsPath),
                        )
renderingMenu.addCommand(
                            "Render",
                            "nuke.createNode('%srenderman/rendering/Render.gizmo')" %(gizmoPath),
                            icon='%srman_render.png' %(iconsPath),
                        )
renderingMenu.addCommand(
                            "TaskList",
                            "nuke.createNode('%srenderman/rendering/TaskList.gizmo')" %(gizmoPath),
                            icon='%srman_render.png' %(iconsPath),
                        )
renderingMenu.addCommand(
                            "Settings",
                            "nuke.createNode('%srenderman/rendering/Settings.gizmo')" %(gizmoPath),
                            icon='%srman_render_options.png' %(iconsPath),
                        )
renderingMenu.addCommand(
                            "AOV",
                            "nuke.createNode('%srenderman/rendering/Aov.gizmo')" %(gizmoPath),
                            icon='%srman_render_options.png' %(iconsPath),
                        )
renderingMenu.addCommand(
                            "Renderpass",
                            "nuke.createNode('%srenderman/rendering/Renderpass.gizmo')" %(gizmoPath),
                            icon='%srman_render_options.png' %(iconsPath),
                        )
renderingMenu.addCommand(
                            "RenderCamera",
                            "nuke.createNode('%srenderman/rendering/RenderCamera.gizmo')" %(gizmoPath),
                            icon='%sRenderCamera.png' %(iconsPath),
                        )
renderingMenu.addCommand(
                            "AssignMaterial",
                            "nuke.createNode('%srenderman/rendering/AssignMaterial.gizmo')" %(gizmoPath),
                            icon='%sAssignMaterial.png' %(iconsPath),
                        )
renderingMenu.addCommand(
                            "Attribute",
                            "nuke.createNode('%srenderman/rendering/Attribute.gizmo')" %(gizmoPath),
                            icon='%sAssignMaterial.png' %(iconsPath),
                        )
renderingMenu.addCommand(
                            "Xpath",
                            "nuke.createNode('%srenderman/rendering/Xpath.gizmo')" %(gizmoPath),
                            icon='%sXpath.png' %(iconsPath),
                        )

