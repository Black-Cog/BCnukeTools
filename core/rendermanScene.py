

def getShadingData( nodes ):
    """define shading data base on shading nodes"""
    '@parameter nodes (list of Gizmo) List of shading nodes.'
    'return shading data (dict)'
    
    shadingData = {}

    for node in nodes:
        nodeName = node.name()
        nodeClass = node.knobs()['__class'].value()

        settings = 'Bxdf "%s" "%s"' %( nodeClass, nodeName )

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

        settings += ' "__instanceid" ["%s_0"]' %( nodeName )


        shadingData[nodeName] = {'class':nodeClass, 'rule':'', 'value':settings}

    return shadingData


def getGeometryData( nodes ):
    """define geometry data base on geometry nodes"""
    '@parameter nodes (list of Gizmo) List of geometry nodes.'
    'return geometry data (dict)'
    
    objectSettings = {}

    for node in nodes:
        for attr in node.knobs().keys():
            if attr == 'm_rib':
                objectSettings[node.name()] = { 'path':node[attr].value() }

    return objectSettings


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


def getRenderData( nodes ):
    """define render data base on render nodes"""
    '@parameter nodes (dict) Nodes to render.'
    'return render data (dict)'
    
    renderData = { 'globals':{}, 'rlf':{}, 'data':{} }
    renderData['globals']['settings'] = getGlobalsSettingsData( nodes['settings'] )
    renderData['globals']['variables'] = getGlobalsVariablesData( nodes['dispatch'], nodes['renderpass'] )

    renderData['rlf']['shading'] = getShadingData( nodes['shader'] )
    renderData['rlf']['attribute'] = [{'class':'primaryOff', 'rule':'', 'value':'' }]

    renderData['data']['object'] = getGeometryData( nodes['geometry'] )
    renderData['data']['light'] = { 'lightName':{'class':'AeraLight', 'value':''} }
    renderData['data']['camera'] = { 'cameraName':{'value':''} }

    return renderData


def getRenderNodes( node ):
    """define a render nodes dict based on a node type dispatch"""
    '@parameter node (Gizmo) Node to render.'
    'return render nodes (dict)'

    nodes = {}
    nodes['shader'] = []
    nodes['settings'] = []
    nodes['geometry'] = []
    nodes['renderpass'] = []

    def climb( node ):
        for i in range( node.inputs() ):
            childNode = node.input(i)
            attrs = childNode.knobs()

            if '__type' in attrs.keys():
                attrType = attrs['__type'].value()
                print attrType
                print childNode

                if attrType == "shader":
                    nodes['shader'].append(childNode)

                elif attrType == "settings":
                    nodes['settings'].append(childNode)

                elif attrType == "geometry":
                    nodes['geometry'].append(childNode)

                elif attrType == "renderpass":
                    nodes['renderpass'].append(childNode)

            climb( childNode )


    if '__type' in node.knobs() and node.knobs()['__type'].value() == "dispatch":
        nodes['dispatch'] = node
        climb( node )
    
    return nodes

