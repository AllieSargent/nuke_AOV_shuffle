############################
# AOV Shuffle              #
# Created 10/30/22         #
# Modified 11/17/22        #
# Created by Allie Sargent #
############################

import fnmatch
#nuke.pluginAddPath('H:\2022_Fall_SCAD\VSFX_313\06_nuke_shuffle\scripts')
#from AOV_shuffle import cleanScene, format_shuf

def cleanScene():
    for node in nuke.allNodes():
        if "n_Merge" in node['name'].value() or "n_DotNode" in node['name'].value()\
        or "n_dotCopy" in node['name'].value() in node['name'].value()\
        or "n_copy" in node['name'].value() or "n_Denoise" in node['name'].value()\
        or "n_ShuffleNode" in node['name'].value() or "n_topDotNode" in node['name'].value():
            nuke.delete(node)

cleanScene()

# Parsing AOV's 
single_channels = []
cln_chan_value = []
        
selectedNode = nuke.selectedNode()
channels = selectedNode.channels()
imX = selectedNode.xpos()
imY = selectedNode.ypos()

      
# Grab AOV's from Selected Node and Add to List
for x in range(len(channels)):
    sm = channels[x].split(".")
    if sm[0].startswith("crypto") or sm[0].startswith("motion") or sm[0].startswith("P")\
    or sm[0].startswith("shadow") or sm[0].startswith("rgb"):
        print("ignore crypto")
    else:
        single_channels.append(sm[0])

        
# set with AOV passes without duplicate layers
clean_channels = set(single_channels)
cln_chan_lst = list(clean_channels)
length = len(cln_chan_lst)


# create dictionary for denoise 
for x in range(length):
    cln_chan_value.append("False")

    cln_chan_dict = dict(zip(cln_chan_lst, cln_chan_value))



# check for dot nodes
def first_dot():
    for node in nuke.allNodes():
        if "n_top" in node['name'].value():
            return True
        else:
            return False

check = "True"


# Node creation for Nuke Layout
def createLayout():
    length = len(cln_chan_lst)
    cln_chan_lst.append("blank")

    # spacing setup
    x = imX - 50
    y = imY + 365
    z = -184
    w = 0
    q = -2
    v = 0

    # create first dot
    nDot = nuke.nodes.Dot(name = "n_DotNode")
    nDot['xpos'].setValue( imX + 34 )
    nDot['ypos'].setValue( imY + 150)
    nDot.setInput(0, selectedNode)
 
    # create itterative top dot nodes
    for i in range(length):

        w = w + 150

        if first_dot() == True:
            topDot = nuke.nodes.Dot(name = f"n_topDotNode_{i}", ypos=nDot.ypos(), xpos=nDot.xpos() + w, inputs = [nuke.toNode(f"n_topDotNode_{i-1}")])
        elif first_dot() == False:
            topDot1 = nuke.nodes.Dot(name = f"n_topDotNode_{0}", ypos=nDot.ypos(), xpos=nDot.xpos() + w, inputs = [nuke.toNode("n_DotNode")])

    # creating Shuffle + lower dot nodes
    for i in (clean_channels):

        z = z + 150
        q = q + 1
        v = v + 75

        if v > 75:
            nShuffle = nuke.nodes.Shuffle2(name = f"n_ShuffleNode_{i}",\
            inputs = [nuke.toNode(f"n_topDotNode_{q}"), nuke.toNode(f"n_topDotNode_{i}")],
            ypos=nDot.ypos() + 150, xpos=nDot.xpos() + z)
            nuke.toNode(f"n_ShuffleNode_{i}")['in1'].setValue(i)
        elif v == 75:
            nShuffle = nuke.nodes.Shuffle2(name = f"n_ShuffleNode_{i}",\
            inputs = [nuke.toNode("n_DotNode"), nuke.toNode(f"n_topDotNode_{i}")],
            ypos=nDot.ypos() + 150, xpos=nDot.xpos() + z)
            nuke.toNode(f"n_ShuffleNode_{i}")['in1'].setValue(i)

        if cln_chan_dict[i] == "True":
            print("go")

            nDenoise = nuke.nodes.Denoise2(name = f"n_DenoiseNode_{i}",\
            inputs = [nuke.toNode(f"n_ShuffleNode_{i}")], 
            ypos=nDot.ypos() + 300, xpos=nDot.xpos() + z)

        # Adding Denoise Nodes
        def denoise_ck():
            for node in nuke.allNodes():
                if f"n_DenoiseNode_{i}" in node['name'].value():
                    print("bejgbowiefgbieowgb")
                    return True
                else:
                    return False

        # Organization compensation for Denoise
        if denoise_ck() == True:
            orgDot = nuke.nodes.Dot(name = f"n_DotNode_{i}",\
            inputs = [nuke.toNode(f"n_DenoiseNode_{i}")],\
            ypos = nShuffle.ypos() + v, xpos=nDot.xpos() + z + 34)
        else:
            orgDot = nuke.nodes.Dot(name = f"n_DotNode_{i}",\
            inputs = [nuke.toNode(f"n_ShuffleNode_{i}")],\
            ypos = nShuffle.ypos() + v, xpos=nDot.xpos() + z + 34)
            
            
    # check for merge nodes
    def first_m():
        for node in nuke.allNodes():
            if "n_Merge" in node['name'].value():
                return True 
    
    
    # create merge nodes and connect them to lower dot Nodes
    for x in range(length-1):

        y = y + 75
        
        if first_m() == True:
            print(cln_chan_lst)
            nMerge = nuke.nodes.Merge2(operation='plus',\
            name = f"n_Merge{x}",\
            inputs = [nuke.toNode(f"n_Merge{x-1}"),\
            nuke.toNode(f"n_DotNode_{cln_chan_lst[x+1]}")],\
            ypos = imY +400+ y, xpos = imX)
    
        # creates first merge node to connect to dot node
        else:
            nMerge2 = nuke.nodes.Merge2(operation='plus', name = f"n_Merge0",\
            inputs = [nuke.toNode(f"n_DotNode_{cln_chan_lst[0]}"),\
            nuke.toNode(f"n_DotNode_{cln_chan_lst[1]}")],\
            ypos = imY + 445 , xpos = imX)


    # Add copy node to keep Aplpha chanel intact 
    dxpos = nuke.toNode(f"n_topDotNode_{length -1}").xpos
    nDotCopy = nuke.nodes.Dot(name = "n_dotCopy", \
    inputs = [nuke.toNode(f"n_topDotNode_{length -1}")],\
    ypos = imY +length*75 + 375, xpos = imX+ length*150 + 32)

    nCopy = nuke.nodes.Copy(name = "n_copy",\
    inputs = [nuke.toNode(f"n_Merge{length -2}"),\
    nuke.toNode("n_dotCopy")],\
    xpos = nuke.toNode(f"n_Merge{length -2}").xpos(),\
    ypos = nuke.toNode(f"n_Merge{length -2}").ypos() + 75)
    nuke.toNode("n_copy")['from0'].setValue('rgba.alpha')
    nuke.toNode("n_copy")['to0'].setValue('rgba.alpha')



# GUI Interface and Interaction 
class nukeShufl_GUI(nukescripts.PythonPanel):
    def __init__(self):
        nukescripts.PythonPanel.__init__(self, "Allies Awesome AOV Shuffle",'uniqueID')

        self.setMinimumSize(0,200)

        #CREATE KNOBS
        #self.searchStr = nuke.String_Knob('searchStr' , 'Search For')
        self.clean = nuke.Text_Knob('bloop', 'Select Show Channels for more options')
        self.text2 = nuke.Text_Knob('test', 'before you ren the script')
        self.update = nuke.PyScript_Knob('select', 'show channels')
        self.update.setName('nselect')
        self.shuffle = nuke.PyScript_Knob('shuffle', 'Shuffle')
        self.shuffle.setName('shuf')



        #ADD KNOBS
        #self.addKnob(self.searchStr)
        self.addKnob(self.clean)
        self.addKnob(self.update)
        self.addKnob(self.shuffle)
        


# When the select button is pressed
    def knobChanged( self, knob):

        # check the denoise and delete inputs
        for key in cln_chan_dict:
            if knob.name() == key:
                cln_chan_dict[key] = "True"     
            else:
                pass

            if knob.name() == f"delete{key}":
                clean_channels.remove(key)
                cln_chan_lst.remove(key)
                print(cln_chan_dict)

        # Show passes button 
        if knob.name() == "nselect":
            print("The select node has been pressed")
            knob_options = ["None" , "Denoise"]

            for x in (cln_chan_lst):
                self.blob = nuke.Enumeration_Knob(f"ye{x}", f"ye{x}", knob_options)
                self.delete = nuke.PyScript_Knob(f"delete{x}", f"delete{x}")
                self.addKnob(nuke.Enumeration_Knob(f"{x}", f"{x}", knob_options))
                self.addKnob(nuke.PyScript_Knob(f"delete{x}", f"delete"))

        # Shuffle Button 
        elif knob.name() == 'shuf':
            cleanScene()
            createLayout()
            self.finishModalDialog(True)
        
        else:
            pass

# Adds to Panels Menu
def addPanel():
    return nukeShufl_GUI().addToPane()

menu = nuke.menu('Pane')
menu.addCommand('AOV Shuffle', addPanel)


# Run the GUI
nukeShufl_GUI().showModal()



