
import BaseAction
import BCnukeTools.core
import BCnukeTools.core.rendermanScene as rendermanScene
import Forge.core.rendermanRib

class DipatchRender( BaseAction.BaseAction ):

    def _doAction( self, arg ):
        import nuke

        node = nuke.thisNode()

        if node['__class'].value() == 'taskList':
            names = node['m_tasks_string'].value().split(';')

            for name in node['m_tasks_string'].value().split(';'):
                nodeRender = nuke.toNode(name)
                if nodeRender and '__type' in nodeRender.knobs() and nodeRender['__type'].value() == 'dispatch':
                    nodeRender['dispatch'].execute()

        else:
            nodes = BCnukeTools.core.rendermanScene.getRenderNodes(node)
            args = BCnukeTools.core.rendermanScene.getRenderData(nodes)

            Forge.core.rendermanRib.launchRender( args )
