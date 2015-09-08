
import BaseAction
import BCnukeTools.core
import BCnukeTools.core.rendermanScene as rendermanScene
import Forge.core.rendermanRib

class DipatchRender( BaseAction.BaseAction ):

    def _doAction( self, arg ):
        import nuke

        node = nuke.thisNode()
        nodes = BCnukeTools.core.rendermanScene.getRenderNodes(node)
        args = BCnukeTools.core.rendermanScene.getRenderData(nodes)

        Forge.core.rendermanRib.launchRender( args )
