

def getNodeAttr(node):
    """define renderman attr data from a node"""
    '@parameter node (Gizmo) Renderman node.'
    'return renderman attr data (string)'

    settings = ''
    for attr in node.knobs().keys():
        if attr.startswith( 'm_' ):
            value = node[attr].getValue()
            valueType = attr.split('_')[-1]
            name = '_'.join( attr.split('_')[:-1][1:] )

            # 3 float data : color, normal
            if valueType in ['color', 'normal', 'vector']:
                if not isinstance( value, list ):
                    value = [value, value, value]
                settings += ' "%s %s" %s' %( valueType, name, str(value).replace(',', '') )

            # float data
            elif valueType == 'float':
                settings += ' "%s %s" [%s]' %(valueType, name, value)

            # int data
            elif valueType == 'int':
                settings += ' "%s %s" [%s]' %(valueType, name, int(value) )

            # int data
            elif valueType == 'string':
                settings += ' "%s %s" ["%s"]' %(valueType, name, node[attr].value() )

    return settings


def getLightTypeId(node):
    """define typeId of a light from a node"""
    '@parameter node (Gizmo) Renderman node.'
    'return typeId (int)'

    attr = 'm_rman__Shape_string'
    typeId = None

    if attr in node.knobs().keys():
        value = node[attr].value()
        if value == 'rect':
            typeId = 1
        if value in ['disk', 'spot']:
            typeId = 2
        if value == 'sphere':
            typeId = 3
        if value == 'distant':
            typeId = 4

    else:
        # env
        typeId = 0

    return typeId


def getCameraData( nodes ):
    """define cameras data base on camera nodes"""
    '@parameter nodes (list of Gizmo) List of camera nodes.'
    'return cameras data (dict)'

    import math

    cameraData =   {}
    for node in nodes:
        cameraData[ node.name() ] = {
                                        'clipping':[ node['near'].value(), node['far'].value() ],
                                        'fov':math.atan( (node['haperture'].value()/2) / node['focal'].value() ) * (360 / math.pi),
                                        'translate':[
                                                        node['translate'].value()[0] * -1,
                                                        node['translate'].value()[1] * -1,
                                                        node['translate'].value()[2] * -1
                                                    ],
                                        'rotate':[
                                                    node['rotate'].value()[0],
                                                    node['rotate'].value()[1],
                                                    node['rotate'].value()[2] * -1
                                                 ]
                                    }

    return cameraData


def getLightData( nodes ):
    """define lights data based on light nodes"""
    '@parameter nodes (list of Gizmo) List of light nodes.'
    'return lights data (dict)'

    lightData =   {}
    for node in nodes:
        matrix = node['matrix'].getValue()
        matrix = [
                    str(matrix[0]), str(matrix[4]), str(matrix[8]), str(matrix[12]),
                    str(matrix[1]), str(matrix[5]), str(matrix[9]), str(matrix[13]),
                    str(matrix[2]), str(matrix[6]), str(matrix[10]), str(matrix[14]),
                    str(matrix[3]), str(matrix[7]), str(matrix[11]), str(matrix[15])
                ]

        lightData[ node.name() ] =  {
                                        'slo':node['__slo'].getValue(),
                                        'type':getLightTypeId(node),
                                        'matrix':'[%s]' %( ' '.join(matrix) ),
                                        'settings':getNodeAttr(node),
                                    }
    return lightData


def climbToNode( node, type ):
    """define shading data base on shading nodes"""
    '@parameter node (Gizmo) Node to start climbing.'
    '@parameter type (str) Node type.'
    'return first node with a matching type (Gizmo)'

    if node:
        if node and '__type' in node.knobs().keys() and node['__type'].value() == type:
            return node

        for i in range( node.inputs() ):
            childNode = node.input(i)

            if childNode and '__type' in childNode.knobs().keys() and childNode['__type'].value() == type:
                return childNode

    return None


def getShadingData( nodes ):
    """define shading data base on shading nodes"""
    '@parameter nodes (list of Gizmo) List of shading nodes.'
    'return shading data (dict)'
    
    shadingData = []

    for node in nodes:
        shader = climbToNode( node.input(1), 'shader' )
        xpath = climbToNode( node.input(2), 'xpath' )

        if shader:
            shaderName = shader.name()
            shaderClass = shader.knobs()['__class'].value()

            settings = 'Bxdf "%s" "%s"' %( shaderClass, shaderName )
            settings += getNodeAttr(shader)
            settings += ' "__instanceid" ["%s_0"]' %( shaderName )

            rule = '/*'
            if xpath:
                rule = xpath['m_xpath_string'].getValue()

            shadingData.append(
                                {
                                    'name':shaderName,
                                    'class':shaderClass,
                                    'rule':rule,
                                    'value':settings
                                }
                                )

    return shadingData


def getAttributeData( nodes ):
    """define attribute data base on attribute nodes"""
    '@parameter nodes (list of Gizmo) List of attribute nodes.'
    'return attribute data (list)'
    
    attributeData = []

    for node in nodes:
        xpath = climbToNode( node.input(1), 'xpath' )

        rule = '/*'

        if xpath:
            rule = xpath['m_xpath_string'].getValue()

        # geometric
        m_matte_int = node['m_matte_int'].value()
        if m_matte_int == 'unchanged':
            m_matte_int = None

        m_side_int = node['m_side_int'].value()
        if m_side_int == 'unchanged':
            m_side_int = None


        # visibility
        m_visibility_camera_int = node['m_visibility_camera_int'].value()
        if m_visibility_camera_int == 'unchanged':
            m_visibility_camera_int = None

        m_visibility_transmission_int = node['m_visibility_transmission_int'].value()
        if m_visibility_transmission_int == 'unchanged':
            m_visibility_transmission_int = None

        m_visibility_indirect_int = node['m_visibility_indirect_int'].value()
        if m_visibility_indirect_int == 'unchanged':
            m_visibility_indirect_int = None


        # trace
        m_trace_maxdiffusedepth_int = node['m_trace_maxdiffusedepth_int'].value()
        if m_trace_maxdiffusedepth_int == 'unchanged':
            m_trace_maxdiffusedepth_int = None

        m_trace_maxspeculardepth_int = node['m_trace_maxspeculardepth_int'].value()
        if m_trace_maxspeculardepth_int == 'unchanged':
            m_trace_maxspeculardepth_int = None

        attributeData.append(
                            {
                                'rule':rule,
                                'm_matte_int':m_matte_int,
                                'm_side_int':m_side_int,
                                'm_visibility_camera_int':m_visibility_camera_int,
                                'm_visibility_transmission_int':m_visibility_transmission_int,
                                'm_visibility_indirect_int':m_visibility_indirect_int,
                                'm_trace_maxdiffusedepth_int':m_trace_maxdiffusedepth_int,
                                'm_trace_maxspeculardepth_int':m_trace_maxspeculardepth_int,
                            }
                        )

    return attributeData


def getGeometryData( nodes ):
    """define geometry data base on geometry nodes"""
    '@parameter nodes (list of Gizmo) List of geometry nodes.'
    'return geometry data (dict)'
    
    geometryData = {}

    for node in nodes:
        matrix = node['matrix'].getValue()
        matrix = [
                    str(matrix[0]), str(matrix[4]), str(matrix[8]), str(matrix[12]),
                    str(matrix[1]), str(matrix[5]), str(matrix[9]), str(matrix[13]),
                    str(matrix[2]), str(matrix[6]), str(matrix[10]), str(matrix[14]),
                    str(matrix[3]), str(matrix[7]), str(matrix[11]), str(matrix[15])
                ]

        path = node['m_rib'].value()
        if '%04d' in path:
            path = path.replace( '%04d', str( int(node['lock_frame'].getValue()) ).zfill(4) )

        geometryData[ node.name() ] =  {
                                        'path':path,
                                        'matrix':'[%s]' %( ' '.join(matrix) ),
                                    }

    return geometryData


def getGlobalsSettingsData( nodes ):
    """define globalsSettings data base on globalsSettings nodes"""
    '@parameter nodes (list of Gizmo) List of globalsSettings nodes.'
    'return globalsSettings data (dict)'
    
    globalsSettings = { 'render':{}, 'display':{} }
    # todo : be able to manage multiple settings node
    node = nodes[0]

    formatObj = node['m_Format_int'].value()
    if not isinstance( formatObj, list ):
        formatObj = [formatObj, formatObj]
    formatObj = [ int( i*node['m_formatMultiplier_float'].value() ) for i in formatObj ]
    formatObj.append( node['m_pixelRatio_float'].value() )

    globalsSettings['render']['Format'] = formatObj
    globalsSettings['render']['pass_camera_name'] = node['m_pass_camera_name_string'].value()
    globalsSettings['render']['CropWindow'] = list( node['m_CropWindow_bb'].value() )
    globalsSettings['render']['minsamples'] = int( node['m_minsamples_int'].value() )
    globalsSettings['render']['maxsamples'] = int( node['m_maxsamples_int'].value() )
    globalsSettings['render']['PixelVariance'] = node['m_PixelVariance_float'].value()
    globalsSettings['render']['maxPathLength'] = int( node['m_maxPathLength_int'].value() )
    globalsSettings['render']['numLightSamples'] = int( node['m_numLightSamples_int'].value() )
    globalsSettings['render']['numBxdfSamples'] = int( node['m_numBxdfSamples_int'].value() )
    globalsSettings['render']['numIndirectSamples'] = int( node['m_numIndirectSamples_int'].value() )
    globalsSettings['render']['allowCaustics'] = int( node['m_allowCaustics_int'].value() )
    globalsSettings['render']['maxdiffusedepth'] = int( node['m_maxdiffusedepth_int'].value() )
    globalsSettings['render']['maxspeculardepth'] = int( node['m_maxspeculardepth_int'].value() )
    globalsSettings['render']['order'] = node['m_order_string'].value()
    globalsSettings['render']['minwidth'] = node['m_minwidth_float'].value()
    globalsSettings['render']['texturememory'] = int( node['m_texturememory_int'].value() )
    globalsSettings['render']['geocachememory'] = int( node['m_geocachememory_int'].value() )
    globalsSettings['render']['proceduralmemory'] = int( node['m_proceduralmemory_int'].value() )
    globalsSettings['render']['opacitycachememory'] = int( node['m_opacitycachememory_int'].value() )


    filterwidthObj = node['m_filterwidth_int'].value()
    if not isinstance( filterwidthObj, list):
        filterwidthObj = [filterwidthObj, filterwidthObj]

    globalsSettings['display']['filter'] = node['m_filter_string'].value()
    globalsSettings['display']['filterwidth'] = filterwidthObj

    return globalsSettings


def getGlobalsVariablesData( dispatcher, renderpass ):
    """define globalsVariables data base on globalsVariables nodes"""
    '@parameter dispatcher (Gizmo) Dispatcher node.'
    '@parameter renderpass (Gizmo) Renderpass node.'
    'return globalsVariables data (dict)'
    
    # todo : get these variable from the nuke script
    path = 'f:/tmp/'
    sceneName = 'scene_002'

    # get passname
    passName = renderpass[0].knobs()['m_renderpassName_string'].value()
    # get frame range
    frames = [int( renderpass[0].knobs()['m_frameRange_string'].value() )]

    # get display type
    dispatcherType = dispatcher.knobs()['__class'].value()
    if dispatcherType == 'render':
        displayType = 0
    elif dispatcherType == 'preview':
        displayType = 1


    globalsVariables = {
                        'path':path,
                        'sceneName':sceneName,
                        'passName':passName,
                        'frames':frames,
                        'displayType':displayType,
                        }

    return globalsVariables


def getRenderNodes( node ):
    """define a render nodes dict based on a node type dispatch"""
    '@parameter node (Gizmo) Node to render.'
    'return render nodes (dict)'

    nodes = {}
    nodes['assignMaterial'] = []
    nodes['settings'] = []
    nodes['geometry'] = []
    nodes['renderpass'] = []
    nodes['camera'] = []
    nodes['light'] = []
    nodes['attribute'] = []

    def climb( node ):
        if node:
            for i in range( node.inputs() ):
                childNode = node.input(i)

                if childNode and '__type' in childNode.knobs().keys():
                    attrType = childNode['__type'].value()

                    if attrType == 'settings':
                        nodes['settings'].append(childNode)

                    elif attrType == 'assignMaterial':
                        nodes['assignMaterial'].append(childNode)

                    elif attrType == 'geometry':
                        nodes['geometry'].append(childNode)

                    elif attrType == 'renderpass':
                        nodes['renderpass'].append(childNode)

                    elif attrType == 'camera':
                        nodes['camera'].append(childNode)

                    elif attrType == 'light':
                        nodes['light'].append(childNode)

                    elif attrType == 'attribute':
                        nodes['attribute'].append(childNode)

                climb( childNode )

    if '__type' in node.knobs() and node.knobs()['__type'].value() == 'dispatch':
        nodes['dispatch'] = node
        climb( node )
    
    return nodes


def getRenderData( nodes ):
    """define render data base on render nodes"""
    '@parameter nodes (dict) Nodes to render.'
    'return render data (dict)'
    
    renderData = { 'globals':{}, 'rlf':{}, 'data':{} }
    renderData['globals']['settings'] = getGlobalsSettingsData( nodes['settings'] )
    renderData['globals']['variables'] = getGlobalsVariablesData( nodes['dispatch'], nodes['renderpass'] )

    renderData['rlf']['shading'] = getShadingData( nodes['assignMaterial'] )
    renderData['rlf']['attribute'] = getAttributeData(  nodes['attribute'] )

    renderData['data']['object'] = getGeometryData( nodes['geometry'] )
    renderData['data']['light'] = getLightData( nodes['light'] )
    renderData['data']['camera'] = getCameraData( nodes['camera'] )

    return renderData
