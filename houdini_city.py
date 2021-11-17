#import du Module Houdini
import hou

#Création d’un objet
objets = hou.node('obj')

#Nettoyage de la scene
for node in objets.children():
    node.destroy()
    
    
scene = objets.createNode('geo','scene')

#Building
building = scene.createNode('box', 'building')
building.parm('ty').set(1.0)
building.parm('sizey').set(2.0)

tBuilding = scene.createNode('xform', 'tBuilding')
tBuilding.setInput(0, building)

colorBuilding = scene.createNode('color', 'colorBuilding')
colorBuilding.setInput(0, tBuilding)
colorBuilding.parm('colorr').set(0)
colorBuilding.parm('colorb').set(1)
colorBuilding.parm('colorg').set(0)

#Tree
tree = scene.createNode('lsystem', 'tree')
tree.parm('type').set('tube')
tTree = scene.createNode('xform', 'tTree')
tTree.setInput(0, tree)

colorTree = scene.createNode('color', 'colorTree')
colorTree.setInput(0, tTree)
colorTree.parm('colorr').set(1)
colorTree.parm('colorb').set(0)
colorTree.parm('colorg').set(0)

#Cailloux
platonic = scene.createNode('platonic', 'rock')
platonic.parm('type').set(4)
edit = scene.createNode('edit', 'rockShape')
edit.setInput(0, platonic)
edit.parm('grouptype').set(3)
edit.parm('group').set('1-3 6-8 12-13 17-18')
edit.parm('ty').set(-1.2)
edit.parm('tz').set(-0.5)
tRock = scene.createNode('xform', 'tRock')
tRock.setInput(0, edit)

#Switch
switch = scene.createNode('switch', 'switch')
switch.setInput(0, colorBuilding)
switch.setInput(1, colorTree)
switch.setInput(2, tRock)

#Sol
sol = scene.createNode('grid','sol')

#Points
points = scene.createNode('scatter::2.0', 'box_points')
points.setInput (0,sol)
nbpoints = points.parm('npts')
nbpoints.set(50)

#Random
pRand = scene.createNode('attribrandomize', 'pRand')
pRand.setInput(0, points)
pRand.parm('name').set('pscale')
pRand.parm('minx').set(0.2)
pRand.parm('miny').set(0.2)
pRand.parm('minz').set(0.2)
pRand.parm('minw').set(0.2)

#Relax
relax = scene.createNode('relax', 'pRelax')
relax.setInput(0,pRand)
relax.setInput(1,sol)

#Sort
sort = scene.createNode('sort', 'sort')
sort.parm('ptsort').set(6)
sort.setInput(0,relax)

#Wrangle
wrangle = scene.createNode('attribwrangle', 'wrangle')
wrangle.parm('snippet').set('i@pt = @ptnum%3;')
wrangle.setInput(0, sort)

#Sol
tGrid = scene.createNode('xform', 'tGrid')
tGrid .setInput(0, sol)

colorGrid = scene.createNode('color', 'colorGrid')
colorGrid.setInput(0, tGrid )
colorGrid.parm('colorr').set(0)
colorGrid.parm('colorb').set(0)
colorGrid.parm('colorg').set(1)

#FOR EACH
forEach_begin = scene.createNode('block_begin', 'foreach_begin1' )
forEach_begin.setInput(0, wrangle)
forEach_end = scene.createNode('block_end', 'foreach_end1')
forEach_begin.parm('method').set(1)
forEach_begin.parm('blockpath').set('../foreach_end1')
forEach_end.parm('blockpath').set('../foreach_begin1')
forEach_end.parm('templatepath').set('../foreach_begin1')
forEach_end.parm('method').set(1)

#SPARE INPUT
param_spare = switch.parmTemplateGroup()
my_parm = hou.StringParmTemplate(name='spare_input0', label='Spare input 0',num_components= 1, default_value = '')
param_spare.append(my_parm)
switch.setParmTemplateGroup(param_spare)
switch.parm('spare_input0').set('../foreach_begin1')
switch.parm('input').setExpression('point(-1,0,"pt",0)')

#COPY TO POINTS
copy = scene.createNode('copytopoints::2.0', 'box_copy')
copy.setInput(0, switch)
copy.setInput(1, forEach_begin)
forEach_end.setInput(0, copy)

#Merge
merge = scene.createNode('merge', 'result')
merge.setInput(0,forEach_end)
merge.setInput(1, colorGrid)


output = scene.createNode('null', 'output')
output.setInput(0,merge)


#gérer l’affichage des nodes
output.setDisplayFlag(True)
output.setRenderFlag(True)


scene.layoutChildren()








